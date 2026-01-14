document.addEventListener('DOMContentLoaded', function () {

    let mcqIndex = 0;
    let multiIndex = 0;

    window.addQuestion = function () {
        const container = document.getElementById('questions-list');
        if (!container) return;

        const div = document.createElement('div');
        div.className = 'question-card';
        div.innerHTML = `
            <input type="text" name="question[]" placeholder="Вопрос" required>
            <input type="text" name="answer[]" placeholder="Правильный ответ" required>
            <button type="button" class="remove-btn" onclick="this.parentElement.remove()">Удалить</button>
        `;
        container.appendChild(div);
    };

    window.addMultipleChoiceQuestion = function () {
        const container = document.getElementById('questions-list');
        if (!container) return;

        mcqIndex++;

        const div = document.createElement('div');
        div.className = 'question-card';

        div.innerHTML = `
            <input 
                type="text" 
                name="mcq_question[]" 
                placeholder="Вопрос (выбор одного ответа)" 
                required
            >

            <div style="display:flex; flex-direction:column; gap:8px; flex:1;">
                ${[1, 2, 3, 4].map(i => `
                    <label style="display:flex; align-items:center; gap:8px;">
                        <input 
                            type="radio" 
                            name="mcq_correct_${mcqIndex}" 
                            value="${i}" 
                            required
                        >
                        <input 
                            type="text" 
                            name="mcq_option_${mcqIndex}[]" 
                            placeholder="Вариант ${i}" 
                            required
                        >
                    </label>
                `).join('')}
            </div>

            <button 
                type="button" 
                class="remove-btn" 
                onclick="this.parentElement.remove()"
            >
                Удалить
            </button>
        `;

        container.appendChild(div);
    };

    window.addMultiAnswerQuestion = function () {
        const container = document.getElementById('questions-list');
        if (!container) return;

        multiIndex++;

        const div = document.createElement('div');
        div.className = 'question-card';

        div.innerHTML = `
            <input 
                type="text" 
                name="multi_question[]" 
                placeholder="Вопрос (несколько правильных ответов)" 
                required
            >

            <div style="display:flex; flex-direction:column; gap:8px; flex:1;">
                ${[1, 2, 3, 4].map(i => `
                    <label style="display:flex; align-items:center; gap:8px;">
                        <input 
                            type="checkbox" 
                            name="multi_correct_${multiIndex}[]" 
                            value="${i}"
                        >
                        <input 
                            type="text" 
                            name="multi_option_${multiIndex}[]" 
                            placeholder="Вариант ${i}" 
                            required
                        >
                    </label>
                `).join('')}
            </div>

            <button 
                type="button" 
                class="remove-btn" 
                onclick="this.parentElement.remove()"
            >
                Удалить
            </button>
        `;

        container.appendChild(div);
    };

    });
