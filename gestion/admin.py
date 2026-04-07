from django.contrib import admin
from .models import CustomUser, Arbitro, Categoria, CategoriaGrupo, Arancel, Partido, Disponibilidad, Designacion

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)

@admin.register(CategoriaGrupo)
class CategoriaGrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grupo')
    list_filter = ('grupo',)

@admin.register(Arancel)
class ArancelAdmin(admin.ModelAdmin):
    list_display = ('rol', 'categoria_grupo', 'monto')
    list_filter = ('rol', 'categoria_grupo')

@admin.register(Arbitro)
class ArbitroAdmin(admin.ModelAdmin):
    list_display = ('user', 'categoria_max', 'phone')

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('title', 'categoria', 'date_time', 'location')
    list_filter = ('categoria', 'date_time')

@admin.register(Disponibilidad)
class DisponibilidadAdmin(admin.ModelAdmin):
    list_display = ('arbitro', 'start_time', 'end_time', 'is_available')
    list_filter = ('is_available', 'arbitro')

@admin.register(Designacion)
class DesignacionAdmin(admin.ModelAdmin):
    list_display = ('arbitro', 'partido', 'rol_asignado', 'status', 'monto_honorario')
    list_filter = ('status', 'rol_asignado')
    readonly_fields = ('monto_honorario',)
