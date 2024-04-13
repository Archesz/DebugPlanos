import pandas as pd
import utils as pu
import json

with open('students.json', 'r', encoding='utf-8') as arquivo:
    student = json.load(arquivo)

pu.analyze(student)
