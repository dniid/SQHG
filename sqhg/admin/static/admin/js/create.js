document.addEventListener('DOMContentLoaded', function () {
  let phoneInput = document.getElementById('phone');

  phoneInput.addEventListener('input', (event) => {
      // Remove all non-digit characters from the input value
      let value = event.target.value.replace(/\D/g, '');
      
      // Add the mask to the input value
      if (value.length > 0) {
        value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
      }
      
      // Set the masked value back to the input field
      event.target.value = value;
  });

  let returnBtn = document.getElementById('returnBtn');
  let sendBtn = document.getElementById('sendBtn');
  
  returnBtn.addEventListener('focus', (e) =>{
    window.location.href = returnBtn.dataset.href;
  });
  
  returning.addEventListener('click', (e) =>{
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirmPassword').value;

    if (password == confirmPassword) {

    } else {
      alert('Senhas não conferem!');
    }
  });
});