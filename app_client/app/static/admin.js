// admin.js
// Загрузка списка опросов для выпадающего списка на странице администратора
fetch('/admin/get_all_surveys')
    .then(res => res.json())
    .then(data => {
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

const select = document.getElementById('survey-select');
select.addEventListener('change', function() {
    const uuid = this.value;
    if (!uuid) return;
    fetch(`/admin/get_stat${uuid}`)
        .then(res => res.json())
        .then(data => {
            const container = document.querySelector('.data-container');
            container.innerHTML = '';
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
                        canvas.width = 400;
                        canvas.height = 400;
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
                                    responsive: true,
                                    plugins: { legend: { display: false } },
                                    scales: { y: { beginAtZero: true } }
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
                container.appendChild(blockDiv);
            });
        });
}); 