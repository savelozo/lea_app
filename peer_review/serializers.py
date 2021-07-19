from rest_framework import serializers
from .models import Curso, Arte, Alumne

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ('id_canvas', 'semestre', 'año')

class ArteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arte
        fields = ('nombre',)

class AlumneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumne
        fields = ('canvas_id','nombre','curso')