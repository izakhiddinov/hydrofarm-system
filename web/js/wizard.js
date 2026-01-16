const API_URL = "http://localhost:8000/api";
let currentSelectedPin = null;
let assignedDevices = {};

// Группировка пинов по вашим схемам [cite: 32, 63, 102, 132, 175]
const RPI5_PINOUT = {
    1: { type: 'system', label: '3.3V' }, 2: { type: 'system', label: '5V' },
    3: { type: 'special', label: 'SDA1', msg: 'Шина I2C. Только для АЦП (pH/TDS Meter).' },
    4: { type: 'system', label: '5V' },
    5: { type: 'special', label: 'SCL1', msg: 'Шина I2C. Только для АЦП (pH/TDS Meter).' },
    6: { type: 'system', label: 'GND' },
    8: { type: 'special', label: 'TXD0', msg: 'UART: Modbus/Debug.' },
    9: { type: 'system', label: 'GND' },
    10: { type: 'special', label: 'RXD0', msg: 'UART: Modbus/Debug.' },
    14: { type: 'system', label: 'GND' }, 20: { type: 'system', label: 'GND' },
    25: { type: 'system', label: 'GND' }, 30: { type: 'system', label: 'GND' },
    34: { type: 'system', label: 'GND' }, 39: { type: 'system', label: 'GND' }
};

function init() {
    const container = document.getElementById('rpi-header-view');
    if (!container) return;
    let html = "";
    for (let i = 1; i <= 40; i++) {
        const pinConfig = RPI5_PINOUT[i] || { type: 'free', label: `GPIO${i}` };
        let statusClass = assignedDevices[i] ? 'busy' : pinConfig.type;
        html += `<div class="pin-slot ${statusClass}" onclick="handlePinClick(${i})">
                    <span>PIN ${i}</span>
                    <span>${assignedDevices[i] ? 'BUSY' : pinConfig.label}</span>
                 </div>`;
    }
    container.innerHTML = html;
    document.getElementById('modal-overlay').classList.add('hidden');
}

async function handlePinClick(num) {
    currentSelectedPin = num;
    const pin = RPI5_PINOUT[num] || { type: 'free', label: `GPIO ${num}` };
    const content = document.getElementById('panel-content');

    if (pin.type === 'system') {
        content.innerHTML = `<div style="color:red; padding:10px; border:1px solid red;"><h3>Пин №${num}</h3>Запрещено. Питание/Земля.</div>`;
        return;
    }

    let warning = pin.type === 'special' ? `<div style="background:#fff3cd; padding:10px; margin-bottom:10px;">⚠️ ${pin.msg}</div>` : "";

    content.innerHTML = `<h3>Настройка Пина №${num}</h3>${warning}
        <div style="display:flex; gap:10px;">
            <button onclick="loadCatalog('IN')" style="flex:1; padding:10px;">📥 ВХОД</button>
            <button onclick="loadCatalog('OUT')" style="flex:1; padding:10px;">📤 ВЫХОД</button>
        </div>`;
}

async function loadCatalog(direction) {
    const res = await fetch(`${API_URL}/catalog?direction=${direction}`);
    const data = await res.json();
    const content = document.getElementById('panel-content');
    content.innerHTML = `<h3>Выбор для PIN ${currentSelectedPin}</h3>
        ${data.map(item => `<div style="border:1px solid #ccc; padding:10px; margin-bottom:5px; cursor:pointer;" onclick="openSchema('${item.id}')">
            <b>${item.model_name}</b></div>`).join('')}
        <button onclick="handlePinClick(${currentSelectedPin})">Назад</button>`;
}

async function openSchema(modelId) {
    const res = await fetch(`${API_URL}/catalog`);
    const catalog = await res.json();
    const item = catalog.find(i => i.id === modelId);
    document.getElementById('modal-overlay').classList.remove('hidden');
    document.getElementById('modal-body').innerHTML = `
        <h2>Схема: ${item.model_name}</h2>
        <div style="background:#eee; padding:20px; text-align:center;">
            <svg width="300" height="100">
                <rect x="10" y="10" width="50" height="80" fill="#2c3e50"/>
                <circle cx="50" cy="50" r="5" fill="green"/>
                <line x1="50" y1="50" x2="200" y2="50" stroke="green" stroke-dasharray="4"/>
                <text x="15" y="45" fill="white" font-size="8">PIN ${currentSelectedPin}</text>
            </svg>
        </div>
        <p>${item.desc} [cite: 32, 63, 102, 132, 175]</p>
        <button onclick="confirmSave('${item.id}', '${item.model_name}')" style="background:green; color:white; padding:10px;">Сохранить</button>
        <button onclick="document.getElementById('modal-overlay').classList.add('hidden')">Отмена</button>`;
}

function confirmSave(id, name) {
    assignedDevices[currentSelectedPin] = { id, name };
    init();
}

window.onload = init;