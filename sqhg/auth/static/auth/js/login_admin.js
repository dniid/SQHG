document.addEventListener('DOMContentLoaded', function () {
  let form = document.querySelector('#loginForm');

  form.onsubmit = function(e) {
    e.preventDefault();

    let email = form.querySelector('#email');
    let password = form.querySelector('#password');

    let redirectUrl = form.querySelector('button[type=submit]').dataset.href;
    let url = form.getAttribute('action');
    let data = JSON.stringify({
      'email': email.value,
      'password': password.value,
    })

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRFTOKEN,
        'Content-Type': 'application/json'
      },
      body: data,
    }).then(async response => {
      data = await response.json();

      if (response.status == 200){
        window.location.href = redirectUrl;
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
