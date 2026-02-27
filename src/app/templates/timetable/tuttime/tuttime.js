window.showLessonModal = function(button) {
    const lessonCard = button.closest('.lesson-card');
    const lessonId = lessonCard.querySelector('input[name="lesson_id"]').value;
    const subject = lessonCard.querySelector('.subject-badge').innerText;
    const student = lessonCard.querySelector('.schedule__lesson-student span').innerText;
    const time = lessonCard.querySelector('.schedule__lesson-time').innerText;

    let tasksHtml = lessonCard.querySelector(".hidden-tasks-content").innerHTML;

    let modal = document.getElementById('lessonModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'lessonModal';
        modal.className = 'modal-overlay';
        document.body.appendChild(modal);
    }

    modal.innerHTML = `
        <div class="modal-container">
            <div class="modal-header">
                <h2>Урок: ${subject}</h2>
                <button class="modal-close" onclick="closeLessonModal()">×</button>
            </div>
            <div class="modal-content">
                <div class="lesson-info-summary">
                    <div class="info-pill"><strong>Ученик:</strong> ${student}</div>
                    <div class="info-pill"><strong>Время:</strong> ${time}</div>
                </div>

                <h3>Текущие задания</h3>
                <div class="tasks-scroll-container">
                    ${tasksHtml}
                </div>

                <form action="/add_lesson_task/${lessonId}" method="POST" enctype="multipart/form-data" class="modal-form">
                    <h3>Добавить еще задание</h3>
                    <div class="task-type-toggle">
                        <label>
                            <input type="radio" name="task_type" value="text" checked onclick="toggleTaskType('text')">
                            <span>Текст</span>
                        </label>
                        <label>
                            <input type="radio" name="task_type" value="image" onclick="toggleTaskType('image')">
                            <span>Картинка</span>
                        </label>
                    </div>

                    <div class="modal-form__input-container">
                        <div id="task_text_input">
                            <textarea name="task_text" placeholder="Текст нового задания..."></textarea>
                        </div>

                        <div id="task_image_input" style="display: none;">
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

// Функция переключения полей
window.toggleTaskType = function(type) {
    const textInput = document.getElementById('task_text_input');
    const imageInput = document.getElementById('task_image_input');
    
    if (type === 'text') {
        textInput.style.display = 'block';
        imageInput.style.display = 'none';
    } else {
        textInput.style.display = 'none';
        imageInput.style.display = 'block';
    }
};

// Функция для закрытия модалки (глобальная)
window.closeLessonModal = function() {
    const modal = document.getElementById('lessonModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Возвращаем скролл
    }
};

// Закрытие по клику на фон
document.addEventListener('click', function(e) {
    const modal = document.getElementById('lessonModal');
    if (e.target === modal) {
        closeLessonModal();
    }
});

// Закрытие по кнопке Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLessonModal();
    }
});

// Функция открытия картинки во весь экран
window.openFullImage = function(src) {
    let overlay = document.getElementById('fullImageOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'fullImageOverlay';
        overlay.className = 'full-image-overlay';
        overlay.innerHTML = `<img src="" id="fullImageItem">`;
        overlay.onclick = function() { this.classList.remove('active'); };
        document.body.appendChild(overlay);
    }
    document.getElementById('fullImageItem').src = src;
    overlay.classList.add('active');
};