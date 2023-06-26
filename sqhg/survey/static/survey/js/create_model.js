document.addEventListener('DOMContentLoaded', function () {    
    let saveBtn = document.querySelector('#saveBtn');
    let surveyModelUrl = saveBtn.dataset.surveymodelurl;

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

        fetch(surveyModelUrl, {
            method: 'POST',
            headers: {
              'X-CSRFToken': CSRFTOKEN,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(modelObject),
        }).then(async response => {
            if (response.status == 201 || response.status == 200) {
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
