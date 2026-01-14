const API_BASE = "http://localhost:8000/api";

const HydroAPI = {
    // Проверка устройств
    async checkDevices() {
        const response = await fetch(`${API_BASE}/devices`);
        return await response.json();
    },

    // Сохранение настроек
    async saveDevice(deviceData) {
        const response = await fetch(`${API_BASE}/devices/setup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(deviceData)
        });
        return await response.json();
    }
};