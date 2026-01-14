// Функция инициализации
async function init() {
    try {
        // Спрашиваем бэкенд про устройства
        const response = await fetch("http://localhost:8000/api/devices");
        const devices = await response.json();

        const wizard = document.getElementById('wizard-screen');
        const dashboard = document.getElementById('dashboard-screen');

        if (devices.length === 0) {
            // Если устройств нет - показываем мастер настройки
            wizard.classList.remove('hidden');
            dashboard.classList.add('hidden');
        } else {
            // Если есть - идем в дашборд
            wizard.classList.add('hidden');
            dashboard.classList.remove('hidden');
            displayDevices(devices);
        }
    } catch (error) {
        console.error("Ошибка связи с бэкендом:", error);
        alert("Бэкенд недоступен. Проверьте Docker.");
    }
}

// Сохранение нового устройства
async function saveDevice() {
    const deviceData = {
        id: document.getElementById('dev_id').value,
        label: document.getElementById('dev_label').value,
        device_type: document.getElementById('dev_type').value,
        connection_type: document.getElementById('conn_type').value,
        pin_number: parseInt(document.getElementById('pin_val').value) || 0
    };

    const response = await fetch("http://localhost:8000/api/devices/setup", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(deviceData)
    });

    if (response.ok) {
        alert("Настройка завершена!");
        init(); // Перезагружаем интерфейс
    }
}

function displayDevices(devices) {
    const list = document.getElementById('device-list');
    list.innerHTML = devices.map(d => `
        <div class="device-item">
            <strong>${d.label}</strong> (ID: ${d.id})<br>
            Пин: ${d.pin_number} | Статус: ${d.status}
        </div>
    `).join('');
}

// Запускаем проверку при загрузке страницы
window.onload = init;