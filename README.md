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

# Setup do Projeto na sua máquina
 Tenha certeza que possui Python intalado.
 Clone ou baixe o repositório e rode o ambiente virtual utilizando
  
```sh
venv\Scripts\activate
```
### Rode o servidor
utilize o comando
```sh
python app.py
```
o App deve estar rodando em http://localhost:5000
rode o [FRONT END VUE JS](https://github.com/mateus-gotardi/data-spector-300-vue) de acordo com a explicação no Read me