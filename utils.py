import pandas as pd

def getInfos(student):
    print(f"Nome: {student['nome']}")
    print(f"Turma: {student['Turma']} - {student['periodo']}")
    print(f"Email: {student['email']}")
    print(f"Nascimento: {student['nascimento'].replace('-', '/')}")
    print(f"Curso: {student['Curso']}")
    
def analyze(student):
    key = list(student.keys())[0]
    student = student[key]
    getInfos(student)
    print("-"*50)
    df = identifyNotas(student)
    assuntos = getAssuntos(df)
    deficts = getDeficts(df)
    print(deficts)

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

    df["Score"] = df["Erros"] / df["Acertos"]

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