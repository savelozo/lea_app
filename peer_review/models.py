from django.db import models

class Arte(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
class Curso(models.Model):
    id_canvas = models.IntegerField()
    semestre = models.IntegerField()
    año = models.IntegerField()
    artes = models.ManyToManyField(Arte)

    def __str__(self):
        return "{} - {}".format(self.año, self.semestre)

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

    def __str__(self):
        return "{} / {}".format(self.curso, self.nombre)

class ArtAlumneRelation(models.Model):
    #Permite saber en qué grupo se encuentra cada alumne por disciplina
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumne = models.ForeignKey(Alumne, on_delete=models.CASCADE)
    arte = models.ForeignKey(Arte, on_delete=models.CASCADE)
    group = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return "{} / {}: Grupo {}".format(self.arte, self.alumne, self.group)

class EnsayoAlumneRelation(models.Model):
    #Permite saber las relaciones de correcciones que se establecen entre alumnes por disciplina.
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)
    corregido = models.ForeignKey(Alumne, on_delete=models.CASCADE)
    arte = models.ForeignKey(Arte, on_delete=models.CASCADE)
    url = models.CharField(max_length=120, null=True)
    corrector_id_1 = models.IntegerField(blank=True, null=True)
    corrector_id_2 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} - Corrección de {}: / Corrector 1: {} / Corrector 2: {}".format(self.arte, self.corregido, self.corrector_id_1, self.corrector_id_2)
    