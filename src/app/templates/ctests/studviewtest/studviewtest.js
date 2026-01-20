document.addEventListener('DOMContentLoaded', function () {
    const testTimeMinutes = parseFloat(document.body.dataset.testTimeMinutes) || 0;
    const TOTAL_TEST_TIME = Math.max(testTimeMinutes * 60, 1);
    let timeLeft = TOTAL_TEST_TIME;
    let timerInterval = null;

    const timerElement = document.getElementById('test-timer');
    const timeoutModal = document.getElementById('timeout-modal');
    const redirectCountdown = document.getElementById('redirect-countdown');
    const redirectNowBtn = document.getElementById('redirect-now-btn');

    function updateTimerDisplay() {
        if (!timerElement) return;
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `⏱ Осталось: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    function startTimer() {
        updateTimerDisplay();

        timerInterval = setInterval(() => {
            timeLeft--;

            updateTimerDisplay();

            if (timerElement) {
                if (timeLeft <= 60) {
                    timerElement.classList.add('danger');
                    timerElement.classList.remove('warning');
                } else if (timeLeft <= 300) {
                    timerElement.classList.add('warning');
                }
            }

            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                showTimeoutModal();
            }
        }, 1000);
    }

    function showTimeoutModal() {
        if (!timeoutModal) return;

        document.querySelectorAll('.btn, .answer-option, .text-answer').forEach(el => {
            el.style.pointerEvents = 'none';
            el.style.opacity = '0.5';
        });

        timeoutModal.classList.add('active');

        let countdown = 5;
        redirectCountdown.textContent = `Перенаправление через: ${countdown} секунд`;

        const interval = setInterval(() => {
            countdown--;
            redirectCountdown.textContent = `Перенаправление через: ${countdown} секунд`;

            if (countdown <= 0) {
                clearInterval(interval);
                redirectToHome();
            }
        }, 1000);
    }

    function redirectToHome() {
        const spent = TOTAL_TEST_TIME - timeLeft;
        document.getElementById('time-spent-input').value = spent;
        document.getElementById('test-form').submit();
    }

    const questionCards = document.querySelectorAll('.question-card');
    const totalQuestions = questionCards.length;

    if (totalQuestions === 0) {
        console.error('❌ Вопросы не найдены');
        return;
    }

    let currentQuestionIndex = 0;

    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const finishBtn = document.getElementById('finish-btn');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const questionDotsContainer = document.getElementById('question-dots');

    function initQuestionDots() {
        questionDotsContainer.innerHTML = '';
        for (let i = 0; i < totalQuestions; i++) {
            const dot = document.createElement('div');
            dot.className = 'question-dot';
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToQuestion(i));
            questionDotsContainer.appendChild(dot);
        }
    }

    function goToQuestion(index) {
        if (index < 0 || index >= totalQuestions) return;

        questionCards[currentQuestionIndex].classList.remove('active');
        document.querySelectorAll('.question-dot')[currentQuestionIndex].classList.remove('active');

        currentQuestionIndex = index;

        questionCards[currentQuestionIndex].classList.add('active');
        document.querySelectorAll('.question-dot')[currentQuestionIndex].classList.add('active');

        updateProgress();
        updateButtons();
    }

    function updateProgress() {
        const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100;
        progressFill.style.width = `${progress}%`;
        progressText.textContent = `Вопрос ${currentQuestionIndex + 1} из ${totalQuestions}`;
    }

    function updateButtons() {
        prevBtn.disabled = currentQuestionIndex === 0;

        if (currentQuestionIndex === totalQuestions - 1) {
            nextBtn.style.display = 'none';
            finishBtn.style.display = 'block';
        } else {
            nextBtn.style.display = 'block';
            finishBtn.style.display = 'none';
        }
    }

    function markAnsweredQuestions() {
        questionCards.forEach((card, index) => {
            let answered = false;

            if (card.dataset.type === 'text') {
                answered = card.querySelector('.text-answer')?.value.trim().length > 0;
            } else {
                answered = card.querySelector('input:checked') !== null;
            }

            const dot = document.querySelectorAll('.question-dot')[index];
            dot.classList.toggle('answered', answered);
        });
    }

    function initTextCounters() {
        document.querySelectorAll('.text-answer').forEach(textarea => {
            const counter = textarea.closest('.text-answer-container')?.querySelector('.char-count');
            if (!counter) return;

            counter.textContent = textarea.value.length;
            textarea.addEventListener('input', () => {
                counter.textContent = textarea.value.length;
            });
        });
    }

    prevBtn.addEventListener('click', () => goToQuestion(currentQuestionIndex - 1));
    nextBtn.addEventListener('click', () => goToQuestion(currentQuestionIndex + 1));


    redirectNowBtn?.addEventListener('click', redirectToHome);

    document.querySelectorAll('input, textarea').forEach(el => {
        el.addEventListener('change', markAnsweredQuestions);
        el.addEventListener('input', markAnsweredQuestions);
    });

    const form = document.getElementById('test-form');

    form.addEventListener('submit', () => {
        const spent = TOTAL_TEST_TIME - timeLeft;
        document.getElementById('time-spent-input').value = spent;
    });
    
    questionCards[0].classList.add('active');
    initQuestionDots();
    initTextCounters();
    updateProgress();
    updateButtons();
    markAnsweredQuestions();
    startTimer();

});
