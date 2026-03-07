window.showLessonModal = function(button) {
    const lessonCard = button.closest('.lesson-card');
    const lessonId = lessonCard.querySelector('input[name="lesson_id"]').value;
    const subject = lessonCard.querySelector('.subject-badge').innerText;
    const tutor = lessonCard.querySelector('.schedule__lesson-student span').innerText;
    
    const time = lessonCard.querySelector('.schedule__lesson-time').innerText;
    const tasksHtml = lessonCard.querySelector(".hidden-tasks-content").innerHTML;

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
                    <div class="info-pill"><strong>Репетитор:</strong> ${tutor}</div>
                    <div class="info-pill"><strong>Время:</strong> ${time}</div>
                </div>

                <h3>Задания к уроку</h3>
                <div class="tasks-scroll-container">
                    ${tasksHtml}
                </div>
            </div>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
};

window.closeLessonModal = function() {
    const modal = document.getElementById('lessonModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
};

document.addEventListener('click', function(e) {
    const modal = document.getElementById('lessonModal');
    if (e.target === modal) {
        closeLessonModal();
    }
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeLessonModal();
    }
});

window.openFullImage = function(src) {
    let overlay = document.getElementById('fullImageOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'fullImageOverlay';
        overlay.className = 'full-image-overlay';
        overlay.innerHTML = '<img src="" id="fullImageItem">';
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
    const tutor = lessonCard.querySelector('input[name="tutor_name"]').value;
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
                    <div class="info-pill"><strong>Ученик:</strong> ${tutor}</div>
                    <div class="info-pill"><strong>Время:</strong> ${time}</div>
                </div>
                <div class="active-link-section">
                    <h4>Активная ссылка на созвон:</h4>
                    <div class="video-link-display">
                        <a href="${videoLink}" target="_blank" class="video-link">
                            ${videoLink}
                        </a>
                        <button class="copy-link-btn" onclick="copyVideoLink('${lessonId}')">Перейти</button>
                    </div>
                </div>
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

// Функция копирования ссылки
window.copyVideoLink = function(lessonId) {
    const videoLink = document.querySelector('.video-link')?.innerText;
    if (videoLink) {
        window.open(videoLink, '_blank');
    } else {
        alert('Ссылка на созвон не найдена');
    }
};

// Закрытие по клику на фон
document.addEventListener('click', function(e) {
    const modal = document.getElementById('videoModal');
    if (e.target === modal) {
        closeVideoModal();
    }
});

// Закрытие по Escape
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeVideoModal();
    }
});
