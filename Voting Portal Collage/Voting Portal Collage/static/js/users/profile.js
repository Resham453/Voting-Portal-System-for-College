import { showNotification } from '../showNotification.js'
import { callAjax } from '../ajax.js'

var candidatePositionList = JSON.parse($('#cnd_p').val()
    .replace(/\(/g, '[')
    .replace(/\)/g, ']')
    .replace(/'/g, '"')
    .replace(/{/g, '(')
    .replace(/}/g, ')'))
console.log(candidatePositionList[0])

$(document).ready(function(){
    if($('#alreadyRegistered').val()==='None'){
        $('#registerCandidateBTN').show()
        $('#candidateRegistedAlready').hide()

    }
    else{
        $('#candidateRegistedAlready').show()
        $('#registerCandidateBTN').hide()

    }
})

$(document).on('click', '#registerCandidateBTN', function () {
    $('#registerCandidate').modal('toggle');
    $('#registerCandidate').modal('show');
    $('#registerCandidate').modal('hide');
})

$(document).on('click', '#voteCandidateBTN', function () {
    $('#castVote').modal('toggle');
    $('#castVote').modal('show');
    $('#castVote').modal('hide');
})

$(document).on('change', '#votePosition', function () {
    var positionId = parseInt($(this).val())
    var candidateList = `<option value="" disabled selected>Select Candidate</option> `
    candidatePositionList.forEach(element => {
        if (positionId === element[1]) {
            candidateList += `<option value="${element[0]}" selected>${element[3]}</option>`
        }
    });
    $('#voteCandidate').html(candidateList)
})

$(document).on('click', '#submitVote', function () {
    let vElection_id = $(this).attr("electionId")
    let vUser_id = $(this).attr("userId")
    let vCandidate_id = $("#voteCandidate").val()
    let vPosition_id = $("#votePosition").val()

    if (validateVote(vElection_id, vCandidate_id, vPosition_id)) {
        $(this).prop('disabled', true);

        let url = '/voting/cast-vote';
        let method = 'POST'; // Use POST method
        let data = JSON.stringify({
            'userId': parseInt(vUser_id),
            'candidateId': parseInt(vCandidate_id.trim()),
            'positionId': parseInt(vPosition_id.trim()),
            'electionId': parseInt(vElection_id.trim())

        })
        callAjax(url, method, data).then(response => {
            console.log(response)
            // Handle the response
            if (response.statusCode === 200) {
                showNotification(response.message, 'success');
                location.reload(); // Reload the page to reflect changes
            } else {
                showNotification(response.message, 'error');
                $(this).prop('disabled', false);
            }
        }).catch(error => {
            showNotification('An error occurred. Please try again later.', 'error');
            location.reload(); // Reload the page to reflect changes
        });
    }
})

function validateVote(election_id, candidate_id, position_id) {
    var errorMessages = [];

    if (candidate_id === null || !candidate_id.length) {
        errorMessages.push('No any candidate is selected');

    }

    if (position_id === null || !position_id.length) {
        errorMessages.push('No any position is selected');

    }

    if (errorMessages.length > 0) {
        showNotification(errorMessages.join('<br>'), 'error');
        return false;
    }

    // If the form is validated successfully
    // showNotification('', 'success');

    // If no errors, return true to allow form submission
    return true;

}

$(document).on('click', '#submitRegCanForm', function () {
    $(this).prop('disabled', true);
    // Validate the form fields
    if (validateRegisterCandidateForm()) {
        // Get values from form fields
        var firstName = $('#regCanFirstName').val().trim();
        var lastName = $('#regCanLastName').val().trim();
        var email = $('#regCanEmail').val().trim();
        var contactNo = $('#regContactNo').val().trim();
        var sgpa = $('#regCanSGPA').val().trim();
        var cgpa = $('#regCanCGPA').val().trim();
        var academicYear = $('#regCanACADYear').val().trim();
        var stream = $('#regCanStream').val().trim();
        var backlogCount = $('#regCanBlacklogCount').val().trim();
        var backlogSubject = $('#regCanBlacklogSubject').val().trim();
        var electionYear = $('#regCanElection').val().trim();
        var electionPosition = $('#regCanElectionPosition').val().trim();
        var marksheet = $('.markSheet'); // Get the file object

        // Prepare the data for submission

        // Prepare the form data object (including file)
        // let formData = new FormData();
        // formData.append('userId', userId);
        // formData.append('first_name', firstName);
        // formData.append('last_name', lastName);
        // formData.append('email', email);
        // formData.append('contact_no', contactNo);
        // formData.append('sgpa', sgpa);
        // formData.append('cgpa', cgpa);
        // formData.append('academic_year', academicYear);
        // formData.append('stream', stream);
        // formData.append('backlog_count', backlogCount);
        // formData.append('backlog_subjects', backlogSubject);
        // formData.append('election_year', electionYear);
        // formData.append('election_position', electionPosition);
        // if (marksheet) {
        //     formData.append('marksheet', marksheet); // Append the file
        // }

        // Prepare the data for submission
        let userId = $('#submitRegCanForm').attr('userid'); // If userId is attached to the form button

        // let documentUploadStatus = uploadDocuments(marksheet)

        // // Depending on the action, set the URL
        // let url = 'registerCandidate';
        // let method = 'POST'; // Use POST method

        for (const documentRow of $('.markSheet')) {
            if ($(documentRow).hasClass("New")) {

                var fileUpload = $(documentRow).prop("files")[0];

                if ($(documentRow).prop("files").length == 0)
                    continue;
                var userName = $(documentRow).attr("id").split("-")[1]
                // var userId = $(documentRow).attr("id").split("-")[2]
                var documentName = "Marksheet-" + userId;
                var documentDescription = "Marksheet for user - " + userName;
                var documentType = "Marksheet Document";
                let returnData = null
                var data = new FormData();
                data.append("userId", userId);
                data.append("documentName", documentName);
                data.append("documentType", documentType);
                data.append("description", documentDescription)
                data.append("file", fileUpload);
                data.append("status", "Pending");
                let url = "UploadDocuments"
                let method = "POST"
                let document = data
                $.ajax({
                    url: url,
                    type: method,
                    data: document,
                    processData: false,
                    mimeType: "multipart/form-data",
                    contentType: false,
                    success: function (response) {
                        let formattedResponse = JSON.parse(response)
                        if (formattedResponse.statusCode === 200) {
                            let url = 'registerCandidate';
                            let method = 'POST'; // Use POST method
                            let data = JSON.stringify({
                                'userId': userId,
                                'candidateData': [{
                                    'first_name': firstName,
                                    'last_name': lastName,
                                    'email': email,
                                    'contact_no': contactNo,
                                    'sgpa': sgpa,
                                    'cgpa': cgpa,
                                    'academic_year': academicYear,
                                    'stream': stream,
                                    'backlog_count': backlogCount,
                                    'backlog_subjects': backlogSubject,
                                    'election_year': electionYear,
                                    'election_position': electionPosition,
                                    'document': formattedResponse.filePath
                                }]
                            });

                            callAjax(url, method, data).then(response => {
                                
                                // Handle the response
                                if (response.statusCode === 200) {
                                    showNotification('Candidate Registration Successful', 'success');
                                    location.reload(); // Reload the page to reflect changes
                                } else {
                                    showNotification('Candidate Registration Failed', 'error');
                                    $(this).prop('disabled', false);
                                }
                            })
                        }
                        else {
                            showNotification('Document upload failed..', 'error')
                            location.reload()
                        }

                    },
                    error: function (xhr, status, error) {
                        return 400
                    }
                });


            }
            else{
                $(this).prop('disabled', false);

            }
        }
    }
});

function validateRegisterCandidateForm() {
    // Get the values from the form fields
    // Check if the element exists before trying to access its value
    var firstName = $('#regCanFirstName').length ? $('#regCanFirstName').val().trim() : '';
    var lastName = $('#regCanLastName').length ? $('#regCanLastName').val().trim() : '';
    var email = $('#regCanEmail').length ? $('#regCanEmail').val().trim() : '';
    var contactNo = $('#regContactNo').length ? $('#regContactNo').val().trim() : '';
    var sgpa = $('#regCanSGPA').length ? $('#regCanSGPA').val().trim() : '';
    var cgpa = $('#regCanCGPA').length ? $('#regCanCGPA').val().trim() : '';
    var academicYear = $('#regCanACADYear').length && $('#regCanACADYear').val() !== null ? $('#regCanACADYear').val().trim() : '';
    var stream = $('#regCanStream').length && $('#regCanStream').val() !== null ? $('#regCanStream').val().trim() : '';
    var backlogCount = $('#regCanBlacklogCount').length ? $('#regCanBlacklogCount').val().trim() : '';
    var backlogSubject = $('#regCanBlacklogSubject').length ? $('#regCanBlacklogSubject').val().trim() : '';
    var electionYear = $('#regCanElection').length && $('#regCanElection').val() !== null ? $('#regCanElection').val().trim() : '';
    var electionPosition = $('#regCanElectionPosition').length && $('#regCanElectionPosition').val() !== null ? $('#regCanElectionPosition').val().trim() : '';
    // var fileUpload = $('#marksheet').length ? $('#marksheet').val().trim() : '';

    // Initialize an array to collect error messages
    var errorMessages = [];

    // Validate first name
    if (firstName === '') {
        errorMessages.push('First Name is required.');
    }

    // Validate last name
    if (lastName === '') {
        errorMessages.push('Last Name is required.');
    }

    // Validate email (basic format check)
    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (email === '') {
        errorMessages.push('Email is required.');
    } else if (!emailPattern.test(email)) {
        errorMessages.push('Please enter a valid email address.');
    }

    // Validate contact number (basic check, numeric)
    var contactPattern = /^[0-9]{10}$/;  // Assuming 10 digit contact number
    if (contactNo === '') {
        errorMessages.push('Contact Number is required.');
    } else if (!contactPattern.test(contactNo)) {
        errorMessages.push('Please enter a valid 10-digit contact number.');
    }

    // Validate SGPA (should be numeric)
    var sgpaPattern = /^[0-9]+(\.\d{1,2})?$/;
    if (sgpa === '') {
        errorMessages.push('SGPA is required.');
    } else if (!sgpaPattern.test(sgpa)) {
        errorMessages.push('SGPA must be a valid number.');
    }

    // Validate CGPA (should be numeric)
    var cgpaPattern = /^[0-9]+(\.\d{1,2})?$/;
    if (cgpa === '') {
        errorMessages.push('CGPA is required.');
    } else if (!cgpaPattern.test(cgpa)) {
        errorMessages.push('CGPA must be a valid number.');
    }

    // Validate academic year
    if (academicYear === '') {
        errorMessages.push('Academic Year is required.');
    }

    // Validate stream selection
    if (stream === '') {
        errorMessages.push('Stream is required.');
    }

    // Validate backlog count (optional but should be numeric if provided)
    if (backlogCount !== '' && !/^[0-9]+$/.test(backlogCount)) {
        errorMessages.push('Backlog Count must be a number.');
    }

    // // Validate backlog subject (optional, if filled it should be alphanumeric)
    // if (backlogSubject !== '' && !/^[a-zA-Z0-9\s,]+$/.test(backlogSubject)) {
    //     errorMessages.push('Backlog Subject must be alphanumeric.');
    // }

    // Validate election year
    if (electionYear === '') {
        errorMessages.push('Election Year is required.');
    }

    // Validate election position
    if (electionPosition === '') {
        errorMessages.push('Election Position is required.');
    }

    // Validate file upload
    if (!checkUploadDocuments($('.markSheet'))) {
        errorMessages.push('Marksheet upload is required.');
    }

    // If there are any errors, display them and return false to prevent form submission
    if (errorMessages.length > 0) {
        // Display the error messages (you can show them in a specific div or alert)
        showNotification(errorMessages.join('<br>'), 'error');
        return false;
    }

    // If the form is validated successfully
    // showNotification('Candidate Registered Successfully', 'success');

    // If no errors, return true to allow form submission
    return true;
}




/**
 * Method to check whether any documents are being uploaded or not
 * @param {any} documentRows
 */
function checkUploadDocuments(documentRows) {

    var documentPresentFlag = false;

    for (var documentRow of documentRows) {

        if ($(documentRow).prop("files").length > 0)
            documentPresentFlag = true;

    }
    return documentPresentFlag;
}

/**
 * Method to upload documents to the backend
 * @param {any} documentRows
 */
function uploadDocuments(documentRows) {
    /*function uploadDocuments(documentRows) {*/
    var successFlag = false;

    for (const documentRow of documentRows) {
        if ($(documentRow).hasClass("New")) {

            var fileUpload = $(documentRow).prop("files")[0];

            if ($(documentRow).prop("files").length == 0)
                continue;
            var userName = $(documentRow).attr("id").split("-")[1]
            var userId = $(documentRow).attr("id").split("-")[2]
            var documentName = "Marksheet-" + userId;
            var documentDescription = "Marksheet for user - " + userName;
            var documentType = "Marksheet Document";
            let returnData = null
            var data = new FormData();
            data.append("userId", userId);
            data.append("documentName", documentName);
            data.append("documentType", documentType);
            data.append("description", documentDescription)
            data.append("file", fileUpload);
            data.append("status", "Pending");
            let url = "UploadDocuments"
            let method = "POST"
            let document = data
            $.ajax({
                url: url,
                type: method,
                data: document,
                processData: false,
                mimeType: "multipart/form-data",
                contentType: false,
                success: function (response) {
                    return response  // Resolve promise with response data
                },
                error: function (xhr, status, error) {
                    return 400
                }
            });


            if (!successFlag) { // keep track of uploaded documents [name, size]
                break;
            }
        }
    }
    return successFlag;
}

/**
 * Method to upload supplier documents to the server
 * @param {any} documentName
 * @param {any} documentDescription
 * @param {any} fileContent
 * @param {any} requestDocumentId
 * @param {any} documentType
 */
function uploadRequestInfoDocuments(documentName, documentDescription, fileContent, userId, documentType) {
    return new Promise(function (resolve, reject) {
        var data = new FormData();
        data.append("userId", userId);
        data.append("documentName", documentName);
        data.append("documentType", documentType);
        data.append("description", documentDescription)
        data.append("file", fileContent);
        data.append("status", "Pending");
        let url = "UploadDocuments"
        let method = "POST"
        let document = data
        callAjax(url, method, document, false).then(response => {
            // Handle the response
            if (response.statusCode === 200) {
                resolve(true)
            }
            // else {
            //     resolve(false)
            // }
        }).catch(error => {
            reject(true)
        });

    });
}