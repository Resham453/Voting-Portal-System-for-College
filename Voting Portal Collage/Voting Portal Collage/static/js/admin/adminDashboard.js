$(document).ready(function() {
    var tableBody = $('table tbody');
    var rowCount = tableBody.children('tr').length;  // Get the number of rows

    if (rowCount > 5) {
        tableBody.css({
            'display': 'block',
            'max-height': '200px',  // Set the max height of the tbody
            'overflow-y': 'auto',   // Enable vertical scrolling
            'overflow-x': 'hidden'  // Disable horizontal scrolling
        });
    }
});

var electionDetails = $('#electionDetails').val();
electionDetails = JSON.parse(electionDetails.replace(/\\/g, '/'))
console.log(electionDetails.length)

// document.addEventListener('DOMContentLoaded', function () {
//     // Sidebar toggle
//     document.getElementById('sidebarCollapse').addEventListener('click', function () {
//         document.getElementById('sidebar').classList.toggle('active');
//         document.getElementById('content').classList.toggle('active');
//     });

//     // Chart
//     var ctx = document.getElementById('voteChart').getContext('2d');
//     var myChart = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: ['John Smith', 'Sarah Johnson', 'Mike Williams', 'Emily Brown', 'David Wilson'],
//             datasets: [{
//                 label: 'Votes Received',
//                 data: [1234, 987, 856, 754, 642],
//                 backgroundColor: [
//                     'rgba(54, 162, 235, 0.8)',
//                     'rgba(255, 99, 132, 0.8)',
//                     'rgba(75, 192, 192, 0.8)',
//                     'rgba(255, 206, 86, 0.8)',
//                     'rgba(153, 102, 255, 0.8)'
//                 ]
//             }]
//         },
//         options: {
//             responsive: true,
//             scales: {
//                 y: {
//                     beginAtZero: true
//                 }
//             }
//         }
//     });
// });

