document.addEventListener('DOMContentLoaded', function () {
    let addQuestionButton = document.getElementById('addQuestion');
    addQuestionButton.addEventListener('click', addNewQuestion);

    function addNewQuestion() {
        let questionsContainer = document.querySelector('.questions-container');
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

            if (selectedType == 'likert') {
                (questionTypeBody.querySelector('.likert-type')).classList.remove('hidden');
            } else if (selectedType === 'alternative') {
                (questionTypeBody.querySelector('.alternative-type')).classList.remove('hidden');
                let addAlternativeButton = questionTypeBody.querySelector('.add-alternative-btn');
                addAlternativeButton.addEventListener('click', function(){
                    addNewAlternative(alternativesContainer)
                });
                if (!(alternativesContainer.querySelector('.alternative-form'))) {
                    addNewAlternative(alternativesContainer);
                };
            } else if (selectedType === 'multiple') {
                (questionTypeBody.querySelector('.multiple-type')).classList.remove('hidden');
                let addMultipleButton = questionTypeBody.querySelector('.add-multiple-btn');
                addMultipleButton.addEventListener('click', function(){
                    addNewMultiple(multiplesContainer)
                });
                if (!(multiplesContainer.querySelector('.multiple-form'))) {
                    addNewMultiple(multiplesContainer);
                };
            } else if (selectedType === 'open') {
                (questionTypeBody.querySelector('.open-type')).classList.remove('hidden');
            }
        });
    };

    let questionHead = document.querySelectorAll('#surveyName, #surveyDescription');
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
});
