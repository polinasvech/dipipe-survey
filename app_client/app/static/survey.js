fetch(`/api/survey/${window.SURVEY_UUID}`)
    .then(response => response.json())
    .then(resp => {
        if (resp.status !== 'ok') {
            alert('Ошибка загрузки опроса: ' + (resp.message || 'unknown error'));
            return;
        }
        const data = resp.frontend_response;
        const form = document.getElementById('survey-form');
        const storageKey = 'survey_answers_' + window.SURVEY_UUID;
        // Restore saved answers if present
        let saved = {};
        try {
            saved = JSON.parse(localStorage.getItem(storageKey)) || {};
        } catch (e) { saved = {}; }

        // Для отслеживания, трогал ли пользователь ползунок (rating)
        let interactedSliders = {};
        try {
            interactedSliders = JSON.parse(localStorage.getItem(storageKey + '_interacted')) || {};
        } catch (e) { interactedSliders = {}; }

        // Set survey title if present
        if (data.title) {
            const titleElem = document.querySelector('.survey-title');
            if (titleElem) titleElem.textContent = data.title;
        }

        // Track required question elements for validation
        const requiredQuestions = {};

        data.questions.forEach((q, idx) => {
            const div = document.createElement('div');
            div.className = 'mb-3';
            const label = document.createElement('label');
            label.textContent = q.text;
            label.className = 'form-label';
            if (q.required) {
                const star = document.createElement('span');
                star.className = 'required-star';
                star.textContent = '*';
                label.appendChild(star);
            }
            div.appendChild(label);
            const qid = q.uuid;
            let inputRef = null;

            if (q.type === 'text' || q.type === 'tin') {
                const input = document.createElement('input');
                input.type = 'text';
                input.name = qid;
                input.id = qid;
                input.className = 'form-control';
                if (saved[qid]) input.value = saved[qid];
                input.addEventListener('input', () => {
                    saveAnswer(qid, input.value);
                    updateProgressBar();
                    if (q.required) {
                        if (input.value && input.value.trim() !== '') {
                            div.classList.remove('border', 'border-danger');
                        } else {
                            div.classList.add('border', 'border-danger');
                        }
                    }
                });
                div.appendChild(input);
                inputRef = input;
            } else if (q.type === 'rating') {
                const sliderDiv = document.createElement('div');
                sliderDiv.style.display = 'flex';
                sliderDiv.style.alignItems = 'center';
                sliderDiv.style.gap = '16px';
                const input = document.createElement('input');
                input.type = 'range';
                input.name = qid;
                input.id = qid;
                input.className = 'form-range';
                // min/max из массива answers
                if (Array.isArray(q.answers) && q.answers.length > 0) {
                    input.min = Math.min(...q.answers);
                    input.max = Math.max(...q.answers);
                } else {
                    input.min = 0;
                    input.max = 10;
                }
                input.value = saved[qid] !== undefined ? saved[qid] : input.min;
                const valueLabel = document.createElement('span');
                valueLabel.textContent = input.value;
                valueLabel.style.minWidth = '2em';
                input.addEventListener('input', () => {
                    valueLabel.textContent = input.value;
                    saveAnswer(qid, input.value);
                    interactedSliders[qid] = true;
                    localStorage.setItem(storageKey + '_interacted', JSON.stringify(interactedSliders));
                    updateProgressBar();
                    if (q.required) {
                        if (interactedSliders[qid]) {
                            div.classList.remove('border', 'border-danger');
                        } else {
                            div.classList.add('border', 'border-danger');
                        }
                    }
                });
                sliderDiv.appendChild(input);
                sliderDiv.appendChild(valueLabel);
                div.appendChild(sliderDiv);
                inputRef = input;
            } else if (q.type === 'bool') {
                // Используем q.answers для вариантов
                const opts = Array.isArray(q.answers) && q.answers.length === 2 ? q.answers : ['yes', 'no'];
                const inputs = [];
                opts.forEach((opt, i) => {
                    const optDiv = document.createElement('div');
                    optDiv.className = 'form-check form-check-inline';
                    const optInput = document.createElement('input');
                    optInput.type = 'radio';
                    optInput.name = qid;
                    optInput.value = opt;
                    optInput.id = `${qid}_${i}`;
                    optInput.className = 'form-check-input';
                    const optLabel = document.createElement('label');
                    optLabel.textContent = opt;
                    optLabel.className = 'form-check-label';
                    optLabel.htmlFor = optInput.id;
                    optDiv.appendChild(optInput);
                    optDiv.appendChild(optLabel);
                    div.appendChild(optDiv);
                    inputs.push(optInput);
                    if (saved[qid] === opt) optInput.checked = true;
                    optInput.addEventListener('change', () => {
                        if (optInput.checked) saveAnswer(qid, opt);
                        updateProgressBar();
                        if (q.required) {
                            if (inputs.some(inp => inp.checked)) {
                                div.classList.remove('border', 'border-danger');
                            } else {
                                div.classList.add('border', 'border-danger');
                            }
                        }
                    });
                });
                inputRef = inputs;
            } else if (q.type === 'datetime') {
                const input = document.createElement('input');
                input.type = 'datetime-local';
                input.name = qid;
                input.id = qid;
                input.className = 'form-control';
                if (saved[qid]) input.value = saved[qid];
                input.addEventListener('input', () => {
                    saveAnswer(qid, input.value);
                    updateProgressBar();
                    if (q.required) {
                        if (input.value && input.value.trim() !== '') {
                            div.classList.remove('border', 'border-danger');
                        } else {
                            div.classList.add('border', 'border-danger');
                        }
                    }
                });
                div.appendChild(input);
                inputRef = input;
            } else if (q.type === 'radio') {
                // Варианты из q.answers
                const inputs = [];
                (q.answers || []).forEach((opt, i) => {
                    const optDiv = document.createElement('div');
                    optDiv.className = 'form-check';
                    const optInput = document.createElement('input');
                    optInput.type = 'radio';
                    optInput.name = qid;
                    optInput.value = opt;
                    optInput.id = `${qid}_radio_${i}`;
                    optInput.className = 'form-check-input';
                    const optLabel = document.createElement('label');
                    optLabel.textContent = opt;
                    optLabel.className = 'form-check-label';
                    optLabel.htmlFor = optInput.id;
                    optDiv.appendChild(optInput);
                    optDiv.appendChild(optLabel);
                    div.appendChild(optDiv);
                    inputs.push(optInput);
                    if (saved[qid] === opt) optInput.checked = true;
                    optInput.addEventListener('change', () => {
                        if (optInput.checked) saveAnswer(qid, opt);
                        updateProgressBar();
                        if (q.required) {
                            if (inputs.some(inp => inp.checked)) {
                                div.classList.remove('border', 'border-danger');
                            } else {
                                div.classList.add('border', 'border-danger');
                            }
                        }
                    });
                });
                inputRef = inputs;
            } else if (q.type === 'checkbox') {
                // Варианты из q.answers
                const inputs = [];
                (q.answers || []).forEach((opt, i) => {
                    const optDiv = document.createElement('div');
                    optDiv.className = 'form-check';
                    const optInput = document.createElement('input');
                    optInput.type = 'checkbox';
                    optInput.name = qid;
                    optInput.value = opt;
                    optInput.id = `${qid}_checkbox_${i}`;
                    optInput.className = 'form-check-input';
                    const optLabel = document.createElement('label');
                    optLabel.textContent = opt;
                    optLabel.className = 'form-check-label';
                    optLabel.htmlFor = optInput.id;
                    optDiv.appendChild(optInput);
                    optDiv.appendChild(optLabel);
                    div.appendChild(optDiv);
                    inputs.push(optInput);
                    if (Array.isArray(saved[qid]) && saved[qid].includes(opt)) optInput.checked = true;
                    optInput.addEventListener('change', () => {
                        // Собираем все отмеченные
                        const checked = inputs.filter(inp => inp.checked).map(inp => inp.value);
                        saveAnswer(qid, checked);
                        updateProgressBar();
                        if (q.required) {
                            if (checked.length > 0) {
                                div.classList.remove('border', 'border-danger');
                            } else {
                                div.classList.add('border', 'border-danger');
                            }
                        }
                    });
                });
                inputRef = inputs;
            }
            form.insertBefore(div, form.lastElementChild);
            if (idx < data.questions.length - 1) {
                const hr = document.createElement('hr');
                hr.className = 'question-divider';
                form.insertBefore(hr, form.lastElementChild);
            }
            if (q.required) {
                requiredQuestions[qid] = { label, inputRef, div };
            }
        });

        // Add click handler for important-img to swap to tomka_touched.png and hide after 0.5s
        const importantImg = document.getElementById('important-img');
        if (importantImg) {
            importantImg.addEventListener('click', function handleClick() {
                importantImg.src = '/static/tomka_touched.png';
                setTimeout(() => {
                    importantImg.style.display = 'none';
                    importantImg.src = '/static/tomka_important.png'; // restore for next time
                }, 500);
            });
        }

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            let answers = {};
            try {
                answers = JSON.parse(localStorage.getItem(storageKey)) || {};
            } catch (e) { answers = {}; }
            let allValid = true;
            let firstInvalidDiv = null;
            Object.entries(requiredQuestions).forEach(([qid, { label, inputRef, div }]) => {
                let answered = false;
                if (Array.isArray(inputRef)) {
                    if (inputRef[0] && inputRef[0].type === 'checkbox') {
                        answered = inputRef.some(inp => inp.checked);
                    } else {
                        answered = inputRef.some(inp => inp.checked);
                    }
                } else if (inputRef && inputRef.type === 'range') {
                    answered = !!interactedSliders[qid];
                } else if (inputRef) {
                    answered = inputRef.value && inputRef.value.trim() !== '';
                }
                if (!answered) {
                    allValid = false;
                    div.classList.add('border', 'border-danger');
                    if (!firstInvalidDiv) firstInvalidDiv = div;
                } else {
                    div.classList.remove('border', 'border-danger');
                }
            });
            if (!allValid) {
                if (firstInvalidDiv) {
                    firstInvalidDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                const img = document.getElementById('important-img');
                if (img) {
                    img.style.display = 'block';
                    img.src = '/static/tomka_important.png';
                    setTimeout(() => { img.style.display = 'none'; }, 5000);
                }
                return;
            }
            // Формируем ответы в новой структуре
            const questionsWithAnswers = data.questions.map(q => {
                const qid = q.uuid;
                let answer = answers[qid];
                if (q.type === 'checkbox' && !Array.isArray(answer)) answer = answer ? [answer] : [];
                return {
                    ...q,
                    answers: answer !== undefined ? answer : []
                };
            });
            const payload = {
                ...data,
                questions: questionsWithAnswers,
                datetime: new Date().toISOString(),
                timezone: new Date().getTimezoneOffset()
            };
            fetch('/api/survey/create_survey', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })
            .then(res => res.json())
            .then(res => {
                if (res.status === 'ok') {
                    form.style.display = 'none';
                    document.getElementById('thankyou-page').style.display = 'block';
                    const msg = res.message || '';
                    const bg = document.getElementById('server-response-bg');
                    const txt = document.getElementById('server-response');
                    if (msg.trim()) {
                        bg.style.display = 'flex';
                        txt.textContent = msg;
                    } else {
                        bg.style.display = 'none';
                        txt.textContent = '';
                    }
                } else {
                    alert('Ошибка отправки: ' + (res.message || 'unknown error'));
                }
            })
            .catch(() => alert('Ошибка отправки запроса'));
        });

        function saveAnswer(qid, value) {
            const answers = JSON.parse(localStorage.getItem(storageKey)) || {};
            answers[qid] = value;
            localStorage.setItem(storageKey, JSON.stringify(answers));
        }

        function updateProgressBar() {
            const totalRequired = Object.keys(requiredQuestions).length;
            if (totalRequired === 0) {
                document.getElementById('progress-bar').style.width = '0';
                return;
            }
            let answered = 0;
            Object.entries(requiredQuestions).forEach(([qid, { inputRef }]) => {
                if (Array.isArray(inputRef)) {
                    if (inputRef[0] && inputRef[0].type === 'checkbox') {
                        if (inputRef.some(inp => inp.checked)) answered++;
                    } else {
                        if (inputRef.some(inp => inp.checked)) answered++;
                    }
                } else if (inputRef && inputRef.type === 'range') {
                    if (interactedSliders[qid]) answered++;
                } else if (inputRef) {
                    if (inputRef.value && inputRef.value.trim() !== '') answered++;
                }
            });
            const percent = Math.round((answered / totalRequired) * 100);
            document.getElementById('progress-bar').style.width = percent + '%';
        }

        updateProgressBar();
    }); 