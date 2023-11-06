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

document.addEventListener("DOMContentLoaded", function () {
    const codeTextarea = document.getElementById("code-textarea");
    const chatButton = document.getElementById("chat-expand-button");
  
    chatButton.onclick = function () {
      // Expand the button
      chatButton.style.width = "100px";
  
      // Insert chat input or trigger AI chat here
      // You can dynamically create and position the chat input within the textarea
      // or open a chat window or implement your desired AI functionality
    };
  });