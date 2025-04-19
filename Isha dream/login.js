document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();

    if (!username || !password) {
        alert('Please enter both username and password.');
        return;
    }

    const loginData = { username, password };

    try {
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        const result = await response.json();

        if (response.ok) {
            alert('✅ Login successful! Redirecting to Rhymes page...');
            // You can store the token if needed
            localStorage.setItem('token', result.token);
            window.location.href = 'rhymes.html';
        } else {
            alert(result.message || '❌ Invalid username or password. Please try again.');
        }

    } catch (error) {
        console.error('Error:', error);
        alert('⚠️ An error occurred while logging in. Please try again later.');
    }
});
