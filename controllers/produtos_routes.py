from services.produtos_services import ProdutosService
from flask import Blueprint, jsonify, request
from sqlalchemy.orm import sessionmaker
from config import engine
from sqlalchemy.exc import IntegrityError

produtos_page = Blueprint('produtos_page', __name__)
Session_local = sessionmaker(bind=engine)


@produtos_page.route('/produtos', methods=['GET'])
def rota_get_produtos():
    session = Session_local()
    try:
        produtos_service = ProdutosService(session)
        produtos = produtos_service.get_produtos()
        return jsonify(produtos), 200
    except Exception as e:
        return jsonify({'Erro': str(e)}), 400
    finally:
        session.close()


@produtos_page.route('/produtos/<codigo>', methods=['GET'])
def rota_get_produto_codigo(codigo):
    session = Session_local()
    try:
        produto_service = ProdutosService(session)
        produto = produto_service.get_produto_codigo(codigo)
        if produto:
            return jsonify(produto), 200
        else:
            return jsonify({'Erro': 'Produto nao encontrado'}), 404
    except Exception as e:
        return jsonify({'Erro': str(e)}), 400
    finally:
        session.close()


@produtos_page.route('/produtos/add', methods=['POST'])
def rota_post_produto():
    data = request.get_json()
    codigo = data.get('codigo')
    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    quantidade_estoque = data.get('quantidade_estoque')
    categoria = data.get('categoria')

    if not (codigo and nome and descricao and preco and quantidade_estoque and categoria):
        return jsonify({'Erro': 'Dados insuficiente para o cadastro'})

    session = Session_local()
    try:
        services_produto = ProdutosService(session)
        services_produto.post_produtos(codigo=codigo,
                                       nome=nome,
                                       descricao=descricao,
                                       preco=preco,
                                       quantidade_estoque=quantidade_estoque,
                                       categoria=categoria)
        return jsonify({'mensagem': f'produto {nome} cadastrado com sucesso'})
    except ValueError:
        return jsonify({'erro': f'{ValueError}'})
    except IntegrityError:
        return jsonify({'erro': f'{IntegrityError}'})
    finally:
        session.close()


@produtos_page.route('/produtos/edit/<codigo>', methods=['PUT'])
def rota_put_produto(codigo):
    data = request.get_json()
    nome = data.get('nome')
    descricao = data.get('descricao')
    preco = data.get('preco')
    quantidade_estoque = data.get('quantidade_estoque')
    categoria = data.get('categoria')

    if not any([nome, descricao, preco, quantidade_estoque, categoria]):
        return 'Dados insuficientes para atualização do produto'

    session = Session_local()
    try:
        services_produto = ProdutosService(session)
        produto = services_produto.put_produtos(
            codigo,
            nome=nome,
            descricao=descricao,
            preco=preco,
            quantidade_estoque=quantidade_estoque,
            categoria=categoria)
        if produto:
            return jsonify(produto), 200
        else:
            return jsonify({'erro': 'produto nao encontrado'}), 404
    finally:
        session.close()


@produtos_page.route('/produtos/delete/<codigo>', methods=['DELETE'])
def rota_delete_produtos(codigo):
    session = Session_local()
    try:
        service_produto = ProdutosService(session)
        produto = service_produto.delete_produtos(codigo)
        if produto:
            return jsonify({'mensagem': f'Produto deletado com sucesso'})
        else:
            return jsonify({'erro': 'Produto nao encontrado em nosso bando de dados'})
    except Exception as e:
        return jsonify({'erro': f'{str(e)}'})
    finally:
        session.close()
