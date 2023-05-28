document.addEventListener('DOMContentLoaded', function () {
  let form = document.querySelector('#resetForm');
  let submitButton = document.querySelector('#submitButton');

  form.onsubmit = function(e) {
    e.preventDefault();

    let redirectUrl = submitButton.dataset.href;

    let url = form.getAttribute('action');
    let email = form.dataset.email;
    let password = form.querySelector('#password');
    let confirmPassword = form.querySelector('#confirmPassword');

    if (password.value != confirmPassword.value) {
      iziToast.error({
        position: 'topRight',
        message: 'As senhas não conferem',
      });
      return;
    }

    let data = JSON.stringify({
      'email': email,
      'password': password.value,
    });

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
        throw new Error(data.detail);
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
