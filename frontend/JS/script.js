fetch('http://127.0.0.1:8000/users/registrar')
  .then(response => {
    if (!response.ok) {
      throw new Error('Erro na requisição!');
    }
    return response.json(); 
  })
  .then(data => {
    console.log(data); 
  })
  .catch(error => {
    console.error('Erro de conexão:', error);
  });
