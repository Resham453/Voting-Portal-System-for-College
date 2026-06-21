// import $ from 'jquery';

import { showNotification } from'../showNotification.js';  // Import the function from userFormValidation.js
import { callAjax } from '../ajax.js';  // Import the function from userFormValidation.js



$(document).on('click','#approvePositionListButton',async function () {
    let electionName = $('#electionName').val();
    let electionDate = $('#electionDate').val();
    let positionList =[]
    let positionName = []
    $(this).prop('disabled', true);
    // Loop through all checkboxes with the class 'positionListCheck' and check if they are checked
    $('.positionListCheck:checked').each(function() {
        positionList.push(parseInt($(this).val()));  // Push the value of each checked checkbox into the array
    });
    $('.positionListCheck:checked').each(function() {
        positionName.push($(this).attr("position"));  // Push the value of each checked checkbox into the array
    });

    // Check if the election name and date are empty
 

    var errorMessage = [];

    // Validation checks
    electionName.trim() === '' ? errorMessage.push('Please provide the Election Name.') : null;
    electionDate.trim() === '' ? errorMessage.push('Please select a valid Election Date.') : null;
    positionList.length === 0 ? errorMessage.push('At least one election position must be selected.') : null;
    
    // Check if there are any error messages
    if (errorMessage.length > 0) {
        showNotification(errorMessage.join(' <br>'), 'error');
    }
    else {
        // Simulating AJAX call
        var data = JSON.stringify({ "electionName": electionName, "electionDate": electionDate, "positionList": positionList,"createFlag":"create" })
        var url = '/voting/create-election'
        data = await callAjax(url,'POST',data)

        if(data.statusCode ===200){
            showNotification('Election Created... <br> Approved Positions: ' + positionName.join(', '), 'success');
            location.reload()
        }
        else{
            showNotification('Error approving positions.', 'error');
            $(this).prop('disabled', false);
        }
        // $.ajax({
        //     url: 'addElection', // Replace with your URL
        //     type: 'POST',
        //     contentType: 'application/json' ,
        //     data: 
        //     success: function(response) {
        //         
        //     },
        //     error: function() {
        //         
        //     }
        // });
    }
  


    
})



