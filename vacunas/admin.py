from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from .models import *

class VacunaResource(resources.ModelResource):
	full_persona = Field()
	encargado = Field()
	fecha_nacimiento = Field()
	tipo_vacuna = Field()

	class Meta:
		model = Vacuna
		fields = ('full_persona', 'fecha_nacimiento', 'encargado', 'tipo_vacuna', 'comunidad__nombre',)
		export_order = ('full_persona', 'fecha_nacimiento', 'encargado', 'tipo_vacuna', 'comunidad__nombre')

	def dehydrate_full_persona(self, vacuna):
		nombres = (vacuna.persona.primer_nombre + ' ' + vacuna.persona.segundo_nombre)
		apellidos = (vacuna.persona.primer_apellido + ' ' + vacuna.persona.segundo_apellido)
		final = nombres + ', ' + apellidos 
		return final

	def dehydrate_encargado(self, vacuna):
		datos = 'N/A'
		if vacuna.personal is not None:
			datos = vacuna.personal.nombres + ', ' + vacuna.personal.apellidos
		return datos

	def dehydrate_fecha_nacimiento(self, vacuna):
		fecha = vacuna.persona.fecha_nac
		return fecha

	def dehydrate_tipo_vacuna(self, vacuna):
		vacune = vacuna.get_vacuna_display()
		return vacune

class VacunaAdmin(ImportExportModelAdmin):
	#change_list_template = 'change_list.html'
	resource_class = VacunaResource
	list_display = ('vacuna', 'tipo', 'fecha', 'persona', 'comunidad')
	list_filter = ['fecha', 'rango', 'comunidad']
	readonly_fields = ('nombre', 'tipo', 'fecha', 'vacuna', 'persona', 'comunidad', 'personal', 'rango')
	search_fields = ['persona__primer_nombre', 'persona__primer_apellido']

	def has_delete_permission(self, request, obj=None):
		return False

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
#admin.site.register(Vacuna)
admin.site.register(Vacuna, VacunaAdmin)
admin.site.register([Persona], PersonaAdmin)
admin.site.site_header = 'Yo Vacuno'
admin.site.site_title = 'Puesto de Salud Xantun'
admin.site.index_title = 'Bienvenido al Sistema'