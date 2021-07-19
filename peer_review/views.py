from .models import Curso, Arte, Alumne
from .serializers import CursoSerializer, ArteSerializer, AlumneSerializer
from .functions import make_distribution, create_assignment_override, peer_review_distribution
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

import json
from canvasapi import Canvas
from datetime import datetime

API_URL = "https://cursos.canvas.uc.cl"

API_KEY = "8976~0g11w22i7QTuQPE2nJKKYrgMNzsX4OPGa5TifdyGbWLXz2te5aPQ5SD5WgQeGpVM"

CANVAS = Canvas(API_URL, API_KEY)

class PeerListCreate(generics.ListCreateAPIView):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class ArtListCreate(generics.ListCreateAPIView):
    queryset = Arte.objects.all()
    serializer_class = ArteSerializer

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Alumne.objects.all()
    serializer_class = AlumneSerializer

@api_view(('POST',))
def MakeAssigns(request):
    body_request = json.loads(request.body)
    print(body_request)

    if "course_id" in body_request:    
        course = Curso.objects.get(id_canvas=body_request['course_id'])
        canvas_course = CANVAS.get_course(course.id_canvas)
        students_canvas = canvas_course.get_users(enrollment_type=['student'])
        assignment_id = body_request["assignment_id"]
        date = datetime(body_request["year"], 
                        body_request["month"],
                        body_request["day"], 
                        body_request["hour"], 
                        body_request["minutes"])
        students = list()

        #Actualización de alumnes en la base de datos
        for student in students_canvas:
            students.append(student)
            _student = Alumne.objects.filter(canvas_id=student.id)
            if not len(_student):
                #Creación de alumne que no está en la base de datos
                Alumne.objects.create(nombre=student.name, curso=course, canvas_id=student.id)
        
        if body_request["title_task"] == "Repartir ensayo":
            art = course.artes.filter(nombre__contains=body_request['art'])
            if not len(art):
                #quan_art permite saber si debemos haber una repartición aleatorio o simplemente respetar los grupos ya establecidos.
                quan_art = course.artes.count()
                art = Arte.objects.filter(nombre=body_request["art"])[0]
                make_distribution(students, art, canvas_course, assignment_id, quan_art, date)
                course.artes.add(art)    
            else:
                print("Disciplina ya repartida")
        
        elif body_request["title_task"] == "Repartir peer review":
            #Necesito saber artes ya repartidas
            arts = course.artes.all()
            for art in arts:
                if art.nombre == body_request["art"]:
                    print("Repartir peer review")
                    peer_review_distribution(canvas_course, art, assignment_id, date)
                    break
            

    response = {'please move along': 'nothing to see here'}
    return Response(response, status=status.HTTP_404_NOT_FOUND)
