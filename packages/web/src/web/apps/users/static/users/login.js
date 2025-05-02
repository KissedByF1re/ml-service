document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('login-btn');

    loginBtn.addEventListener('click', async function() {
        const data = {
            email: document.getElementById('email').value,
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
        };

        try {
            const response = await axios.post(
                `${domain}/api/users/auth/login/`,
                data,
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    withCredentials: true
                }
            );
            window.location.href = `${redirectURL}`;
        } catch (error) {
            if (error.response) {
                console.error('Ошибка входа:', error.response);
                alert('Ошибка входа: ' + (JSON.stringify(error.response.data) || 'Проверьте введённые данные'));
            } else {
                console.error('Ошибка сети:', error);
                alert('Ошибка соединения');
            }
        }
    });
});
