document.addEventListener('DOMContentLoaded', function () {
  let phoneInput = document.getElementById('phone');

  phoneInput.addEventListener('input', (event) => {
      let value = event.target.value.replace(/\D/g, '');
      
      if (value.length > 0) {
        value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
      }
      
      event.target.value = value;
  });

  let returnBtn = document.getElementById('returnBtn');
  let sendBtn = document.getElementById('sendBtn');
  
  returnBtn.addEventListener('click', (e) =>{
    window.location.href = returnBtn.dataset.href;
  });

  let password = document.getElementById('password');
  let confirmPassword = document.getElementById('confirmPassword');
  let errorMessage = document.getElementById('errorMessage');

  password.addEventListener('change', (e) => {
    if (!(password.value == confirmPassword.value)){
      sendBtn.setAttribute('disabled', '');
      if (errorMessage.value == undefined) errorMessage.innerHTML = 'Senhas não conferem.'
    } else {
      sendBtn.removeAttribute('disabled');
      errorMessage.innerHTML = '';
    }
  });

  confirmPassword.addEventListener('change', (e) => {
    if (!(password.value == confirmPassword.value)){
      sendBtn.setAttribute('disabled', '');
      if (errorMessage.value == undefined) errorMessage.innerHTML = 'Senhas não conferem.'
    } else {
      sendBtn.removeAttribute('disabled');
      errorMessage.innerHTML = '';
    }
  });

  let form = document.querySelector('#adminForm');

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

    console.log(data);

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRFTOKEN,
        'Content-Type': 'application/json'
      },
      body: data,
    }).then(response => {
      if (response.status == 201) {
        response.json();
        console.log(response)
      } else {
        throw new Error(response.statusText);
      }
    }).then(response => {
      iziToast.success({
        position: 'topRight',
        message: response.message,
      });
      setTimeout(() => {
        window.location.href = sendBtn.dataset.href;
      }, 1000);
    }).catch(error => {
      console.error(error);
      iziToast.error({
        position: 'topRight',
        message: 'Erro ao salvar.',
      });
    });
  }

});