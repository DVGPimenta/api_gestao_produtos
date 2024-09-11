from sqlalchemy.orm import Session
from models.produtos_models import Produtos


class ProdutosService:
    def __init__(self, session: Session):
        self.session = session

    def get_produtos(self):
        produtos = self.session.query(Produtos).all()
        produtos_lista = []
        for produto in produtos:
            produtos_lista.append(produto.as_dict())
        return produtos_lista

    def get_produto_codigo(self, codigo):
        produto = self.session.query(Produtos).filter_by(codigo=codigo).first()
        produto_json = produto.as_dict()
        return produto_json

    def post_produtos(self, codigo: str, nome: str, descricao: str,
                      preco: float, quantidade_estoque: int, categoria: str):
        novo_produto = Produtos(codigo=codigo, nome=nome, descricao=descricao,
                                preco=preco, quantidade_estoque=quantidade_estoque, categoria=categoria)
        self.session.add(novo_produto)
        self.session.commit()
        return novo_produto.as_dict()

    def put_produtos(self, codigo, nome=None, descricao=None, preco=None,
                     quantidade_estoque=None, categoria=None):
        produto = self.session.query(Produtos).filter_by(codigo=codigo).first()
        if not produto:
            return f'Produto não encontrado'

        if nome:
            produto.nome = nome
        if descricao:
            produto.descricao = descricao
        if preco:
            produto.preco = preco
        if quantidade_estoque:
            produto.quantidade_estoque = quantidade_estoque
        if categoria:
            produto.categoria = categoria

        try:
            self.session.commit()
            return produto.as_dict()
        except Exception as e:
            self.session.rollback()
            raise f'Erro ao atualizar produto {str(e)}'

    def delete_produtos(self, codigo):
        produto = self.session.query(Produtos).filter_by(codigo=codigo).first()
        if produto:
            try:
                self.session.delete(produto)
                self.session.commit()
                return f'Produto {produto.nome} deletado com sucesso'
            except Exception as e:
                self.session.rollback()
                return f'Erro {e} ao deletar produto'

