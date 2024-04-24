import streamlit as st
from simulados import simulados
import firebase_admin
import pandas as pd
from firebase_admin import credentials, db
from Betinho import Betinho 
import utils as pu
import plotly.express as px
import json

# Inicializar

# try:
#     betinho = Betinho("start")
# except:
#     betinho = Betinho("get")
    
with open('alunos_atualizados.json', 'r', encoding="utf-8") as arquivo:
    # Carregar os dados do arquivo JSON
    dados = json.load(arquivo)

relational = pd.read_csv("relational.csv", sep=";")
flag = 0

st.title("Betinho Analisa")
st.write("Olá, esse é uma das etapas do projeto LUNA. Esse projeto tem como objetivo auxiliar os estudantes do projeto Herbert de Souza com os estudos e vestibulares.")
st.text("Para iniciar, acesse sua página")

cpf = st.text_input("Digite o seu CPF (Sem pontos ou traços):", help="Não use traços ou pontos.")
analise = st.button("Realizar análise")

if analise:
    identificador = relational.query(f"CPF == '{cpf}'")["ID"].iloc[0]
    # data = pu.get_student_data(betinho.ref, identificador)
    data = pu.get_student_data(dados, identificador)
    st.write(f"Nome: {data['nome']}")
#     st.subheader("Informações")
#     st.write("Primeiro, pediremos que você confirme se as informações abaixo estão corretas sobre você! Caso encontre algum erro, por favor chamar o Jovi para correção :)")
# 
#     col1, col2 = st.columns(2)
# 
#     with col1:
#         st.write(f"Nome: {data['nome']}")
#         st.write(f"CPF: {data['cpf']}")   
#         st.write(f"Turma: {data['Turma']} - {data['periodo']}'")
#              
#     with col2:
#         st.write(f"Email: {data['email']}")
#         st.write(f"Celular: {data['telefone']}") 
#         st.write(f"Nascimento: {data['nascimento'].replace('-', '/')}")
    
    st.divider()


    st.write("Analise Geral rápida do estudante:")

    df, erros = pu.analyze(data)

    st.subheader("Acertos ao longo dos simulados")
    fig1 = px.bar(df.sort_values(by="Acertos"), x="Disciplinas", y="Acertos", title="Total de acertos por disciplina")
    st.plotly_chart(fig1)

    st.subheader("Principais Erros:")
    fig2 = px.bar(erros.sort_values(by="Quantidade"), x="Conteudo", y="Quantidade", title="Principais erros")
    st.plotly_chart(fig2)
    
# 
# if flag == 1:
#     desempenho_simulados, plano_estudo = st.tabs(["Simulados", "Plano de Estudo"])
#     st.selectbox("")
