function importData() {
    let input = document.createElement('input');
    input.type = 'file';
    input.onchange = _ => {
              let files =   Array.from(input.files);
              console.log(files);
          };
    input.click();
    
  }