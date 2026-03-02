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

// Функция для открытия модального окна видеосозвона
window.showVideoModal = function(button) {
    const lessonCard = button.closest('.lesson-card');
    const lessonId = lessonCard.querySelector('input[name="lesson_id"]').value;
    const subject = lessonCard.querySelector('input[name="subject"]').value;
    const student = lessonCard.querySelector('input[name="student_name"]').value;
    const time = lessonCard.querySelector('input[name="lesson_time"]').value;
    const videoLink = lessonCard.querySelector('input[name="video_link"]').value;
    
    let modal = document.getElementById('videoModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'videoModal';
        modal.className = 'modal-overlay';
        document.body.appendChild(modal);
    }

    modal.innerHTML = `
        <div class="modal-container">
            <div class="modal-header" style="background: #4a90e2;">
                <h2>Видеосозвон: ${subject}</h2>
                <button class="modal-close" onclick="closeVideoModal()">×</button>
            </div>
            <div class="modal-content">
                <div class="lesson-info-summary">
                    <div class="info-pill"><strong>Ученик:</strong> ${student}</div>
                    <div class="info-pill"><strong>Время:</strong> ${time}</div>
                </div>

                <form action="/savevideolink/${lessonId}" method="POST" class="video-form">
                    <div class="video-form__group">
                        <label for="video_link">Ссылка на видеосозвон:</label>
                        <input 
                            type="url" 
                            id="video_link" 
                            name="video_link" 
                            class="video-form__input"
                            placeholder="Ваша ссылка..."
                            value="${videoLink}"
                            required
                        >
                    </div>

                    <button type="submit" class="btn-save-video">Сохранить ссылку</button>
                </form>

                <!-- Информационный блок -->
                <!-- <div class="video-info-box"> --> 
                <!--     <h4>Как это работает?</h4> -->
                <!--     <ul> -->
                <!--         <li>Ссылка будет доступна ученику в его расписании</li> -->
                 <!--        <li>Появится за 15 минут до начала урока</li> -->
                <!--         <li>Можно изменить в любой момент</li> -->
                <!--     </ul> -->
                <!--  </div> -->
            </div>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
};

// Функция закрытия
window.closeVideoModal = function() {
    const modal = document.getElementById('videoModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
};

// Закрытие по клику на фон
document.addEventListener('click', function(e) {
    const modal = document.getElementById('videoModal');
    if (e.target === modal) {
        closeVideoModal();
    }
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeVideoModal();
    }
});