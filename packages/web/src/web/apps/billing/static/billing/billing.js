axios.defaults.withCredentials = true;

function formatDate(dateString) {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${day}.${month}.${year} ${hours}:${minutes}`;
}

function formatTransactionType(type) {
    if (type === 'debit') return 'Списание';
    if (type === 'deposit') return 'Пополнение';
    return type;
}

async function loadBillingData() {
    try {
        const balanceResp = await axios.get(`${domain}/api/billing/balance/`);
        const transactionsResp = await axios.get(`${domain}/api/billing/transactions/`);
        const servicesResp = await axios.get(`${domain}/api/billing/service_orders/`);

        document.getElementById('balance').innerText = `${balanceResp.data.value} ${balanceResp.data.currency}`;

        const transactionsList = document.getElementById('transactionsList');
        transactionsList.innerHTML = '';
        transactionsResp.data.forEach(tx => {
            const item = document.createElement('li');
            item.className = 'list-group-item';
            const formattedDate = formatDate(tx.created_at);
            const formattedType = formatTransactionType(tx.type);
            item.innerText = `${formattedDate} ${formattedType}: ${tx.value} ${balanceResp.data.currency}`;
            transactionsList.appendChild(item);
        });

        const servicesList = document.getElementById('servicesList');
        servicesList.innerHTML = '';
        servicesResp.data.forEach(service => {
            const item = document.createElement('li');
            item.className = 'list-group-item';
            const formattedDate = formatDate(service.created_at);
            item.innerText = `${formattedDate} ${service.service.name} (${service.service.model}): ${service.price} ${balanceResp.data.currency}`;
            servicesList.appendChild(item);
        });

    } catch (error) {
        console.error(error);
        alert('Ошибка при загрузке данных');
    }
}

async function DepositBalance() {
    const amount = document.getElementById('depositAmount').value;
    if (!amount || amount <= 0) {
        alert('Введите корректную сумму');
        return;
    }

    try {
        const response = await axios.put(`${domain}/api/billing/balance/deposit/`, {
            amount: parseInt(amount),
        });

        document.getElementById('balance').innerText = `${response.data.value} ${response.data.currency}`;
        document.getElementById('depositAmount').value = '';
        await loadBillingData();
    } catch (error) {
        console.error(error);
        alert('Ошибка при пополнении');
    }
}

document.addEventListener('DOMContentLoaded', loadBillingData);