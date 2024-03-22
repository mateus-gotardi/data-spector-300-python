from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
def get_prev_month(data):
    data_object = datetime.strptime(data, '%y-%m')
    day_one_month_actual = data_object.replace(day=1)
    day_one_prev_month = day_one_month_actual - timedelta(days=1)
    prev_month_formated = day_one_prev_month.strftime('%y-%m')
    return prev_month_formated
def verificar_cancelamento(data_cancelamento, data_proximo_ciclo):
    formato = "%m/%d/%y %H:%M"
    data_cancelamento_obj = datetime.strptime(data_cancelamento, formato)
    data_proximo_ciclo_obj = datetime.strptime(data_proximo_ciclo, formato)
    data_cancelamento_sem_horas = data_cancelamento_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    data_proximo_ciclo_sem_horas = data_proximo_ciclo_obj.replace(hour=0, minute=0, second=0, microsecond=0)
    if data_cancelamento_sem_horas <= data_proximo_ciclo_sem_horas:
        return True
    else:
        return False
def get_next_month(data):
    data_object = datetime.strptime(data, '%y-%m')
    proximo_mes = data_object + timedelta(days=31)
    primeiro_dia_proximo_mes = proximo_mes.replace(day=1)
    proximo_mes_formatado = primeiro_dia_proximo_mes.strftime('%y-%m')
    return proximo_mes_formatado

def make_yy_mm(x):
    year = x.split('/')[2].split(' ')[0]
    month = x.split('/')[0]
    if len(month) == 1:
        month = '0'+month
    return year+'-'+month

duplicated = 0

def fix_next_cicle_date(date):
    yy = date.split('/')[2][-2:]
    mm = date.split('/')[1]
    if int(mm) > 12:
        mm = date.split('/')[0]
    return yy+'-'+mm

def calc_data(data):
    novas_assinaturas = {}
    churn_cancels = {}
    churn_amount = {}
    churn_amount_total = 0.0
    churn_details = {}
    active_clients = {}
    new_clients = {}
    active_clients_total = 0
    churns_total = 0
    churn_rate_monthly = {}
    upgrades_mensal = {}
    total_lines = 0

    for linha in data:
        total_lines+=1
        qtd_cobrancas = linha[0]
        frequencia = linha[1]
        data_inicio = linha[2]
        status = linha[3]
        data_status = linha[4]
        data_cancelamento = linha[5]
        valor = float(linha[6].replace(',', '.').replace('"', ''))
        prox_ciclo = fix_next_cicle_date(linha[7])
        month_inicio = make_yy_mm(data_inicio)
        if frequencia == '30':
            new_clients[month_inicio] = new_clients.get(month_inicio, 0) + 1
            novas_assinaturas[month_inicio] = novas_assinaturas.get(month_inicio, 0) + valor
            if status == 'Ativa':
                active_clients_total += 1
            elif status == 'Cancelada':
                churns_total += 1
                churn_amount_total += valor
                month_cancelamento = make_yy_mm(data_cancelamento)
                next_month = get_next_month(prox_ciclo)
                churn_cancels[month_cancelamento] = churn_cancels.get(month_cancelamento, 0) + 1
                churn_amount[next_month] = churn_amount.get(next_month, 0) + valor
                if not month_cancelamento in churn_details:
                    churn_details[month_cancelamento] = []
                churn_details[month_cancelamento].append({
                    'value': valor,
                    'start_date': data_inicio,
                    'charges_amount': qtd_cobrancas,
                    'cancel_date': data_cancelamento,
                })
            elif status == 'Upgrade':
                #cancelar assinatura
                churn_amount[make_yy_mm(data_cancelamento)] = churn_amount.get(data_cancelamento, 0) + valor
                upgrades_mensal[make_yy_mm(data_status)] = upgrades_mensal.get(make_yy_mm(data_status), 0) + 1

            elif status == 'Atrasada':
                churn_amount[make_yy_mm(data_status)] = churn_amount.get(data_status, 0) + valor

    clients_active_monthly = 0
    cancels_monthly = 0
    monthly_user_grow = {}
    user_grow = 0
    mrr_mensal = {}
    for mes, num_clients in new_clients.items():
        user_grow += num_clients
        monthly_user_grow[mes] = user_grow
        clients_active_monthly += num_clients - churn_cancels.get(mes, 0)
        cancels_monthly += churn_cancels.get(mes,0)
        prev_month = get_prev_month(mes)
        mrr_prev = 0
        if prev_month in mrr_mensal:
            mrr_prev = mrr_mensal.get(prev_month,0)
        mrr_mensal[mes] = (mrr_prev+novas_assinaturas.get(mes,0))-churn_amount.get(mes,0)
        active_clients[mes] = clients_active_monthly
        churn_rate_monthly[mes] = (churn_cancels.get(mes, 0)/active_clients.get(prev_month, clients_active_monthly))*100

    response = {
        'general': {
            'churn_rate': (churns_total/total_lines-duplicated)*100,
            'churn_amount': churn_amount_total,
            'cancels': churns_total,
            'users_active': active_clients_total
        },
        'monthly': {
            'mrr': mrr_mensal,
            'new_clients': new_clients,
            'new_clients_amount': novas_assinaturas,
            'churn_rate':churn_rate_monthly,
            'cancels': churn_cancels,
            'churn_amount':churn_amount,
            'users_active': active_clients,
            'churn_details': churn_details,
            'user_growth': monthly_user_grow,
        }   
    }
    return response

def verificar_usuarios_repetidos(lista_dados):
    lista_dados = sorted(lista_dados, key=lambda x: x[-1])
    duplicatedList = []
    if len(lista_dados) <= 1:
        return False
    
    for i in range(1, len(lista_dados)):
        if lista_dados[i][-1] == lista_dados[i-1][-1]:
            duplicatedList.append(lista_dados[i][-1])
            
    if len(duplicatedList) > 0:
        duplicated = len(duplicatedList)
        return True
    
    return False

def processar_linha(linha):
    colunas = []
    coluna = ""
    dentro_das_aspas = False

    for char in linha:
        if char == ',' and not dentro_das_aspas:
            colunas.append(coluna.strip())
            coluna = ""
        else:
            coluna += char

            if char == '"':
                dentro_das_aspas = not dentro_das_aspas
    
    colunas.append(coluna.strip())
    return colunas


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado', 400
    file = request.files['file']
    file_content = file.read().decode('utf-8')
    linhas = file_content.split('\n')
    cabecalho = linhas[0]
    data_processados = []
    data = linhas[1:]
    for linha in data:
        colunas = processar_linha(linha)
        data_processados.append(colunas)


    data_ordenados = sorted(data_processados, key=lambda x: make_yy_mm(x[2]))
    verificar_usuarios_repetidos(data_ordenados)
    mrr_data = calc_data(data_ordenados)
    return jsonify(mrr_data), 200

if __name__ == '__main__':
    app.run(debug=True)
