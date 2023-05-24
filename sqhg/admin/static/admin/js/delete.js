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
        if (response.status == 202) {
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

    let deleteForm = form.querySelector('#adminDeleteForm');
    let showModal = form.querySelector('#trashBtn');
  
    showModal.addEventListener('click', () => {
      Swal.fire({
        title: 'Tem certeza que deseja excluir o admin?',
        text: "Essa ação não pode ser revertida!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#853A9E',
        confirmButtonText: 'Sim, desejo excluir!'
      }).then((result) => {
        if (result.isConfirmed) {
          deleteForm.submit();
        }
      })
    })
  });

});