function fetchData() {
    fetch('/dados_do_grafico')
        .then(async response => {
            if (response.status == 200) {
                let data = await response.json()
            }
        }).catch(function (error) {
            console.log('Ocorreu um erro:', error);
        });
}


