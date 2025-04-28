document.addEventListener('DOMContentLoaded', function() {
    const exitBtn = document.getElementById('exit-btn');

    exitBtn.addEventListener('click', async function() {
        try {
            const response = await axios.post(
                `${domain}/api/users/auth/logout/`,
                null,
                {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    withCredentials: true
                }
            );
            window.location.href = `${logoutRedirectURL}`;
        } catch (error) {
            if (error.response) {
                console.error('Ошибка выхода:', error.response);
                alert('Ошибка выхода: ' + (JSON.stringify(error.response.data)));
            } else {
                console.error('Ошибка сети:', error);
                alert('Ошибка соединения');
            }
        }
    });
});
