import { showNotification } from '../showNotification.js';  // Import the function from userFormValidation.js
import { callAjax } from '../ajax.js';  // Import the function from userFormValidation.js

var errorMessages = [];

function hideAllSectionUserForm() {
    $('#userFormAddUpdate').hide()
    $('#uploadUserData').hide()
    $('#resetUserForm').hide()
    $('#submitUserForm').hide()

}

$(document).on('click', '#addUserBtn, .userListRow, #uploadUserList', function () {
    hideAllSectionUserForm()
    if ($(this).attr('fileupload') === 'none') {

        if ($(this).attr('userid') !== '0') {
            let userId = $(this).attr('userid');
            let userRow = $(this).children('td');  // Get all <td> elements of the clicked row

            // Example: Access individual <td> elements by index
            let userName = $(userRow[0]).text();  // Get text of the first <td> (ID)
            let userEmail = $(userRow[1]).text();  // Get text of the second <td> (Name)
            let userMobile = $(userRow[2]).text();  // Get text of the third <td> (Role)
            let userRole = $(userRow[3]).text();  // Get text of the third <td> (Role)
            let userStatus = $(userRow[3]).text();  // Get text of the third <td> (Role)
            $('#userFirstName').val(userName.split(' ')[0])
            $('#userLastName').val(userName.split(' ')[1])
            $('#userEmail').val(userEmail)
            $('#userContactNo').val(userMobile)
            $('#userUserType').val(userRole === 'Admin' ? 'ADMIN' : userRole === 'Supervisor' ? 'SUP' : userRole === 'User' ? 'USR' : '')
            $('#userUserStatus').val(userStatus === 'Active' ? 'ACTV' :  'INAC')
            $('#submitUserForm').attr('userid', userId)
            $('#submitUserForm').attr('action', 'update')
            $('#userLabel').text('Update User')
        }
        else {
            $('#userFirstName').val('')
            $('#userLastName').val('')
            $('#userEmail').val('')
            $('#userContactNo').val('')
            $('#userUserType').val('')
            $('#submitUserForm').attr('userid', 0)
            $('#submitUserForm').attr('action', 'insert')
            $('#resetUserForm').show()
            $('#userLabel').text('Add User')
        }

        $('#userFormAddUpdate').show()
        $('#submitUserForm').show()
    }
    else {
        $('#uploadUserData').show()
        $('#resetUserForm').show()
        $('#submitUserForm').show()
        $('#submitUserForm').attr('userid', 0)
        $('#submitUserForm').attr('action', 'insert')
        $('#userLabel').text('Add User')

    }
    $('#userModal').modal('toggle');
    $('#userModal').modal('show');
    $('#userModal').modal('hide');
})

$(document).on('click', '#submitUserForm',  function () {
    $(this).prop('disabled', true);
    if (validateUserForm()) {
        var firstName =  $('#userFirstName').val().trim();
        var lastName =  $('#userLastName').val().trim() ;
        var email =  $('#userEmail').val().trim() ;
        var contactNo =  $('#userContactNo').val().trim() ;
        var role =  $('#userUserType').val().trim() ;
        let userStatus = $("#userUserStatus").val();
        var password = firstName.charAt(0).toUpperCase() + firstName.slice(1).toLowerCase() + '@'+contactNo+'#'+role;
        let action = $(this).attr('action')
        let userId = $('#submitUserForm').attr('userid')
        
        let url = action==='insert'?'addUser':'updateUser'
        let method = 'POST'
        let data = JSON.stringify({'userId':userId,'userData':[{'first_name':firstName,'last_name':lastName,'email':email,'contact_no':contactNo,'password':password,'status':userStatus,'role':role}]})
         callAjax(url,method,data).then(response =>{

        if(response.statusCode ==200){
            showNotification('Transaction Successful','success')
            location.reload()
        }
        else{
            showNotification('Transaction Failed','error')
            $(this).prop('disabled', false);
        }});
    }
})

function validateUserForm() {
    // Get the values from the form fields
    // Check if the element exists before trying to access its value
    var firstName = $('#userFirstName').length ? $('#userFirstName').val().trim() : '';
    var lastName = $('#userLastName').length ? $('#userLastName').val().trim() : '';
    var email = $('#userEmail').length ? $('#userEmail').val().trim() : '';
    var contactNo = $('#userContactNo').length ? $('#userContactNo').val().trim() : '';
    var role = $('#userUserType').length && $('#userUserType').val() !== null ? $('#userUserType').val().trim() : '';

    // Initialize an array to collect error messages
    errorMessages = []
    // Validate first name
    if (firstName === '') {
        errorMessages.push('First name is required.');
    }

    // Validate last name
    if (lastName === '') {
        errorMessages.push('Last name is required.');
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
        errorMessages.push('Contact number is required.');
    } else if (!contactPattern.test(contactNo)) {
        errorMessages.push('Please enter a valid 10-digit contact number.');
    }

    // Validate role selection
    if (role === '') {
        errorMessages.push('User role is required.');
    }

    // If there are any errors, display them and return false to prevent form submission
    if (errorMessages.length > 0) {
        // Display the error messages (you can show them in a specific div or alert)

        showNotification(errorMessages.join('<br>'), 'error')

        return false;
    }

    showNotification('User Validated Successfully', 'successful')

    // If no errors, return true to allow form submission
    return true;
}



