import streamlit as st
from simulados import simulados
import firebase_admin
import pandas as pd
from firebase_admin import credentials, db
from Betinho import Betinho 
import utils as pu
import plotly.express as px

# Inicializar

try:
    betinho = Betinho("start")
except:
    betinho = Betinho("get")
    
relational = pd.read_csv("relational.csv", sep=";")
flag = 0
st.title("Betinho Analisa")
st.write("Olá, esse é uma das etapas do projeto LUNA. Esse projeto tem como objetivo auxiliar os estudantes do projeto Herbert de Souza com os estudos e vestibulares.")
st.text("Para iniciar, acesse sua página")

cpf = st.text_input("Digite o seu CPF (Sem pontos ou traços):", help="Não use traços ou pontos.")
analise = st.button("Realizar análise")

if analise:
    identificador = relational.query(f"CPF == '{cpf}'")["ID"].iloc[0]
    data = pu.get_student_data(betinho.ref, identificador)
    
    st.subheader("Informações")
    st.write("Primeiro, pediremos que você confirme se as informações abaixo estão corretas sobre você! Caso encontre algum erro, por favor chamar o Jovi para correção :)")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"Nome: {data['nome']}")
        st.write(f"CPF: {data['cpf']}")   
        st.write(f"Turma: {data['Turma']} - {data['periodo']}'")
             
    with col2:
        st.write(f"Email: {data['email']}")
        st.write(f"Celular: {data['telefone']}") 
        st.write(f"Nascimento: {data['nascimento'].replace('-', '/')}")
    
    st.divider()

    tab1, tab2, tab3 = st.tabs(["Geral", "Simulados", "Plano"]) 

    with tab1:
        st.write("Analise Geral rápida do estudante:")

        assuntos, df, fig1, fig2 = pu.analyze(data)

        st.write("Assuntos que é necessário revisão (Com base em desempenho geral):")
        
        for assunto in assuntos.keys():
            st.subheader(f"{assunto}")

            for i, a in enumerate(assuntos[assunto]):
                if i < 6:
                    st.write(f"- {a}")

        st.subheader("Principais Erros:")

        st.write("Vamos verificar seus principais acertos e erros!")

        st.plotly_chart(fig1)
        st.write("Pra ajudar a interpretar: Quanto maiores as barras, mais acertos nesse tipo de conteúdo!")

        st.plotly_chart(fig2)
        st.write("Pra ajudar a interpretar: Quanto maiores as barras, mais erros nesse tipo de conteúdo!")

    with tab2:
        st.write("Área de verificação dos simulados: ")
        simulado = st.selectbox("Selecione o simulado", simulados.keys())

        acertos = data["Simulados"][simulado]["Acertos"]
        erros = pd.Series(data["Simulados"][simulado]["Erros"]).value_counts().reset_index()
        erros.columns = ["Assunto", "Quantidade"]

        st.write(f"Simulado: {simulado}")
        st.write(f"Total de acertos: {sum(list(acertos.values()))}/{len(data['Simulados'][simulado]['Gabarito'])}")

        st.divider()
        st.write("Para ajudar a entender, vamos ver alguns gráficos:")

        fig3 = px.bar(x=acertos.keys(), y=acertos.values(), color=acertos.values(), title="Número de Acertos por questão.", labels={"x": "Disciplinas", "y": "Acertos"})
        st.plotly_chart(fig3)

        table = pd.DataFrame({"Disciplina": acertos.keys(), "Acertos": acertos.values()})
        table

        fig3 = px.bar(erros, x="Assunto", y="Quantidade", color="Assunto", title="Seus principais erros no simulado", labels={"x": "Conteudos", "y":"Grau de erro"})
        st.plotly_chart(fig3)

    with tab3:
        st.write("Planejamento")

        st.write("Aguarde um pouco! Após domingo, essa aba estará disponível para vocês :)")  
    
# 
# if flag == 1:
#     desempenho_simulados, plano_estudo = st.tabs(["Simulados", "Plano de Estudo"])
#     st.selectbox("")