from django.db import models
from datetime import date

RANGOS = (
    (1, '< 1 año'),
    (2, '< 2 año'),
    (3, '< 3 año'),
)

TIPO_P=(
    (1, 'Produccion'),
    (2, 'Cobertura'),
)

VACUNAS=(
    #al nacer
    (1, 'BCG'),
    (2, 'HEPATITIS'),
    #2 meses    
    (3, 'IPV'),
    (4, 'PENTA 1'),
    (5,'ROTAVIRUS 1'),
    (6, 'NEUMO 1'),
    #4 meses
    (7, 'PENTA 2'),
    (8, 'POLIO 2'),
    (9, 'ROTAVIRUS 2'),
    (10, 'NEUMO 2'),
    #6 meses
    (11, 'POLIO 3'), 
    (12, 'PENTA 3'),
    #12 meses
    (13, 'SPR 1'),
    (14, 'NEUMO R1'),
    #18 meses
    (15, 'SPR 2'),
    (16, 'DPT R1'),
    (17, 'POLIO R1'),
    #4 a 6 a;os
    (18, 'DPT R2'),
    (19, 'POLIO R2'),
)

SEXO = (
    (1, 'Masculino'),
    (2, 'Femenino'),
)
# Create your models here.
class Personal(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    cui= models.CharField(max_length=255)
    renglon = models.IntegerField(default=0)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombres + ', ' + self.apellidos

class Rango (models.Model):
    rango = models.CharField(max_length=255)
    choice = models.PositiveSmallIntegerField(choices=RANGOS)
    
    def __str__(self):
        return self.rango

class Comunidad(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Persona (models.Model):
    cui = models.CharField(max_length=25, blank=True, null=True)
    sexo = models.IntegerField(choices=SEXO) 
    primer_nombre = models.CharField(max_length=255)
    segundo_nombre = models.CharField(max_length=255, blank=True, null=True)
    primer_apellido = models.CharField(max_length=255)
    segundo_apellido = models.CharField(max_length=255, blank=True, null=True)
    fecha_nac = models.DateField("Fecha de nacimiento") 
    direccion = models.CharField(max_length=255)
    a_os = models.IntegerField(default = 0)
    meses = models.IntegerField(default = 0)
    dias = models.IntegerField(default = 0)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)

    def __str__(self):
        return self.primer_nombre

    def crearVacunas(self):
        for i in range(1, 20):
            vacuna = Vacuna(nombre='V'+str(i), tipo=1, vacuna=i)
            if i<= 12:
                vacuna.rango= Rango.objects.get(pk=1)
            elif i >12 and i<= 17:
                vacuna.rango= Rango.objects.get(pk=2)
            else:
                vacuna.rango= Rango.objects.get(pk=4)
            print(vacuna.nombre + ': ' + str(vacuna.tipo) + ', ' + str(vacuna.vacuna) + ', ' + vacuna.rango.rango + '\n')

    def calcular_edad(self):
        hoy = date.today()
        if (hoy < self.fecha_nac):
            print('Error')
        else: 
            ano = self.fecha_nac.year
            mes = self.fecha_nac.month   
            dia = self.fecha_nac.day
            fecha=self.fecha_nac
            edad = hoy.year - ano
            if (mes > hoy.month):
                edad -= 1
            else:
                if (mes == hoy.month and dia > hoy.day):
                    edad -= 1
            meses = hoy.month - mes
            if (meses < 0):
                meses = 12 + meses
            if (meses == 0 and edad == 0):
                meses = 11
            delta1 = date(hoy.year, mes, dia)
            delta2 = date(hoy.year+1, mes, dia)
            dias = (max(delta1, delta2) - hoy).days
            dias=(hoy.day-dia)
            if (dias<0):
                dias=30+dias
            resultado = str(edad) + ' años, ' + str(meses) + ' meses y ' + str(dias) + ' dias'
        return resultado



class Vacuna(models.Model):
    nombre = models.CharField(max_length=255)
    tipo= models.PositiveSmallIntegerField(choices=TIPO_P)
    fecha = models.DateField("Fecha aplicación", blank=True, null=True)
    vacuna= models.PositiveSmallIntegerField(choices=VACUNAS)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE, blank=True, null=True)
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, blank=True, null=True)
    rango= models.ForeignKey(Rango,on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre 

    def edad_meses(selft):
        return self.meses

    def edad_dias(selft):
        return self.meses
