from app import db, login_manager, generate_password_hash, check_password_hash, func, UserMixin, datetime


class Usuario(UserMixin, db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    dataCriacao = db.Column(db.DateTime(), default=func.localtimestamp(), nullable=False)


    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = generate_password_hash(senha)

    def verifica_senha(self, senhaTemp):
        check_password_hash(self.senha, senhaTemp)
        return generate_password_hash(senhaTemp)

class Log(UserMixin, db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.DateTime(), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    mensagem = db.Column(db.String(255), nullable=False)

    def __init__(self, data, ip, mensagem):
        self.data = data
        self.ip = ip
        self.mensagem = mensagem


# db.session.remove()
# db.reflect() # reflete tabelas no banco
# db.drop_all()
# db.create_all()