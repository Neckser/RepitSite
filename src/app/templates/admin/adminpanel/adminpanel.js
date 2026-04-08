
        // ========== API ENDPOINTS (настройте под свой бекенд) ==========
        const API_BASE = '';
        const API = {
            stats: `${API_BASE}/api/v1/admin/stats`,
            graph: `${API_BASE}/api/v1/admin/graph`,
            users: `${API_BASE}/api/v1/admin/users`,
            homeworks: `${API_BASE}/api/v1/admin/homeworks`,
            grades: `${API_BASE}/api/v1/admin/grades`,
            lessons: `${API_BASE}/api/v1/admin/lessons`,
            tutors: `${API_BASE}/api/v1/admin/tutors`,
            students: `${API_BASE}/api/v1/admin/students`,
            createTutor: `${API_BASE}/api/v1.admin/tutor/create`,
            createStudent: `${API_BASE}/api/v1/admin/student/create`,
            createHomework: `${API_BASE}/api/v1/admin/homework/create`,
            createGrade: `${API_BASE}/api/v1/admin/grade/create`,
            createLesson: `${API_BASE}/api/v1/admin/lesson/create`,
            deleteUser: `${API_BASE}/api/v1/admin/user/delete`,
            deleteHomework: `${API_BASE}/api/v1/admin/homework/delete`,
            deleteGrade: `${API_BASE}/api/v1/admin/grade/delete`,
            deleteLesson: `${API_BASE}/api/v1/admin/lesson/delete`
        };

        // ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
        async function fetchJSON(url, options = {}) {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        }

        function escapeHtml(str) {
            if (!str) return '';
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            });
        }

        function showNotification(message, isError = false) {
            // Простое уведомление, можно заменить на красивый тост
            alert(message);
        }

        // ========== ЗАГРУЗКА ДАННЫХ ==========
        async function loadStats() {
            try {
                const stats = await fetchJSON(API.stats);
                document.getElementById('totalStudents').textContent = stats.total_students || 0;
                document.getElementById('totalTutors').textContent = stats.total_tutors || 0;
                document.getElementById('totalHomeworks').textContent = stats.total_homeworks || 0;
                document.getElementById('totalGrades').textContent = stats.total_grades || 0;
                document.getElementById('totalLessons').textContent = stats.total_lessons || 0;
            } catch (e) {
                console.error('Ошибка загрузки статистики:', e);
            }
        }

        async function loadUsers() {
            try {
                const users = await fetchJSON(API.users);
                document.getElementById('usersTableBody').innerHTML = users.map(u => `
                    <tr>
                        <td>${escapeHtml(u.id)}</td>
                        <td>${escapeHtml(u.name)}</td>
                        <td>${escapeHtml(u.role)}</td>
                        <td><span class="badge badge-active">${escapeHtml(u.status)}</span></td>
                        <td class="action-buttons">
                            <button class="btn btn_small btn_danger" onclick="deleteItem('user', '${u.id}')">Удалить</button>
                        </td>
                    </tr>
                `).join('');
            } catch (e) {
                console.error('Ошибка загрузки пользователей:', e);
                document.getElementById('usersTableBody').innerHTML = '<tr><td colspan="5">Ошибка загрузки</td></tr>';
            }
        }

        async function loadHomeworks() {
            try {
                const homeworks = await fetchJSON(API.homeworks);
                document.getElementById('homeworksTableBody').innerHTML = homeworks.map(h => `
                    <tr>
                        <td>${h.id}</td>
                        <td>${escapeHtml(h.student_name)}</td>
                        <td>${escapeHtml(h.tutor_name)}</td>
                        <td>${escapeHtml(h.subject)}</td>
                        <td>${escapeHtml(h.title)}</td>
                        <td><span class="badge ${h.status === 'Активно' ? 'badge-active' : 'badge-warning'}">${escapeHtml(h.status)}</span></td>
                        <td>${h.deadline || '—'}</td>
                        <td class="action-buttons">
                            <button class="btn btn_small btn_danger" onclick="deleteItem('homework', ${h.id})">Удалить</button>
                        </td>
                    </tr>
                `).join('');
            } catch (e) {
                console.error('Ошибка загрузки домашек:', e);
                document.getElementById('homeworksTableBody').innerHTML = '<tr><td colspan="8">Ошибка загрузки</td></tr>';
            }
        }

        async function loadGrades() {
            try {
                const grades = await fetchJSON(API.grades);
                document.getElementById('gradesTableBody').innerHTML = grades.map(g => `
                    <tr>
                        <td>${g.id}</td>
                        <td>${escapeHtml(g.student_name)}</td>
                        <td>${escapeHtml(g.tutor_name)}</td>
                        <td>${escapeHtml(g.subject)}</td>
                        <td><strong style="color:#6b8e23">${g.grade}</strong></td>
                        <td>${escapeHtml(g.reason)}</td>
                        <td>${g.date || '—'}</td>
                        <td class="action-buttons">
                            <button class="btn btn_small btn_danger" onclick="deleteItem('grade', ${g.id})">Удалить</button>
                        </td>
                    </tr>
                `).join('');
            } catch (e) {
                console.error('Ошибка загрузки оценок:', e);
                document.getElementById('gradesTableBody').innerHTML = '<tr><td colspan="8">Ошибка загрузки</td></tr>';
            }
        }

        async function loadLessons() {
            try {
                const lessons = await fetchJSON(API.lessons);
                document.getElementById('lessonsTableBody').innerHTML = lessons.map(l => `
                    <tr>
                        <td>${l.id}</td>
                        <td>${escapeHtml(l.student_name)}</td>
                        <td>${escapeHtml(l.tutor_name)}</td>
                        <td>${escapeHtml(l.subject)}</td>
                        <td>${l.date || '—'}</td>
                        <td>${l.time || '—'}</td>
                        <td><span class="badge badge-active">${escapeHtml(l.status)}</span></td>
                        <td class="action-buttons">
                            <button class="btn btn_small btn_danger" onclick="deleteItem('lesson', ${l.id})">Удалить</button>
                        </td>
                    </tr>
                `).join('');
            } catch (e) {
                console.error('Ошибка загрузки уроков:', e);
                document.getElementById('lessonsTableBody').innerHTML = '<tr><td colspan="8">Ошибка загрузки</td></tr>';
            }
        }

        async function loadTutorsForSelect() {
            try {
                const tutors = await fetchJSON(API.tutors);
                const select = document.getElementById('studentTutorSelect');
                if (select) {
                    select.innerHTML = '<option value="">Без репетитора</option>' + 
                        tutors.map(t => `<option value="${t.id}">${escapeHtml(t.name)} (${t.subjects?.join(', ') || ''})</option>`).join('');
                }
                return tutors;
            } catch (e) {
                console.error('Ошибка загрузки репетиторов:', e);
                return [];
            }
        }

        async function loadStudentsForSelect() {
            try {
                const students = await fetchJSON(API.students);
                return students;
            } catch (e) {
                console.error('Ошибка загрузки учеников:', e);
                return [];
            }
        }

        // ========== УДАЛЕНИЕ ==========
        async function deleteItem(type, id) {
            if (!confirm(`Удалить ${type} #${id}?`)) return;
            
            let url = '';
            if (type === 'user') url = `${API.deleteUser}/${id}`;
            else if (type === 'homework') url = `${API.deleteHomework}/${id}`;
            else if (type === 'grade') url = `${API.deleteGrade}/${id}`;
            else if (type === 'lesson') url = `${API.deleteLesson}/${id}`;
            
            try {
                const response = await fetch(url, { method: 'DELETE' });
                if (response.ok) {
                    await loadAllData();
                    showNotification('Удалено успешно');
                } else {
                    showNotification('Ошибка удаления', true);
                }
            } catch (e) {
                showNotification('Ошибка соединения', true);
            }
        }

        // ========== СОЗДАНИЕ (ФОРМЫ) ==========
        async function submitCreate(event, type) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            // Преобразуем subjects из select multiple в массив
            if (data.subjects && typeof data.subjects === 'string') {
                const subjectsSelect = form.querySelector('select[name="subjects"]');
                if (subjectsSelect) {
                    data.subjects = Array.from(subjectsSelect.selectedOptions).map(opt => opt.value);
                } else {
                    data.subjects = [data.subjects];
                }
            }
            
            let url = '';
            if (type === 'tutor') url = API.createTutor;
            else if (type === 'student') url = API.createStudent;
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    await loadAllData();
                    form.reset();
                    showNotification('Создано успешно');
                } else {
                    const error = await response.text();
                    showNotification(`Ошибка: ${error}`, true);
                }
            } catch (e) {
                showNotification('Ошибка соединения', true);
            }
        }

        // ========== МОДАЛЬНОЕ ОКНО ДЛЯ СОЗДАНИЯ ==========
        let currentCreateType = null;

        async function openCreateModal(type) {
            currentCreateType = type;
            const modal = document.getElementById('createModal');
            const title = document.getElementById('modalTitle');
            const fieldsDiv = document.getElementById('modalFormFields');
            
            const students = await loadStudentsForSelect();
            const tutors = await loadTutorsForSelect();
            
            if (type === 'homework') {
                title.innerText = '📚 Создать домашнее задание';
                fieldsDiv.innerHTML = `
                    <div class="form-group"><label class="form-label">Ученик</label><select name="student_id" class="form-select" required>${students.map(s => `<option value="${s.id}">${escapeHtml(s.name)} (${s.grade} кл)</option>`).join('')}</select></div>
                    <div class="form-group"><label class="form-label">Репетитор</label><select name="tutor_id" class="form-select" required>${tutors.map(t => `<option value="${t.id}">${escapeHtml(t.name)} (${t.subjects?.join(', ') || ''})</option>`).join('')}</select></div>
                    <div class="form-group"><label class="form-label">Предмет</label><select name="subject" class="form-select" required><option>Математика</option><option>Физика</option><option>Английский</option><option>Русский</option><option>Информатика</option><option>Химия</option><option>Биология</option></select></div>
                    <div class="form-group"><label class="form-label">Тема</label><input type="text" name="title" class="form-input" required></div>
                    <div class="form-group"><label class="form-label">Описание</label><textarea name="description" class="form-textarea"></textarea></div>
                    <div class="form-group"><label class="form-label">Дедлайн</label><input type="date" name="deadline" class="form-input" required></div>
                `;
            } else if (type === 'grade') {
                title.innerText = '⭐ Выставить оценку';
                fieldsDiv.innerHTML = `
                    <div class="form-group"><label class="form-label">Ученик</label><select name="student_id" class="form-select" required>${students.map(s => `<option value="${s.id}">${escapeHtml(s.name)} (${s.grade} кл)</option>`).join('')}</select></div>
                    <div class="form-group"><label class="form-label">Репетитор</label><select name="tutor_id" class="form-select" required>${tutors.map(t => `<option value="${t.id}">${escapeHtml(t.name)} (${t.subjects?.join(', ') || ''})</option>`).join('')}</select></div>
                    <div class="form-group"><label class="form-label">Предмет</label><select name="subject" class="form-select" required><option>Математика</option><option>Физика</option><option>Английский</option><option>Русский</option></select></div>
                    <div class="form-group"><label class="form-label">Оценка</label><select name="grade" class="form-select" required><option>5</option><option>4</option><option>3</option><option>2</option></select></div>
                    <div class="form-group"><label class="form-label">За что</label><select name="reason" class="form-select" required><option>Домашнее задание</option><option>Контрольная работа</option><option>Работа на уроке</option><option>Проект</option><option>Эссе</option></select></div>
                    <div class="form-group"><label class="form-label">Комментарий</label><textarea name="comment" class="form-textarea"></textarea></div>
                `;
            } else if (type === 'lesson') {
                title.innerText = '📅 Создать урок';
                fieldsDiv.innerHTML = `
                    <div class="form-group"><label class="form-label">Ученик</label><select name="student_id" class="form-select" required>${students.map(s => `<option value="${s.id}">${escapeHtml(s.name)} (${s.grade} кл)</option>`).join('')}</select></div>
                    <div class="form-group"><label class="form-label">Репетитор</label><select name="tutor_id" class="form-select" required>${tutors.map(t => `<option value="${t.id}">${escapeHtml(t.name)} (${t.subjects?.join(', ') || ''})</option>`).join('')}</select></div>
                    <div class="form-group"><label class="form-label">Предмет</label><select name="subject" class="form-select" required><option>Математика</option><option>Физика</option><option>Английский</option><option>Русский</option></select></div>
                    <div class="form-group"><label class="form-label">Дата</label><input type="date" name="date" class="form-input" required></div>
                    <div class="form-group"><label class="form-label">Время</label><input type="time" name="time" class="form-input" required></div>
                    <div class="form-group"><label class="form-label">Длительность</label><select name="duration" class="form-select"><option>45 мин</option><option>60 мин</option><option>90 мин</option><option>120 мин</option></select></div>
                `;
            }
            modal.classList.add('active');
        }

        async function submitCreateModal(event) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            let url = '';
            if (currentCreateType === 'homework') url = API.createHomework;
            else if (currentCreateType === 'grade') url = API.createGrade;
            else if (currentCreateType === 'lesson') url = API.createLesson;
            
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    closeModal();
                    await loadAllData();
                    showNotification('Создано успешно');
                } else {
                    const error = await response.text();
                    showNotification(`Ошибка: ${error}`, true);
                }
            } catch (e) {
                showNotification('Ошибка соединения', true);
            }
        }

        function closeModal() {
            document.getElementById('createModal').classList.remove('active');
        }

        // ========== ГРАФ ==========
        let svg, g, zoom, simulation;

        async function loadAndRenderGraph() {
            try {
                const graphData = await fetchJSON(API.graph);
                document.getElementById('graph').innerHTML = '';
                renderGraph(graphData);
            } catch (e) {
                console.error('Ошибка загрузки графа:', e);
                document.getElementById('graph').innerHTML = '<div class="loading">Ошибка загрузки графа</div>';
            }
        }

        function renderGraph(data) {
            const container = document.getElementById('graph');
            const width = container.clientWidth;
            const height = 550;

            svg = d3.select("#graph")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .style("background", "linear-gradient(135deg, #fafdfa 0%, #f8f9fa 100%)")
                .style("border-radius", "12px");

            g = svg.append("g");

            zoom = d3.zoom()
                .scaleExtent([0.3, 3])
                .on("zoom", (event) => g.attr("transform", event.transform));
            svg.call(zoom);

            simulation = d3.forceSimulation(data.nodes)
                .force("link", d3.forceLink(data.links).id(d => d.id).distance(150))
                .force("charge", d3.forceManyBody().strength(-350))
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("collide", d3.forceCollide().radius(55));

            // Рисуем связи
            const link = g.append("g")
                .selectAll(".link")
                .data(data.links)
                .enter()
                .append("line")
                .attr("class", "link")
                .attr("stroke", "#cbd5e0")
                .attr("stroke-width", 2);

            // Рисуем узлы
            const node = g.append("g")
                .selectAll(".node")
                .data(data.nodes)
                .enter()
                .append("g")
                .attr("class", "node")
                .call(d3.drag()
                    .on("start", (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
                    .on("drag", (e, d) => { d.fx = e.x; d.fy = e.y; })
                    .on("end", (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }));

            node.append("circle")
                .attr("r", d => d.type === "tutor" ? 26 : 20)
                .attr("fill", d => d.type === "tutor" ? "#6b8e23" : "#4a90e2")
                .attr("stroke", "white")
                .attr("stroke-width", 3)
                .on("click", (e, d) => showNodeInfo(d));

            node.append("text")
                .attr("text-anchor", "middle")
                .attr("dy", "0.3em")
                .attr("fill", "white")
                .attr("font-size", d => d.type === "tutor" ? "18" : "16")
                .text(d => d.type === "tutor" ? "👨‍🏫" : "🎓");

            node.append("text")
                .attr("dx", d => d.type === "tutor" ? 32 : 28)
                .attr("dy", "0.35em")
                .attr("fill", "#333")
                .attr("font-size", "10px")
                .text(d => d.name && d.name.length > 14 ? d.name.slice(0, 12) + "..." : (d.name || '?'));

            simulation.on("tick", () => {
                link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
                node.attr("transform", d => `translate(${d.x},${d.y})`);
            });

            // Управление зумом
            document.getElementById('zoomInBtn').onclick = () => svg.transition().call(zoom.scaleBy, 1.2);
            document.getElementById('zoomOutBtn').onclick = () => svg.transition().call(zoom.scaleBy, 0.8);
            document.getElementById('resetViewBtn').onclick = () => svg.transition().call(zoom.transform, d3.zoomIdentity);
        }

        async function showNodeInfo(node) {
            const panel = document.getElementById('infoPanel');
            const content = document.getElementById('infoPanelContent');
            
            if (node.type === 'tutor') {
                content.innerHTML = `
                    <div class="info-card"><div class="info-card__label">👨‍🏫 Репетитор</div><div class="info-card__value">${escapeHtml(node.name)}</div></div>
                    <div class="info-card"><div class="info-card__label">📚 Предметы</div><div class="info-card__value">${node.subjects?.join(', ') || '—'}</div></div>
                    <div class="info-card"><div class="info-card__label">👥 Учеников</div><div class="info-card__value">${node.students_count || 0}</div></div>
                `;
            } else {
                content.innerHTML = `
                    <div class="info-card"><div class="info-card__label">🎓 Ученик</div><div class="info-card__value">${escapeHtml(node.name)}</div></div>
                    <div class="info-card"><div class="info-card__label">📖 Класс</div><div class="info-card__value">${node.grade || '—'} класс</div></div>
                    <div class="info-card"><div class="info-card__label">👨‍🏫 Репетитор</div><div class="info-card__value">${escapeHtml(node.tutor_name) || '—'}</div></div>
                `;
            }
            panel.classList.add('active');
        }

        // ========== ВКЛАДКИ ==========
        function initTabs() {
            const tabs = document.querySelectorAll('#mainTabs .admin-tab');
            tabs.forEach(tab => {
                tab.addEventListener('click', () => {
                    tabs.forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                    document.getElementById(`tab-${tab.dataset.tab}`).classList.add('active');
                });
            });
        }

        // ========== ЗАГРУЗКА ВСЕХ ДАННЫХ ==========
        async function loadAllData() {
            await Promise.all([
                loadStats(),
                loadUsers(),
                loadHomeworks(),
                loadGrades(),
                loadLessons(),
                loadTutorsForSelect(),
                loadAndRenderGraph()
            ]);
        }

        // ========== ОБРАБОТЧИКИ РАЗМЕРА ОКНА ==========
        window.addEventListener('resize', () => {
            if (svg) {
                svg.attr("width", document.getElementById('graph').clientWidth);
                if (simulation) simulation.alpha(0.3).restart();
            }
        });

        // ========== ЗАПУСК ==========
        initTabs();
        loadAllData();

        // Клик вне модального окна для закрытия
        window.onclick = function(event) {
            const modal = document.getElementById('createModal');
            if (event.target === modal) closeModal();
        };