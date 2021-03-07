from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pessoas.sqlite3'

db = SQLAlchemy(app)
class Pessoa(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(150))
    telefone = db.Column(db.String(150))
    nascimento = db.Column(db.String(150))
    
    def __init__(self, nome, email, telefone, nascimento):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.nascimento = nascimento
    

@app.route('/')
def index():
    pessoas = Pessoa.query.all()
    return render_template('index.html', pessoas=pessoas)


@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        pessoa = Pessoa(request.form['nome'], request.form['email'], request.form['telefone'], request.form['nascimento'])
        db.session.add(pessoa)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    pessoa = Pessoa.query.get(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)