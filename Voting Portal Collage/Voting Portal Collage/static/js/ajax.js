// export function callAjax(url,method,data){
//     $.ajax({
//             url: url, // Replace with your URL
//             type: method,
//             contentType: 'application/json' ,
//             data: data,
//             success: function(response) {
//                 return 200
//             },
//             error: function() {
//                 return 400
//             }
//         });
//     }


export function callAjax(url, method, data,contentType=null) {
    let content = contentType!== null ? contentType:'application/json'
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: method,
            contentType: content,
            data: data,
            beforeSend: function() {
                // Show loader before sending request
                $('#loader').show();
            },
            success: function(response) {
                resolve(response);  // Resolve promise with response data
            },
            error: function(xhr, status, error) {
                reject({ status: 400, message: error });  // Reject promise on error
            },
            complete: function() {
                // Hide loader after success or error
                $('#loader').hide();
            }
        });
    });
}
