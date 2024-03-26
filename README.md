# Data Spector 300 Back-End
 App desenvolvido como teste técnico para o Processo Seletivo de Desenvolvedor Full-stack da Copybase
 Esse servidor flask recebe uma planilha de dados e processa informações como MRR, Churn Rate, entre outras e reotrna os dados mês a mês para serem consumidos pelo front end pelo [FRONT END VUE JS](https://github.com/mateus-gotardi/data-spector-300-vue)

## Deploy
 O deploy do Back-End foi efetuado na [RAILWAY](https://railway.app/)

## Rotas
 O app possui somente uma rota `/upload` que recebe o upload de um arquivo CSV ou XLSX

## Tecnologias utilizadas
 - Python
 - Pytest
 - Flask

## Modelo de resposta
 A resposta da requisição é um objeto no seguinte formato:
 ```sh
{
        'general': {
            'churn_rate': média do churn rate para todo o período analisado,
            'churn_amount': total de churns para todo o período analisado,
            'cancels': total de cancelamentos para todo o período analisado,
            'users_active': total de clientes ativos em todo o período analisado
        },
        'monthly': {
            'mrr': {mes: mrr ...},
            'new_clients': {mes: novos clientes nesse mês ...},
            'new_clients_amount': {mes: valor total das novas assinaturas do mês ...},
            'churn_rate':{mes: churn rate do mês ...},
            'cancels': {mes: cancelamentos no mês ...},
            'churn_amount':{mes: valor que não será mais recebido a partir desse mes...},
            'users_active': {mes: usuários ativos no final do mês...},
            'user_growth': {mes: numero total de usuários ativos e cancelados que ja utilizaram o sistema até aquele mês...},
        },
        'years': [], #lista com todos os anos do espaço amostral
        'months': [] #lista com todos os meses do espaço amostral
}
```
# Setup do Projeto na sua máquina
 Tenha certeza que possui Python intalado.
 Clone ou baixe o repositório e rode o ambiente virtual utilizando
  
```sh
venv\Scripts\activate
```
altere o cors para permitir requisições de qualquer fonte ou do seu localhost
```sh
linha 7 app.py: CORS(app, resources={r"/*": {"origins": "*"}})
```
### Rode o servidor
utilize o comando
```sh
python app.py
```
o App deve estar rodando em http://localhost:5000
rode o [FRONT END VUE JS](https://github.com/mateus-gotardi/data-spector-300-vue) de acordo com a explicação no Read me
