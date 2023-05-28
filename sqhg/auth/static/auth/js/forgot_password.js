document.addEventListener('DOMContentLoaded', function () {
  let form = document.querySelector('#forgotPasswordForm');
  let cancelButton = document.querySelector('#cancelButton');

  cancelButton.addEventListener('click', function (e) {
    e.preventDefault();

    window.location.href = cancelButton.dataset.href;
  });

  form.onsubmit = function(e) {
    e.preventDefault();

    let redirectUrl = cancelButton.dataset.href;

    let email = form.querySelector('#email');
    let url = form.getAttribute('action');
    let data = JSON.stringify({
      'email': email.value,
    })

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRFTOKEN,
        'Content-Type': 'application/json'
      },
      body: data,
    }).then(async response => {
      let data = await response.json();

      if (response.status == 200){
        Swal.fire({
          title: 'Sucesso!',
          text: data.detail,
          icon: 'success',
          confirmButtonText: 'OK'
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = redirectUrl;
          }
        });
      } else {
        iziToast.error({
          position: 'topRight',
          message: data.detail,
        });
      }
    }).catch(error => {
      console.error(error);
      iziToast.error({
        position: 'topRight',
        message: 'Erro interno do servidor',
      });
    });
  };

});
