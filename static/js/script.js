$(document).ready(function() {
    $('nav ul li a:not(:only-child)').click(function(e) {
        $(this).siblings('.nav-dropdown').toggle();
        e.stopPropagation();
    });

    $('html').click(function(){
        $('.nav-dropdown').hide();
    })
    $('#nav-toggle').click(function(){
        $('nav ul').slideToggle();
    })
    $('#nav-toggle').on('click', function(){
        this.classList.toggle('active');
    });
});

const codeInput = document.getElementById('code-input');

// Function to save input box size to local storage
function saveInputBoxSize() {
  const numRows = codeInput.rows;
  const numCols = codeInput.cols;

  // Store the size values in local storage
  localStorage.setItem('inputBoxSize', JSON.stringify({ rows: numRows, cols: numCols }));
}

// Function to load and apply input box size from local storage
function loadInputBoxSize() {
  const inputBoxSize = localStorage.getItem('inputBoxSize');

  if (inputBoxSize) {
    const { rows, cols } = JSON.parse(inputBoxSize);
    codeInput.rows = rows;
    codeInput.cols = cols;
  }
}

// Add an event listener for input box size changes
codeInput.addEventListener('change', saveInputBoxSize);

// Load and apply the input box size when the page loads
loadInputBoxSize();

// implemenying shortcuts 
document.addEventListener("keydown", function (e) {
    if (e.ctrlKey && e.key === "s") {
        // Handle Ctrl+S event (e.g., trigger saving)
        e.preventDefault(); // Prevent the default browser save dialog
        saveCode(); // Call your save function
    }
});
// adding dark theme to text area
// script.js
const darkModeToggle = document.getElementById('dark-mode-toggle');
const textArea = document.getElementById('code-input');

darkModeToggle.addEventListener('change', () => {
    if (darkModeToggle.checked) {
        document.body.classList.add('dark-mode');
        textArea.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
        textArea.classList.remove('dark-mode');
    }
});
