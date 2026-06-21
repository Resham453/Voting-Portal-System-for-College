export function showNotification(message, type) {
       

    // Apply a class based on the notification type
    if (type === 'error') {
        $('#errorAlert').html(message);
        $('#errorAlert').show();
        setTimeout(function() {
            $('#errorAlert').fadeOut();
        }, 3000);
    } else if (type === 'success') {
        $('#successAlert').html(message);
        $('#successAlert').show();
        setTimeout(function() {
            $('#successAlert').fadeOut();
            location.reload();
        }, 3000);
        
            }



    // Append the notification to the body (or a specific element)

    // Auto-hide the notification after 3 seconds
  
}