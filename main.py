#!/usr/bin/env python3
#
# zapy-simplied
# autor: José Eduardo de Souza Pimentel, 2023
# github/jespimentel
#
# !pip install requests pandas openpyxl
# Importação das bibliotecas necessárias

import re, requests, json
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfile


# Configurações do usuário
chave = '9ee3d61ed9bfc45a1d6f8208c638f5d1' # Chave pessoal de ipapi.com

features = ['Timestamp', 'Message Id', 'Sender', 'Recipients',
            'Group Id', 'Sender Ip', 'Sender Port','Sender Device', 
            'Type', 'Message Style', 'Message Size']

def escolhe_arquivo(title):
    """Seleciona o caminho do arquivo com caixa de diálogo Tkinter"""
    root = Tk()
    root.withdraw()
    caminho_do_arquivo = askopenfile(title=title)
    return(caminho_do_arquivo)

def gera_dicionario_da_mensagem(msg, features=features):
    """Gera o dicionário das mensagens tendo as 'features' como chaves"""
    elemento = {}
    for item in msg:
        for feature in features[::-1]:
            if feature in item:
                item = item.replace(feature, '')
                item = item.strip()
                if feature == 'Message Size':
                    item = item.split()
                    item = item[0]
                elemento[feature] = item
    return elemento 

caminho_do_arquivo = escolhe_arquivo('Selecione o arquivo texto...')

with open(f'{caminho_do_arquivo.name}', 'rb') as f:
    texto = f.read()

texto = texto.decode('utf-8', errors='ignore')
texto = re.sub('\s', ' ', texto)
texto = re.sub('\n', ' ', texto)
corte = '<->'
texto = texto.replace(features[0], corte + features[0])

mensagens = texto.split(corte)

lista_mensagens = [] 
for msg in mensagens:
    for feature in features[1:]:
        msg = msg.replace(feature, corte + feature)
    msg = msg.split(corte)
    lista_mensagens.append(msg)

lista_final = []
for msg in lista_mensagens:
    if 'Timestamp' not in msg[0]:
        continue
    else:
        # Adiciona o elemento como dicionário na lista final
        lista_final.append(gera_dicionario_da_mensagem(msg))

print(f'Foram encontradas {len(lista_final)} mensagens.')
print('--------------------------------')

# Criação do dataframe com as mensagens extraídas
df = pd.DataFrame(lista_final, columns=features)

# DF com Sender_IP
df_com_ips = df[df['Sender Ip'].notna()]
ips = df_com_ips['Sender Ip'].value_counts()
ips_lista = ips.index.to_list()

print(f'Foram encontrados {len(ips_lista)} IPs diversos.')
resposta = input('Deseja restringir a consulta à API? <s/n> ')
if resposta.lower() == 's':
  cond = True
  while (cond):
    num = input ('Qtde. consultas: ')
    if num.isdigit() and int(num)>0 and int(num)<=len(ips_lista):
      cond = False
      num = int(num)
      ips_lista = ips_lista[:num]

# Consulta à API da IPAPI
# Cria a lista com as informações de IP obtidas nas requisições
# Documentação da API: https://ipapi.com/quickstart 

operadoras = []
for ip in ips_lista:
  elemento = {}
  try:
    dados = requests.get (f'http://api.ipapi.com/api/{ip}?access_key={chave}&hostname=1')
    dados_json = json.loads(dados.content)
    elemento = {'ip': dados_json['ip'], 'hostname' : dados_json['hostname'], 'latitude': dados_json['latitude'], 
              'longitude': dados_json['longitude'],'city': dados_json['city'], 'region_name': dados_json['region_name']}
    operadoras.append(elemento)
  except:
    resposta = 'API s/ resp.'
    elemento = {'ip': ip, 'hostname' : resposta, 'latitude': resposta, 'longitude': resposta,'city': resposta, 'region_name': resposta}
    operadoras.append(elemento)

# Criação do dataframe de operadoras com os dados obtidos da API
df_operadoras = pd.DataFrame(operadoras)

# Merge de df com df_operadoras
merged = pd.merge(df, df_operadoras, how='outer', left_on = 'Sender Ip', right_on = 'ip')
merged = merged.drop(columns='ip', axis=1)
merged = merged.set_index('Timestamp')

# Criação de planilha Excel para resumir o trabalho

print('Gravando a planilha...')
with pd.ExcelWriter('resumo.xlsx') as writer:
    merged.to_excel(writer, sheet_name='Geral')
print('Planilha gerada.')