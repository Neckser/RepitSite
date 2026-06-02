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


window.openFullImage = function(src) {
    let overlay = document.getElementById('fullImageOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'fullImageOverlay';
        overlay.className = 'full-image-overlay';
        overlay.innerHTML = '<img src="" id="fullImageItem">';
        document.body.appendChild(overlay);
        
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                closeFullscreenImage();
            }
        });
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeFullscreenImage();
            }
        });
    }
    document.getElementById('fullImageItem').src = src;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
};

window.closeFullscreenImage = function() {
    const overlay = document.getElementById('fullImageOverlay');
    if (overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            const img = document.getElementById('fullImageItem');
            if (img) img.src = '';
        }, 300);
    }
};


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
                        <div class="video-link">${videoLink}</div>
                        <button class="copy-link-btn" onclick="copyVideoLink('${lessonId}')">Перейти</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
};

window.closeVideoModal = function() {
    const modal = document.getElementById('videoModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
};

window.copyVideoLink = function(lessonId) {
    const videoLink = document.querySelector('.video-link')?.innerText;
    if (videoLink) {
        window.open(videoLink, '_blank');
    } else {
        alert('Ссылка на созвон не найдена');
    }
};

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

window.showDeskModal = function(button) {
    const lessonCard = button.closest('.lesson-card');
    const lessonId = lessonCard.querySelector('input[name="lesson_id"]').value;
    const subject = lessonCard.querySelector('input[name="subject"]').value;
    const tutor = lessonCard.querySelector('input[name="tutor_name"]').value;
    const time = lessonCard.querySelector('input[name="lesson_time"]').value;
    const deskLink = lessonCard.querySelector('input[name="desk_link"]').value;
    
    let modal = document.getElementById('deskModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'deskModal';
        modal.className = 'modal-overlay';
        document.body.appendChild(modal);
    }

    modal.innerHTML = `
        <div class="modal-container">
            <div class="modal-header" style="background: linear-gradient(135deg, #f1c40f, #f39c12);">
                <h2>Доска: ${subject}</h2>
                <button class="modal-close" onclick="closeDeskModal()">×</button>
            </div>
            <div class="modal-content">
                <div class="lesson-info-summary">
                    <div class="info-pill"><strong>Репетитор:</strong> ${tutor}</div>
                    <div class="info-pill"><strong>Время:</strong> ${time}</div>
                </div>
                
                <div class="active-link-section" style="background: #fff3cd; border-left-color: #f1c40f;">
                    <h4>Активная ссылка на доску:</h4>
                    <div class="video-link-display">
                        <div class="video-link">${deskLink}</div>
                        <button class="go-desklink-btn" 
                                onclick="openDeskLink('${deskLink}')">Перейти
                        </button>
                    </div>
                </div>
                <div class="desk-action-section">
                    <button class="btn-internal-desk" onclick="openDeskLink('/studboard/${lessonId}')">
                        <span class="btn-internal-desk__icon">📋</span>
                        <span class="btn-internal-desk__text">Перейти на внутреннюю доску</span>
                        <span class="btn-internal-desk__arrow">→</span>
                    </button>
                </div>
            </div>
        </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
};

window.openDeskLink = function(link) {
    if (link) {
        window.open(link, '_blank');
    } else {
        alert('Ссылка на доску не найдена');
    }
};

window.closeDeskModal = function() {
    const modal = document.getElementById('deskModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
};

document.addEventListener('click', function(e) {
    const modal = document.getElementById('deskModal');
    if (e.target === modal) {
        closeDeskModal();
    }
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeDeskModal();
    }
});