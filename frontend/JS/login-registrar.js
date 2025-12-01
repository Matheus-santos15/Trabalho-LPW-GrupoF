$('#opcao-login').click(function() {
    $('#form-cadastro, #titulo-cadastro, #titulo-login, #form-login').fadeToggle();
    $('#cortina-login').toggleClass('-translate-x-75 z-2');
    $('#cortina-login').toggleClass('rounded-br-xl')
    $('#cortina-login').toggleClass('rounded-bl-xl')
    $('#cortina-login').toggleClass('rounded-tl-xl')
    $('#cortina-login').toggleClass('rounded-tr-xl')

    if($('#cortina-login > h1').text() == 'Já tem uma conta?') {
      $('#cortina-login > h1').text('Não tem uma conta?')
      $('#cortina-login > button').text('Cadastre-se')
    } else {
      $('#cortina-login > h1').text('Já tem uma conta?')
      $('#cortina-login > button').text('Fazer log-in')
    }
})