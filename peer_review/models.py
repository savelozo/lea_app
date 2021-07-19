from django.db import models

class Arte(models.Model):
    nombre = models.CharField(max_length=50)

class Curso(models.Model):
    id_canvas = models.IntegerField()
    semestre = models.IntegerField()
    año = models.IntegerField()
    artes = models.ManyToManyField(Arte)

class Ensayo(models.Model):
    fecha_entrega = models.DateTimeField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    arte = models.ForeignKey(Arte, on_delete=models.CASCADE)

class Alumne(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, default=1)
    nombre = models.CharField(max_length=120)
    canvas_id = models.IntegerField()
    ensayos = models.ForeignKey(Ensayo, on_delete=models.CASCADE, blank=True, null=True)
    last_group = models.IntegerField(blank=True, null=True)

class ArtAlumneRelation(models.Model):
    #Permite saber en qué grupo se encuentra cada alumne por disciplina
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumne = models.ForeignKey(Alumne, on_delete=models.CASCADE)
    arte = models.ForeignKey(Arte, on_delete=models.CASCADE)
    group = models.IntegerField(blank=True, null=True)

class EnsayoAlumneRelation(models.Model):
    #Permite saber las relaciones de correcciones que se establecen entre alumnes por disciplina.
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    corregido = models.ForeignKey(Alumne, on_delete=models.CASCADE)
    arte = models.ForeignKey(Arte, on_delete=models.CASCADE)
    url = nombre = models.CharField(max_length=120)
    corrector_id_1 = models.IntegerField(blank=True, null=True)
    corrector_id_2 = models.IntegerField(blank=True, null=True)

    