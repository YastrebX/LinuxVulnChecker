// Utility function to update results table
function updateResultsTable(results) {
    const resultsTable = document.getElementById('resultsTable');
    const noResultsMessage = document.getElementById('noResultsMessage');

    if (noResultsMessage) {
        noResultsMessage.style.display = 'none';
    }

    // Clear old results
    resultsTable.querySelector('tbody').innerHTML = '';

    // Add new results
    Object.entries(results).forEach(([check, result]) => {
        const row = `<tr>
                        <td>${check.replace('_', ' ').title()}</td>
                        <td>${result}</td>
                     </tr>`;
        resultsTable.querySelector('tbody').insertAdjacentHTML('beforeend', row);
    });
}

// Handle Run All Checks
document.getElementById('runAllChecksBtn').addEventListener('click', function () {
    const button = this;
    button.disabled = true;
    button.textContent = 'Running All Checks...';

    fetch('/run_all_checks', { method: 'POST' })
        .then(response => {
            if (!response.ok) {
                console.error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                // Automatically refresh the page
                location.reload();
            } else {
                console.error(`Error while running checks: ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
        })
        .finally(() => {
            button.disabled = false;
            button.textContent = 'Run All Checks';
        });
});

// Handle Run Selected Checks
document.getElementById('runSelectedChecksBtn').addEventListener('click', function () {
    const selectedChecks = Array.from(document.querySelectorAll('input[name="checks"]:checked')).map(input => input.value);
    if (selectedChecks.length === 0) {
        alert('Please select at least one check.');
        return;
    }

    fetch('/run_selected_checks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ checks: selectedChecks })
    })
    .then(response => {
        if (!response.ok) {
            console.error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            // Automatically refresh the page
            location.reload();
        } else {
            console.error(`Error while running selected checks: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Fetch Error:', error);
    });
});

// Handle Clear Results
document.getElementById('clearResultsBtn').addEventListener('click', function () {
    // Clear the results table
    const resultsTable = document.getElementById('resultsTable');
    const noResultsMessage = document.getElementById('noResultsMessage');

    if (resultsTable) {
        resultsTable.querySelector('tbody').innerHTML = '';
    }

    if (noResultsMessage) {
        noResultsMessage.style.display = '';
    }

    // Optional: Notify the backend to reset results
    fetch('/clear_results', { method: 'POST' })
        .then(response => {
            if (!response.ok) {
                console.error(`HTTP error! Status: ${response.status}`);
            }
        })
        .catch(error => {
            console.error('Fetch Error:', error);
        });
});

