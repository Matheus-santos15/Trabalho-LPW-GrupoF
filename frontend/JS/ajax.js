function verificarLogin() {
    const token = localStorage.getItem('acess_token');
    
    if (!token) {
        console.warn('Usuário não autenticado, redirecionando para login');
        window.location.href = 'http://127.0.0.1:5500/Trabalho-LPW-GrupoF/pagina-registro.html'; 
        return false;
    }
    return true;
}

function renovarToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    if (!refreshToken) {
        console.warn('Refresh token não encontrado, redirecionando para login');
        window.location.href = 'http://127.0.0.1:5500/Trabalho-LPW-GrupoF/pagina-registro.html';
        return false;
    }
    
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:5000/auth/refresh',
        headers: {
            'Authorization': `Bearer ${refreshToken}`
        },
        
        success: function(resposta) {
            console.log('Token renovado com sucesso');
            localStorage.setItem('acess_token', resposta.acess_token);
            return true;
        },
        
        error: function(erro) {
            console.error('Erro ao renovar token:', erro);
            console.warn('Refresh token expirou também, redirecionando para login');
            localStorage.removeItem('acess_token');
            localStorage.removeItem('refresh_token');
            window.location.href = '/login.html';
            return false;
        }
    });
}

formCadastro = $('#form-cadastro')
formLogin = $('#form-login')

formCadastro.on('submit', function(f) {
    f.preventDefault()

    dados = {
        nome:  $('#input-nome').val(),
        email: $('#input-email').val(),
        senha: $('#input-senha').val()
    }

    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/auth/registrar',
        data: JSON.stringify(dados),
        contentType: 'application/json; charset=utf-8',

        success: function(sucesso) {
            console.log(sucesso)

            loginDados = {
                email: dados.email,
                senha: dados.senha
            }

            $.ajax({
                type: 'POST',
                url: 'http://127.0.0.1:5000/auth/login',
                data: JSON.stringify(dados),
                contentType: 'application/json; charset=utf-8',

                success: function(resposta) {
                    localStorage.setItem('acess_token', resposta.acess_token)
                    localStorage.setItem('refresh_token', resposta.refresh_token)

                    window.location.href = 'http://127.0.0.1:5500/Trabalho-LPW-GrupoF/index.html'
                },

                error: function(erro) {
                    alert('Erro no login automático! Status: ' + erro.status)
                }
            })
        },

        error: function(erro) {
            console.log(erro)
        }
    })
})

formLogin.on('submit', function(f) {
    f.preventDefault()

    dados = {
        email: $('#email-login').val(),
        senha: $('#senha-login').val()
    }

    $.ajax({
        type: 'POST',
        url: 'http://127.0.0.1:5000/auth/login',
        data: JSON.stringify(dados),
        contentType: 'application/json; charset=utf-8',

        success: function(resposta) {
            localStorage.setItem('acess_token', resposta.acess_token)
            localStorage.setItem('refresh_token', resposta.refresh_token)

            window.location.href = 'http://127.0.0.1:5500/Trabalho-LPW-GrupoF/index.html'
        },

        error: function(erro) {
            console.error('Erro no login:', erro)
            $('#error-message').html('Status: ' + erro.status + ' Erro nas credenciais')
            setTimeout(function() {
                $('#error-message').html('')
            }, 3000)
        }
    })
})