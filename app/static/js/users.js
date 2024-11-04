function fetchUsers() {
    // Show refresh indicator
    const indicator = document.getElementById('refreshIndicator');
    indicator.classList.add('show');
  
    // Fetch users from JSON Placeholder API
    fetch('http://127.0.0.1/users')
      .then(response => response.json())
      .then(users => {
        const usersContainer = document.getElementById('users');
        usersContainer.innerHTML = ''; // Clear previous list
  
        users.forEach(user => {
          const userElement = document.createElement('div');
          userElement.className = 'user-item';
          userElement.innerHTML = `
            <span class="user-id">ID: ${user.id}</span>
          `;
          usersContainer.appendChild(userElement);
        });
  
        // Hide refresh indicator after small delay
        setTimeout(() => {
          indicator.classList.remove('show');
        }, 500);
      })
      .catch(error => {
        console.error('Error fetching users:', error);
        indicator.textContent = 'Error refreshing!';
        indicator.style.background = '#f44336';
        setTimeout(() => {
          indicator.classList.remove('show');
        }, 2000);
      });
  }
  
  // Initial fetch
  fetchUsers();
  
  // Fetch every minute
  setInterval(fetchUsers, 60000);