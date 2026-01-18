
    document.addEventListener('DOMContentLoaded', function() {
        // Получаем данные из шаблона
        const { percent, score, total } = window.TEST_RESULT;
            
        const correctPercentage = percent;
        const correctAnswers = score;
        const totalQuestions = total;
        
        // Элементы для анимации
        const progressCircle = document.getElementById('progressCircle');
        const scorePercent = document.getElementById('scorePercent');
        const correctAnswersElement = document.getElementById('correctAnswers');
        
        // Длина окружности: 2 * π * r (r = 120)
        const circumference = 2 * Math.PI * 120;
        
        // Устанавливаем начальное состояние
        progressCircle.style.strokeDasharray = `0 ${circumference}`;
        
        // Функция для плавной анимации числа
        function animateNumber(element, start, end, duration, suffix = '') {
            const startTime = performance.now();
            const difference = end - start;
            
            function updateNumber(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                // Используем easeOutQuad для плавного замедления
                const easeProgress = 1 - (1 - progress) * (1 - progress);
                const currentValue = Math.floor(start + (difference * easeProgress));
                
                element.textContent = currentValue + suffix;
                
                if (progress < 1) {
                    requestAnimationFrame(updateNumber);
                } else {
                    element.textContent = end + suffix;
                }
            }
            
            requestAnimationFrame(updateNumber);
        }
        
        // Функция для анимации круга
        function animateCircle() {
            // Рассчитываем длину заполненной части
            const targetLength = (correctPercentage / 100) * circumference;
            
            // Анимация круга с помощью Web Animations API для лучшей производительности
            const circleAnimation = progressCircle.animate([
                { strokeDasharray: `0 ${circumference}` },
                { strokeDasharray: `${targetLength} ${circumference}` }
            ], {
                duration: 2000,
                easing: 'cubic-bezier(0.68, -0.55, 0.27, 1.55)',
                fill: 'forwards'
            });
            
            // Анимация процента одновременно с кругом
            circleAnimation.onfinish = () => {
                scorePercent.textContent = correctPercentage + '%';
            };
            
            // Запускаем анимацию числа процента
            setTimeout(() => {
                animateNumber(scorePercent, 0, correctPercentage, 1800, '%');
            }, 200);
            
            // Анимация счетчика правильных ответов
            setTimeout(() => {
                animateNumber(correctAnswersElement, 0, correctAnswers, 1500, '/' + totalQuestions);
            }, 500);
            
            // Добавляем дополнительные эффекты
            setTimeout(() => {
                // Пульсация при завершении
                scorePercent.style.transition = 'transform 0.3s';
                scorePercent.style.transform = 'scale(1.1)';
                
                setTimeout(() => {
                    scorePercent.style.transform = 'scale(1)';
                }, 300);
            }, 2000);
        }
        
        // Запускаем анимацию с небольшой задержкой
        setTimeout(animateCircle, 500);
        
        // Добавляем интерактивность кнопке
        const nextButton = document.querySelector('.btn-next');
        if (nextButton) {
            nextButton.addEventListener('mouseenter', () => {
                nextButton.style.transform = 'translateY(-3px) scale(1.05)';
            });
            
            nextButton.addEventListener('mouseleave', () => {
                nextButton.style.transform = 'translateY(0) scale(1)';
            });
            
            // Анимация появления кнопки
            setTimeout(() => {
                nextButton.style.opacity = '0';
                nextButton.style.transform = 'translateY(20px)';
                nextButton.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
                
                setTimeout(() => {
                    nextButton.style.opacity = '1';
                    nextButton.style.transform = 'translateY(0)';
                }, 50);
            }, 100);
        }
        
        // Анимация появления статистических карточек
        const statItems = document.querySelectorAll('.stat-item');
        statItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                item.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-out';
                item.style.opacity = '1';
                item.style.transform = 'translateY(0)';
            }, 1000 + (index * 100));
        });
    });