document.addEventListener('DOMContentLoaded', function() {
    const { percent, score, total } = window.TEST_RESULT;
    const correctPercentage = percent;
    const correctAnswers = score;
    const totalQuestions = total;
    
    const progressCircle = document.getElementById('progressCircle');
    const scorePercent = document.getElementById('scorePercent');
    const correctAnswersElement = document.getElementById('correctAnswers');
    
    const circumference = 2 * Math.PI * 120;
    
    progressCircle.style.strokeDasharray = `0 ${circumference}`;
    function animateNumber(element, start, end, duration, suffix = '') {
        const startTime = performance.now();
        const difference = end - start;
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
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
    
    function animateCircle() {
        const targetLength = (correctPercentage / 100) * circumference;
        const circleAnimation = progressCircle.animate([
            { strokeDasharray: `0 ${circumference}` },
            { strokeDasharray: `${targetLength} ${circumference}` }
        ], {
            duration: 2000,
            easing: 'cubic-bezier(0.68, -0.55, 0.27, 1.55)',
            fill: 'forwards'
        });
        
        circleAnimation.onfinish = () => {
            scorePercent.textContent = correctPercentage + '%';
        };
        
        setTimeout(() => {
            animateNumber(scorePercent, 0, correctPercentage, 1800, '%');
        }, 200);
        
        setTimeout(() => {
            animateNumber(correctAnswersElement, 0, correctAnswers, 1500, '/' + totalQuestions);
        }, 500);
        
        setTimeout(() => {
            scorePercent.style.transition = 'transform 0.3s';
            scorePercent.style.transform = 'scale(1.1)';
            
            setTimeout(() => {
                scorePercent.style.transform = 'scale(1)';
            }, 300);
        }, 2000);
    }
    
    setTimeout(animateCircle, 500);
    
    const nextButton = document.querySelector('.btn-next');
    if (nextButton) {
        nextButton.addEventListener('mouseenter', () => {
            nextButton.style.transform = 'translateY(-3px) scale(1.05)';
        });
        
        nextButton.addEventListener('mouseleave', () => {
            nextButton.style.transform = 'translateY(0) scale(1)';
        });
        
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
})