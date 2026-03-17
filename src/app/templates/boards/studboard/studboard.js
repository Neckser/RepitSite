// Состояние приложения
let roomToken = null;
let ws = null;
let isConnected = false;

// Canvas элементы
const canvas = document.getElementById('whiteboard');
const ctx = canvas.getContext('2d');
const container = document.getElementById('canvasContainer');

// Инструменты
const TOOLS = {
    CURSOR: 'cursor',
    BRUSH: 'brush',
    ERASER: 'eraser'
};

let currentTool = TOOLS.CURSOR;
let color = '#000000';
let brushSize = 5;

// Хранилище элементов
let images = []; // картинки
let drawings = []; // линии
let selectedImageId = null;
let isDraggingImage = false;
let isResizing = false;
let dragOffsetX = 0;
let dragOffsetY = 0;
let resizeDirection = null;
let initialSize = { width: 0, height: 0 };
let initialPosition = { x: 0, y: 0 };
let initialMouse = { x: 0, y: 0 };

// Рисование
let isDrawing = false;
let lastX = 0;
let lastY = 0;
let currentLine = null;

// Масштабирование и панорамирование
let scale = 1;
let panX = 0;
let panY = 0;
let isPanning = false;
let panStartX = 0;
let panStartY = 0;

// Счетчик пользователей
let usersCount = 1;

// УДАЛЯЕМ ЭТОТ БЛОК (он вызывает ошибку):
// document.getElementById('copyRoomLink').addEventListener('click', () => {
//     const url = `${window.location.origin}?room=${roomToken}`;
//     navigator.clipboard.writeText(url);
//     alert('Ссылка скопирована!');
// });

// Функция для правильного определения протокола WebSocket (как в чате)
function getWebSocketUrl(roomToken) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    return `${protocol}//${host}/ws/board/${roomToken}`;
}
// Автоматическое подключение при загрузке страницы
window.addEventListener('load', () => {
    // Получаем room_token из скрытого поля
    const token = document.getElementById('currentRoom')?.value;
    
    if (token) {
        // Сразу подключаемся
        roomToken = token;
        // НЕ НАДО менять textContent, потому что это скрытое поле
        // document.getElementById('currentRoom').textContent = token;
        connectWebSocket();
    } else {
        console.error('Нет токена комнаты!');
    }
});

function connectWebSocket() {
    try {
        const wsUrl = getWebSocketUrl(roomToken);
        console.log('Connecting to WebSocket:', wsUrl);
        ws = new WebSocket(wsUrl);
        
        ws.onopen = () => {
            console.log('Connected to room:', roomToken);
            isConnected = true;
        };
        
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            
            if (message.type === 'init') {
                // Инициализация - загружаем состояние комнаты
                console.log('Получена инициализация:', message.data);
                
                // Загружаем линии
                drawings = message.data.drawings || [];
                
                // Загружаем картинки (асинхронно)
                images = [];
                if (message.data.images && message.data.images.length > 0) {
                    loadImagesSequentially(message.data.images);
                } else {
                    redrawCanvas();
                }
            } 
            else if (message.sender !== id(ws)) {
                // Получено сообщение от другого пользователя
                console.log('Получено сообщение:', message.type);
                
                switch(message.type) {
                    case 'draw_line':
                        drawings.push(message.data);
                        redrawCanvas();
                        break;
                        
                    case 'add_image':
                        // Добавляем картинку не удаляя существующие
                        addImageFromData(message.data);
                        break;
                        
                    case 'move_image':
                        updateImagePosition(message.data.id, message.data.x, message.data.y);
                        break;
                        
                    case 'resize_image':
                        updateImageSize(message.data.id, message.data);
                        break;
                        
                    case 'delete_image':
                        images = images.filter(img => img.id !== message.data.id);
                        if (selectedImageId === message.data.id) {
                            selectedImageId = null;
                        }
                        redrawCanvas();
                        break;
                        
                    case 'clear_board':
                        drawings = [];
                        images = [];
                        selectedImageId = null;
                        redrawCanvas();
                        break;
                }
            }
        };
        
        ws.onclose = () => {
            console.log('Disconnected from room');
            isConnected = false;
            // Пробуем переподключиться через 2 секунды
            setTimeout(connectWebSocket, 2000);
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
        
    } catch (error) {
        console.error('Error creating WebSocket:', error);
    }
}

// Функция для последовательной загрузки изображений
function loadImagesSequentially(imageDataArray) {
    let loadedCount = 0;
    
    imageDataArray.forEach(imgData => {
        const img = new Image();
        img.onload = () => {
            images.push({
                id: imgData.id,
                img: img,
                x: imgData.x,
                y: imgData.y,
                width: imgData.width,
                height: imgData.height
            });
            
            loadedCount++;
            if (loadedCount === imageDataArray.length) {
                // Все картинки загружены - перерисовываем
                redrawCanvas();
            }
        };
        img.onerror = () => {
            console.error('Ошибка загрузки изображения:', imgData.id);
            loadedCount++;
            if (loadedCount === imageDataArray.length) {
                redrawCanvas();
            }
        };
        img.src = imgData.data;
    });
}

function id(ws) {
    // Простой способ получить ID соединения
    return ws._id || (ws._id = Math.random());
}

// Инструменты
document.getElementById('toolCursor').addEventListener('click', () => setTool(TOOLS.CURSOR));
document.getElementById('toolBrush').addEventListener('click', () => setTool(TOOLS.BRUSH));
document.getElementById('toolEraser').addEventListener('click', () => setTool(TOOLS.ERASER));

function setTool(tool) {
    currentTool = tool;
    
    document.querySelectorAll('.tool-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    if (tool === TOOLS.CURSOR) {
        document.getElementById('toolCursor').classList.add('active');
        canvas.style.cursor = 'default';
    } else if (tool === TOOLS.BRUSH) {
        document.getElementById('toolBrush').classList.add('active');
        canvas.style.cursor = 'crosshair';
    } else if (tool === TOOLS.ERASER) {
        document.getElementById('toolEraser').classList.add('active');
        canvas.style.cursor = 'cell';
    }
}

// Цвет и размер
document.getElementById('colorPicker').addEventListener('input', (e) => {
    color = e.target.value;
});

document.getElementById('brushSize').addEventListener('input', (e) => {
    brushSize = parseInt(e.target.value);
    document.getElementById('sizeValue').textContent = brushSize;
});

// Зум
document.getElementById('zoomIn').addEventListener('click', () => {
    scale = Math.min(3, scale + 0.25);
    updateZoom();
});

document.getElementById('zoomOut').addEventListener('click', () => {
    scale = Math.max(0.25, scale - 0.25);
    updateZoom();
});

document.getElementById('zoomReset').addEventListener('click', () => {
    scale = 1;
    panX = 0;
    panY = 0;
    updateZoom();
});

function updateZoom() {
    canvas.style.transform = `translate(${panX}px, ${panY}px) scale(${scale})`;
    document.getElementById('zoomLevel').textContent = Math.round(scale * 100) + '%';
}

// Зум колесиком
container.addEventListener('wheel', (e) => {
    e.preventDefault();
    
    const delta = e.deltaY > 0 ? -0.1 : 0.1;
    const newScale = Math.min(3, Math.max(0.25, scale + delta));
    
    const rect = container.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    const scaleChange = newScale / scale;
    panX = mouseX - (mouseX - panX) * scaleChange;
    panY = mouseY - (mouseY - panY) * scaleChange;
    
    scale = newScale;
    updateZoom();
}, { passive: false });

// Перемещение правой кнопкой
container.addEventListener('mousedown', (e) => {
    if (e.button === 2) {
        e.preventDefault();
        isPanning = true;
        panStartX = e.clientX - panX;
        panStartY = e.clientY - panY;
        container.classList.add('dragging');
    }
});

container.addEventListener('mousemove', (e) => {
    if (isPanning) {
        panX = e.clientX - panStartX;
        panY = e.clientY - panStartY;
        updateZoom();
    }
});

container.addEventListener('mouseup', (e) => {
    if (e.button === 2) {
        isPanning = false;
        container.classList.remove('dragging');
    }
});

container.addEventListener('contextmenu', (e) => e.preventDefault());

// Координаты мыши на canvas
function getCanvasCoordinates(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: (e.clientX - rect.left) / scale,
        y: (e.clientY - rect.top) / scale
    };
}

// События мыши на canvas
canvas.addEventListener('mousedown', (e) => {
    if (e.button !== 0 || isPanning) return;
    
    const { x, y } = getCanvasCoordinates(e);
    
    if (currentTool === TOOLS.CURSOR) {
        handleCursorMouseDown(e, x, y);
    } else if (currentTool === TOOLS.BRUSH) {
        startDrawing(x, y, color);
    } else if (currentTool === TOOLS.ERASER) {
        startDrawing(x, y, '#ffffff');
    }
});

canvas.addEventListener('mousemove', (e) => {
    if (isPanning) return;
    
    const { x, y } = getCanvasCoordinates(e);
    
    if (currentTool === TOOLS.CURSOR) {
        handleCursorMouseMove(x, y);
    } else if (isDrawing) {
        continueDrawing(x, y);
    }
});

canvas.addEventListener('mouseup', () => {
    if (isDrawing && currentLine) {
        console.log('Отправляем линию на сервер, точек:', currentLine.points.length);
        
        // Сохраняем локально
        drawings.push(currentLine);
        
        // Отправляем на сервер
        ws.send(JSON.stringify({
            type: 'draw_line',
            data: currentLine
        }));
        
        // Перерисовываем
        redrawCanvas();
    }
    
    isDrawing = false;
    isDraggingImage = false;
    isResizing = false;
    currentLine = null;
});

canvas.addEventListener('mouseout', () => {
    isDrawing = false;
    isDraggingImage = false;
    isResizing = false;
    currentLine = null;
});

// Обработка курсора
function handleCursorMouseDown(e, x, y) {
    // Ищем картинку под курсором
    for (let i = images.length - 1; i >= 0; i--) {
        const img = images[i];
        if (x >= img.x - 5 && x <= img.x + img.width + 5 &&
            y >= img.y - 5 && y <= img.y + img.height + 5) {
            
            selectedImageId = img.id;
            
            // Проверяем углы для изменения размера
            const cornerSize = 10;
            if (Math.abs(x - (img.x + img.width)) < cornerSize && 
                Math.abs(y - (img.y + img.height)) < cornerSize) {
                isResizing = true;
                resizeDirection = 'se';
            } else if (Math.abs(x - img.x) < cornerSize && 
                       Math.abs(y - img.y) < cornerSize) {
                isResizing = true;
                resizeDirection = 'nw';
            } else if (Math.abs(x - (img.x + img.width)) < cornerSize && 
                       Math.abs(y - img.y) < cornerSize) {
                isResizing = true;
                resizeDirection = 'ne';
            } else if (Math.abs(x - img.x) < cornerSize && 
                       Math.abs(y - (img.y + img.height)) < cornerSize) {
                isResizing = true;
                resizeDirection = 'sw';
            }
            
            if (isResizing) {
                initialSize = { width: img.width, height: img.height };
                initialPosition = { x: img.x, y: img.y };
                initialMouse = { x, y };
            } else {
                isDraggingImage = true;
                dragOffsetX = x - img.x;
                dragOffsetY = y - img.y;
                
                // Поднимаем картинку наверх
                images.splice(i, 1);
                images.push(img);
            }
            
            redrawCanvas();
            return;
        }
    }
    
    selectedImageId = null;
    redrawCanvas();
}

function handleCursorMouseMove(x, y) {
    if (isResizing && selectedImageId) {
        const img = images.find(i => i.id === selectedImageId);
        if (img) {
            const deltaX = x - initialMouse.x;
            const deltaY = y - initialMouse.y;
            
            let newX = img.x;
            let newY = img.y;
            let newWidth = img.width;
            let newHeight = img.height;
            
            if (resizeDirection === 'se') {
                newWidth = Math.max(20, initialSize.width + deltaX);
                newHeight = Math.max(20, initialSize.height + deltaY);
            } else if (resizeDirection === 'nw') {
                newWidth = Math.max(20, initialSize.width - deltaX);
                newHeight = Math.max(20, initialSize.height - deltaY);
                newX = initialPosition.x + (initialSize.width - newWidth);
                newY = initialPosition.y + (initialSize.height - newHeight);
            } else if (resizeDirection === 'ne') {
                newWidth = Math.max(20, initialSize.width + deltaX);
                newHeight = Math.max(20, initialSize.height - deltaY);
                newY = initialPosition.y + (initialSize.height - newHeight);
            } else if (resizeDirection === 'sw') {
                newWidth = Math.max(20, initialSize.width - deltaX);
                newHeight = Math.max(20, initialSize.height + deltaY);
                newX = initialPosition.x + (initialSize.width - newWidth);
            }
            
            // Обновляем картинку
            img.x = newX;
            img.y = newY;
            img.width = newWidth;
            img.height = newHeight;
            
            // Отправляем изменения на сервер
            ws.send(JSON.stringify({
                type: 'resize_image',
                data: {
                    id: img.id,
                    x: newX,
                    y: newY,
                    width: newWidth,
                    height: newHeight
                }
            }));
            
            redrawCanvas();
        }
    } else if (isDraggingImage && selectedImageId) {
        const img = images.find(i => i.id === selectedImageId);
        if (img) {
            img.x = x - dragOffsetX;
            img.y = y - dragOffsetY;
            
            // Отправляем новую позицию на сервер
            ws.send(JSON.stringify({
                type: 'move_image',
                data: {
                    id: img.id,
                    x: img.x,
                    y: img.y
                }
            }));
            
            redrawCanvas();
        }
    }
}

// Рисование
function startDrawing(x, y, lineColor) {
    isDrawing = true;
    currentLine = {
        points: [{ x, y }],
        color: lineColor,
        width: brushSize
    };
    lastX = x;
    lastY = y;
}

function continueDrawing(x, y) {
    if (!currentLine) return;
    
    // Рисуем локально
    ctx.beginPath();
    ctx.strokeStyle = currentLine.color;
    ctx.lineWidth = brushSize;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(x, y);
    ctx.stroke();
    
    // Сохраняем точку
    currentLine.points.push({ x, y });
    lastX = x;
    lastY = y;
}

// Добавление картинки
document.getElementById('imageInput').addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const imageId = 'img_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                
                // Вычисляем размер
                let width = img.width;
                let height = img.height;
                const maxSize = 400;
                
                if (width > maxSize || height > maxSize) {
                    if (width > height) {
                        height = (height / width) * maxSize;
                        width = maxSize;
                    } else {
                        width = (width / height) * maxSize;
                        height = maxSize;
                    }
                }
                
                // Центрируем
                const viewportCenterX = (-panX / scale) + (container.clientWidth / (2 * scale));
                const viewportCenterY = (-panY / scale) + (container.clientHeight / (2 * scale));
                
                const imageData = {
                    id: imageId,
                    data: event.target.result,
                    x: viewportCenterX - width/2,
                    y: viewportCenterY - height/2,
                    width: width,
                    height: height
                };
                
                // Добавляем в локальное хранилище
                addImageFromData(imageData);
                
                // Отправляем на сервер
                ws.send(JSON.stringify({
                    type: 'add_image',
                    data: imageData
                }));
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    }
});

function addImageFromData(imageData) {
    // Проверяем, есть ли уже такая картинка
    const exists = images.some(img => img.id === imageData.id);
    if (exists) return;
    
    const img = new Image();
    img.onload = () => {
        images.push({
            id: imageData.id,
            img: img,
            x: imageData.x,
            y: imageData.y,
            width: imageData.width,
            height: imageData.height
        });
        redrawCanvas();
    };
    img.src = imageData.data;
}

function updateImagePosition(id, x, y) {
    const img = images.find(i => i.id === id);
    if (img) {
        img.x = x;
        img.y = y;
        redrawCanvas();
    }
}

function updateImageSize(id, data) {
    const img = images.find(i => i.id === id);
    if (img) {
        img.x = data.x;
        img.y = data.y;
        img.width = data.width;
        img.height = data.height;
        redrawCanvas();
    }
}

// Удаление по Delete
document.addEventListener('keydown', (e) => {
    if (e.key === 'Delete' && selectedImageId && currentTool === TOOLS.CURSOR) {
        ws.send(JSON.stringify({
            type: 'delete_image',
            data: { id: selectedImageId }
        }));
        
        images = images.filter(img => img.id !== selectedImageId);
        selectedImageId = null;
        redrawCanvas();
    }
});

// Очистка доски
document.getElementById('clearBtn').addEventListener('click', () => {
    if (confirm('Очистить всю доску?')) {
        ws.send(JSON.stringify({
            type: 'clear_board',
            data: {}
        }));
        
        drawings = [];
        images = [];
        selectedImageId = null;
        redrawCanvas();
    }
});

// Сохранение
document.getElementById('saveBtn').addEventListener('click', () => {
    // Сохраняем текущее состояние
    const currentTransform = canvas.style.transform;
    
    // Создаем временный canvas для сохранения
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext('2d');
    
    // Заливаем белым фоном
    tempCtx.fillStyle = '#FFFFFF';
    tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
    
    // Рисуем оригинальный canvas поверх белого фона
    tempCtx.drawImage(canvas, 0, 0);
    
    // Сохраняем
    const link = document.createElement('a');
    link.download = `whiteboard-${roomToken}-${Date.now()}.png`;
    link.href = tempCanvas.toDataURL('image/png');
    link.click();
    
    // Возвращаем оригинальное состояние
    canvas.style.transform = currentTransform;
});

// Перерисовка canvas
function redrawCanvas() {
    // Полностью очищаем canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 1. СНАЧАЛА рисуем ВСЕ картинки (они как подложка)
    if (images && images.length > 0) {
        images.forEach(img => {
            if (img && img.img) {
                try {
                    ctx.drawImage(img.img, img.x, img.y, img.width, img.height);
                    
                    // Рамка для выделенной картинки
                    if (img.id === selectedImageId && currentTool === TOOLS.CURSOR) {
                        ctx.strokeStyle = '#007bff';
                        ctx.lineWidth = 2;
                        ctx.setLineDash([5, 5]);
                        ctx.strokeRect(img.x - 2, img.y - 2, img.width + 4, img.height + 4);
                        ctx.setLineDash([]);
                        
                        // Маркеры углов
                        ctx.fillStyle = '#007bff';
                        ctx.fillRect(img.x - 4, img.y - 4, 8, 8);
                        ctx.fillRect(img.x + img.width - 4, img.y - 4, 8, 8);
                        ctx.fillRect(img.x - 4, img.y + img.height - 4, 8, 8);
                        ctx.fillRect(img.x + img.width - 4, img.y + img.height - 4, 8, 8);
                    }
                } catch (e) {
                    console.error('Ошибка при рисовании картинки:', e);
                }
            }
        });
    }
    
    // 2. ПОТОМ рисуем ВСЕ линии (они поверх картинок)
    if (drawings && drawings.length > 0) {
        drawings.forEach(line => {
            if (!line || !line.points || line.points.length < 2) return;
            
            try {
                ctx.beginPath();
                ctx.strokeStyle = line.color || '#000000';
                ctx.lineWidth = line.width || 5;
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                
                ctx.moveTo(line.points[0].x, line.points[0].y);
                for (let i = 1; i < line.points.length; i++) {
                    ctx.lineTo(line.points[i].x, line.points[i].y);
                }
                ctx.stroke();
            } catch (e) {
                console.error('Ошибка при рисовании линии:', e);
            }
        });
    }
    
    console.log('Canvas перерисован. Линий:', drawings?.length, 'Картинок:', images?.length);
}