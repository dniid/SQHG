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
    let surveyModelUrl = saveBtn.dataset.surveymodelurl;
    let questionUrl = saveBtn.dataset.questionurl;
    let optionUrl = saveBtn.dataset.optionurl;

    saveBtn.addEventListener('click', ()=> {
        // dialog

        let surveyNameTitle = document.querySelector('#surveyNameTitle');
        let surveyDescriptionTitle = document.querySelector('#surveyDescriptionTitle');
        let questionsContainer = document.querySelector('#questions-container');
        let containerQuestions = questionsContainer.querySelectorAll('.question-form');

        let surveyModelData = JSON.stringify({
            'name': surveyNameTitle.value,
            'description': surveyDescriptionTitle.value,
        });

        fetch(surveyModelUrl, {
            method: 'POST',
            headers: {
              'X-CSRFToken': CSRFTOKEN,
              'Content-Type': 'application/json'
            },
            body: surveyModelData,
          }).then(async response => {
            if (response.status == 201) {
              let data = await response.json();
              let surveyModelId = data.survey_model_id;

                containerQuestions.forEach(question => {
                    let questionDescription = question.querySelector('#questionDescription');
                    let questionType = question.querySelector('#questionType').value;

                    let questionData = JSON.stringify({
                        'description': questionDescription.value,
                        'type': parseInt(questionType),
                        'survey_model_id': parseInt(surveyModelId),
                    });
                    
                    fetch(questionUrl, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': CSRFTOKEN,
                            'Content-Type': 'application/json'
                        },
                        body: questionData,
                      }).then(async response => {
                        if (response.status == 201) {
                            let data = await response.json();
                            let questionId = data.question_id;
                            
                            if (questionType == '2') {
                                let questionAlternatives = question.querySelectorAll('#questionAlternative');

                                questionAlternatives.forEach(questionAlternative =>{
                                    let optionData = JSON.stringify({
                                        'description': questionAlternative.value,
                                        'question_id': parseInt(questionId),
                                    });
                                    fetch(optionUrl, {
                                        method: 'POST',
                                        headers: {
                                            'X-CSRFToken': CSRFTOKEN,
                                            'Content-Type': 'application/json'
                                        },
                                        body: optionData,
                                    }).then(async response => {
                                        if (response.status == 201) {
                                            let data = await response.json();
                                        } else {
                                            throw new Error(response.statusText);
                                        }
                                    }).catch(error => {
                                        console.error(error);
                                        iziToast.error({
                                            position: 'topRight',
                                            message: 'Erro ao gravar opções.',
                                        });
                                    });
                                });

                            } else if (questionType == '3') {

                                let questionMultiples = question.querySelectorAll('#questionMultiple');

                                questionMultiples.forEach(questionMultiple =>{
                                    let optionData = JSON.stringify({
                                        'description': questionMultiple.value,
                                        'question_id': parseInt(questionId),
                                    });
                                    fetch(optionUrl, {
                                        method: 'POST',
                                        headers: {
                                            'X-CSRFToken': CSRFTOKEN,
                                            'Content-Type': 'application/json'
                                        },
                                        body: optionData,
                                    }).then(async response => {
                                        if (response.status == 201) {
                                            let data = await response.json();
                                        } else {
                                            throw new Error(response.statusText);
                                        }
                                    }).catch(error => {
                                        console.error(error);
                                        iziToast.error({
                                            position: 'topRight',
                                            message: 'Erro ao gravar opções.',
                                        });
                                    });
                                });

                            }
 
                        } else {
                            throw new Error(response.statusText);
                        }
                      }).catch(error => {
                        console.error(error);
                        iziToast.error({
                          position: 'topRight',
                          message: 'Erro ao gravar questões.',
                        });
                    });
                });
                iziToast.success({
                    position: 'topRight',
                    message: data.message,
                });
                setTimeout(() => {
                    window.location.href = sendBtn.dataset.href;
                }, 1000);

            } else {
              throw new Error(response.statusText);
            }
          }).catch(error => {
            console.error(error);
            iziToast.error({
              position: 'topRight',
              message: 'Erro ao criar modelo de questionário.',
            });
        });
    });
});
