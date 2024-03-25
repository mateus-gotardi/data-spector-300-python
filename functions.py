from datetime import datetime, timedelta

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

def get_prev_month(data):
    data_object = datetime.strptime(data, '%y-%m')
    day_one_month_actual = data_object.replace(day=1)
    day_one_prev_month = day_one_month_actual - timedelta(days=1)
    prev_month_formated = day_one_prev_month.strftime('%y-%m')
    return prev_month_formated

def get_next_month(data):
    data_object = datetime.strptime(data, '%y-%m')
    proximo_mes = data_object + timedelta(days=31)
    primeiro_dia_proximo_mes = proximo_mes.replace(day=1)
    proximo_mes_formatado = primeiro_dia_proximo_mes.strftime('%y-%m')
    return proximo_mes_formatado

def make_yy_mm(x):
    year = x.split('/')[2]
    if ' ' in year:
        year = year.split(' ')[0]
    month = x.split('/')[0]
    if len(month) == 1:
        month = '0'+month
    return year+'-'+month

def fix_next_cicle_date(date):
    yy = date.split('/')[2][-2:]
    mm = date.split('/')[1]
    if int(mm) > 12:
        mm = date.split('/')[0]
    return yy+'-'+mm


def calc_totalPeriod(data):
    inicio = make_yy_mm(data[0][2])
    fim = make_yy_mm(data[-1][2])
    years_ = int(fim.split('-')[0])-int(inicio.split('-')[0])+1
    ano_inicio = int(inicio.split('-')[0])
    mes_inicio = int(inicio.split('-')[1])
    mes_termino = int(fim.split('-')[1])
    keys = []
    years = []
    for i in range(years_):
        ano = i+ano_inicio
        years.append(str(ano))
        if ano == ano_inicio:
            for k in range(13 - mes_inicio):
                mes = str(k + mes_inicio)
                if len(mes) < 2:
                    mes =('0'+mes)
                if str(ano) != fim.split('-')[0]:
                    keys.append(str(ano)+'-'+mes)
                elif str(ano) == fim.split('-')[0] and int(mes) <= mes_termino:
                    keys.append(str(ano)+'-'+mes)
        else:
            for j in range(12):
                mes = str(j+1)
                if len(mes) < 2:
                    mes =('0'+mes)
                if str(ano) != fim.split('-')[0]:
                    keys.append(str(ano)+'-'+mes)
                elif str(ano) == fim.split('-')[0] and int(mes) <= mes_termino:
                    keys.append(str(ano)+'-'+mes)
    return {'keys': keys, 'years': years}

def calc_data(data):
    period_ = calc_totalPeriod(data)
    period = period_.get('keys', [])
    years = period_.get('years', [])
    novas_assinaturas = {}
    churn_cancels = {}
    churn_amount = {}
    churn_amount_total = 0.0
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
                next_month = get_next_month(prox_ciclo)
                churn_amount[next_month] = churn_amount.get(next_month, 0) + valor
                month_cancelamento = make_yy_mm(data_cancelamento)
                churn_cancels[month_cancelamento] = churn_cancels.get(month_cancelamento, 0) + 1
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
    for mes in period:
        user_grow += new_clients.get(mes,0)
        clients_active_monthly += new_clients.get(mes,0) - churn_cancels.get(mes, 0)
        cancels_monthly += churn_cancels.get(mes,0)
        prev_month = get_prev_month(mes)
        mrr_prev = 0
        if prev_month in mrr_mensal:
            mrr_prev = mrr_mensal.get(prev_month,0)
        novas_assinaturas[mes]= round(novas_assinaturas.get(mes,0),2)
        monthly_user_grow[mes] = user_grow
        mrr_mensal[mes] = round((mrr_prev+novas_assinaturas.get(mes,0))-churn_amount.get(mes,0), 2)
        churn_amount[mes] = round(churn_amount.get(mes,0), 2)
        active_clients[mes] = clients_active_monthly
        churn_cancels[mes] = churn_cancels.get(mes,0)
        new_clients[mes] = new_clients.get(mes,0)
        churn_rate_monthly[mes] = round((churn_cancels.get(mes, 0)/active_clients.get(prev_month, clients_active_monthly))*100, 2)

    response = {
        'general': {
            'churn_rate': (churns_total/total_lines)*100,
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
            'user_growth': monthly_user_grow,
        },
        'years': years,
        'months': period
    }
    return response