
import { callAjax } from './ajax.js';  // Import the function from userFormValidation.js
var userNameList= null

$(window).on('load', function() {
        let statusCode = $('#loginStatus').val()
    if (statusCode === '400') {

        showNotification('Username or Password Incorrect..', 'error')
    }

    callAjax('getUserName','GET',1).then(response=>{
        userNameList = response.userNameList
        
    })
})


function showNotification(message, type) {


    // Apply a class based on the notification type
    if (type === 'error') {
        $('#errorAlert').html(message);
        $('#errorAlert').show();
        setTimeout(function () {
            $('#errorAlert').fadeOut();
        }, 3000);
    } else if (type === 'success') {
        $('#successAlert').html(message);
        $('#successAlert').show();
        setTimeout(function () {
            $('#successAlert').fadeOut();
            location.reload();
        }, 3000);

    }



    // Append the notification to the body (or a specific element)

    // Auto-hide the notification after 3 seconds

}



$(document).on('click', '#submitUserForm',  function () {
    $(this).prop('disabled', true);
    if (validateUserForm()) {
        var firstName =  $('#userFirstName').val().trim();
        var lastName =  $('#userLastName').val().trim() ;
        var email =  $('#userEmail').val().trim() ;
        var contactNo =  $('#userContactNo').val().trim() ;
        var userPrn =  $('#userPRN').val().trim() ;
        var role =  'USR';
        var password = firstName.charAt(0).toUpperCase() + firstName.slice(1).toLowerCase() + '@'+contactNo+'#USR';
        let action = $(this).attr('action')
        let userId = $('#submitUserForm').attr('userid')
        
        let url = 'register_user'
        let method = 'POST'
        let data = JSON.stringify({'userId':userId,'userData':[{'first_name':firstName,'last_name':lastName,'email':email,'contact_no':contactNo,'password':password,'prn_no':userPrn,'status':'ACTV','role':role}]})
         callAjax(url,method,data).then(response =>{

        if(response.statusCode ==200){
            showNotification(response.message,'success')
            window.location.href = response.redirect_url;
        }
        else{
            showNotification(response.message,'error')
            $(this).prop('disabled', false);
        }});
    }
    else{
        $(this).prop('disabled', false);

    }
})

function validateUserForm() {
    // Get the values from the form fields
    // Check if the element exists before trying to access its value
    var firstName = $('#userFirstName').length ? $('#userFirstName').val().trim() : '';
    var lastName = $('#userLastName').length ? $('#userLastName').val().trim() : '';
    var email = $('#userEmail').length ? $('#userEmail').val().trim() : '';
    var contactNo = $('#userContactNo').length ? $('#userContactNo').val().trim() : '';
    var userPrn = $('#userPRN').length ? $('#userPRN').val().trim() : '';

    // Initialize an array to collect error messages
    let errorMessages = []
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
    else if (userNameList.map((rec) => rec.email).includes(email)){
        errorMessages.push('This email address already in used');

    }

    if(userPrn===''){
        errorMessages.push('PRN No is required.');

    }
    else if(userNameList.map((rec) => rec.prn_no).includes(userPrn.toUpperCase().trim())){
        errorMessages.push('This PRN No already in used');
    }
//         const emails = data.map(([email, _]) => email);
// const prns = data.map(([_, prn]) => prn);

    // Validate contact number (basic check, numeric)
    var contactPattern = /^[0-9]{10}$/;  // Assuming 10 digit contact number
    if (contactNo === '') {
        errorMessages.push('Contact number is required.');
    } else if (!contactPattern.test(contactNo)) {
        errorMessages.push('Please enter a valid 10-digit contact number.');
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


