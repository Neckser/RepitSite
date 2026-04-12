document.addEventListener('DOMContentLoaded', function (): void {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const assignmentCards = document.querySelectorAll('.assignment-card');
    const statsItems = document.querySelectorAll('.stat-item strong');
    const sortSelect = document.getElementById('sortSelect') as HTMLSelectElement;

    if (!sortSelect) {
        console.error('Элемент sortSelect не найден');
        return;
    }

    // ========== СТАРАЯ ЛОГИКА (СТАТИСТИКА, ФИЛЬТРАЦИЯ, СОРТИРОВКА) ==========
    
    function updateStats(): void {
        const total = document.querySelectorAll('.assignment-card').length;
        const active = document.querySelectorAll('.assignment-card .status.active').length;
        const completed = document.querySelectorAll('.assignment-card .status.completed').length;

        if (statsItems[0]) statsItems[0].textContent = total.toString();
        if (statsItems[1]) statsItems[1].textContent = active.toString();
        if (statsItems[2]) statsItems[2].textContent = completed.toString();
    }

    function filterAssignments(filterType: string): void {
        assignmentCards.forEach(card => {
            const cardElement = card as HTMLElement;
            const statusElement = card.querySelector('.status');

            if (!statusElement) return;

            switch (filterType) {
                case 'все':
                    cardElement.style.display = 'block';
                    break;
                case 'активные':
                    cardElement.style.display = statusElement.classList.contains('active') ? 'block' : 'none';
                    break;
                case 'завершенные':
                    cardElement.style.display = statusElement.classList.contains('completed') ? 'block' : 'none';
                    break;
                default:
                    cardElement.style.display = 'block';
            }
        });
        updateStats();
    }

    function sortAssignments(sortType: string): void {
        const container = document.querySelector('.assignments-list');
        if (!container) return;

        const cards = Array.from(assignmentCards) as HTMLElement[];
        cards.sort((a, b) => {
            switch (sortType) {
                case 'deadline-asc':
                    return getDeadlineValue(a) - getDeadlineValue(b);
                case 'deadline-desc':
                    return getDeadlineValue(b) - getDeadlineValue(a);
                case 'created-desc':
                    return getCreatedValue(b) - getCreatedValue(a);
                case 'created-asc':
                    return getCreatedValue(a) - getCreatedValue(b);
                case 'subject':
                    return getSubjectValue(a).localeCompare(getSubjectValue(b));
                default:
                    return 0;
            }
        });

        cards.forEach(card => {
            container.appendChild(card);
        });
    }

    function getDeadlineValue(card: Element): number {
        const dueDateElement = card.querySelector('.due-date');
        if (!dueDateElement || !dueDateElement.textContent) return 0;

        const deadlineText = dueDateElement.textContent;
        const date = new Date(deadlineText.replace('До ', ''));
        return isNaN(date.getTime()) ? 0 : date.getTime();
    }

    function getCreatedValue(card: Element): number {
        return Array.from(assignmentCards).indexOf(card);
    }

    function getSubjectValue(card: Element): string {
        const subjectBadge = card.querySelector('.subject-badge');
        return subjectBadge && subjectBadge.textContent ? subjectBadge.textContent : '';
    }

    filterButtons.forEach(button => {
        button.addEventListener('click', function (this: HTMLButtonElement) {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const filterType = this.textContent?.toLowerCase() || 'все';
            filterAssignments(filterType);
        });
    });

    sortSelect.addEventListener('change', function (this: HTMLSelectElement) {
        sortAssignments(this.value);
    });

    // ========== РАСКРЫТИЕ ЗАДАЧ ==========
    
    function toggleTasks(button: HTMLButtonElement): void {
        const card = button.closest('.assignment-card') as HTMLElement | null;
        if (!card) return;
        
        const tasksContainer = card.querySelector('.tasks-container') as HTMLElement | null;
        const toggleText = button.querySelector('.toggle-text') as HTMLElement | null;
        
        if (!tasksContainer || !toggleText) return;
        
        if (tasksContainer.classList.contains('hidden')) {
            tasksContainer.classList.remove('hidden');
            button.classList.add('expanded');
            toggleText.textContent = 'Скрыть задания';
        } else {
            tasksContainer.classList.add('hidden');
            button.classList.remove('expanded');
            toggleText.textContent = 'Показать задания';
        }
    }

    // ========== ПОДСЧЁТ ПРОГРЕССА ДЛЯ ПОЛОСОЧКИ ==========
    
    function updateProgressBars(): void {
        const cards = document.querySelectorAll('.assignment-card');
        
        cards.forEach(card => {
            const cardElement = card as HTMLElement;
            const tasks = cardElement.querySelectorAll('.task-item');
            const completedTasks = cardElement.querySelectorAll('.task-status.completed');
            
            const total = tasks.length;
            const completed = completedTasks.length;
            const percentage = total > 0 ? (completed / total) * 100 : 0;
            
            // Обновляем полоску прогресса
            const progressFill = cardElement.querySelector('.progress-fill') as HTMLElement;
            if (progressFill) {
                progressFill.style.width = `${percentage}%`;
            }
            
            // Обновляем статус карточки
            const statusElement = cardElement.querySelector('.status') as HTMLElement;
            if (statusElement) {
                if (completed === total && total > 0) {
                    statusElement.className = 'status completed';
                    statusElement.textContent = 'Завершено';
                } else if (completed > 0) {
                    statusElement.className = 'status active';
                    statusElement.textContent = 'В процессе';
                } else {
                    statusElement.className = 'status active';
                    statusElement.textContent = 'Активно';
                }
            }
        });
        
        // Обновляем общую статистику
        updateStats();
    }

    // Навешиваем обработчики на кнопки раскрытия
    const toggleButtons = document.querySelectorAll('.toggle-tasks-btn');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function(this: HTMLButtonElement) {
            toggleTasks(this);
        });
    });

    // Инициализация прогресс-баров при загрузке
    updateProgressBars();
    
    // Обновляем статистику при загрузке
    updateStats();
});

// ========== ФУНКЦИИ ДЛЯ РАБОТЫ С ИЗОБРАЖЕНИЯМИ ==========

// Функция открытия картинки во весь экран
(window as any).openFullImage = function(src: string): void {
    let overlay = document.getElementById('fullImageOverlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'fullImageOverlay';
        overlay.className = 'full-image-overlay';
        overlay.innerHTML = `<img src="" id="fullImageItem" alt="Полноэкранное изображение">`;
        document.body.appendChild(overlay);
        
        overlay.addEventListener('click', function(e: MouseEvent) {
            if (e.target === overlay || (e.target as HTMLElement).classList.contains('full-image-overlay')) {
                (window as any).closeFullscreenImage();
            }
        });
    }
    
    const img = document.getElementById('fullImageItem') as HTMLImageElement;
    img.src = src;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    
    // Закрытие по Escape
    const escHandler = function(e: KeyboardEvent): void {
        if (e.key === 'Escape') {
            (window as any).closeFullscreenImage();
            document.removeEventListener('keydown', escHandler);
        }
    };
    document.addEventListener('keydown', escHandler);
};

// Функция закрытия полноэкранного режима
(window as any).closeFullscreenImage = function(): void {
    const overlay = document.getElementById('fullImageOverlay');
    if (overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            const img = document.getElementById('fullImageItem') as HTMLImageElement;
            if (img) img.src = '';
        }, 300);
    }
};