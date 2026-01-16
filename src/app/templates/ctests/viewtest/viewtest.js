
    document.addEventListener('DOMContentLoaded', function() {
        const testTimeMinutes = parseInt(document.body.dataset.testTimeMinutes);
        const TOTAL_TEST_TIME = testTimeMinutes * 60;
        let timeLeft = TOTAL_TEST_TIME;
        let timerInterval = null;
        const timerElement = document.getElementById('test-timer');
        const timeoutModal = document.getElementById('timeout-modal');
        const redirectCountdown = document.getElementById('redirect-countdown');
        const redirectNowBtn = document.getElementById('redirect-now-btn');

        // ========== ФУНКЦИИ ТАЙМЕРА ==========
        function startTimer() {
            updateTimerDisplay();
            
            timerInterval = setInterval(() => {
                timeLeft--;
                updateTimerDisplay();
                
                // Меняем стили при малом времени
                if (timeLeft <= 60) { // меньше минуты
                    timerElement.classList.add('danger');
                    timerElement.classList.remove('warning');
                } else if (timeLeft <= 300) { // меньше 5 минут
                    timerElement.classList.add('warning');
                }
                
                // Время вышло
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    showTimeoutModal();
                }
            }, 1000);
        }

        function updateTimerDisplay() {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerElement.textContent = `⏱ Осталось: ${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }

        function showTimeoutModal() {
            // Блокируем взаимодействие с тестом
            document.querySelectorAll('.btn, .answer-option, .text-answer').forEach(el => {
                el.style.pointerEvents = 'none';
                el.style.opacity = '0.5';
            });
            
            // Показываем модальное окно
            timeoutModal.classList.add('active');
            
            // Обратный отсчет для перенаправления
            let countdown = 5;
            const countdownInterval = setInterval(() => {
                redirectCountdown.textContent = `Перенаправление через: ${countdown} секунд`;
                countdown--;
                
                if (countdown < 0) {
                    clearInterval(countdownInterval);
                    redirectToHome();
                }
            }, 1000);
        }

        function redirectToHome() {
            // Здесь можно добавить отправку результатов на сервер
            // localStorage.setItem('testResults', JSON.stringify(getAllAnswers()));
            
            // Перенаправляем на главную
            window.location.href = '/home';
        }

        // ========== ОСНОВНАЯ ЛОГИКА ТЕСТА ==========
        const questionCards = document.querySelectorAll('.question-card');
        const totalQuestions = questionCards.length;
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
                if (i === currentQuestionIndex) dot.classList.add('active');
                
                dot.addEventListener('click', () => {
                    goToQuestion(i);
                });
                
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
            nextBtn.disabled = currentQuestionIndex === totalQuestions - 1;
            
            if (currentQuestionIndex === totalQuestions - 1) {
                nextBtn.style.display = 'none';
                finishBtn.style.display = 'block';
            } else {
                nextBtn.style.display = 'block';
                finishBtn.style.display = 'none';
            }
        }
        
        function initTextCounters() {
            document.querySelectorAll('.text-answer').forEach(textarea => {
                const counter = textarea.closest('.text-answer-container').querySelector('.char-count');
                counter.textContent = textarea.value.length;
                
                textarea.addEventListener('input', function() {
                    counter.textContent = this.value.length;
                });
            });
        }
        
        function markAnsweredQuestions() {
            questionCards.forEach((card, index) => {
                const type = card.dataset.type;
                let isAnswered = false;

                if (type === 'single') {
                    const checked = card.querySelector('input[type="radio"]:checked');
                    isAnswered = !!checked;
                } else if (type === 'multiple') {
                    const checked = card.querySelectorAll('input[type="checkbox"]:checked');
                    isAnswered = checked.length > 0;
                } else if (type === 'text') {
                    const textarea = card.querySelector('.text-answer');
                    isAnswered = textarea.value.trim().length > 0;
                }

                const dot = document.querySelectorAll('.question-dot')[index];
            });
        }

        // ========== СОБИРАЕМ ВСЕ ОТВЕТЫ (для отправки на сервер) ==========
        function getAllAnswers() {
            const answers = {};
            
            questionCards.forEach((card, index) => {
                const type = card.dataset.type;
                const questionNumber = index + 1;
                
                if (type === 'single') {
                    const checked = card.querySelector('input[type="radio"]:checked');
                    answers[`question_${questionNumber}`] = checked ? checked.value : null;
                } else if (type === 'multiple') {
                    const checked = card.querySelectorAll('input[type="checkbox"]:checked');
                    answers[`question_${questionNumber}`] = Array.from(checked).map(cb => cb.value);
                } else if (type === 'text') {
                    const textarea = card.querySelector('.text-answer');
                    answers[`question_${questionNumber}`] = textarea.value.trim();
                }
            });
            
            return answers;
        }

        // ========== ОБРАБОТЧИКИ СОБЫТИЙ ==========
        prevBtn.addEventListener('click', () => {
            goToQuestion(currentQuestionIndex - 1);
        });
        
        nextBtn.addEventListener('click', () => {
            goToQuestion(currentQuestionIndex + 1);
        });
        
        finishBtn.addEventListener('click', () => {
            if (confirm('Вы уверены, что хотите завершить тест?')) {
                // Останавливаем таймер
                clearInterval(timerInterval);
                
                // Отправляем ответы на сервер (в реальном приложении)
                // fetch('/api/submit-test', { method: 'POST', body: JSON.stringify(getAllAnswers()) });
                
                alert('Тест завершен! Ответы отправлены.');
                setTimeout(() => {
                    window.location.href = '/home';
                }, 2000);
            }
        });

        // Кнопка для немедленного перенаправления
        redirectNowBtn.addEventListener('click', redirectToHome);
        
        // Отслеживание изменения ответов
        document.querySelectorAll('input, .text-answer').forEach(element => {
            element.addEventListener('change', markAnsweredQuestions);
            element.addEventListener('input', markAnsweredQuestions);
        });
        
        // ========== ИНИЦИАЛИЗАЦИЯ ==========
        initQuestionDots();
        questionCards[0].classList.add('active');
        initTextCounters();
        updateProgress();
        updateButtons();
        markAnsweredQuestions();
        startTimer(); // Запускаем таймер
        
        // Навигация с клавиатуры
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft' && currentQuestionIndex > 0) {
                goToQuestion(currentQuestionIndex - 1);
            } else if (e.key === 'ArrowRight' && currentQuestionIndex < totalQuestions - 1) {
                goToQuestion(currentQuestionIndex + 1);
            }
        });
    });