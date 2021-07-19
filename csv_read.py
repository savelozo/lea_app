# -*- coding: utf-8 -*-

import csv

def read_csv():
    with open("Clase 1.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        #Lista con tuplas (correctas, total)
        list_students = list()

        for row in csv_reader:
            list_students.append(row[1])

        return list_students

def read_csv_2():
    with open("Asistencia obra Ballet.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        f = open("Asistencia Ballet.csv", "a")
        for row in csv_reader:
            f.write("{},{}\n".format(row[2],row[5]))
        f.close()
