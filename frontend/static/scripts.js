// Running Loop keeping alive connection with back-end

// document.addEventListener('DOMContentLoaded', function () {
//     keep_alive_server()
//     try {setInterval(keep_alive_server, 5 * 1000)()
//     } catch (error) {}
// });

jQuery.fn.rotate = function(degrees) {
    $(this).css({'-webkit-transform' : 'rotate('+ degrees +'deg)',
                 '-moz-transform' : 'rotate('+ degrees +'deg)',
                 '-ms-transform' : 'rotate('+ degrees +'deg)',
                 'transform' : 'rotate('+ degrees +'deg)'});
};

// Accordion buttons animation
let rotation1 = 0;
let rotation2 = 0;
let rotation3 = 0;

$(document).ready(function(){
    $("#headingOne").click(function(){
        rotation1 += 180;
        $("#costsIcon").rotate(rotation1);
    });
    $("#headingTwo").click(function(){
        rotation2 += 180;
        $("#rigIcon").rotate(rotation2);
    });
    $("#headingThree").click(function(){
        rotation3 += 180;
        $("#resultIcon").rotate(rotation3);
    });
});


function keep_alive_server() {
    fetch(document.location + "keep-alive/?alive=true", {
        method: 'GET',
        cache: 'no-cache'
    })
        .then(resp => resp.json())
        .then(data => {
            document.getElementById("heightText").innerHTML = data.height
            document.getElementById("algoIcon").innerHTML = data.algo.icon
            document.getElementById("algoText").innerHTML = data.algo.text
            document.getElementById("deltaText").innerHTML = data.delta
        })
        .catch(error => {console.error(error)});
    }


function apiCall(body, query, method='POST') {
    return fetch(query, {
        method: method,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body),
    }).then(response => response.json()
    ).catch(err => console.log(err))

}