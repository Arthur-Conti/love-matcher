from flask import Flask, render_template, request
import requests
import json
import pandas as pd

app = Flask(__name__,  static_folder='static', static_url_path='/static')

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/postar', methods=['POST',])   # recebendo os dados do formulário via POST     
def dados():      
    pessoa1 = request.form['p1']
    pessoa2 = request.form['p2']
    
    url = "https://love-calculator.p.rapidapi.com/getPercentage"

    querystring = {"sname":pessoa1,"fname":pessoa2}

    headers = {
        "X-RapidAPI-Key": "22d0035b4bmshff583fcca809ee4p18e8c1jsn6b4764df2dd7",
        "X-RapidAPI-Host": "love-calculator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    data = response.text
    dict_data = json.loads(data)
    
    porcentagem = dict_data['fname'] + " e " + dict_data['sname'] + " tem " + dict_data['percentage'] + "% de compatibilidade"
    porcentagem_num = int(dict_data['percentage'])
    resultado = dict_data['result']
    
    if porcentagem_num <= 30:
        resultado = "Não é uma boa escolha 😢"
    elif porcentagem_num > 30 and porcentagem_num <= 50:
        resultado = "Pode escolher alguém melhor 😢"
    elif porcentagem_num > 50 and porcentagem_num <= 75:
        resultado = "Tudo de bom para o casal!"
    elif porcentagem_num > 75:
        resultado = "Parabéns, melhor escolha impossivel!"
        
    historico = []
    
    historico.append(porcentagem)
        
    arquivo = open('historico.csv', 'a+')
    for item in historico:
        arquivo.write(f'{item}\n')
    
    arquivo.close()
    
    df = pd.read_csv("historico.csv")

    historico = df.values.tolist()
    historico_limpo = []
    
    for item in historico:
        item = str(item)
        item_limpo = item.strip("['']")
        historico_limpo.append(item_limpo)
        
    return render_template('index.html', porcento = porcentagem, frase = resultado, historico=historico_limpo)

app.run()

