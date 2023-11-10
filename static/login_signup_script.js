document.addEventListener('DOMContentLoaded', function () {
    const passwordField = document.getElementById('signup-password');
    const confirmPasswordField = document.getElementById('signup-confirm-password');
    const passwordMatchMessage = document.getElementById('password-match-message');
    const signupButton = document.getElementById('signup-button');
    const signupForm = document.getElementById('signup-form');

    confirmPasswordField.addEventListener('input', function () {
        if (passwordField.value === confirmPasswordField.value) {
            passwordMatchMessage.textContent = 'Passwords match';
            passwordMatchMessage.style.color = 'green';
            signupButton.disabled = false;
        } else {
            passwordMatchMessage.textContent = 'Passwords do not match';
            passwordMatchMessage.style.color = 'red';
            signupButton.disabled = true;
        }
    });

    signupForm.addEventListener('submit', function (event) {
        if (passwordField.value !== confirmPasswordField.value) {
            event.preventDefault(); // Prevent form submission
            passwordMatchMessage.textContent = 'Passwords do not match. Please try again.';
            passwordMatchMessage.style.color = 'red';
            signupButton.disabled = true;
        }
    });

    // --------Handle signup failure message display
    const signupFailedMessage = document.getElementById('signup-failed-message');
    if (signupFailedMessage) {
        signupFailedMessage.style.display = 'block';
    }
});




// Get references to the login and signup form elements
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");

// Get references to the "Sign up" and "Login" links
const showSignupLink = document.getElementById("show-signup");
const showLoginLink = document.getElementById("show-login");

// Initially, only show the login form
loginForm.style.display = "block";
signupForm.style.display = "none";

// Add click event listeners to the "Sign up" and "Login" links
showSignupLink.addEventListener("click", () => {
    loginForm.style.display = "none";
    signupForm.style.display = "block";
});

showLoginLink.addEventListener("click", () => {
    signupForm.style.display = "none";
    loginForm.style.display = "block";
});







// Check if the signup failed and the message is displayed
const signupFailedMessage = document.querySelector("#signup-failed-message");
if (signupFailedMessage && signupFailedMessage.style.display === "block") {
    signupForm.style.display = "block";
}





























    


// document.getElementById("signup-link").addEventListener("click", function(e) {
//     e.preventDefault(); // Prevent the default link behavior
//     document.getElementById("signup-form").style.display = "block";
// });


// document.addEventListener('DOMContentLoaded', function () {
//     const loginForm = document.getElementById('login-form');
//     const signupForm = document.getElementById('signup-form');
//     const showSignupLink = document.getElementById('show-signup');
//     const showLoginLink = document.getElementById('show-login');

//     // Initially hide the signup form
//     signupForm.style.display = 'none';

//     showSignupLink.addEventListener('click', function (event) {
//         event.preventDefault();
//         loginForm.style.display = 'none';
//         signupForm.style.display = 'block';
//     });

//     showLoginLink.addEventListener('click', function (event) {
//         event.preventDefault();
//         signupForm.style.display = 'none';
//         loginForm.style.display = 'block';
//     });
// });


// document.addEventListener('DOMContentLoaded', function () {
//     const loginForm = document.getElementById('login-form');
//     const signupForm = document.getElementById('signup-form');
//     const showSignupLink = document.getElementById('show-signup');
//     const showLoginLink = document.getElementById('show-login');

//     // Initially hide the signup form
//     signupForm.style.display = 'none';

//     showSignupLink.addEventListener('click', function (event) {
//         event.preventDefault();
//         loginForm.style.display = 'none';
//         signupForm.style.display = 'block';
//     });

//     showLoginLink.addEventListener('click', function (event) {
//         event.preventDefault();
//         signupForm.style.display = 'none';
//         loginForm.style.display = 'block';
//     });
// });
