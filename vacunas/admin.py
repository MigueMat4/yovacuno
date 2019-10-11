from django.contrib import admin

from .models import *

class VacunaInline(admin.TabularInline):
	model = Vacuna
	extra = 0
	fields = ('vacuna', 'tipo', 'fecha', 'comunidad', 'personal', 'rango')
	readonly_fields = ('vacuna', 'rango')

	def has_delete_permission(self, request, obj):
		return False

class PersonaAdmin(admin.ModelAdmin):
	fieldsets = [
		('Informacion Personal', {'fields': ['cui', 'sexo','primer_nombre','segundo_nombre','primer_apellido','segundo_apellido','fecha_nac']}),
		('Datos de Residencia', {'fields': ['direccion','comunidad']}),
	]
	#readonly_fields = ('sexo', 'fecha_nac')
	inlines = [
		VacunaInline,
	] 

	def get_readonly_fields(self, request, obj=None):
		if obj:
			return ['sexo', 'fecha_nac']
		else:
			return [] 

	def save_model(self, request, obj, form, change):
		if not change:
			super().save_model(request, obj, form, change)
			for i in range(1, 20):
				vacuna = Vacuna(nombre='Vacuna ' + str(i), tipo=1, vacuna=i)
				if i<= 12:
					vacuna.rango= Rango.objects.get(pk=1)
				elif i >12 and i<= 17:
					vacuna.rango= Rango.objects.get(pk=2)
				else:
					vacuna.rango= Rango.objects.get(pk=4)
				vacuna.persona = obj
				vacuna.save()
		else:
			super().save_model(request, obj, form, change)

admin.site.register(Personal)
#admin.site.register(Persona)
admin.site.register(Comunidad)
admin.site.register(Rango)
admin.site.register(Vacuna)
admin.site.register([Persona], PersonaAdmin)
admin.site.site_header = 'Yo Vacuno'
admin.site.site_title = 'Puesto de Salud Xantun'
admin.site.index_title = 'Bienvenido al Sistema'