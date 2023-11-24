// scripts.js
// Function to generate sliders dynamically based on selected start date
function generateSliders() {
    var startDate = new Date(document.getElementById('startDate').value);
    var slidersDiv = document.getElementById('sliders');
    slidersDiv.innerHTML = ''; // Clear previous sliders

    for (var i = 1; i < 8; i++) {
        var currentDate = new Date(startDate);
        currentDate.setDate(startDate.getDate() + i);

        var label = document.createElement('label');
        label.className = 'mt-3';
        label.textContent = 'Day ' + (i ) + ' (' + currentDate.toDateString() + '):';

        var input = document.createElement('input');
        input.type = 'range';
        input.min = '300000000';
        input.max = '400000000';
        input.step = '250000';
        input.value = '300000000';
        input.className = 'form-control-range';

        var countDisplay = document.createElement('span');
        countDisplay.textContent = '300000000';

        label.appendChild(input);
        label.appendChild(document.createTextNode(' Count: '));
        label.appendChild(countDisplay);

        slidersDiv.appendChild(label);
    }
}

// Update count display when slider value changes
document.addEventListener('input', function(event) {
    if (event.target.type === 'range') {
        event.target.nextElementSibling.textContent = event.target.value;
    }
});

// Function to submit the form
function submitForm() {
    var startDate = document.getElementById('startDate').value;

    // Create data object
    var formData = {
        startDate: startDate,
        counts: []
    };

    // Get values from the sliders
    document.querySelectorAll('input[type="range"]').forEach(function(slider) {
        formData.counts.push({
            date: slider.parentNode.textContent.trim().split(' ')[2],
            count: slider.value
        });
    });

    // Send data to Flask backend (Assuming Flask endpoint is '/submit_form')
    fetch('/submit_form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Display the result
        document.getElementById('result').textContent = 'Predicted Count of receipt for next day : ' + data.nextCount;
        // document.getElementById('result').textContent = 'Predicted Count of next 30 days basis this week trend receipt : ' + data.nextMonth;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Call generateSliders initially and whenever the start date changes
document.getElementById('startDate').addEventListener('input', generateSliders);
generateSliders();
