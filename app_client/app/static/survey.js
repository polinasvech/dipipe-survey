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

        // Debug: print all survey_answers_* keys in localStorage
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith('survey_answers_')) {
                console.log(key, localStorage.getItem(key));
            }
        });

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
            const qid = q.id;

            // For validation, keep reference to input(s)
            let inputRef = null;

            if (q.type === 'str' || q.type === 'tin') {
                const input = document.createElement('input');
                input.type = 'text';
                input.name = qid;
                input.id = qid;
                input.className = 'form-control';
                if (saved[qid]) input.value = saved[qid];
                input.addEventListener('input', () => {
                    saveAnswer(qid, input.value);
                });
                div.appendChild(input);
                inputRef = input;
            } else if (q.type === 'int') {
                const sliderDiv = document.createElement('div');
                sliderDiv.style.display = 'flex';
                sliderDiv.style.alignItems = 'center';
                sliderDiv.style.gap = '16px';
                const input = document.createElement('input');
                input.type = 'range';
                input.name = qid;
                input.id = qid;
                input.className = 'form-range';
                input.min = q.min !== undefined ? q.min : 0;
                input.max = q.max !== undefined ? q.max : 10;
                input.value = saved[qid] !== undefined ? saved[qid] : input.min;
                const valueLabel = document.createElement('span');
                valueLabel.textContent = input.value;
                valueLabel.style.minWidth = '2em';
                input.addEventListener('input', () => {
                    valueLabel.textContent = input.value;
                    saveAnswer(qid, input.value);
                });
                sliderDiv.appendChild(input);
                sliderDiv.appendChild(valueLabel);
                div.appendChild(sliderDiv);
                inputRef = input;
            } else if (q.type === 'bool') {
                const yesDiv = document.createElement('div');
                yesDiv.className = 'form-check form-check-inline';
                const yesInput = document.createElement('input');
                yesInput.type = 'radio';
                yesInput.name = qid;
                yesInput.value = 'yes';
                yesInput.id = `${qid}_yes`;
                yesInput.className = 'form-check-input';
                const yesLabel = document.createElement('label');
                yesLabel.textContent = 'Да';
                yesLabel.className = 'form-check-label';
                yesLabel.htmlFor = yesInput.id;
                yesDiv.appendChild(yesInput);
                yesDiv.appendChild(yesLabel);
                div.appendChild(yesDiv);
                const noDiv = document.createElement('div');
                noDiv.className = 'form-check form-check-inline';
                const noInput = document.createElement('input');
                noInput.type = 'radio';
                noInput.name = qid;
                noInput.value = 'no';
                noInput.id = `${qid}_no`;
                noInput.className = 'form-check-input';
                const noLabel = document.createElement('label');
                noLabel.textContent = 'Нет';
                noLabel.className = 'form-check-label';
                noLabel.htmlFor = noInput.id;
                noDiv.appendChild(noInput);
                noDiv.appendChild(noLabel);
                div.appendChild(noDiv);
                inputRef = [yesInput, noInput];
                if (saved[qid]) {
                    if (saved[qid] === 'yes') yesInput.checked = true;
                    if (saved[qid] === 'no') noInput.checked = true;
                }
                yesInput.addEventListener('change', () => {
                    if (yesInput.checked) saveAnswer(qid, 'yes');
                });
                noInput.addEventListener('change', () => {
                    if (noInput.checked) saveAnswer(qid, 'no');
                });
            } else if (q.type === 'datetime') {
                const input = document.createElement('input');
                input.type = 'datetime-local';
                input.name = qid;
                input.id = qid;
                input.className = 'form-control';
                if (saved[qid]) input.value = saved[qid];
                input.addEventListener('input', () => {
                    saveAnswer(qid, input.value);
                });
                div.appendChild(input);
                inputRef = input;
            }
            form.insertBefore(div, form.lastElementChild);
            // Add divider after each question except the last
            if (idx < data.questions.length - 1) {
                const hr = document.createElement('hr');
                hr.className = 'question-divider';
                form.insertBefore(hr, form.lastElementChild);
            }
            if (q.required) {
                requiredQuestions[qid] = { label, inputRef, div };
            }
        });

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Collect answers from localStorage
            let answers = {};
            try {
                answers = JSON.parse(localStorage.getItem(storageKey)) || {};
            } catch (e) { answers = {}; }
            // Validate required questions
            let allValid = true;
            Object.entries(requiredQuestions).forEach(([qid, { label, inputRef, div }]) => {
                let answered = false;
                if (Array.isArray(inputRef)) {
                    answered = inputRef.some(inp => inp.checked);
                } else if (inputRef && inputRef.type === 'range') {
                    answered = answers[qid] !== undefined && answers[qid] !== '';
                } else if (inputRef) {
                    answered = inputRef.value && inputRef.value.trim() !== '';
                }
                if (!answered) {
                    allValid = false;
                    div.classList.add('border', 'border-danger');
                } else {
                    div.classList.remove('border', 'border-danger');
                }
            });
            if (!allValid) {
                window.scrollTo({ top: 0, behavior: 'smooth' });
                return;
            }
            // Fill ansvers fields in questions
            const questionsWithAnswers = data.questions.map(q => {
                return {
                    ...q,
                    ansvers: [answers[q.id] !== undefined ? answers[q.id] : '']
                };
            });
            const payload = {
                ...data,
                questions: questionsWithAnswers
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
    }); 