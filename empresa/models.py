from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Nome da empresa')
    logo = models.ImageField(upload_to='empresa/static/images/', null=True, blank=True, verbose_name='Logo')  # Armazena imagens no diretório 'images/'
    bg_logo = models.FileField(upload_to='empresa/static/media/', null=True, blank=True, verbose_name='Imagem ou Vídeo de Fundo', help_text='Aceita imagens ou vídeos')  # Alterado para aceitar arquivos de mídia
    sobre = models.CharField(max_length=255, verbose_name='Sobre', help_text='Texto que descreve a empresa')
    contato = models.BooleanField(default=False, verbose_name='Contato', help_text='Ativar formulário de contato?')
    email = models.EmailField(max_length=100, verbose_name='Email', help_text='Email para contato')

    class Meta:
        verbose_name = 'Configuração da Empresa'
        verbose_name_plural = 'Configurações da Empresa'

    def __str__(self):
        return self.nome


class Aba(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Nome da aba')
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, verbose_name='Empresa', related_name='abas')

    class Meta:
        verbose_name_plural = 'Abas'

    def __str__(self):
        return self.nome


class AbaItem(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Nome do item da aba')
    descricao = models.CharField(max_length=255, verbose_name='Descrição', help_text='Descrição do item da aba')
    imagem = models.ImageField(upload_to='empresa/static/images/', verbose_name='Imagem', help_text='Imagem do Item')  # Armazena imagens no diretório 'itens/'
    aba = models.ForeignKey(Aba, on_delete=models.PROTECT, verbose_name='Aba', related_name='itens')

    class Meta:
        verbose_name = 'Item de Aba'
        verbose_name_plural = 'Itens de Aba'

    def __str__(self):
        return self.nome


class RedeSocial(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Nome', help_text='Nome da rede social')
    link = models.CharField(max_length=255, verbose_name='Link', help_text='Link da rede social')
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, verbose_name='Empresa', related_name='redes_sociais')

    class Meta:
        verbose_name = 'Rede Social'
        verbose_name_plural = 'Redes Sociais'

    def __str__(self):
        return self.nome