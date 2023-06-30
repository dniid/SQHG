document.addEventListener('DOMContentLoaded', function () {
  let importBtns = document.querySelectorAll('#importBtn');

  importBtns.forEach(importBtn => {
    importBtn.addEventListener('click', () => {
      let input = document.createElement('input');
      input.type = 'file';
      input.onchange = _ => {
        let files = Array.from(input.files);
        if (importBtn.dataset.btncontext == 'units'){
          console.log(files);
        } else if (importBtn.dataset.btncontext == 'managers') {
          console.log(files);
        }
      };
      input.click();
    })
  })
});