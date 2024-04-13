import pandas as pd
import plotly.express as px

def analyze(student):
    df = identifyNotas(student)
    assuntos = getAssuntos(df)
    df_deficts = getDeficts(df)
    fig1, fig2 = getFigs(df)

    return assuntos, df_deficts, fig1, fig2

def getFigs(df):
    fig1 = px.bar(df, x="Assunto", y="Acertos", color="Disciplina", title="Acertos por conteudo")
    fig2 = px.bar(df, x="Assunto", y="Erros", color="Disciplina", title="Erros por conteudo")
    return fig1, fig2

def getPlans(deficts):

    disciplinas = list(deficts["Disciplina"])

    if "Matemática" in disciplinas:
        plan = ""


    return

def getAssuntos(df):
    df = df.query("Erros != 0 and Erros > Acertos").sort_values(by="Erros", ascending=False)
    data = {}
    for i in range(0, 10):
        try:
            row = df.iloc[i]
            if row["Acertos"] * 2 <= row["Erros"]:
                if row["Disciplina"] not in data.keys():
                    data[row["Disciplina"]] = [row["Conteudo"]]
                else:
                    data[row["Disciplina"]].append(row["Conteudo"])
        except:
            continue
        
    return data

def getDeficts(df):
    df = df.query("Erros != 0 and Erros > Acertos")

    return df

def identifyNotas(student):
    desempenho = student["desempenho"]
    disciplina_list = []
    assunto_list = []
    content_list = []
    erros = []
    acertos = []
    
    for disciplina in desempenho.keys():
        for assunto in desempenho[disciplina].keys():
            for content in desempenho[disciplina][assunto].keys():
                try:
                    acerto = desempenho[disciplina][assunto][content]["Acertos"]
                    erro = desempenho[disciplina][assunto][content]["Erros"]

                    disciplina_list.append(disciplina)
                    assunto_list.append(assunto)
                    content_list.append(content)
                    erros.append(erro)
                    acertos.append(acerto)
                except:
                    continue

    df = pd.DataFrame({"Disciplina": disciplina_list, "Assunto": assunto_list, "Conteudo": content_list, "Acertos": acertos, "Erros": erros})
    df["Acertos"] = df["Acertos"] / 3
    df["Erros"] = df["Erros"] / 3

    return df

def get_student_data(ref, student_id):
    student_ref = ref.child(student_id)
    
    student_data = student_ref.get()

    return student_data