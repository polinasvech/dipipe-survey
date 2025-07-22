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