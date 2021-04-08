from app import login_user, render_template, redirect, url_for, login_required, current_user, request, logout_user, \
    login_manager, Mail, Message, mail, generate_password_hash
from flask import Blueprint, flash, render_template, redirect, url_for
# from flask_login import login_required
from app.login.forms import LoginForm, Usuario, CadastroUsuario, Recuperar
from app.models.tables import Usuario, db
# from app..routes import 
import random
import string

# from app.pessoas.routes import pessoa

login = Blueprint('login', __name__, template_folder='templates', url_prefix='/login')

login_manager.login_view = "form.index"
login_manager.login_message = "Por favor se autenticar antes de acessar o sistema!!!"
login_manager.login_message_category = "info"
login_manager.refresh_view = "form.index"
login_manager.needs_refresh_message = u"Para proteger sua conta, por favor reautentique para acessar a pagina"
login_manager.needs_refresh_message_category = "info"

# mail = Mail(form)


# @form.route("/", methods=["GET"])
# def index():
#     return render_template('login.html')

@login.route('/recuperar', methods=["GET", "POST"])
def recuperar():
    forms = Recuperar()
    if forms.validate_on_submit():
        print(forms.email.data)
        email = User.query.filter_by(email=forms.email.data).first()
        if email is not None:
            email.senha = "123@mudar"
            db.session.commit()
            print("EMAIL VINDO DO BANCO {}".format(email))
            msg = Message('Ola isso é um teste', sender='matheusrodriguesh@hotmail.com', recipients=[email.email])
            msg.body = "Sua senha foi resetada para 123@mudar para mudar clique no link http://127.0.0.1:58000/form/alterarSenha"
            mail.send(msg)
            flash('Email disparado com sucesso!!!', 'info')
            return redirect(url_for('form.index'))
        else:
            flash("Email não cadastrado na base de dados", "warning")
            return redirect(url_for('form.index'))
    return render_template("recuperar.html", form=forms)


@login.route('/alterarSenha', methods=["GET", "POST"])
def recuperarAlterar():
    forms = LoginForm()
    if forms.validate_on_submit():
        email = User.query.filter_by(email=forms.email.data).first()
        if email is not None:
            email.senha = generate_password_hash(forms.senha.data)
            db.session.commit()
            # print(email.senha, email, email.email, forms.senha.data)
            flash("Senha alterada com sucesso!!!", "success")
            return redirect(url_for('form.index'))
        else:
            flash("Erro ao alterar a senha", "warning")
            return redirect(url_for("form.index"))
    return render_template('recuperarAlterar.html', form=forms)


@login.route('/register', methods=["GET", "POST"])
def register():
    formRegistroPessoa = CadastroUsuario()
    print(formRegistroPessoa.nome.data)
    if formRegistroPessoa.validate_on_submit():
        user = User(formRegistroPessoa.nome.data, formRegistroPessoa.email.data, formRegistroPessoa.senha.data)
        print(user.nome)
        print(formRegistroPessoa.nome.data)
        db.session.add(user)
        db.session.commit()
        flash("Usuario cadastrado com sucesso!!!", "success")
        # return redirect(url_for('listar'))
    return render_template('register.html', form=formRegistroPessoa)


@login.route('/login', methods=["GET", "POST"])
def index():
    forms = LoginForm()
    if forms.validate_on_submit():
        print(forms.email.data, forms.senha.data)
        user = User.query.filter_by(email=forms.email.data).first()
        if user is None or not user.verifica_senha(forms.senha.data):
            flash("Verifique email ou senha!!!", 'danger')
            return redirect(url_for('.index'))

        print(user.nome)
        login_user(user, remember=True)
        return redirect(url_for('form.listar'))
    else:
        print(forms.errors)
    return render_template('login.html', form=forms)


@login.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.index'))


@login.app_template_filter('strftime')
def formataDataTemplate(date, fmt='%d/%m/%Y %H:%M:%S'):
    return date.strftime(fmt)


@login.route('/listarUsuarios', methods=["GET"])
@login_required
def listar():
    forms = Usuario()
    if current_user.is_authenticated:
        user = User.query.all()
        print(user[0].dataCriacao)
        return render_template('usuariosBlue.html', user=user, f=forms, name=current_user, pessoa=pessoa)
    return redirect(url_for('logout'))


@login.route('/insereFormulario', methods=["GET", "POST"])
def insereFormulario():
    formUser = Usuario()
    return render_template('usuariosInsereBlue.html', f=formUser)


@login.route('/inserir', methods=["GET", "POST"])
@login_required
def insert():
    forms = Usuario()
    print(forms.nome.data)
    # if forms.validate_on_submit():
    user = User(forms.nome.data, forms.email.data, forms.senha.data)
    db.session.add(user)
    db.session.commit()
    flash("Usuario cadastrado com sucesso!!!", "success")
    # return redirect(url_for('listar'))
    return redirect(url_for('form.listar'))
