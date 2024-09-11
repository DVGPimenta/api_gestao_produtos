from config import engine, Base
from sqlalchemy import Column, Integer, String, Float


class Produtos(Base):
    __tablename__ = 'produtos'
    codigo = Column(String(13), primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(200), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=False)

    def as_dict(self):
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "quandidade_estoque": self.quantidade_estoque,
            "categoria": self.categoria
        }


Base.metadata.create_all(engine)
