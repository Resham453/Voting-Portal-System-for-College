import { showNotification } from "../showNotification.js";

import { callAjax } from "../ajax.js";

const candidateList = JSON.parse($("#userDetailsListHidden").val()
    .replace(/\(/g, '[')
    .replace(/\)/g, ']')
    .replace(/'/g, '"'));
const candidateListRejc = JSON.parse($("#userDetailsListHiddenREJC").val()
    .replace(/\(/g, '[')
    .replace(/\)/g, ']')
    .replace(/'/g, '"'));

var unapprovedCandidateList = []
var unapprovedCandidateEmail = []


document.addEventListener('DOMContentLoaded', function () {
    // Sidebar toggle
    document.getElementById('sidebarCollapse').addEventListener('click', function () {
        document.getElementById('sidebar').classList.toggle('active');
        document.getElementById('content').classList.toggle('active');
    });


});
$(document).ready(function () {
    // Approve candidates function

    $('.userDocumentHidden').each(function () {
        let userDocument = $(this).val().replace(/\\/g, '/');

        // Find the corresponding <span> and <a> tag
        $(this).siblings('.userDocument').find('a').attr('href', '/' + userDocument);
    });



   
    // Remove candidate function


    // Toggle cross visibility based on checkbox state
    $('.list-group input[type="checkbox"]').change(function () {
        let cross = $(this).closest('.list-group-item').find('.remove-candidate');
        cross.toggle(!$(this).is(':checked'));
    });
});


$('.remove-candidate').click(function () {
    let listItem = $(this).closest('.list-group-item');
    $(this).prop('disabled', true);
    let applicationId = parseInt($(this).attr('applicationId'));
    let email = $(this).attr('email');
    if (unapprovedCandidateList.includes(applicationId)){
        unapprovedCandidateList = unapprovedCandidateList.filter(e => e !== applicationId);
        unapprovedCandidateEmail = unapprovedCandidateEmail.filter(e => e !== email);
    }
    unapprovedCandidateList.push(applicationId);
    unapprovedCandidateEmail.push(email);
    $(this).closest('li').remove();
    // Simulating AJAX call
  
});

$(document).on('click', '#approveCandidateButton', function () {
    var checkedCandidates = [];
    var approvedCandidateEmail = [];
    $(this).prop('disabled', true);
    $('.candidateList:checked').each(function () {
        checkedCandidates.push(parseInt($(this).attr('applicationId'))); // or $(this).attr('value') depending on the checkbox attribute
        approvedCandidateEmail.push($(this).attr('email')); // or $(this).attr('value') depending on the checkbox attribute
    });

    if (checkedCandidates.length > 0 || unapprovedCandidateList.length > 0) {
        let method = 'POST'
        let url = 'approveCandidate'
        let data = JSON.stringify({ 'applicationList': checkedCandidates, 'unapprovedCandidateList': unapprovedCandidateList,'approvedCandidateEmail':approvedCandidateEmail, 'unapprovedCandidateEmail':unapprovedCandidateEmail });

        callAjax(url, method, data).then(response => {
            // Handle the response
            if (response.statusCode === 200) {
                if(response.positionCandidatePairs.length > 0){
                callAjax('/voting/create-election', 'POST', JSON.stringify({ "electionId": response.electionId, "positionList": response.positionCandidatePairs, "createFlag": "update" }))
                    .then(electionResponse => {
                        if (electionResponse.statusCode === 200) {
                            showNotification('Candidate Approved Successfully', 'success');
                            location.reload(); // Reload the page to reflect changes
                        } else {
                            showNotification('Transaction Failed', 'error');
                            $(this).prop('disabled', false);
                        }
                    });
                }
                showNotification(response.message, 'success');
                location.reload(); // Reload the page to reflect changes
            } else {
                showNotification(response.message, 'error');
                $(this).prop('disabled', false);
            }
        }).catch(error => {
            showNotification('An error occurred. Please try again later.', 'error');
            $(this).prop('disabled', false);
        });
    }
})
// Get all checked checkboxes with class 'candidateList'







$('#downloadApprovalList , .candidateInfo , #downloadRejectionList').click(function () {
    if ($(this).attr('userid') === '0') {
        createApprovalCandidatePDF($(this).attr('id')==='downloadRejectionList'? candidateListRejc: candidateList, $(this).attr('id')==='downloadRejectionList'?'Rejected Candidates':'Candidate Approval Details');
    }
    else {
        const candidate = JSON.parse($("#userDetailsHidden-"+$(this).attr('userid')).val()
            .replace(/\(/g, '[')
            .replace(/\)/g, ']')
            .replace(/'/g, '"'));
        $(this).attr('status') === 'REJC' ? createApprovalCandidatePDF([candidate], 'Rejected Candidate') :
        createApprovalCandidatePDF([candidate],'Candidate Approval Details');
    }
});

function createApprovalCandidatePDF(dataList,heading) {
    let counter = 0;
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    let startY = 40;
    doc.setFontSize(18);
    // doc.setFont("helvetica", "bold");
    const pageWidth = doc.internal.pageSize.width; // Get the page width
    const columnWidths = [pageWidth / 8, pageWidth / 8, pageWidth / 8, pageWidth / 8, pageWidth / 12, pageWidth / 10, pageWidth / 10, pageWidth / 9]; // Example fixed column widths for each column

    const headers = [
        ['First Name', 'Last Name', 'Position Name', 'Last Year CGPA', 'Backlog Number', ' Academic Year', 'SGPA', 'Stream']
    ];
    doc.setFont('times', 'bold');
    const textWidth = doc.getTextWidth(heading); // Get the width of the header text
    const x = (pageWidth - textWidth) / 2;
    doc.text(heading, x, 20);
    doc.autoTable({
        body: headers,
        startY: 30, // Position the table below the header
        theme: 'grid',
        headStyles: {
            halign: 'center',
            fontSize: 10,
            // fontStyle: 'bold',
        },
        styles: {
            halign: 'center',
            fontSize: 10,
            fontStyle: 'bold',
            fillColor: [240, 240, 240]
        },
        pageBreak: 'auto',  // Automatically break pages if the table exceeds page size
        columnStyles: {
            0: { cellWidth: columnWidths[0] },  // First column
            1: { cellWidth: columnWidths[1] },  // Second column
            2: { cellWidth: columnWidths[2] },  // Third column
            3: { cellWidth: columnWidths[3] },  // Fourth column
            4: { cellWidth: columnWidths[4] },  // Fifth column
            5: { cellWidth: columnWidths[5] },  // Sixth column
            6: { cellWidth: columnWidths[6] },  // Seventh column
            7: { cellWidth: columnWidths[7] },  // Eighth column
        }
    });

    while (counter <= dataList.length - 1) {
        const candidateData = dataList[counter];

        // Set up the table headers
        doc.setFontSize(12);
        doc.setFont("times", "normal");


        // Create the row data
        const data = [
            [
                candidateData[0],
                candidateData[1],
                candidateData[4],
                candidateData[5],
                candidateData[6],
                candidateData[8],
                candidateData[9],
                candidateData[11],
            ]
        ];

        // Table start at position y = 30, x = 20 (with headers at top)
        const margin = 10;
        const rowHeight = 10;
        const firstHalf = data.slice(0, Math.ceil(data.length / 2)); // First half

        doc.autoTable({
            body: firstHalf,
            startY: startY, // Position the table below the header
            theme: 'grid',
            headStyles: {
                halign: 'center',
                fontSize: 12,
                fontStyle: 'bold',
            },
            styles: {
                halign: 'center',
                fontSize: 10,
            },
            pageBreak: 'auto',  // Automatically break pages if the table exceeds page size
            columnStyles: {
                0: { cellWidth: columnWidths[0] },  // First column
                1: { cellWidth: columnWidths[1] },  // Second column
                2: { cellWidth: columnWidths[2] },  // Third column
                3: { cellWidth: columnWidths[3] },  // Fourth column
                4: { cellWidth: columnWidths[4] },  // Fifth column
                5: { cellWidth: columnWidths[5] },  // Sixth column
                6: { cellWidth: columnWidths[6] },  // Seventh column
                7: { cellWidth: columnWidths[7] }  // Eighth column

            }
        });
        const linkText = 'Result Document (Click to Open)';
        const linkUrl = "http://127.0.0.1:5000/" + candidateData[13].replace(/\\/g, '/');
        console.log(linkUrl)
        let linkPosition = doc.autoTable.previous.finalY + margin / 3;
        console.log(doc.autoTable.previous.finalY);
        console.log(margin);

        doc.setFontSize(8);
        doc.setTextColor(0, 0, 255);
        doc.textWithLink(linkText, 15, linkPosition, { url: linkUrl });
        startY = doc.autoTable.previous.finalY + margin;
        console.log(doc.autoTable.previous.finalY);

        counter += 1
    }


    // Create a clickable link for the result document


    // Open the PDF in a new tab instead of downloading
    const pdfBlob = doc.output('blob');
    const pdfUrl = URL.createObjectURL(pdfBlob);
    window.open(pdfUrl, '_blank');

    // Close the modal after generating the PDF
    // $('#secondModal').modal('hide');
}
