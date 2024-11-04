// Функция для получения текущего ID пользователя из localStorage
// В реальном приложении этот ID может храниться в сессии или куках
function getCurrentUserId() {
    return localStorage.getItem('currentUserId') || 'guest';
}

// Функция обработки выхода
function handleExit() {
    const userId = getCurrentUserId();
    
    // Отправляем ID пользователя на сервер
    fetch('http://127.0.0.1/auth/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            userId: userId
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Logout successful:', data);
        // Очищаем данные пользователя
        localStorage.removeItem('currentUserId');
        // Перенаправляем на страницу входа
        window.location.href = 'http://127.0.0.1/auth';
    })
    .catch(error => {
        console.error('Error during logout:', error);
        alert('Произошла ошибка при выходе из системы');
    });
}
