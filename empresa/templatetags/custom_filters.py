from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Retorna o valor de um dicionário com base na chave fornecida.
    """
    return dictionary.get(key)