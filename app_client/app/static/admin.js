// admin.js
// Загрузка списка опросов для выпадающего списка на странице администратора
let allSurveys = [];
fetch('/admin/get_all_surveys')
    .then(res => res.json())
    .then(data => {
        allSurveys = Array.isArray(data) ? data : [];
        const select = document.getElementById('survey-select');
        select.innerHTML = '';
        if (Array.isArray(data)) {
            data.forEach(survey => {
                const opt = document.createElement('option');
                opt.value = survey.uuid;
                opt.textContent = survey.name;
                select.appendChild(opt);
            });
        }
        select.insertAdjacentHTML('afterbegin', '<option value="" disabled selected>Выберите опрос</option>');
    });

function renderSurveyInfo(survey, stat) {
    const infoDiv = document.getElementById('survey-info') || document.createElement('div');
    infoDiv.id = 'survey-info';
    infoDiv.style.marginTop = '18px';
    infoDiv.style.fontSize = '1em';
    infoDiv.innerHTML = '';
    if (!survey) {
        infoDiv.innerHTML = '';
        return infoDiv;
    }
    // 1. Ссылка на опрос
    const link = document.createElement('a');
    link.href = `/survey/${survey.uuid}`;
    link.textContent = 'Ссылка на опрос';
    link.target = '_blank';
    link.style.display = 'block';
    link.style.marginBottom = '8px';
    infoDiv.appendChild(link);
    // 2. Дата начала
    const start = document.createElement('div');
    start.textContent = 'Дата начала: ' + (survey.start_date ? new Date(survey.start_date).toLocaleString() : '-');
    infoDiv.appendChild(start);
    // 3. Дата окончания
    const end = document.createElement('div');
    end.textContent = 'Дата окончания: ' + (survey.end_date ? new Date(survey.end_date).toLocaleString() : '-');
    infoDiv.appendChild(end);
    // 4. Число заполнений
    const count = document.createElement('div');
    count.textContent = 'Число заполнений: ' + (stat && typeof stat.count === 'number' ? stat.count : '-');
    infoDiv.appendChild(count);
    // 5. Число вопросов
    let questionsCount = '-';
    if (stat && Array.isArray(stat.answers) && stat.answers.length > 0) {
        // Считаем уникальные question_id
        const qids = new Set(stat.answers.map(a => a.question_id));
        questionsCount = qids.size;
    }
    infoDiv.appendChild(document.createElement('div')).textContent = 'Число вопросов: ' + questionsCount;
    return infoDiv;
}

const select = document.getElementById('survey-select');
select.addEventListener('change', function() {
    const uuid = this.value;
    if (!uuid) return;
    const survey = allSurveys.find(s => s.uuid === uuid);
    fetch(`/admin/get_stat${uuid}`)
        .then(res => res.json())
        .then(data => {
            // Информация об опросе
            const infoDiv = renderSurveyInfo(survey, data);
            const infoContainer = document.getElementById('survey-select-container');
            // Удаляем старую инфу если есть
            const old = document.getElementById('survey-info');
            if (old) old.remove();
            infoContainer.appendChild(infoDiv);
            // Диаграммы
            const dataContainer = document.querySelector('.data-container');
            dataContainer.innerHTML = '';
            if (!data.blocks || !Array.isArray(data.blocks)) return;
            data.blocks.forEach((block, blockIdx) => {
                const blockDiv = document.createElement('div');
                blockDiv.className = 'admin-block';
                if (block.diagrams && Array.isArray(block.diagrams)) {
                    block.diagrams.forEach((diagram, dIdx) => {
                        const diagramDiv = document.createElement('div');
                        diagramDiv.className = 'admin-diagram color' + ((dIdx % 5) + 1);
                        const title = document.createElement('div');
                        title.className = 'admin-diagram-title';
                        title.textContent = diagram.title;
                        diagramDiv.appendChild(title);
                        // Chart.js canvas
                        const canvas = document.createElement('canvas');
                        canvas.style.width = '100%';
                        canvas.style.height = '100%';
                        canvas.width = canvas.height = undefined; // Chart.js сам управляет размером
                        diagramDiv.appendChild(canvas);
                        if (diagram.type === 'round') {
                            new Chart(canvas, {
                                type: 'pie',
                                data: {
                                    labels: diagram.categories.map(cat => cat.label),
                                    datasets: [{
                                        data: diagram.categories.map(cat => cat.value),
                                        backgroundColor: diagram.categories.map(cat => cat.color || '#3498db'),
                                    }]
                                },
                                options: {
                                    responsive: true,
                                    plugins: { legend: { position: 'bottom' } }
                                }
                            });
                        } else if (diagram.type === 'column') {
                            const labels = diagram.categories.map(cat => cat.label);
                            const hasLongLabel = labels.some(l => l.length > 15);
                            const dataset = {
                                label: '',
                                data: diagram.categories.map(cat => cat.value),
                                backgroundColor: diagram.categories.map(cat => cat.color || '#3498db'),
                            };
                            new Chart(canvas, {
                                type: 'bar',
                                data: {
                                    labels: labels,
                                    datasets: [dataset]
                                },
                                options: {
                                    responsive: true,
                                    plugins: {
                                        legend: {
                                            display: hasLongLabel,
                                            labels: hasLongLabel ? {
                                                generateLabels: function(chart) {
                                                    // Формируем легенду по label/цвету
                                                    return chart.data.labels.map((label, i) => ({
                                                        text: label,
                                                        fillStyle: chart.data.datasets[0].backgroundColor[i],
                                                        strokeStyle: chart.data.datasets[0].backgroundColor[i],
                                                        index: i
                                                    }));
                                                }
                                            } : {}
                                        }
                                    },
                                    scales: {
                                        y: { beginAtZero: true },
                                        x: {
                                            ticks: { display: !hasLongLabel }
                                        }
                                    }
                                }
                            });
                        } else if (diagram.type === 'bar') {
                            new Chart(canvas, {
                                type: 'bar',
                                data: {
                                    labels: diagram.categories.map(cat => cat.label),
                                    datasets: [{
                                        label: diagram.title,
                                        data: diagram.categories.map(cat => cat.value),
                                        backgroundColor: diagram.categories.map(cat => cat.color || '#3498db'),
                                    }]
                                },
                                options: {
                                    indexAxis: 'y',
                                    responsive: true,
                                    plugins: { legend: { display: false } },
                                    scales: { x: { beginAtZero: true } }
                                }
                            });
                        } else if (diagram.type === 'text') {
                            // Рисуем текст в canvas
                            const ctx = canvas.getContext('2d');
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                            ctx.font = '24px Arial';
                            ctx.textAlign = 'center';
                            ctx.textBaseline = 'middle';
                            ctx.fillStyle = '#222';
                            const text = diagram.categories.map(cat => cat.label).join(', ');
                            ctx.fillText(text, canvas.width / 2, canvas.height / 2);
                        } else if (diagram.type === 'image') {
                            // Рисуем картинку в canvas
                            const ctx = canvas.getContext('2d');
                            ctx.clearRect(0, 0, canvas.width, canvas.height);
                            diagram.categories.forEach(cat => {
                                const img = new window.Image();
                                img.onload = function() {
                                    // Центрируем картинку
                                    let scale = Math.min(canvas.width / img.width, canvas.height / img.height, 1);
                                    let w = img.width * scale;
                                    let h = img.height * scale;
                                    let x = (canvas.width - w) / 2;
                                    let y = (canvas.height - h) / 2;
                                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                                    ctx.drawImage(img, x, y, w, h);
                                };
                                img.src = cat.label;
                            });
                        } else if (diagram.type === 'table') {
                            // Рисуем таблицу по двумерному массиву
                            const table = document.createElement('table');
                            table.className = 'admin-table';
                            const rows = diagram.categories;
                            if (Array.isArray(rows)) {
                                rows.forEach((row, rIdx) => {
                                    const tr = document.createElement('tr');
                                    row.forEach((cell, cIdx) => {
                                        const td = document.createElement(rIdx === 0 ? 'th' : 'td');
                                        td.textContent = cell;
                                        tr.appendChild(td);
                                    });
                                    table.appendChild(tr);
                                });
                            }
                            // Вставляем таблицу в центр canvas
                            canvas.style.display = 'none';
                            diagramDiv.appendChild(table);
                        } else {
                            // fallback: просто список
                            const cats = document.createElement('div');
                            cats.style.fontSize = '0.95em';
                            cats.innerHTML = diagram.categories.map(cat => `<div>${cat.label}: <b>${cat.value}</b></div>`).join('');
                            diagramDiv.appendChild(cats);
                        }
                        blockDiv.appendChild(diagramDiv);
                    });
                }
                dataContainer.appendChild(blockDiv);
            });
        });
}); 