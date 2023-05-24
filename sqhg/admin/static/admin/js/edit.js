document.addEventListener('DOMContentLoaded', function () {
  let form = document.querySelector('#adminEditForm');

  form.onsubmit = function (e) {
    e.preventDefault();

    let name = form.querySelector('#name');
    let phone = form.querySelector('#phone');
    let password = form.querySelector('#password');

    let url = form.getAttribute('action');
    let data = JSON.stringify({
      'name': name.value,
      'phone': (phone.value).replace(/\D/g, ""),
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
      if (response.status == 202) {
        let data = await response.json();
        iziToast.success({
          position: 'topRight',
          message: data.message,
        });
        setTimeout(() => {
          window.location.href = sendBtn.dataset.href;
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