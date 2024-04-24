import firebase_admin
from firebase_admin import credentials, db

import pandas as pd
import statistics as stats

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go

from simulados import simulados

class Betinho():

    def __init__(self, mode):
        self.name = "Betinho"
        self.mode = mode
        self.initialize()

    def initialize(self):
        if self.mode == "start":
            try:
                cred = credentials.Certificate("key2.json")
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://crudherbert-default-rtdb.firebaseio.com',
                    #'storageBucket': 'gs://herbert2024-be557.appspot.com'
                }) 
            except:
                cred = credentials.Certificate("key2.json")
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://crudherbert-default-rtdb.firebaseio.com',
                    #'storageBucket': 'gs://herbert2024-be557.appspot.com'
                }, name="Secundary")
        elif self.mode == "get":
            firebase_admin.get_app()

        self.ref = db.reference("/students")
