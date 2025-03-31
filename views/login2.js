document.addEventListener('DOMContentLoaded', function () {
    // Handle login form submission
    document.getElementById('loginForm').addEventListener('submit', function (event) {
        event.preventDefault();  // Prevent form submission from reloading the page

        let user = document.getElementById('user').value;
        let password = document.getElementById('password').value;

        console.log("Login attempt:", user);

        // Attempt to authenticate the user by calling the FastAPI backend
        fetch(`/login?user=${encodeURIComponent(user)}&password=${encodeURIComponent(password)}`)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        console.log("Error response:", errorData);
                        alert(`Login failed: ${errorData.detail}`);
                    });
                } else {
                    // Successful login
                    return response.json().then(data => {
                        console.log("Login successful:", data);
                        if (data.message === "Login successful!") {
                            localStorage.setItem('loggedInUser', user);
                            window.location.href = 'dashboard2.html';
                        }
                    });
                }
            })
            .catch(err => {
                console.error("Error during login:", err);
                alert("Login error occurred.");
            });
    });

    // Handle registration via the clickable element
    document.querySelector('.forgot-password a').addEventListener('click', function (event) {
        event.preventDefault();  // Prevent default link behavior

        // Prompt for new user credentials
        const newUser = prompt("Enter a username for registration:");
        if (newUser) {
            const newPassword = prompt("Please set a password for your new account:");
            if (newPassword) {
                // Make the registration request to the backend
                fetch(`/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user: newUser,
                        password: newPassword
                    })
                })
                .then(registerResponse => registerResponse.json())
                .then(registerData => {
                    if (registerData.message === "Password set successfully") {
                        alert("Registration complete! Please log in with your new credentials.");
                        document.getElementById('user').value = newUser;  // Pre-fill username
                        document.getElementById('password').value = "";  // Clear password input
                    } else {
                        alert("Failed to register the new user.");
                    }
                })
                .catch(registerError => {
                    console.error("Error during registration:", registerError);
                    alert("Error occurred during registration.");
                });
            }
        }
    });
});