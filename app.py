# IMPORTANDO OS PACOTES
import pandas as pd
from flask import Flask
from flask import render_template
from flask import request

#FUNÇÂO MINIMAL APPLICATION
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    total = carregar_total()
    total_top4 = carregar_top4_horas()
    total_bottom4 = carregar_bottom4_horas()
    total_estacao = carregar_estacao()
    return render_template("index.html", total= total, total_top4= total_top4, total_bottom4= total_bottom4, total_estacao= total_estacao)

@app.route("/filtros", methods=["GET"])
def ativar_filtros():
    ano = int(request.args.get('ano')) if len(request.args.get('ano'))>0 else None
    mes = int(request.args.get('mes')) if len(request.args.get('mes'))>0 else None
    total = carregar_total(ano, mes)
    total_top4 = carregar_top4_horas(ano, mes)
    total_bottom4 = carregar_bottom4_horas(ano, mes)
    total_estacao = carregar_estacao()
    return render_template("index.html", total= total, total_top4= total_top4, total_bottom4= total_bottom4, total_estacao= total_estacao)

#FUNÇÃO PARA CAREREGAR OS DADOS
def carregar_dados(ano=None, mes=None):
  df = pd.read_csv("https://pycourse.s3.amazonaws.com/bike-sharing.csv")
  if ano is not None:
    df = df[df["year"] == ano]
  if mes is not None:
    df = df[df["month"] == mes]
  return df

#FUNÇÃO PARA OS TOTALIZADORES DE LOCAÇÕES
def carregar_total(ano=None, mes=None):
  df = carregar_dados(ano, mes)
  total= sum(df["total_count"])
  total11 = df.loc[df['year'] == 0,['total_count']].sum(axis=0)
  total12 = df.loc[df['year'] == 1,['total_count']].sum(axis=0)
  return [
  {"title": "Locações", "total": total},   
  {"title": "Locações em 2011", "total": total11},
  {"title": "Locações em 2012", "total": total12},
  ]

#FUNÇÃO PARA CALCULAR AS MAIORES MÉDIA DE LOCAÇÕES POR HORÁRIO
def carregar_top4_horas(ano=None, mes=None):
    df = carregar_dados(ano, mes)
    df2= df.copy()
# Agrupa média de locações por horário do dia:
    df2 = df2.groupby('hour')['total_count'].mean()
    df2 = pd.DataFrame(df2)
    df2['hour'] = df2.index
# Ordenar horários de locações pela média, maior -> menor:
    df2_sort = df2.sort_values(by= "total_count", ascending=False)
# Top 4 horários com maiores locações:
    df2_top4 = round(df2_sort.head(4), 2)
    cols = ['hour', 'total_count']
    df2_top4 = df2_top4[cols]
    df2_top4.rename(columns={'total_count': 'media'}, inplace = True)
# Converte o dataframe em um dicionário Python:
    top4 = df2_top4.to_dict("records")
    count= 1
    for item in top4:
        item['indice']= count
        count +=1
    return top4

#FUNÇÃO PARA CALCULAR AS MENORES MÉDIA DE LOCAÇÕES POR HORÁRIO
def carregar_bottom4_horas(ano=None, mes=None):
    df = carregar_dados(ano, mes)
    df2= df.copy()
# Agrupa média de locações por horário do dia:
    df2 = df2.groupby('hour')['total_count'].mean()
    df2 = pd.DataFrame(df2)
    df2['hour'] = df2.index
# Ordenar horários de locações pela média, menor -> maior:
    df2_sort = df2.sort_values(by= "total_count", ascending=True)
# Top 4 horários com maiores locações:
    df2_bottom4 = round(df2_sort.head(4), 2)
    cols = ['hour', 'total_count']
    df2_bottom4 = df2_bottom4[cols]
    df2_bottom4.rename(columns={'total_count': 'media'}, inplace = True)
# Converte o dataframe em um dicionário Python:
    bottom4 = df2_bottom4.to_dict("records")
    count= 1
    for item in bottom4:
        item['indice']= count
        count +=1
    return bottom4

#FUNÇÃO PARA CALCULAR A MÉDIA DE LOCAÇÕES POR ESTAÇÃO
def carregar_estacao(ano=None, mes=None):
    df = carregar_dados(ano, mes)
    df2= df.copy()
# Agrupa média de locações por estações do ano:
    df2 = df2.groupby('season')['total_count'].mean()
    df2 = pd.DataFrame(df2)
    df2['season'] = df2.index
# Ordenar horários de locações pela média, maior -> menor:
    df2_sort = df2.sort_values(by= "total_count", ascending=False)
# Estações com maiores locações:
    df2_estacao = round(df2_sort.head(), 2)
    cols = ['season', 'total_count']
    df2_estacao = df2_estacao[cols]
    df2_estacao.rename(columns={'total_count': 'media'}, inplace = True)
# Converte o dataframe em um dicionário Python:
    estacao = df2_estacao.to_dict("records")
    count= 1
    for item in estacao:
        item['indice']= count
        count +=1
    return estacao