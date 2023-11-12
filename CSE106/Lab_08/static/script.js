const API_URL = "http://localhost:5000/login"; 

function handleLogin(event) {
    event.preventDefault(); // prevent the default form submission

    const username = document.getElementById('Username').value;
    const password = document.getElementById('Password').value;

    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    fetch(API_URL, {
        method: 'POST',
        body: formData // send as form data
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Login failed: ${response.statusText}`);
        }
        // If the login is successful, the server should redirect to the myStudentCourses page
        window.location.href = response.url; // redirect the client to the new page
    })
    .catch(error => {
        console.error('Error during login:', error);
        // Handle failed login, perhaps by showing an error message to the user
    });
}


// document.getElementById('loginForm').addEventListener('submit', handleLogin);
