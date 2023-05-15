document.addEventListener('DOMContentLoaded', function () {
  let forms = document.querySelectorAll('#adminDeleteForm');

  let botao = document.querySelector('#btExcluir');

  botao.addEventListener('click',(e) =>{

  })

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
  });

});