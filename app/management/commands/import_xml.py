import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from app.models import *

class Command(BaseCommand):
    help = 'Importa dados de um arquivo XML para o banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('xml_file', type=str)

    def handle(self, *args, **kwargs):
        xml_file = kwargs['xml_file']

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Arquivo '{xml_file}' não encontrado."))
            return
        except ET.ParseError as e:
            self.stderr.write(self.style.ERROR(f"Erro ao processar o XML: {e}"))
            return

        # Importar marcas
        for marca_element in root.findall('Marca'):
            nome_marca = marca_element.find('nome_marca')
            if nome_marca is not None:
                nome_marca = nome_marca.text.strip()
                Marca.objects.get_or_create(nome_marca=nome_marca)

        # Importar produtos
        for produto_element in root.findall('Produto'):
            nome_produto = produto_element.find('nome_produto')
            marca_nome = produto_element.find('marca')
            modelo_nome = produto_element.find('modelo')
            fabricante_nome = produto_element.find('fabricante')

            nome_produto = nome_produto.text.strip() if nome_produto is not None else None
            marca = None
            modelo = None
            fabricante = None

            if marca_nome is not None:
                marca_nome = marca_nome.text.strip()
                marca, _ = Marca.objects.get_or_create(nome_marca=marca_nome)

            if modelo_nome is not None:
                modelo_nome = modelo_nome.text.strip()
                modelo, _ = Modelo.objects.get_or_create(nome_modelo=modelo_nome)

            if fabricante_nome is not None:
                fabricante_nome = fabricante_nome.text.strip()
                fabricante, _ = Fabricante.objects.get_or_create(nome_fabricante=fabricante_nome)

            if nome_produto:
                produto, _ = Produto.objects.get_or_create(
                    nome_produto=nome_produto,
                    marca=marca,
                    modelo=modelo,
                    fabricante=fabricante
                )

                # Importar detalhes do produto
                for detalhe_element in produto_element.findall('DetalheProduto'):
                    cor_produto = detalhe_element.find('cor_produto')
                    sabor_produto = detalhe_element.find('sabor_produto')
                    quantidade_embalagem_produto = detalhe_element.find('quantidade_embalagem_produto')
                    tipo_embalagem_nome = detalhe_element.find('tipo_embalagem_produto')
                    quantidade_produto = detalhe_element.find('quantidade_produto')
                    preco_custo_produto = detalhe_element.find('preco_custo_produto')
                    preco_venda_produto = detalhe_element.find('preco_venda_produto')
                    subsetor_nome = detalhe_element.find('subsetor')
                    setor_nome = detalhe_element.find('setor')

                    cor_produto = cor_produto.text.strip() if cor_produto is not None else None
                    sabor_produto = sabor_produto.text.strip() if sabor_produto is not None else None
                    quantidade_embalagem_produto = int(quantidade_embalagem_produto.text.strip()) if quantidade_embalagem_produto is not None else None
                    tipo_embalagem = None
                    quantidade_produto = int(quantidade_produto.text.strip()) if quantidade_produto is not None else None
                    preco_custo_produto = float(preco_custo_produto.text.strip()) if preco_custo_produto is not None else None
                    preco_venda_produto = float(preco_venda_produto.text.strip()) if preco_venda_produto is not None else None

                    if tipo_embalagem_nome is not None:
                        tipo_embalagem_nome = tipo_embalagem_nome.text.strip()
                        tipo_embalagem, _ = TipoEmbalagem.objects.get_or_create(nome_embalagem=tipo_embalagem_nome)

                    setor = None
                    if setor_nome is not None:
                        setor_nome = setor_nome.text.strip()
                        setor, _ = Sector.objects.get_or_create(
                            nome_setor=setor_nome,
                            defaults={'super_setor': None}  # Adiciona um valor padrão para super_setor
                        )

                    subsetor = None
                    if subsetor_nome is not None and setor is not None:
                        subsetor_nome = subsetor_nome.text.strip()
                        subsetor, _ = Subsector.objects.get_or_create(nome_sub_setor=subsetor_nome, setor=setor)

                    if subsetor:
                        DetalheProduto.objects.get_or_create(
                            produto=produto,
                            cor_produto=cor_produto,
                            sabor_produto=sabor_produto,
                            quantidade_embalagem_produto=quantidade_embalagem_produto,
                            tipo_embalagem_produto=tipo_embalagem,
                            quantidade_produto=quantidade_produto,
                            preco_custo_produto=preco_custo_produto,
                            preco_venda_produto=preco_venda_produto,
                            subsetor=subsetor
                        )

        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
