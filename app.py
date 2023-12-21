from flask import Flask, redirect, render_template, request, session, Response, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Rota para exibir o formulário de verificação de idade
@app.route('/')
def age_verification():
    return render_template('age_form.html')

# Rota para coletar a idade do usuário no início da sessão
@app.route('/set_age', methods=['POST'])
def set_age():
    age = request.form.get('age')
    session['age'] = age
    return redirect(url_for('index'))

# Rota para redirecionar para a página de teste após a verificação da idade
@app.route('/index')
def index():
    user_age = session.get('age')
    if user_age:
        return render_template('index.html')
    else:
        return redirect(url_for('age_verification'))


# Rota para lidar com requisições dos usuários
@app.route('/proxy', methods=['GET'])
def proxy():
    url = request.args.get('url')  # Obtém a URL do site de destino
    user_age = session.get('age')  # Obtém a idade do usuário da sessão

    if user_age and int(user_age) < 18:
        sensitive_words = ['porra', 'xvideos', 'caralho', 'suicidio', 'morte', 'buceta', 'piroca']  # Palavras-chave sensíveis
        response = requests.get(url)

        if any(word in response.text for word in sensitive_words):
            return f"<script>alert('ISSO NÃO É COISA PRA VC ESTAR PROCURANDO, VÁ VER NARUTO!');</script>"

    # Obtém o conteúdo HTML do site de destino
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Modifica todos os links para apontar para o próprio proxy
    for link in soup.find_all('a'):
        link['href'] = '/proxy?url=' + link.get('href', '')

    return str(soup)

if __name__ == '__main__':
    app.run(debug=True)
