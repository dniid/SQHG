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

  returnBtn.addEventListener('click', (e) => {
    window.location.href = returnBtn.dataset.href;
  });

  let password = document.getElementById('password');
  let confirmPassword = document.getElementById('confirmPassword');
  let errorMessage = document.getElementById('errorMessage');

  password.addEventListener('change', (e) => {
    if (!(password.value == confirmPassword.value)) {
      sendBtn.setAttribute('disabled', '');
      if (errorMessage.value == undefined) errorMessage.innerHTML = 'Senhas não conferem.'
    } else {
      sendBtn.removeAttribute('disabled');
      errorMessage.innerHTML = '';
    }
  });

  confirmPassword.addEventListener('change', (e) => {
    if (!(password.value == confirmPassword.value)) {
      sendBtn.setAttribute('disabled', '');
      if (errorMessage.value == undefined) errorMessage.innerHTML = 'Senhas não conferem.'
    } else {
      sendBtn.removeAttribute('disabled');
      errorMessage.innerHTML = '';
    }
  });

  const modal = document.querySelector('.modal');

  const showModal = document.querySelector('.show-Modal')
  const closeModal = document.querySelector('.close-Modal')

  showModal.addEventListener('click', function () {
    modal.classList.remove('hidden')
  })
  closeModal.addEventListener('click', function () {
    modal.classList.add('hidden')
  })


});