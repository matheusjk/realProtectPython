from app import login_user, render_template, redirect, url_for, login_required, current_user, request, logout_user, login_manager, Blueprint, flash
from app.api.forms import ApiForm
from app.models.tables import Log, db
from datetime import datetime

api = Blueprint('api', __name__, template_folder='templates', url_prefix='/api')

@api.route('/listarLogs', methods=["GET"])
def listarTodos():
    try:
        formLog = ApiForm()
        logs = Log.query.all()
        return render_template('logs.html', logs=logs, formLog=formLog)
    except Exception as error:
        print("Erro no metodo listarTodos {}".format(error))
        return error

@api.route('/filtro', methods=["POST"])
def listarFiltro():
    formLog = ApiForm()
    if formLog.validate_on_submit():
        print(formLog.dataInicio.data, formLog.dataFim.data, formLog.contenha.data)
        # print(dataInicio.strftime('%Y-%m-%d %H:%M:%S'))
        contenha = "%{}%".format(formLog.contenha.data)
        logs = Log.query.filter(Log.data >= formLog.dataInicio.data).filter(Log.data <= formLog.dataFim.data).filter(Log.mensagem.like(contenha)).all()
        print("TESTE logs {}".format(logs))
       
        for linha in logs:
            print("TESTE LOG None {}".format(linha))
        
        if logs is None or len(logs) is None or len(logs) == 0:
            flash('NENHUM REGISTRO ENCONTRADOS', "warning")
            return redirect(url_for('.listarTodos'))
        else:
            flash('REGISTROS ENCONTRADOS', "info")
            return render_template('resultadoLogFiltro.html', logs=logs)
    else:
        flash("Erro ao fazer o filtro", "danger")
    return redirect(url_for('.listarTodos'))

@api.route('/registrarLogs', methods=["GET", "POST"])
def registrarLogs():
    arquivo = open('auth.log')
    # print(arquivo.read())
    cont = 0
    for linhas in arquivo.readlines():
        print(linhas.split())
        dataString =  linhas.split()[1] + "-" + linhas.split()[0] + "-2020 " + linhas.split()[2]
        print(dataString)
        data = datetime.strptime(dataString, "%d-%b-%Y %H:%M:%S") # colocando data vindo do Log num padrao americano pra fazer insert no banco
        print(data)
        ip = linhas.split()[3]
        print(ip.replace("ip-", "").replace("-","."))
        ipFormatado = ip.replace("ip-", "").replace("-",".") # formanto IP
        print(str(linhas.split()[4:]).replace("'", "").replace(",", "").replace("[","").replace("]", "")) 
        mensagem  = "{} {}".format(linhas.split()[4],str(linhas.split()[5:]).replace("'", "").replace(",", "").replace("[","").replace("]", "").rstrip())  # limpando o \n nas strings e no final de cada linha 
        log = Log(data, ipFormatado, mensagem) # montando o objeto com os dados vindo do Log
        db.session.add(log) # adicionando na tabela
        db.session.commit()
        if cont == 12500:
            break
        cont = cont + 1
    log = None
    flash('LOGS REGISTRADOS COM SUCESSO', "success")
    return redirect(url_for('api.listarTodos'))

@api.errorhandler(404)
def not_found_error(error):
    return render_template("error.html"),404
