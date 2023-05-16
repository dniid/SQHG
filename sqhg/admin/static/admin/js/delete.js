document.addEventListener('DOMContentLoaded', function () {
  let forms = document.querySelectorAll('#adminDeleteForm');

  forms.forEach(form => {   
    form.onsubmit = function (e) {
      e.preventDefault();
  
      let url = form.getAttribute('action');
  
      fetch(url, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': CSRFTOKEN,
          'Content-Type': 'application/json'
        }
      }).then(async response => {
        if (response.status == 201) {
          let data = await response.json();
          iziToast.success({
            position: 'topRight',
            message: data.message,
          });
          setTimeout(() => {
            window.location.href = window.location.href;
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
    }

    let modal = form.querySelector('#modal');
    let showModal = form.querySelector('#trashBtn');
    let closeModal = form.querySelector('#closeModal');
  
    showModal.addEventListener('click', () => {
      modal.classList.remove('hidden')
    })

    closeModal.addEventListener('click', () => {
      modal.classList.add('hidden')
    })
  });

});