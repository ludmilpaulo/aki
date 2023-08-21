from django.contrib import admin
from .models import Fornecedor, HorarioFuncionamento, Produto, Categoria

@admin.register(Categoria)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nome',)

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nome_fornecedor', 'aprovado', 'criado_em')
    list_display_links = ('usuario', 'nome_fornecedor')
    list_editable = ('aprovado',)

class HorarioAberturaAdmin(admin.ModelAdmin):
    list_display = ('fornecedor', 'dia', 'hora_inicial', 'hora_final')

admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(HorarioFuncionamento, HorarioAberturaAdmin)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('fornecedor', 'nome', 'preco')
    list_filter = ('fornecedor', 'nome')
#    search_fields = ('fornecedor', 'nome')
