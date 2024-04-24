import pandas as pd
import plotly.express as px

def analyze(student):
    df, erros = identifyNotas(student)
    #assuntos = getAssuntos(df)
    #df_deficts = getDeficts(df)
    #fig1, fig2 = getFigs(df)
    return df, erros

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
    simulados = student["Simulados"].keys()
    
    disciplinas_dict = {}
    erros_list = []

    for simulado in simulados:
        disciplinas = student["Simulados"][simulado]["Acertos"].keys()
        for disciplina in disciplinas:
            if disciplina not in disciplinas_dict.keys():
                disciplinas_dict[disciplina] = student["Simulados"][simulado]["Acertos"][disciplina]
            else:
                disciplinas_dict[disciplina] += student["Simulados"][simulado]["Acertos"][disciplina]
        erros_list.extend(student["Simulados"][simulado]["Erros"])

    df = pd.DataFrame({"Disciplinas": disciplinas_dict.keys(), "Acertos": disciplinas_dict.values()})
    erros = pd.DataFrame({"Conteudo": erros_list})
    erros = erros["Conteudo"].value_counts().reset_index()
    erros.columns = ["Conteudo", "Quantidade"]
    return df, erros

def get_student_data(ref, student_id):
    
    #student_ref = ref.child(student_id)
    student_data = ref[student_id]
    # student_data = student_ref.get()

    return student_data