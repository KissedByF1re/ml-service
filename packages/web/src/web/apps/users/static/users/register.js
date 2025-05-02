document.addEventListener('DOMContentLoaded', function() {
    const registerBtn = document.getElementById('register-btn');

    registerBtn.addEventListener('click', async function() {
        const data = {
            email: document.getElementById('email').value,
            username: document.getElementById('username').value,
            password1: document.getElementById('password1').value,
            password2: document.getElementById('password2').value
        };

        try {
            const response = await axios.post(
                `${domain}/api/users/auth/registration/`,
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
                console.error('Ошибка регистрации:', error.response);
                alert('Ошибка регистрации: ' + (JSON.stringify(error.response.data) || 'Проверьте введённые данные'));
            } else {
                console.error('Ошибка сети:', error);
                alert('Ошибка соединения');
            }
        }
    });
});
