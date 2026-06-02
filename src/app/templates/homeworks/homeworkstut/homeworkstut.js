window.showHomeworkTasksModal = function(button) {
    const assignmentItem = button.closest('.assignment-item');
    const homeworkId = assignmentItem.querySelector('input[name="homework_id"]').value;
    const subject = assignmentItem.querySelector('.subject-badge').innerText;
    const title = assignmentItem.querySelector('.assignment-item__title').innerText;
    const deadline = assignmentItem.querySelector('.assignment-item__date')?.innerText || '';
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

window.closeHomeworkModal = function() {
    const modal = document.getElementById('homeworkModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
};

document.addEventListener('click', function(e) {
    const modal = document.getElementById('homeworkModal');
    if (e.target === modal) closeHomeworkModal();
});
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeHomeworkModal();
});


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
    const escHandler = function(e) {
        if (e.key === 'Escape') {
            closeFullscreenImage();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
};

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