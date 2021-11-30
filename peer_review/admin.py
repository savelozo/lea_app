from django.contrib import admin
from .models import Alumne, Curso, Arte, ArtAlumneRelation, EnsayoAlumneRelation

class Filter(admin.ModelAdmin):
    list_filter = ("curso", "arte", "group")

admin.site.register(Curso)
admin.site.register(Arte)
admin.site.register(Alumne)
admin.site.register(ArtAlumneRelation, Filter)
admin.site.register(EnsayoAlumneRelation)