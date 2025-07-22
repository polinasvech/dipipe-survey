// admin.js
// Загрузка списка опросов для выпадающего списка на странице администратора
fetch('/admin/get_all_surveys')
    .then(res => res.json())
    .then(data => {
        const select = document.getElementById('survey-select');
        select.innerHTML = '';
        Object.entries(data).forEach(([uuid, title]) => {
            const opt = document.createElement('option');
            opt.value = uuid;
            opt.textContent = title;
            select.appendChild(opt);
        });
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
                        // Построение диаграммы
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