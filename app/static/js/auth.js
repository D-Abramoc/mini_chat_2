document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        document.querySelectorAll('.form').forEach(form => {
          form.classList.remove('active');
        });
        
        if (tab.dataset.tab === 'login') {
          document.getElementById('loginForm').classList.add('active');
        } else {
          document.getElementById('registrationForm').classList.add('active');
        }
      });
    });
  
    // Login Form Handling
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      const loginEmail = document.getElementById('loginEmail').value;
      const loginPassword = document.getElementById('loginPassword').value;
  
      try {
        const response = await fetch('http://127.0.0.1:8000/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: loginEmail,
            password: loginPassword
          })
        });
  
        if (response.ok) {
          const data = await response.json();
          alert('Login successful!');
          if (data.token) {
              localStorage.setItem('authToken', data.token);
            }
            // Redirect to chat page
            window.location.href = '/chat';
          // Handle successful login (e.g., store token, redirect)
        } else {
          const error = await response.json();
          alert('Login failed: ' + error.message);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login');
      }

      if (data && formType === 'login') {
          window.location.href = '/chat';
      }
    });
  
    // Registration Form Handling
    const registrationForm = document.getElementById('registrationForm');
    const password = document.getElementById('password');
    const strengthMeter = document.getElementById('strengthMeter');
  
    password.addEventListener('input', function() {
      const strength = checkPasswordStrength(this.value);
      updateStrengthMeter(strength);
    });
  
    function checkPasswordStrength(password) {
      let strength = 0;
      if (password.length >= 8) strength += 25;
      if (password.match(/[a-z]+/)) strength += 25;
      if (password.match(/[A-Z]+/)) strength += 25;
      if (password.match(/[0-9]+/)) strength += 25;
      return strength;
    }
  
    function updateStrengthMeter(strength) {
      strengthMeter.style.width = strength + '%';
      if (strength <= 25) {
        strengthMeter.style.backgroundColor = '#f44336';
      } else if (strength <= 50) {
        strengthMeter.style.backgroundColor = '#ffa726';
      } else if (strength <= 75) {
        strengthMeter.style.backgroundColor = '#ffeb3b';
      } else {
        strengthMeter.style.backgroundColor = '#4caf50';
      }
    }
  
    registrationForm.addEventListener('submit', async function(e) {
      e.preventDefault();
      let isValid = true;
  
      // Reset errors
      document.querySelectorAll('.error-message').forEach(error => {
        error.style.display = 'none';
      });
  
      const email = document.getElementById('email');
      const name = document.getElementById('name');
      const password = document.getElementById('password');
      const confirmPassword = document.getElementById('confirmPassword');
  
      // Validation
      if (!email.value.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
        document.getElementById('emailError').textContent = 'Please enter a valid email address';
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
      }
  
      if (name.value.length < 2) {
        document.getElementById('nameError').textContent = 'Name must be at least 2 characters long';
        document.getElementById('nameError').style.display = 'block';
        isValid = false;
      }
  
      if (password.value.length < 8) {
        document.getElementById('passwordError').textContent = 'Password must be at least 8 characters long';
        document.getElementById('passwordError').style.display = 'block';
        isValid = false;
      }
  
      if (password.value !== confirmPassword.value) {
        document.getElementById('confirmError').textContent = 'Passwords do not match';
        document.getElementById('confirmError').style.display = 'block';
        isValid = false;
      }
  
      if (isValid) {
        try {
          const response = await fetch('http://127.0.0.1:8000/register', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              email: email.value,
              name: name.value,
              password: password.value
            })
          });
  
          if (response.ok) {
            const data = await response.json();
            alert('Registration successful!');
            registrationForm.reset();
            strengthMeter.style.width = '0';
            // Handle successful registration (e.g., redirect to login)
          } else {
            const error = await response.json();
            alert('Registration failed: ' + error.message);
          }
        } catch (error) {
          console.error('Error:', error);
          alert('An error occurred during registration');
        }
      }
    });
  });
