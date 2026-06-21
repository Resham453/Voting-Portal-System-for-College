
import { callAjax } from "../ajax.js";
// $(document).ready(function() {
// Example positions and candidates data
var voteRecords = '';
var electionList = JSON.parse($("#electionList").val().replace(/'/g, '"').replace(/\(/g, '[').replace(/\)/g, ']'))
var userRecords = JSON.parse($("#mappingUserList").val()
    .replace(/\(/g, '[')
    .replace(/\)/g, ']')
    .replace(/'/g, '"'));
var electionStatus = '';
var actElectionStatus = '';

// Create a map for quick lookup of user names by candidate_id
var userMap = {};
userRecords.forEach(user => {
    userMap[user[0]] = user[1];
});





$('#electionSelect').change(function () {
    let electionId = parseInt($(this).val());
    let positionList = `<option value="">Select a position</option> <option value="0">All</option>`
    let electionPositionDetails = []
    if(electionId>0){
        const tbody = $('#resultsTable tbody');
        tbody.empty();
        callAjax('/voting/vote_results', 'POST', JSON.stringify({ "electionId": electionId })).then(response => {
            voteRecords = response.data
            console.log(voteRecords)
            electionStatus = $(this).find('option:selected').attr('electionStatus')
            actElectionStatus = $(this).find('option:selected').attr('finalStatus')
            const groupedByPosition = voteRecords.positionList.reduce((acc, record) => {
                if (!acc[record.positionId]) {
                    acc[record.positionId] = [];
                }
                acc[record.positionId].push(record);
                return acc;
            }, {});
    
            // Step 2: Tag each candidate with status
            const recordsWithStatus = Object.values(groupedByPosition).flatMap(positionGroup => {
                const topVote = Math.max(...positionGroup.map(c => c.total_votes));
                console.log(topVote)
    
                return positionGroup.map(candidate => ({
                    ...candidate,
                    status: candidate.total_votes === topVote ? "Elected" : "Not Elected"
                })).filter(rec=> rec.candidateList.length>0);
            });
    
            let electedCandidate = recordsWithStatus.filter(rec=> rec.status='Elected').map(rec=> rec.candidateList[0].candidateId)
            console.log(electedCandidate)
            if(electionStatus ==='DONE' && electionStatus!== actElectionStatus){
                callAjax('/admin/updateElectionStatus', 'POST',JSON.stringify({"electionId":voteRecords.electionId,"candidateList":electedCandidate}))
            }
            callAjax('/admin/getElectionPositionList','POST',JSON.stringify({"electionId":electionId})).then(response =>{
                electionPositionDetails = response.data
                console.log(electionPositionDetails)
                for (let index = 0; index < electionPositionDetails.length; index++) {
                    positionList += `<option value="${electionPositionDetails[index][0]}">${electionPositionDetails[index][1]}</option>`
            
                }
                $('#positionSelect').html(positionList)
                $('#positionSelect').attr('disabled', false)
            })
        })
       
    
      
        

    }
    else{
        $('#positionSelect').html(positionList)
        $('#positionSelect').attr('disabled', true)
    }
   

})

// Handle position selection
$('#positionSelect').change(function () {
    const selectedPosition = $(this).val();
    let electionStatus = electionList.filter(rec=> rec[0]===voteRecords.electionId)[0][5]
    var filteredRecords = voteRecords.positionList;
    // Filter vote records by selected position
    if (parseInt(selectedPosition) === 0) {
        // If "All" is selected, show all records
        filteredRecords = voteRecords.positionList;
    }
    else {

        filteredRecords = voteRecords.positionList.filter(record => record.positionId == selectedPosition);
    }

    // Now, map over filteredRecords to extract positionId, candidateId, and total_votes
    filteredRecords = filteredRecords.map(record => {
        return record.candidateList.map(candidate => {
            return {
                positionId: record.positionId,         // The positionId for the current record
                candidateId: candidate.candidateId,    // The candidateId for the current candidate
                total_votes: candidate.voteCount       // The total votes for the candidate
            };
        });
    }).flat();  // .flat() to merge the nested arrays from candidateList

    console.log(filteredRecords);
    if (electionStatus === 'ONGOING') {

        // Sort records by vote count in descending order
        filteredRecords.sort((a, b) => {
            // First, sort by positionId (ascending)
            if (a.positionId !== b.positionId) {
                return a.positionId - b.positionId;
            }

            // If positionIds are the same, sort by total_votes (descending)
            return b.total_votes - a.total_votes;  // descending order by vote count
        });
        const tbody = $('#resultsTable tbody');
        tbody.empty();
        filteredRecords.forEach(record => {
            const userName = userMap[record.candidateId] || 'Unknown';
            tbody.append(`<tr><td>${userName}</td><td>${record.total_votes}</td><td>Pending </td></tr>`);
        });
    }
    else if (electionStatus === 'DONE') {

        // Group records by positionId
        // const groupedByPosition = filteredRecords.reduce((acc, record) => {
        //     if (!acc[record.positionId]) {
        //         acc[record.positionId] = [];
        //     }
        //     acc[record.positionId].push(record);
        //     return acc;
        // }, {});

        // // For each position, find the candidate with the maximum votes
        // filteredRecords = Object.values(groupedByPosition).map(records => {
        //     return records.reduce((max, record) => {
        //         return (record.total_votes > max.total_votes) ? record : max;
        //     });
        // });

        // filteredRecords = filteredRecords.sort((a, b) => a.positionId - b.positionId);
        // Step 1: Group candidates by positionId
        const groupedByPosition = filteredRecords.reduce((acc, record) => {
            if (!acc[record.positionId]) {
                acc[record.positionId] = [];
            }
            acc[record.positionId].push(record);
            return acc;
        }, {});

        // Step 2: Tag each candidate with status
        const recordsWithStatus = Object.values(groupedByPosition).flatMap(positionGroup => {
            const topVote = Math.max(...positionGroup.map(c => c.total_votes));

            return positionGroup.map(candidate => ({
                ...candidate,
                status: candidate.total_votes === topVote ? "Elected" : "Not Elected"
            }));
        });


        console.log(recordsWithStatus);

        // console.log(maxVotesPerPosition);

        const tbody = $('#resultsTable tbody');
        tbody.empty();
        recordsWithStatus.forEach(record => {
            const userName = userMap[record.candidateId] || 'Unknown';
            tbody.append(`<tr class="electedCandidate"><td>${userName}</td><td>${record.total_votes}</td><td>${record.status} </td></tr>`);
        });
    }

    $('#noResultsMessage').hide()
    // Populate the table with users and their vote counts


    // Show the table if a position is selected
    // if (selectedPosition) {
    //     $('#resultsTable').show();
    // } else {
    //     $('#resultsTable').hide();
    // }
});
// });
