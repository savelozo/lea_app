from .models import Alumne, EnsayoAlumneRelation, Curso, ArtAlumneRelation
import random
from datetime import datetime

def make_distribution(students, art, canvas_course, assignment_id, int_arts_assigned, date):
    #Generación de grupos para peer review
    #First group son las personas que deben realizar el ensayo

    course = Curso.objects.get(id_canvas=canvas_course.id)

    if int_arts_assigned % 2 == 0:            
        print("Realizando repartición aleatorio. Armando grupos...")
        nsample = len(students) // 2
        first_group = random.sample(students, nsample)

        #BORRAR LA LÍNEA DE ABAJO!
        #EnsayoAlumneRelation.objects.all().delete()

        for student in students:
            student_bd = Alumne.objects.get(canvas_id=student.id)
            if student in first_group:                
                student_bd.last_group = 1
                f = open(("{} - grupo1.csv".format(art)), "a")
                f.write("{}\n".format(student_bd.nombre))
                f.close()
                ArtAlumneRelation.objects.create(curso=course, alumne=student_bd, arte=art, group=1)
            else:
                student_bd.last_group = 2
                f = open(("{} - grupo2.csv").format(art), "a")
                f.write("{}\n".format(student_bd.nombre))
                f.close()
                ArtAlumneRelation.objects.create(curso=course, alumne=student_bd, arte=art, group=2)
            student_bd.save()
                        
    else:
        print("Respetar grupo anterior. Repartir ensayo a grupo 2...")
        first_group = list()
        for student in students:
            student_bd = Alumne.objects.get(canvas_id=student.id)
            if student_bd.last_group == 2:
                first_group.append(student)
                f = open(("{} - grupo1.csv".format(art)), "a")
                f.write("{}\n".format(student_bd.nombre))
                f.close()
                student_bd.last_group=1
                student_bd.save()
                ArtAlumneRelation.objects.create(curso=course, alumne=student_bd, arte=art, group=1)
            else:
                f = open(("{} - grupo2.csv").format(art), "a")
                f.write("{}\n".format(student_bd.nombre))
                f.close()
                student_bd.last_group=2
                student_bd.save()
                ArtAlumneRelation.objects.create(curso=course, alumne=student_bd, arte=art, group=2)
                    
    create_assignment_override(first_group, canvas_course, art, assignment_id, date)

def create_assignment_override(students, course, art, assignment_id, date):
    #Asigna las tareas a los estudiantes del grupo 1
    list_students_id = list()

    for student in students:
        list_students_id.append(student.id)

    users_ids = {"student_ids": list_students_id}
    print("Assignment ID: {}".format(assignment_id))
    assignment = course.get_assignment(assignment_id)
    assignment.create_override(assignment_override=users_ids)
    assignment.edit(assignment={ "turnitin_enabled" : True,
                                 "due_at": date,
                                 "lock_at": date,
                                 "only_visible_to_overrides": True})
    print("Ensayo asignado")
    #send_message(art, curso.semestre)

def peer_review_distribution(canvas_course, art, assignment_id, date, max_reviews=2):
    #https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index
    assignment = canvas_course.get_assignment(assignment_id)
    group_id = canvas_course.create_assignment_group(name="Revisión entre pares {}".format(art.nombre)).id
    submissions = assignment.get_submissions()
    course = Curso.objects.get(id_canvas=canvas_course.id)
    list_submissions = list()

    for submission in submissions:
        list_submissions.append(submission)

    # students_canvas = canvas_course.get_users(enrollment_type=['student'])
    # for student in students_canvas:
    #     if student.name in students_group_2:
    #         student_bd = Alumne.objects.get(nombre=student.name)
    #         student_bd.last_group=2
    #         student_bd.save()

    reviewers = Alumne.objects.filter(last_group=2)
    #reviewers_2 debería reemplazar a reviewers
    reviewers_2 = ArtAlumneRelation.objects.filter(curso=course, arte=art, group=2)
    
    set_1 = list()
    set_2 = list()
    sent_messages = list()
    reviews = dict()
    urls_students = dict()

    for i in range(max_reviews):

        for student in reviewers:

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
                    
                    reviewed = canvas_course.get_user(random_subm.user_id).name
                    reviewed_bd = Alumne.objects.get(canvas_id=random_subm.user_id)
                    
                    if reviewed not in reviews.keys():                        
                        reviews[reviewed] = [student]                        
                        create_peer_review(canvas_course, random_subm, student, date, urls_students, art, reviewed_bd, group_id)
                        
                        f = open(("{} - Correcciones.csv").format(art.nombre), "a")
                        f.write("Corregide: {}, Corrector/a: {}\n".format(reviewed, student.nombre))
                        f.close()

                        f = open(("{} - URLS Grupo 1.csv").format(art.nombre), "a")
                        f.write("{},{}\n".format(reviewed, random_subm.attachments[0]['url']))
                        f.close()

                    else:
                        if student not in reviews[reviewed]:                            
                            reviews[reviewed].append(student)
                            create_peer_review(canvas_course, random_subm, student, date, urls_students, art, reviewed_bd, group_id)
                            # if student not in sent_messages:
                            #     canvas_course.create_conversation(recipients=[student.canvas_id], subject= "Peer review", body= ("Estimade:\n\nSe ha realizado la asignación respectiva a la evaluación de pares de la entrega de {}.\n\nFavor revisar sección Tareas\n\nSaludos cordiales, Sebastián.").format(art.nombre))
                            #     sent_messages.append(student)
                            f = open(("{} - Correcciones.csv").format(art.nombre), "a")
                            f.write("Corregide: {}, Corrector/a: {}\n".format(reviewed, student.nombre))
                            f.close()

                        else:
                            #Se devuelve a la lista cuando sale repetido
                            set_1.append(random_subm)

                except:
                    student = canvas_course.get_user(random_subm.user_id).name
                    print("{} no entregó su tarea".format(student))

def create_peer_review(canvas_course, random_subm, student, date, url, art, reviewed, group_id=None):
    
    course = Curso.objects.get(id_canvas=canvas_course.id)
    user_id = {"student_ids":[student.canvas_id]}
    assignment = { "name": ("Peer review {}").format(art.nombre),
                    "submission_types": ["online_text_entry"],
                    "description": "Revisa la tarea de tu compañere en el siguiente formulario:  https://forms.gle/fWLeCzA2WE73mbxu9.\nRecuerda ingresar con tu correo UC.\nEl ensayo a revisar podrás encontrarlo en el siguiente link (ojo! este link debes pegarlo en el form que te mandamos): {}\nAdemás de llenar el formulario, copia y pega cada una de las secciones en el cuadro de respuesta de canvas :) (solo para tener un respaldo)".format(random_subm.attachments[0]['url']),
                    'due_at': date,
                    'lock_at': date,
                    'assignment_group_id': group_id,
                    "only_visible_to_overrides": True }

    new_assignment = canvas_course.create_assignment(assignment=assignment)
    new_assignment.create_override(assignment_override=user_id)
    new_assignment.edit(assignment={'published': True})

    try:
        essay_relation = EnsayoAlumneRelation.objects.filter(curso=course, corregido__canvas_id=reviewed.canvas_id, arte__nombre=art.nombre)
        has_reviewed = True
    except:
        essay_relation = EnsayoAlumneRelation.objects.create(curso=course, corregido=reviewed, arte=art, url=random_subm.attachments[0]['url'])
        essay_relation.save()
        has_reviewed = False

    if has_reviewed:
        essay_relation.corrector_id_1 = student.canvas_id
    else:
        essay_relation.corrector_id_2 = student.canvas_id