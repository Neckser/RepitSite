window.showLessonModal = function(button) {
    const lessonCard = button.closest('.lesson-card');
    const lessonId = lessonCard.querySelector('input[name="lesson_id"]').value;
    const subject = lessonCard.querySelector('.subject-badge').innerText;
    
    // Ищем репетитора в .schedule__lesson-student span (как в вашем HTML)
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