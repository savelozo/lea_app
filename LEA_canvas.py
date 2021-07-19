from canvasapi import Canvas
from csv_read import read_csv
from datetime import datetime
from bs4 import BeautifulSoup
import pdfkit
import random
import csv

API_URL = "https://cursos.canvas.uc.cl"

API_KEY = "8976~0g11w22i7QTuQPE2nJKKYrgMNzsX4OPGa5TifdyGbWLXz2te5aPQ5SD5WgQeGpVM"

CANVAS = Canvas(API_URL, API_KEY)

course = CANVAS.get_course(30298)
students = course.get_users(enrollment_type=['student'])
list_students = list()
students_ids = dict()
students_names = dict()
dict_students = dict()
asistentes = list()

for student in students:
    students_ids[student.name] = student.id
    students_names[student.id] = student.name
    dict_students[student.sortable_name] = student
    list_students.append(student)
    
#Realiza distibución de dos grupos. Recibe lista objetos de estudiantes asistentes
#La cantidad de alumnos que harán la tarea (nsample) y el nombre de la experiencia
def make_distribution(experience, semestre):

    nsample = len(list_students)//2
    first_group = random.sample(list_students, nsample)
    second_group = list()
    revisados = list()

    for student in list_students:
        if student not in first_group:
            f = open("{}/{}/{} - grupo2.csv".format(semestre, experience, experience), "a")
            f.write("{}\n".format(student.name))
            f.close()
        else:
            f = open("{}/{}/{} - grupo1.csv".format(semestre, experience, experience), "a")
            f.write("{}\n".format(student.name))
            f.close()

def create_assignment_override(experience, assignment_id, semestre):
    #Asigna las tareas a los estudiantes del grupo 1
    list_students = list()
    with open("{}/{}/{} - grupo1.csv".format(semestre, experience, experience), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for student in csv_reader:
            list_students.append(students_ids[student[0]])

    users_ids = {"student_ids": list_students}
    #new_assignment = course.get_assignment(assignment_id)
    #new_assignment.create_override(assignment_override=users_ids)
    #new_assignment.edit(assignment={'published': True})
    send_message(experience, semestre)

def send_message(experience, semestre, read_csv=False):
    #Envía mensaje de cada grupo de manera diferenciada.

    if not read_csv:
        id_revisados = list()
        id_revisores = list()
        with open("{}/{}/{} - grupo1.csv".format(semestre, experience, experience), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                id_revisados.append(students_ids[row[0]])

        with open("{}/{}/{} - grupo2.csv".format(semestre, experience, experience), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                id_revisores.append(students_ids[row[0]])

    msg_revisados = ("Estimades;\n\nLes escribo para informar que para la entrega de {} deberán generar un informe escrito. La asignación ya está realizada en la plataforma CANVAS.\n\n Cualquier duda no duden en escribirme, Sebastián.").format(experience)
    CANVAS.create_conversation(id_revisados, msg_revisados, subject="Entrega {}".format(experience))

    msg_revisores = ("Estimades;\n\nLes escribo para informar que para la entrega de {} deberán revisar 2 trabajos realizados por algunes de sus compañeres. La asignación se realizará la próxima semana en la plataforma CANVAS.\n\n Cualquier duda no dudes en escribirme, Sebastián.").format(experience)
    CANVAS.create_conversation(id_revisores, msg_revisores, subject="Entrega {}".format(experience))

def peer_review_distribution(assignment_name, assignment_id, max_reviews, day, month, year, hour, minutes):
    #https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index
    assignment = course.get_assignment(assignment_id)
    group_id = course.create_assignment_group(name="Revisión entre pares {}".format(assignment_name)).id
    submissions = assignment.get_submissions()
    list_submissions = list()

    for submission in submissions:
        list_submissions.append(submission)

    #Distribución de peer review
    f = open("2021-1/{}/peer_{}.csv".format(assignment_name, assignment_name), "a")
    f.write("nombre_corregido,nombre_correctores\n")
    f.close()

    with open("2021-1/{}/{} - grupo2.csv".format(assignment_name, assignment_name)) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        list_group2 = list()

        for row in csv_reader:
            if row[0] != "Nombres":
                list_group2.append(row[0])

    set_1 = list()
    set_2 = list()
    sent_messages = list()
    reviews = dict()
    urls_students = dict()

    for i in range(max_reviews):

        for student in list_group2:

            if student in students_ids:
                random_distribution =  True

                if len(list_submissions) > 0:
                    random_subm = list_submissions.pop(random.randrange(len(list_submissions)))
                    set_1.append(random_subm)
                elif len(set_1) > 0:
                    random_subm = set_1.pop(random.randrange(len(set_1)))
                    set_2.append(random_subm)
                else:
                    random_distribution = False

                if random_distribution:
                    try:
                        reviewed = course.get_user(random_subm.user_id).name
                        if reviewed not in reviews.keys():
                            reviews[reviewed] = [student]
                            user_id = {"student_ids":[students_ids[student]]}
                            assignment = { "name": ("Peer review {} - Ingrese sus argumentos en el cuadro de texto y la nota en la barra COMENTARIOS.").format(assignment_name),
                                            "submission_types": ["online_text_entry"],
                                            "description": "Revisa la tarea de tu compañere en el siguiente formulario:  https://forms.gle/fWLeCzA2WE73mbxu9.\nRecuerda ingresar con tu correo UC.\nEl ensayo a revisar podrás encontrarlo en el siguiente link (ojo! este link debes pegarlo en el form que te mandamos): {}\nAdemás de llenar el formulario, copia y pega cada una de las secciones en el cuadro de respuesta de canvas :) (solo para tener un respaldo)".format(random_subm.attachments[0]['url']),
                                            'due_at': datetime(year, month, day, hour, minutes),
                                            'lock_at': datetime(year, month, day, hour, minutes),
                                            'assignment_group_id': group_id,
                                            "only_visible_to_overrides": True }
                            new_assignment = course.create_assignment(assignment=assignment)
                            new_assignment.create_override(assignment_override=user_id)
                            new_assignment.edit(assignment={'published': True})
                            urls_students[random_subm.attachments[0]['url']] = student
                        else:
                            if student not in reviews[reviewed]:
                                reviews[reviewed].append(student)
                                user_id = {"student_ids":[students_ids[student]]}
                                assignment = { "name": ("Peer review {} - Ingrese sus argumentos en el cuadro de texto y la nota en la barra COMENTARIOS").format(assignment_name),
                                                "submission_types": ["online_text_entry"],
                                                "description": "Revisa la tarea de tu compañere en el siguiente formulario:  https://forms.gle/fWLeCzA2WE73mbxu9.\nRecuerda ingresar con tu correo UC.\nEl ensayo a revisar podrás encontrarlo en el siguiente link (ojo! este link debes pegarlo en el form que te mandamos): {}\nAdemás de llenar el formulario, copia y pega cada una de las secciones en el cuadro de respuesta de canvas :) (solo para tener un respaldo)".format(random_subm.attachments[0]['url']),
                                                'due_at': datetime(year, month, day, hour, minutes),
                                                'lock_at': datetime(year, month, day, hour, minutes),
                                                'assignment_group_id': group_id,
                                                "only_visible_to_overrides": True }
                                new_assignment = course.create_assignment(assignment=assignment)
                                new_assignment.create_override(assignment_override=user_id)
                                new_assignment.edit(assignment={'published': True})
                                urls_students[random_subm.attachments[0]['url']] = student

                                if student not in sent_messages:
                                    CANVAS.create_conversation(recipients=[students_ids[student]], subject= "Peer review", body= ("Estimade:\n\nSe ha realizado la asignación respectiva a la evaluación de pares de la entrega de {}.\n\nFavor revisar sección Tareas\n\nSaludos cordiales, Sebastián.").format(assignment_name))
                                    sent_messages.append(student)

                            else:
                                #Se devuelve a la lista cuando sale repetido
                                set_1.append(random_subm)

                    except:
                        student = course.get_user(random_subm.user_id).name
                        print("{} no entregó su tarea".format(student))

    for reviewed in reviews:
        f = open("2021-1/{}/peer_{}.csv".format(assignment_name, assignment_name), "a")
        f.write("{},{}\n".format(reviewed, reviews[reviewed]))
        f.close()

    for url in urls_students:
        f = open("2021-1/{}/urls_students_{}.csv".format(assignment_name, assignment_name), "a")
        f.write("{},{}\n".format(url, urls_students[url]))
        f.close()

def make_redistribution(experience, assignment_id, day, month, year, hour, minutes):

    #Diccionario con llave corregido y valor correctores dict[corrector] = lista corregidos
    revisiones = dict()

    original_asignment = course.get_assignment(assignment_id)
    dict_original_submissions = dict()
    original_submissions = original_asignment.get_submissions()

    for submission in original_submissions:
        try:
            dict_original_submissions[submission.user_id] = submission.attachments[0]['url'].split("=")[-1]
        except:
            pass

    with open("{}/peer_{}.csv".format(experience, experience), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line = 0
        for row in csv_reader:
            if line:
                if row[1] == row[-1]:
                    #Caso con un solo corrector
                    complete_row = row[1]
                else:
                    complete_row = row[1] + row[-1]
                revisores = complete_row.strip('][').split('\' \'')
                for revisor in revisores:
                    revisor = revisor.replace('\'', "")
                    if revisor in revisiones.keys():
                        revisiones[revisor].append(row[0])
                    else:
                        revisiones[revisor] = [row[0]]
            line += 1

    assignments = course.get_assignments()
    group_id = course.create_assignment_group(name="Recorrección notas {}".format(experience)).id
    sent_messages = list()

    counter = 1
    for assignment in assignments:
        if "Peer review {}".format(experience).lower() in assignment.name.lower():
            submissions = assignment.get_submissions(include=['submission_comments'])

            for submission in submissions:

                try:
                    if len(submission.submission_comments) > 0:
                        argumentos = submission.body
                        nota = submission.submission_comments[-1]['comment']
                        revisados = revisiones[students_names[submission.user_id]]
                        for revisado in revisados:
                            if revisado in students_ids:

                                if dict_original_submissions[students_ids[revisado]] in assignment.description.split("=")[-1].strip('</p>') or assignment.description.split("=")[-1].strip('</p>') in dict_original_submissions[students_ids[revisado]]:
                                    user_id = {"student_ids":[students_ids[revisado]]}
                                    _assignment = { "name": ("Recorrección {} - Ingrese sus argumentos en el cuadro de texto y la nota en la barra COMENTARIOS").format(experience),
                                                    "submission_types": ["online_text_entry"],
                                                    "description": "NOTA: {}\n\nARGUMENTOS: {}".format(nota, argumentos),
                                                    'due_at': datetime(year, month, day, hour, minutes),
                                                    'lock_at': datetime(year, month, day, hour, minutes),
                                                    'assignment_group_id': group_id,
                                                    "only_visible_to_overrides": True }
                                    new_assignment = course.create_assignment(assignment=_assignment)
                                    new_assignment.create_override(assignment_override=user_id)
                                    new_assignment.edit(assignment={'published': True})

                                    if students_ids[revisado] not in sent_messages:
                                        CANVAS.create_conversation(recipients=[students_ids[revisado]], subject= "Corrección Peer Review", body= ("Estimade:\n\nSe ha realizado la asignación respectiva a la corección de las evaluaciones de pares de la entrega de {}.\n\nFavor revisar sección Tareas\n\nSaludos cordiales, Sebastián.").format(experience))
                                        sent_messages.append(students_ids[revisado])

                    else:
                        argumentos = submission.body
                        revisados = revisiones[students_names[submission.user_id]]
                        for revisado in revisados:
                            if revisado in students_ids:
                                if dict_original_submissions[students_ids[revisado]] in assignment.description.split("=")[-1].strip('</p>'):
                                    user_id = {"student_ids":[students_ids[revisado]]}
                                    _assignment = { "name": ("Recorrección {} - Ingrese sus argumentos en el cuadro de texto y la nota en la barra COMENTARIOS").format(experience),
                                                    "submission_types": ["online_text_entry"],
                                                    "description": "NOTA y ARGUMENTOS: {}".format(argumentos),
                                                    'due_at': datetime(year, month, day, hour, minutes),
                                                    'lock_at': datetime(year, month, day, hour, minutes),
                                                    'assignment_group_id': group_id,
                                                    "only_visible_to_overrides": True }
                                    new_assignment = course.create_assignment(assignment=_assignment)
                                    new_assignment.create_override(assignment_override=user_id)
                                    new_assignment.edit(assignment={'published': True})
                except:
                    print("Entrega atrasada enviada por mail de {}".format(revisado))

def asistencia(experience, n_class):
    #Experiencie, string con el nombre de la disciplina artística donde se desea revisar la asistencia.
    #n_class, número de clase; donde 1 es clase teórica y 2 es clase práctica.

    asistentes = list()

    with open("{}/Asistencia/Asistencia {} {}.csv".format(experience, experience, n_class), 'r') as csv_file:
        #Recorre el csv obtenido desde el form de asistencia y recolecta los mails.
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if row[2].lower() not in asistentes:
                asistentes.append(row[1].lower())

    with open("lista estudiantes.csv".format(experience, experience), 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            if row[2][1:].lower() in asistentes:
                if n_class == 1:
                    f = open("{}/Asistencia/Clase {} Teórica - Asistentes.csv".format(experience, experience), "a")
                else:
                    f = open("{}/Asistencia/Clase {} Práctica - Asistentes.csv".format(experience, experience), "a")
                f.write("{} {}\n".format(row[1][1:], row[0]))
                f.close()

def get_grades(experience):

    assignments = course.get_assignments()

    url_submits = dict()
    submits = dict()

    for assignment in assignments:
        description = assignment.description

        if "{}".format(experience).lower() in assignment.name.lower() and "entrega" in assignment.name.lower():
            submissions = assignment.get_submissions()

            for submission in submissions:
                try:
                    if submission.attachments[0]['url'].split("=")[-1] is not None:
                        url_submits[submission.attachments[0]['url'].split("=")[-1]] = {"user_id": submission.user_id}
                except:
                    print("Sin entrega de {}".format(students_names[submission.user_id]))

        elif "Peer review {}".format(experience).lower() in assignment.name.lower():

            for url in url_submits.keys():
                if url in description:

                    if "Peer 1" not in url_submits[url].keys():
                        peer = 1
                    else:
                        peer = 2

                    submissions = assignment.get_submissions(include=['submission_comments'])
                    #ID URL de entrega
                    for submission in submissions:
                        if len(submission.submission_comments) > 0:
                            grade = submission.submission_comments[0]['comment']
                            student = students_names[submission.user_id]
                            arguments = BeautifulSoup(submission.body).get_text()
                            url_submits[url]["Peer {}".format(peer)] = {'grade': grade,'student': student, 'arguments': arguments}
                        else:
                            grade = "No puso comentarios"
                            student = students_names[submission.user_id]
                            if submission.body is None:
                                arguments = "SIN REVISIÓN"
                            else:
                                arguments = BeautifulSoup(submission.body).get_text()
                            url_submits[url]["Peer {}".format(peer)] = {'grade': grade,'student': student, 'arguments': arguments}

        # elif "Recorrección".format(experience).lower() in assignment.name.lower() and "{}".format(experience).lower() in assignment.name.lower():
        #
        #     peer = None
        #     for _url in url_submits.keys():
        #         if "Peer 1" in url_submits[_url].keys():
        #             if url_submits[_url]["Peer 1"]["arguments"] in BeautifulSoup(description).get_text():
        #                 peer = 1
        #                 url = _url
        #             elif "Peer 2" in url_submits[_url].keys():
        #                 if url_submits[_url]["Peer 2"]["arguments"] in BeautifulSoup(description).get_text():
        #                     peer = 2
        #                     url = _url
        #
        #     if peer is not None:
        #         submissions = assignment.get_submissions(include=['submission_comments'])
        #
        #         for submission in submissions:
        #             if len(submission.submission_comments) > 0:
        #                 grade = submission.submission_comments[0]['comment']
        #                 student = students_names[submission.user_id]
        #                 arguments = BeautifulSoup(submission.body).get_text()
        #                 url_submits[url]["Recorrección {}".format(peer)] = {'grade': grade, 'student': student, 'arguments': arguments}


    f = open("2021-1/{}/{} - Resumen Respuestas.csv".format(experience, experience), "a")
    for url in url_submits:
        f.write("REVISADE: {}\n".format(students_names[url_submits[url]["user_id"]]))
        if "Peer 1" in url_submits[url].keys():
            f.write("PEER 1: {}\n".format(url_submits[url]["Peer 1"]["arguments"]))
            f.write("REVISOR 1: {}\n".format(url_submits[url]["Peer 1"]["student"]))
            f.write("NOTA PEER 1: {}\n".format(url_submits[url]["Peer 1"]["grade"]))
            f.write("\n")

            # if "Recorrección 1" in url_submits[url].keys():
            #     f.write("RECORRECCIÓN 1: {}\n".format(url_submits[url]["Recorrección 1"]["arguments"]))
            #     f.write("NOTA RECORRECCIÓN 1: {}\n".format(url_submits[url]["Recorrección 1"]["grade"]))
            #     f.write("\n")
            # else:
            #     f.write("SIN RECORRECCIÓN 1")
            #     f.write("\n")

        else:
            f.write("SIN PEER 1")
            f.write("\n")

        if "Peer 2" in url_submits[url].keys():
            f.write("PEER 2: {}\n".format(url_submits[url]["Peer 2"]["arguments"]))
            f.write("REVISOR 2: {}\n".format(url_submits[url]["Peer 2"]["student"]))
            f.write("NOTA PEER 2: {}\n".format(url_submits[url]["Peer 2"]["grade"]))
            f.write("\n")

            # if "Recorrección 2" in url_submits[url].keys():
            #     f.write("RECORRECCIÓN 2: {}\n".format(url_submits[url]["Recorrección 2"]["arguments"]))
            #     f.write("NOTA RECORRECCIÓN 2: {}\n".format(url_submits[url]["Recorrección 2"]["grade"]))
            #     f.write("\n")
            # else:
            #     f.write("SIN RECORRECCIÓN 2: {}\n")
            #     f.write("\n")

        else:
            f.write("SIN PEER 2")
            f.write("\n")

        f.write("\n")
        f.write("------------------------------------------------------------------------------")
        f.write("\n")

    f.close()

if __name__ == "__main__":
    #make_distribution("Ópera", "2021-1")
    #create_assignment_override("Cine", 141890, "2021-1")
    #peer_review_distribution("Cine",141890,2,26,5,2021,23,59)
    #send_message("Arquitectura", "2020-2")
    #make_redistribution("Poesía",22167,14,7,2020,23,59)
    #get_grades("Poesía")
    assignment = course.get_assignment(153971)
    submissions = assignment.get_submissions()
    print(submissions.__dict__)

    for submission in submissions:
        print(submission)

#Problemas a solucionar: ¿Qué pasa cuando alguien bota el ramo?¿Qué pasa cuando a alguien le dan el ramo?
