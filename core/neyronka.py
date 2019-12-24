import csv

import numpy as np
from django.db import connection
from django.db.models import Count
from sklearn.linear_model import LinearRegression

from core.models import Repo


class CustomLinearRegression(object):

    def __init__(self):
        self._model = LinearRegression()

    def train(self):
        inputs = []
        outputs = []
        cursor = connection.cursor()
        cursor.execute("select creation_date, count(id) from core_repo where is_test = true group by creation_date;")

        for row in cursor.fetchall():
            inputs.append(int(row[0].strftime("%Y")))
            outputs.append(row[1])

        cursor.close()
        self._model.fit(np.array(inputs).reshape((-1, 1)), np.array(outputs))

    def predict(self, year):
        return int(self._model.predict(np.array([year]).reshape((-1, 1)))[0])