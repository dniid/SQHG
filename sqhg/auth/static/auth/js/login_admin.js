document.addEventListener('DOMContentLoaded', function () {
  let form = document.querySelector('#loginForm');

  form.onsubmit = function(e) {
    e.preventDefault();

    let email = form.querySelector('#email');
    let password = form.querySelector('#password');

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
    }).then(response => {
      if (response.status == 200) {
        window.location.href = response.url;
      } else {
        throw new Error(response.statusText);
      }
    }).catch(error => {
      console.error(error);
      iziToast.error({
        position: 'topRight',
        message: 'Credenciais inválidas',
      });
    });
  };

});
