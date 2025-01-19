from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Configuração do MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Altere se estiver usando MongoDB remoto
db = client["cadastro_db"]  # Nome do banco de dados
colecao = db["usuarios"]  # Nome da coleção

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Coletar dados do formulário
    nome = request.form['nome']
    sobrenome = request.form['sobrenome']
    data_nascimento = request.form['data_nascimento']
    email = request.form['email']
    profissao = request.form['profissao']
    
    # Criar documento para o MongoDB
    documento = {
        "nome": nome,
        "sobrenome": sobrenome,
        "data_nascimento": data_nascimento,
        "email": email,
        "profissao": profissao
    }
    # Verificar se o e-mail já existe no MongoDB
    usuario_existente = colecao.find_one({"email": email})

    if usuario_existente:
        # Redirecionar para a página de erro com os dados existentes
        return render_template(
            'exists.html',
            usuario=usuario_existente
        )
    else:
        # Criar documento para o MongoDB
        documento = {
            "nome": nome,
            "sobrenome": sobrenome,
            "data_nascimento": data_nascimento,
            "email": email,
            "profissao": profissao
        }

        # Inserir documento no MongoDB
        colecao.insert_one(documento)
        
    # Redirecionar para a página de sucesso
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')  # Página de confirmação

if __name__ == "__main__":
    app.run(debug=True)