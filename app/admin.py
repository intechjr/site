from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *
from .models import CustomUser


class DetalheProdutoEstoqueInline(admin.TabularInline):
    model = DetalheProdutoEstoque
    extra = 1
class DetalheProdutoFotoInline(admin.TabularInline):
    model = DetalheProdutoFoto
    extra = 1
admin.site.register(DetalheProdutoFoto)

class DetalheProdutoAdmin(admin.ModelAdmin):
    inlines = [DetalheProdutoEstoqueInline, DetalheProdutoFotoInline]
    
admin.site.register(DetalheProduto, DetalheProdutoAdmin)
admin.site.register(DetalheProdutoEstoque)

class SubsectorInline(admin.TabularInline):
    model = Subsector
    extra = 1

class SectorAdmin(admin.ModelAdmin):
    inlines = [SubsectorInline]
    
admin.site.register(Sector, SectorAdmin)
admin.site.register(Subsector)

class InstituicUInline(admin.TabularInline):
    model = InstituicUnidade
    extra = 1

class InstituicAdmin(admin.ModelAdmin):
    inlines = [InstituicUInline]
    
admin.site.register(Instituic, InstituicAdmin)
admin.site.register(InstituicUnidade)


class SubCategoriaUInline(admin.TabularInline):
    model = SubCategoria
    extra = 1

class CategoriaAdmin(admin.ModelAdmin):
    inlines = [SubCategoriaUInline]
    
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria)

class SubTipoUInline(admin.TabularInline):
    model = Subtipo
    extra = 1

class TipoAdmin(admin.ModelAdmin):
    inlines = [SubTipoUInline]
 
    
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Subtipo)


class SectorUInline(admin.TabularInline):
    model = Sector
    extra = 1
class SuperSectorAdmin(admin.ModelAdmin):
    inlines = [SectorUInline]

admin.site.register(SectorSuper, SuperSectorAdmin)




admin.site.register(Produto)
admin.site.register(TipoEmbalagem)
admin.site.register(Modelo)
admin.site.register(Fabricante)
admin.site.register(Marca)
admin.site.register(Transaction)
admin.site.register(UnidadeMedida)
admin.site.register(MovimentacaoProduto)
admin.site.register(ProdutoMovimentoItem)



class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'subsetor', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'subsetor')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'subsetor')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'subsetor'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
