axios.defaults.withCredentials = true;

async function loadServices() {
    try {
        const response = await axios.get(`${domain}/api/billing/services/`);
        const services = response.data;
        const serviceSelect = document.getElementById('serviceSelect');

        serviceSelect.innerHTML = '<option value="">Выберите услугу</option>';

        services.forEach(service => {
            const option = document.createElement('option');
            option.value = service.id;
            option.textContent = `${service.name} (${service.model}) - ${service.price} RUB`;
            serviceSelect.appendChild(option);
        });
    } catch (error) {
        console.error(error);
        alert('Ошибка при загрузке списка услуг');
    }
}

document.getElementById('predictionForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const serviceId = document.getElementById('serviceSelect').value;
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];

    if (!serviceId || !file) {
        alert('Пожалуйста, выберите услугу и загрузите CSV-файл');
        return;
    }

    try {
        const orderResponse = await axios.post(`${domain}/api/billing/services/order/`, {
            service_id: parseInt(serviceId)
        });

        const serviceOrderId = orderResponse.data.id;

        const formData = new FormData();
        formData.append('file', file);

        const predictionResponse = await axios.post(`${domain}/api/prediction/?service_order_id=${serviceOrderId}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        const taskId = predictionResponse.data.task_id;

        document.getElementById('statusCard').classList.remove('d-none');
        document.getElementById('taskStatus').textContent = 'Задача отправлена. Ожидание результата...';

        pollTaskStatus(taskId);

    } catch (error) {
        console.error(error);
        alert('Ошибка при отправке запроса на предсказание');
    }
});

function pollTaskStatus(taskId) {
    const interval = setInterval(async () => {
        try {
            const response = await axios.get(`${domain}/api/prediction/?task_id=${taskId}`, {
                responseType: 'blob'
            });

            const result = await response.data.text();
            let jsonResponse;
            try {
                jsonResponse = JSON.parse(result);
            } catch (e) {
                jsonResponse = null;
            }

            if (jsonResponse && (jsonResponse.status === 'PENDING' || jsonResponse.status === 'STARTED')) {
                document.getElementById('taskStatus').textContent = 'Задача в процессе выполнения...';
            } else if (response.headers['content-type'].includes('text/csv')) {
                clearInterval(interval);
                document.getElementById('taskStatus').textContent = 'Файл готов. Начинаем скачивание...';

                const blob = new Blob([response.data]);
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = downloadUrl;
                a.download = 'prediction_result.csv';
                document.body.appendChild(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(downloadUrl);
            } else {
                document.getElementById('taskStatus').textContent = 'Неизвестный статус задачи.';
                clearInterval(interval);
            }
        } catch (error) {
            console.error(error);
            clearInterval(interval);
            document.getElementById('taskStatus').textContent = 'Ошибка при получении статуса задачи.';
        }
    }, 250);
}

document.addEventListener('DOMContentLoaded', loadServices);