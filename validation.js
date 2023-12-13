// validation.js
console.log("Script executed");
function predictCrop() {
    var value_N = document.getElementById("N").value;
    var value_P = document.getElementById("P").value;
    var value_K = document.getElementById("K").value;
    var value_humidity = document.getElementById("humidity").value;

    if (validateInput(value_N) && validateInput(value_P) && validateInput(value_K) && validateInput(value_humidity)) {
        var url = '/predict?N=' + value_N + '&P=' + value_P + '&K=' + value_K + '&humidity=' + value_humidity;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                document.getElementById("result").innerText = "Predicted Crop: " + data.predicted_crop;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        alert("Please enter valid percentage values (0 to 100) for all inputs.");
    }
}

function validateInput(value) {
    // Check if the input is a valid numeric value and in the range of 0 to 100
    return !isNaN(value) && value >= 0 && value <= 100;
}

document.getElementById("cropForm").addEventListener('submit', function(event) {
    var form = event.target;
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        alert("Please enter valid percentage values (0 to 100) for all inputs.");
    }
});
