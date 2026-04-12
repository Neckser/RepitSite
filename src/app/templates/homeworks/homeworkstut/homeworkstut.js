// ========== МОДАЛЬНОЕ ОКНО ДЛЯ ДОМАШНИХ ЗАДАНИЙ ==========

window.showHomeworkTasksModal = function(button) {
    const assignmentItem = button.closest('.assignment-item');
    const homeworkId = assignmentItem.querySelector('input[name="homework_id"]').value;
    const subject = assignmentItem.querySelector('.subject-badge').innerText;
    const title = assignmentItem.querySelector('.assignment-item__title').innerText;
    const deadline = assignmentItem.querySelector('.assignment-item__date')?.innerText || '';

    // ПРИМЕРЫ ЗАДАЧ ДЛЯ ТЕСТИРОВАНИЯ (можно будет заменить на реальные данные)
    // const tasksHtml = `
    //     <div class="task-mini-card">
    //         <div class="task-mini-header">Задание 1 • Текст</div>
    //         <p class="task-content">Решить квадратное уравнение: 2x² + 5x - 3 = 0. Найти оба корня и сделать проверку.</p>
    //     </div>
    //     <div class="task-mini-card">
    //         <div class="task-mini-header">Задание 3 • Текст</div>
    //         <p class="task-content">Найти производную функции f(x) = x³ - 6x² + 9x - 2 и определить точки экстремума.</p>
    //     </div>
    //     <div class="task-mini-card">
    //         <div class="task-mini-header">Задание 4 • Текст</div>
    //         <p class="task-content">Решить систему уравнений: { x + y = 7; x² + y² = 25 }</p>
    //     </div>
    //     <div class="task-mini-card">
    //         <div class="task-mini-header">Задание 6 • Текст</div>
    //         <p class="task-content">Доказать теорему Пифагора тремя разными способами.</p>
    //     </div>
    // `;

    const hiddenTasks = assignmentItem.querySelector(".hidden-tasks-content");
    let tasksHtml = hiddenTasks ? hiddenTasks.innerHTML : '<p style="text-align: center; color: #888; padding: 20px;">Нет заданий</p>';

    let modal = document.getElementById('homeworkModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'homeworkModal';
        modal.className = 'modal-overlay';
        document.body.appendChild(modal);
    }

    modal.innerHTML = `
        <div class="modal-container">
            <div class="modal-header">
                <h2>Домашнее задание: ${subject}</h2>
                <button class="modal-close" onclick="closeHomeworkModal()">×</button>
            </div>
            <div class="modal-content">
                <div class="lesson-info-summary">
                    <div class="info-pill"><strong>Тема:</strong> ${title}</div>
                    <div class="info-pill"><strong>Срок:</strong> ${deadline}</div>
                </div>

                <h3>Текущие задания</h3>
                <div class="tasks-scroll-container">
                    ${tasksHtml}
                </div>
                <form action="/add_homework_task/${homeworkId}" method="POST" enctype="multipart/form-data">
                    <h3 style="margin-bottom: 8px !important;">Добавить еще задание</h3>
                    <div class="task-type-toggle">
                        <label>
                            <input type="radio" name="task_type" value="text" checked onclick="toggleHomeworkTaskType('text')">
                            <span>Текст</span>
                        </label>
                        <label>
                            <input type="radio" name="task_type" value="image" onclick="toggleHomeworkTaskType('image')">
                            <span>Картинка</span>
                        </label>
                    </div>

                    <div class="modal-form__input-container">
                        <div id="homework_task_text_input">
                            <textarea name="task_text" placeholder="Текст нового задания..."></textarea>
                        </div>

                        <div id="homework_task_image_input" style="display: none;">
                            <div class="file-upload-styled">
                                <input type="file" name="task_file" accept="image/*">
                                <p>Загрузите фото задания</p>
                            </div>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn-save-all">Добавить в список</button>
                </form>
            </div>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
};

// Функция переключения типа задания (моментальное переключение полей)
window.toggleHomeworkTaskType = function(type) {
    const textInput = document.getElementById('homework_task_text_input');
    const imageInput = document.getElementById('homework_task_image_input');
    
    if (textInput && imageInput) {
        if (type === 'text') {
            textInput.style.display = 'block';
            imageInput.style.display = 'none';
        } else {
            textInput.style.display = 'none';
            imageInput.style.display = 'block';
        }
    }
};

// Закрытие модалки
window.closeHomeworkModal = function() {
    const modal = document.getElementById('homeworkModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
};

// Закрытие по клику на фон и Escape
document.addEventListener('click', function(e) {
    const modal = document.getElementById('homeworkModal');
    if (e.target === modal) closeHomeworkModal();
});
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeHomeworkModal();
});

// Функция открытия картинки во весь экран
window.openFullImage = function(src) {
    let overlay = document.getElementById('fullImageOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'fullImageOverlay';
        overlay.className = 'full-image-overlay';
        overlay.innerHTML = `<img src="" id="fullImageItem" alt="Полноэкранное изображение">`;
        document.body.appendChild(overlay);
        
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay || e.target.classList.contains('full-image-overlay')) {
                closeFullscreenImage();
            }
        });
    }
    
    const img = document.getElementById('fullImageItem');
    img.src = src;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Закрытие по Escape
    const escHandler = function(e) {
        if (e.key === 'Escape') {
            closeFullscreenImage();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
};

// Функция закрытия полноэкранного режима
window.closeFullscreenImage = function() {
    const overlay = document.getElementById('fullImageOverlay');
    if (overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(function() {
            const img = document.getElementById('fullImageItem');
            if (img) img.src = '';
        }, 300);
    }
};