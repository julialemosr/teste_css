import sqlalchemy
import plotly.express as px
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select, func, desc
from models import Funcionario, Produto, Categoria, Entrada_saida, db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def inicial():
    return render_template('base.html')


@app.route('/Funcionarios', methods=['GET'])
def funcionarios():
    sql_funcionarios = select(Funcionario)
    resultado_funcionarios = db_session.execute(sql_funcionarios).scalars()
    lista_de_funcionario = []
    for n in resultado_funcionarios:
        lista_de_funcionario.append(n.serialize_funcionario())
        print(lista_de_funcionario[-1])
    return render_template('lista_funcionario.html',
                           lista_de_funcionarios=lista_de_funcionario)


@app.route('/produto', methods=['GET'])
def produtos():
    sql_produtos = (select(Produto, Categoria)
                    .join(Categoria, Categoria.id_categoria == Produto.iDcategoria))

    resultado_produtos = db_session.execute(sql_produtos).fetchall()

    print(resultado_produtos)
    return render_template('lista_produto.html',
                           lista_de_produtos=resultado_produtos)


@app.route('/categoria', methods=['GET'])
def categorias():
    sql_categoria = select(Categoria)
    resultado_produtos = db_session.execute(sql_categoria).scalars()
    lista_categorias = []
    for n in resultado_produtos:
        lista_categorias.append(n.serialize_categoria())
        print(lista_categorias[-1])
    return render_template('lista_categoria.html',
                           lista_categoria=lista_categorias)


@app.route('/entrada_saida', methods=['GET'])
def entrada_saidas():
    sql_entrada_saida = (select(Entrada_saida, Produto, Funcionario)
                         .join(Produto, Produto.id_produto == Entrada_saida.id_produtos)
                         .join(Funcionario, Funcionario.id_funcionario == Entrada_saida.idFuncionario))
    resultado_entrada_saida = db_session.execute(sql_entrada_saida).fetchall()

    print(resultado_entrada_saida)
    return render_template('lista_entrada_saida.html',
                           lista_entrada_saida=resultado_entrada_saida)


@app.route('/saidas', methods=['GET'])
def saida():
    sql_entrada_saida = (select(Entrada_saida, Produto, Funcionario)
                         .join(Produto, Produto.id_produto == Entrada_saida.id_produtos)
                         .join(Funcionario, Funcionario.id_funcionario == Entrada_saida.idFuncionario)).where(Entrada_saida.tipo=="Saida")
    resultado_entrada_saida = db_session.execute(sql_entrada_saida).fetchall()

    print(resultado_entrada_saida)
    return render_template('saida.html',
                           saida=resultado_entrada_saida)


@app.route('/entradas', methods=['GET'])
def entrada():
    sql_entrada_saida = (select(Entrada_saida, Produto, Funcionario)
                         .join(Produto, Produto.id_produto == Entrada_saida.id_produtos)
                         .join(Funcionario, Funcionario.id_funcionario == Entrada_saida.idFuncionario)).where(Entrada_saida.tipo=="Entrada")
    resultado_entrada_saida = db_session.execute(sql_entrada_saida).fetchall()

    print(resultado_entrada_saida)
    return render_template('entrada.html',
                           entrada=resultado_entrada_saida)


@app.route('/nova_entrada', methods=["POST", "GET"])
def criar_entrada_saida():
    if request.method == "POST":
        if not request.form['dia_entrada']:
            flash("peencher todos os campos", "error")
        if not request.form['qtd']:
            flash("peencher todos os campos", "error")
        if not request.form['tipo']:
            flash("peencher todos os campos", "error")
        else:
            form_evento = Entrada_saida(data=request.form['dia_entrada'],
                                        tipo=str(request.form['tipo']),
                                        qtd=int(request.form['qtd']),
                                        idFuncionario=int(request.form['id_funcionario']),
                                        id_produtos=int(request.form['id_produtos'])
                                        )


            form_produto = db_session.execute(select(Produto).filter_by(id_produto=int(request.form['id_produtos']))).scalar()

            if request.form['tipo'] == 'Entrada':
                form_produto.quantidade = int(request.form.get('qtd')) + form_produto.quantidade
                form_produto.save()
                form_evento.save()

                print('bruna lindassssssss')

            else:
                if form_produto.quantidade >= int(request.form.get('qtd')):

                    form_produto.quantidade = form_produto.quantidade - int(request.form.get('qtd'))
                    print('bruna linda SAIDSAAAA')
                    form_produto.save()
                    form_evento.save()

            db_session.close()
            flash("entrada ou saida criado  com sucesso", "success")
            return redirect(url_for('entrada_saidas'))

    sql_funcionario = select(Funcionario)
    resultado_funcionario = db_session.execute(sql_funcionario).scalars()
    lista_funcionarios = []
    for n in resultado_funcionario:
        lista_funcionarios.append(n.serialize_funcionario())
        print(lista_funcionarios[-1])

    sql_produto = select(Produto)
    resultado_produto = db_session.execute(sql_produto).scalars()
    lista_produto = []
    for n in resultado_produto:
        lista_produto.append(n.serialize_produto())
        print(lista_produto[-1])

    return render_template('cadastro_entrada_saida.html',
                           lista_de_funcionarios=lista_funcionarios,
                           lista_de_produtos=lista_produto)


@app.route('/cadastro_produto', methods=["POST", "GET"])
def criar_produto():
    if request.method == "POST":
        if not request.form['Nome do produto']:
            flash("peencher todos os campos", "error")
        if not request.form['Valor do produto']:
            flash("peencher todos os campos", "error")
        if not request.form['Data de fabricação']:
            flash("peencher todos os campos", "error")
        else:
            form_evento = Produto(nome_produto=request.form['Nome do produto'],
                                  valor_produto=float(request.form['Valor do produto']),
                                  data_fabricacao=request.form['Data de fabricação'],
                                  iDcategoria=int(request.form['id_categoria']),
                                  )

            print(form_evento)
            form_evento.save()
            db_session.close()
            flash("Produto criado  com sucesso", "success")
            return redirect(url_for('produtos'))

    sql_categoria = select(Categoria)
    resultado_categoria = db_session.execute(sql_categoria).scalars()
    lista_categorias = []
    for n in resultado_categoria:
        lista_categorias.append(n.serialize_categoria())
        print(lista_categorias[-1])

    return render_template('cadastro_produto.html',
                           lista_de_categorias=lista_categorias)


@app.route('/cadastro_funcionario', methods=["POST", "GET"])
def criar_funcionario():
    if request.method == "POST":
        if not request.form['nome_funcionario']:
            flash("peencher todos os campos", "error")
        if not request.form['CPF']:
            flash("peencher todos os campos", "error")
        if not request.form['email']:
            flash("peencher todos os campos", "error")
        else:
            form_evento = Funcionario(nome_funcionario=request.form['nome_funcionario'],
                                      CPF=int(request.form['CPF']),
                                      email=str(request.form['email']),
                                      )
            print(form_evento)
            form_evento.save()
            db_session.close()
            flash("Funcionário criado  com sucesso", "success")
            return redirect(url_for('funcionarios'))

    return render_template(('cadastro_funcionario.html'))


@app.route('/cadastro_categoria', methods=["POST", "GET"])
def criar_categoria():
    if request.method == "POST":
        if not request.form['nome_categoria']:
            flash("peencher todos os campos", "error")
        else:
            form_evento = Categoria(nome_categoria=request.form['nome_categoria'],
                                    )
            print(form_evento)
            form_evento.save()
            db_session.close()
            flash("Categoria criada  com sucesso", "success")
            return redirect(url_for('categorias'))

    return render_template(('cadastro_categoria.html'))


@app.route(rule='/editar_pessoa/<int:funcionario_id>', methods=['GET', 'POST'])
def editar_funcionario(funcionario_id):
    funcionario_edt = db_session.execute(select(Funcionario).filter_by(id_funcionario=funcionario_id)).scalar()
    if request.method == 'POST':
        if not request.form.get('form_nome'):
            flash("*Preencher nome", 'error')
        if not request.form.get('form_email'):
            flash("*Preencher email", 'error')
        else:
            try:
                funcionario_edt.nome_funcionario = request.form.get('form_nome')
                funcionario_edt.email = request.form.get('form_email')
                funcionario_edt.save()

                flash("Pessoa editada com sucesso", "success")
                return redirect(url_for('funcionarios'))
            except sqlalchemy.exc.IntegrityError:
                flash("este funcionario ja esta cadastrado", "success")
    return render_template('atualizar_funcionario.html', base_funcionario=funcionario_edt)



@app.route(rule='/editar_categoria/<int:categoria_id>', methods=['GET', 'POST'])
def editar_categoria(categoria_id):
    categoria_edt = db_session.execute(select(Categoria).filter_by(id_categoria=categoria_id)).scalar()
    if request.method == 'POST':
        if not request.form.get('form_nome_categoria'):
            flash("*Preencher nome", 'error')

        else:
            try:
                categoria_edt.nome_categoria = request.form.get('form_nome_categoria')
                categoria_edt.save()

                flash("Pessoa editada com sucesso", "success")
                return redirect(url_for('categorias'))
            except sqlalchemy.exc.IntegrityError:
                flash("este funcionario ja esta cadastrado", "success")
    return render_template('atualizar_categoria.html', base_categoria=categoria_edt)


@app.route(rule='/editar_produto/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto_edt = db_session.execute(select(Produto).filter_by(id_produto=produto_id)).scalar()
    if request.method == 'POST':
        if not request.form.get('form_nome_produto'):
            flash("*Preencher nome", 'error')
        if not request.form.get('form_valor'):
            flash("*Preencher nome", 'error')
        if not request.form.get('form_data'):
            flash("*Preencher nome", 'error')
        else:
            try:
                produto_edt.nome_produto = request.form.get('form_nome_produto')
                produto_edt.valor_produto = request.form.get('form_valor')
                produto_edt.data_fabricacao = request.form.get('form_data')
                produto_edt.save()

                flash("Pessoa editada com sucesso", "success")
                return redirect(url_for('produtos'))
            except sqlalchemy.exc.IntegrityError:
                flash("este funcionario ja esta cadastrado", "success")
    return render_template('atualizar_produto.html', base_produto=produto_edt)


@app.route(rule='/editar_entrada_sida/<int:entrada_saida_id>', methods=['GET', 'POST'])
def editar_entrada_saida(entrada_saida_id):
    entrada_saida_edt = db_session.execute(select(Entrada_saida).filter_by(id_entrada_saida=entrada_saida_id)).scalar()
    if request.method == 'POST':
        if not request.form.get('form_tipo'):
            flash("*Preencher nome", 'error')
        if not request.form.get('form_qtd'):
            flash("*Preencher nome", 'error')
        if not request.form.get('form_data_entrada'):
            flash("*Preencher nome", 'error')
        else:
            try:
                entrada_saida_edt.tipo = request.form.get('form_tipo')
                entrada_saida_edt.qtd = request.form.get('form_qtd')
                entrada_saida_edt.data_fabricacao = request.form.get('form_data_entrada')
                entrada_saida_edt.save()

                flash("Pessoa editada com sucesso", "success")
                return redirect(url_for('entrada_saidas'))
            except sqlalchemy.exc.IntegrityError:
                flash("este funcionario ja esta cadastrado", "success")
    return render_template('atualizar_entrada_saida.html', base_entrada_saida=entrada_saida_edt)


# @app.route('/Funcionarios', methods=['GET'])


 # def analise_produto():
 #    maior_movimentacao = (
 #        select(
 #            Produto.nome_produto,
 #            func.sum(Entrada_saida.qtd).label('total_movimentacoes')
 #        )
 #        .join(Entrada_saida, Produto.id_produto == Entrada_saida.produto)
 #        .where(Entrada_saida.tipo == 'Saida')
 #        .group_by(Entrada_saida.produto)
 #        .order_by(desc('total_movimentacoes'))
 #        .limit(10)
 #        .all()
 #    )
 #    maior_movimentacao = maior_movimentacao
 #    print(maior_movimentacao)
 #
 #    return render_template('analise.html', maior_movimentacao=maior_movimentacao)

# @app.route('/analise', methods=['GET'])
# def analise():
#     quantidade = select(Produto.quantidade)
#     sum(quantidade)


@app.route('/grafico_produto')
def grafico_produto():
    # Consulta ao banco para pegar nome e quantidade de cada produto (limite de 5)
    valor_produtos = db_session.execute(
        select(Produto.nome_produto, Produto.quantidade).limit(5)  # Limite de 5 produtos
    ).fetchall()

    # Verificando se há produtos retornados pela consulta
    if not valor_produtos:
        return "Nenhum produto encontrado no estoque.", 404

    # Exibindo os dados dos produtos no console para depuração
    print("Produtos encontrados:", valor_produtos)

    # Dados dos produtos conforme sua estrutura
    produtos = [
        {"nome": valor_produtos[0][0], "quantidade": valor_produtos[0][1]},
        {"nome": valor_produtos[1][0], "quantidade": valor_produtos[1][1]},
        {"nome": valor_produtos[2][0], "quantidade": valor_produtos[2][1]},
        {"nome": valor_produtos[3][0], "quantidade": valor_produtos[3][1]},
        {"nome": valor_produtos[4][0], "quantidade": valor_produtos[4][1]}
    ]

    # Exibindo a estrutura dos dados organizados
    print("Estrutura dos produtos:", produtos)

    # Convertendo os dados para um DataFrame para facilitar o gráfico
    df = pd.DataFrame(produtos)

    # Criando o gráfico com Plotly Express
    fig = px.bar(
        df,
        x="nome",
        y="quantidade",
        title="Quantidade dos produtos no estoque (Top 5)",
        labels={"quantidade": "Quantidade", "nome": "Produto"},
        color="nome"
    )

    # Adicionando rótulos com os valores das quantidades nas barras
    fig.update_traces(text=df['quantidade'], textposition='auto')

    # Convertendo o gráfico para HTML
    graph_html = fig.to_html(full_html=False)

    # Renderizando o template com o gráfico
    return render_template("grafico_produto.html", graph_html=graph_html)




if __name__ == '__main__':
    app.run(debug=True)