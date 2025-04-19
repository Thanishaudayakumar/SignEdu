const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();

// Enable CORS for allowing cross-origin requests (helpful for frontend-backend communication)
app.use(cors());

// Middleware to parse JSON bodies for POST requests
app.use(express.json());

// Serve static files (HTML, CSS, JS) from the current directory
app.use(express.static(path.join(__dirname)));

// Serve the signup.html page when accessing the root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'signup.html')); // Sends the signup page (HTML)
});

// Handle the signup POST request
app.post('/signup', (req, res) => {
    const { username, email, password, confirmPassword } = req.body;

    // Check if the passwords match
    if (password !== confirmPassword) {
        return res.status(400).json({ message: 'Passwords do not match!' });
    }

    // Placeholder for inserting data into the database
    // You can add your database logic here (e.g., save user details to MySQL)

    // Sending a success message (you can modify this based on your logic)
    return res.status(200).json({ message: 'User created successfully!' });
});

// Start the server on port 5000
app.listen(5000, () => {
    console.log('Server is running on http://localhost:5000');
});
