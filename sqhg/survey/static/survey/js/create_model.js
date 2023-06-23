document.addEventListener('DOMContentLoaded', function () {
    let addQuestionButton = document.getElementById('addQuestion');
    addQuestionButton.addEventListener('click', addNewQuestion);

    function addNewQuestion() {
        let questionsContainer = document.querySelector('#questions-container');
        let question = document.querySelector('.question-form-template').cloneNode(true);
        question.classList.remove('question-form-template', 'hidden');
        question.classList.add('question-form');
        questionsContainer.appendChild(question);

        let removeButton = question.querySelector('.btn-remove-question');
        removeButton.addEventListener('click', (el) => {
            removeButton.closest('.question-form').remove();
        });

        let questionType = question.querySelector('.question-type');
        let questionTypeBody = question.querySelector('.question-type-body');
        questionType.addEventListener('change', (qt) => {
            let selectedType = qt.target.value;
            let divsNotHidden = questionTypeBody.querySelectorAll('.type:not(.hidden)')
            divsNotHidden.forEach(dnh => {
                dnh.classList.add('hidden');
            });
            let alternativesContainer = questionTypeBody.querySelector('.alternatives-container');
            let multiplesContainer = questionTypeBody.querySelector('.multiples-container');

            if (selectedType == '1') {
                (questionTypeBody.querySelector('.likert-type')).classList.remove('hidden');
            } else if (selectedType === '2') {
                (questionTypeBody.querySelector('.alternative-type')).classList.remove('hidden');
                let addAlternativeButton = questionTypeBody.querySelector('.add-alternative-btn');
                if (addAlternativeButton.dataset.viewed == 'false') {
                    addAlternativeButton.dataset.viewed = 'true';
                    addAlternativeButton.addEventListener('click', function(){
                        addNewAlternative(alternativesContainer)
                    })
                }
                if (!(alternativesContainer.querySelector('.alternative-form'))) {
                    addNewAlternative(alternativesContainer);
                };
            } else if (selectedType === '3') {
                (questionTypeBody.querySelector('.multiple-type')).classList.remove('hidden');
                let addMultipleButton = questionTypeBody.querySelector('.add-multiple-btn');
                if (addMultipleButton.dataset.viewed == 'false') {
                    addMultipleButton.dataset.viewed = 'true';
                    addMultipleButton.addEventListener('click', function(){
                        addNewMultiple(multiplesContainer)
                    });
                }
                if (!(multiplesContainer.querySelector('.multiple-form'))) {
                    addNewMultiple(multiplesContainer);
                };
            } else if (selectedType === '4') {
                (questionTypeBody.querySelector('.open-type')).classList.remove('hidden');
            }
        });
    };

    let questionHead = document.querySelectorAll('#surveyNameTitle, #surveyDescriptionTitle');
    questionHead.forEach(el => {
        el.addEventListener('focus', () => {
            let input = el.parentNode.querySelector('input');

            el.classList.add("hidden");
            input.classList.remove("hidden");
            input.focus();

            input.addEventListener('blur', () => {
                const inputValue = input.value;

                if (!(input.value.trim() === "")) {
                    el.innerHTML = inputValue;
                    el.classList.remove("hidden");
                    input.classList.add("hidden");
                }
            });
        });
    });

    function addNewAlternative(container) {
        let alternative = container.querySelector('.alternative-form-template').cloneNode(true);
        alternative.classList.remove('alternative-form-template', 'hidden');
        alternative.classList.add('alternative-form');
        container.appendChild(alternative);

        let removeAlternativeButton = alternative.querySelector('.btn-remove-alternative');
        removeAlternativeButton.addEventListener('click', (el) => {
            removeAlternativeButton.closest('.alternative-form').remove();
        });
    };

    function addNewMultiple(container) {
        let multiple = container.querySelector('.multiple-form-template').cloneNode(true);
        multiple.classList.remove('multiple-form-template', 'hidden');
        multiple.classList.add('multiple-form');
        container.appendChild(multiple);

        let removeMultipleButton = multiple.querySelector('.btn-remove-multiple');
        removeMultipleButton.addEventListener('click', (el) => {
            removeMultipleButton.closest('.multiple-form').remove();
        });
    };

    addNewQuestion();

    let saveBtn = document.querySelector('#saveBtn');
    let createModelUrl = saveBtn.dataset.surveymodelurl;

    saveBtn.addEventListener('click', ()=> {
        // dialog

        let surveyNameTitle = document.querySelector('#surveyNameTitle');
        let surveyDescriptionTitle = document.querySelector('#surveyDescriptionTitle');

        let modelObject = {
            name: surveyNameTitle.textContent,
            description: surveyDescriptionTitle.textContent,
            questions: [],
        }

        let questionsContainer = document.querySelector('#questions-container');
        let questionForm = questionsContainer.querySelectorAll('.question-form');

        questionForm.forEach(question => {
            let questionDescription = question.querySelector('#questionDescription').value;
            let questionType = question.querySelector('#questionType').value;

            let questionObject = {
                description: questionDescription,
                type: questionType,
                options: [],
            }

            if (questionType == '2') {
                let alternativesContainer = question.querySelector('.alternatives-container');
                let alternativeForm = alternativesContainer.querySelectorAll('.alternative-form');

                alternativeForm.forEach(option => {
                    let optionDescription = option.querySelector('#questionAlternative').value;
                    let optionObject = {
                        description: optionDescription,
                    }
                    questionObject.options.push(optionObject);
                });

            } else if (questionType == '3') {
                let multiplesContainer = question.querySelector('.multiples-container');
                let multipleForm = multiplesContainer.querySelectorAll('.multiple-form');
                
                multipleForm.forEach(option => {
                    let optionDescription = option.querySelector('#questionMultiple').value;
                    let optionObject = {
                        description: optionDescription,
                    }
                    questionObject.options.push(optionObject);
                });

            }
            modelObject.questions.push(questionObject);
        });

        fetch(createModelUrl, {
            method: 'POST',
            headers: {
              'X-CSRFToken': CSRFTOKEN,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(modelObject),
        }).then(async response => {
            if (response.status == 201) {
                let data = await response.json();
                iziToast.success({
                    position: 'topRight',
                    message: data.message,
                });
                setTimeout(() => {
                    window.location.href = saveBtn.dataset.href;
                }, 1000);
            } else {
                throw new Error(response.statusText);
            }
        }).catch(error => {
            console.error(error);
            iziToast.error({
                position: 'topRight',
                message: 'Erro ao salvar.',
            });
        });

        
    });
});
