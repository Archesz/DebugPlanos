
import streamlit as st
from simulados import simulados
import firebase_admin
import pandas as pd
from firebase_admin import credentials, db
from Betinho import Betinho 
import utils as pu
import plotly.express as px
import plotly.graph_objects as go

import json

msg = ""
n = 1

with open('alunos_atualizados.json', 'r', encoding="utf-8") as arquivo:
    # Carregar os dados do arquivo JSON
    dados = json.load(arquivo)

relational = pd.read_csv("relational.csv", sep=";")


cpf = st.text_input("Digite o seu CPF (Sem pontos ou traços):", help="Não use traços ou pontos.")
simulado = st.selectbox("Selecione o simulado", ["Colmeias_Inicial", "Unicamp_00001"])

if simulado == "Unicamp_00001":
    msg = "Atenção! As provas podem ter 3 questões de física diferentes! As últimas 3 de Física devem ser conferidas manualmente."
    n = 0

analise = st.button("Realizar análise")

if analise:
    identificador = relational.query(f"CPF == '{cpf}'")["ID"].iloc[0]
    # data = pu.get_student_data(betinho.ref, identificador)
    data = pu.get_student_data(dados, identificador)

    st.write(msg)
    st.divider()

    st.write("Área de verificação dos simulados: ")

    acertos = data["Simulados"][simulado]["Acertos"]
    erros = pd.Series(data["Simulados"][simulado]["Erros"]).value_counts().reset_index()
    erros.columns = ["Assunto", "Quantidade"]

    st.write(f"Simulado: {simulado}")
    st.write(f"Total de acertos: {data['Simulados'][simulado]['Acertos']['Total']}/{len(data['Simulados'][simulado]['Gabarito']) - n}")

    st.divider()
    st.write("Para ajudar a entender, vamos ver alguns gráficos:")

    fig3 = px.bar(x=acertos.keys(), y=acertos.values(), color=acertos.values(), title="Número de Acertos por Disciplina.", labels={"x": "Disciplinas", "y": "Acertos"})
    st.plotly_chart(fig3)

    table = pd.DataFrame({"Disciplina": acertos.keys(), "Acertos": acertos.values()})
    fig_table = go.Figure()

    # Adicionando a tabela
    fig_table.add_trace(go.Table(
        header=dict(values=["Disciplina", "Acertos"],
                    align='left'),
        cells=dict(values=[table["Disciplina"], table["Acertos"]],
                align='left')),
    )
    
    st.plotly_chart(fig_table, use_container_width=True)

    fig3 = px.bar(erros.sort_values(by="Quantidade"), x="Assunto", y="Quantidade", color="Assunto", title="Seus principais erros no simulado", labels={"x": "Conteudos", "y":"Grau de erro"})
    st.plotly_chart(fig3, use_container_width=True)

    st.write("Tabela com o Nível de Erro")
    st.write("Quanto maior o grau, mais importante seria rever o assunto :)")

    fig_table_2 = go.Figure()

    # Adicionando a tabela
    fig_table_2.add_trace(go.Table(
        header=dict(values=["Disciplina", "Grau de Erro"],
                    align='left'),
        cells=dict(values=[erros["Assunto"], erros["Quantidade"]],
                align='left')),
    )

    st.plotly_chart(fig_table_2, use_container_width=True)