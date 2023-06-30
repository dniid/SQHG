document.addEventListener('DOMContentLoaded', function () {
  let form = document.querySelector('#adminCreateForm');

  form.onsubmit = function (e) {
    e.preventDefault();

    let tag = form.querySelector('#tag');
    let name = form.querySelector('#name');
    let email = form.querySelector('#email');
    let phone = form.querySelector('#phone');
    let password = form.querySelector('#password');

    let [year, month, day] = (form.querySelector('#birthDate').value).split("-").map(Number);
    let jsDate = new Date(year, month - 1, day);
    let birthDate = moment(jsDate).format("YYYY-MM-DD");


    let url = form.getAttribute('action');
    let data = JSON.stringify({
      'tag': tag.value,
      'name': name.value,
      'birth_date': birthDate,
      'email': email.value,
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
      if (response.status == 201) {
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