document.addEventListener('DOMContentLoaded', function () {
  let deleteBtns = document.querySelectorAll('#deleteBtn');

  deleteBtns.forEach(deleteBtn => {
    let url = deleteBtn.dataset.url;
    let modelName = deleteBtn.dataset.model;

    deleteBtn.addEventListener('click', () => {
      Swal.fire({
        title: `Tem certeza que deseja excluir o modelo '${modelName}'?`,
        text: "Essa ação não pode ser revertida!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#853A9E',
        confirmButtonText: 'Sim, desejo excluir!'
      }).then((result) => {
        if (result.isConfirmed) {
          submitDelete();
        }
      })
    });

    function submitDelete() {

      fetch(url, {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': CSRFTOKEN,
          'Content-Type': 'application/json'
        }
      }).then(async response => {
        if (response.status == 200) {
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
    };
  })
});
