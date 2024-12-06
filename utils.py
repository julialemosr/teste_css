from models import Funcionario,Produto,Categoria,Entrada_saida,db_session
from sqlalchemy import select


def inserir_funcionario():
    funcionario = Funcionario(nome_funcionario=str(input('Nome do funcioario: ')),
                              CPF=int(input('CPF do funcionario: ')),
                              email=str(input('Email do funcionario: '))
                              )
    print(funcionario)
    funcionario.save()


def consultar_funcionario():
    var_funcionario = select(Funcionario)
    var_funcionario = db_session.execute(var_funcionario).all()
    print(var_funcionario)


def atualizar_funcionario():
    var_funcionario = select(Funcionario).where(Funcionario.nome_funcionario == str(input('Nome do veterinario: ')) == Funcionario.nome_funcionario)
    var_funcionario = select(Funcionario).where(Funcionario.CPF == int(input('crmv: ')) == Funcionario.CPF)
    var_funcionario = select(Funcionario).where(Funcionario.email == float(input('salario: ')) == Funcionario.email)
    var_funcionario = db_session.execute(var_funcionario).scalar()
    print(var_funcionario)
    var_funcionario.nome_funcionario = str(input('Novo nome: '))
    var_funcionario.CPF = str(input('Novo CPF: '))
    var_funcionario.email = input('Novo email: ')
    var_funcionario.save()

def deletar_funcionario():
    funcionario_deletar = input('Quem você deseja deletar? ')
    var_funcionario = select(Funcionario).where(funcionario_deletar == Funcionario.nome_funcionario)
    var_funcionario = db_session.execute(var_funcionario).scalar()
    var_funcionario.delete()




def inserir_produto():
    produto = Produto(nome_produto=str(input('Nome do produto: ')),
                              valor_produto=float(input('Valor do produto: ')),
                              data_fabricacao=str(input('data de fabricaça: ')),
                              iDcategoria= int(input('ID categoria: ')),
                              )
    print(produto)
    produto.save()


def consultar_produto():
    var_produto = select(Produto)
    var_produto = db_session.execute(var_produto).all()
    print(var_produto)


def atualizar_produto():
    var_produto = select(Produto).where(Produto.nome_produto == str(input('Nome do produto: ')) == Produto.nome_produto)
    var_produto = select(Produto).where(Produto.valor_produto == int(input('Valor do produto: ')) == Produto.valor_produto)
    var_produto = select(Produto).where(Produto.data_fabricacao == float(input('Data de fabricação do produto: ')) == Produto.data_fabricacao)
    var_produto = db_session.execute(var_produto).scalar()
    print(var_produto)
    var_produto.nome_produto = str(input('Novo nome do produto: '))
    var_produto.valor_produto = str(input('Nova valor do produto: '))
    var_produto.data_fabricacao = input('Nova data de fabricação do produto: ')
    var_produto.save()

def deletar_produto():
    produto_deletar = input('Qual produto você deseja deletar? ')
    var_produto = select(Produto).where(produto_deletar == Produto.nome_produto)
    var_produto = db_session.execute(var_produto).scalar()
    var_produto.delete()



def inserir_categoria():
    categoria = Categoria(
        nome_categoria=str(input('nome da categoria: ')),
    )
    print(categoria)
    categoria.save()

def atualizar_categoria():
    var_categoria = select(Categoria).where(str(input('Nome da categoria: ')) == Categoria.nome_categoria)
    var_categoria = db_session.execute(var_categoria).scalar()
    print(var_categoria)
    var_categoria.nome_categoria = str(input('Novo nome da categorioa: '))
    var_categoria.save()

def consultar_categoria():
    var_categoria = select(Categoria)
    var_categoria = db_session.execute(var_categoria).all()
    print(var_categoria)

def deletar_categoria():
    categoria_deletar = input('Qual categoria vc desesja apagar? ')
    var_categoria = select(Categoria).where(categoria_deletar == Categoria.data)
    var_categoria = select(Categoria).where(categoria_deletar == Categoria.hora)
    var_categoria = db_session.execute(var_categoria).scalar()
    var_categoria.delete()



def entrada_saida():
    entrada_saida = Entrada_saida(
        qtd = int(input('quantidade do produto: ')),
        data = str(input('data da entrada ou saida: ')),
        tipo = str(input('tipo: ')),
        id_produtos=int(input('id_produtos: ')),
        idFuncionario= int(input('idFuncionario: ')),
    )
    print(entrada_saida)
    entrada_saida.save()

def atualizar_entrada_saida():
    var_entrada_saida = select(Entrada_saida).where(Entrada_saida.data == str(input('data da entrada ou saida: ')) == Entrada_saida.data)
    var_entrada_saida = select(Entrada_saida).where(Entrada_saida.qtd == str(input('qtd do produto: ')) == Entrada_saida.qtd)
    var_entrada_saida = select(Entrada_saida).where(Entrada_saida.tipo == str(input('tipo do produto: ')) == Entrada_saida.tipo)
    var_entrada_saida = db_session.execute(var_entrada_saida).scalar()
    print(var_entrada_saida)
    var_entrada_saida.data = str(input('Nova data: '))
    var_entrada_saida.qtd = str(input('Nova quantidade: '))
    var_entrada_saida.tipo = str(input('Novo tipo do produto: '))
    var_entrada_saida.save()

def consultar_entrada_saida():
    var_entrada_saida = select(Entrada_saida)
    var_entrada_saida = db_session.execute(var_entrada_saida).all()
    print(var_entrada_saida)

def deletar_entrada_saida():
    entrada_saida_deletar = input('Qual entrada ou saida vc precisa deletear? ')
    var_entrada_saida = select(Entrada_saida).where(entrada_saida_deletar == Entrada_saida.data,)
    var_entrada_saida = db_session.execute(var_entrada_saida).scalar()
    var_entrada_saida.delete()

if __name__ == '__main__':
    while True:
        print("MENU")
        print("1 - inserir funcionario")
        print("2 - atualizar funcionario")
        print("3 - deletar funcionario")
        print("4 - consultar funcionario")
        print("5 - inserir produto")
        print("6 - atualizar produto")
        print("7 - deletar produto")
        print("8 - consultar produto")
        print("9 - inserir categoria")
        print("10 - atualizar categoria")
        print("11 - deletar categoria")
        print("12 - consultar categoria")
        print("13 -  inserir entrada saida")
        print("14 - atualizar entrada saida")
        print("15 - consultar entrada saida")
        print("16 - deletar entrada saida")
        print("0 -  sair ")
        escolha = input('Escolha: ')
        if escolha == '1':
            inserir_funcionario()
        elif escolha == '2':
            atualizar_funcionario()
        elif escolha == '3':
            deletar_funcionario()
        elif escolha == '4':
            consultar_funcionario()
        elif escolha == '5':
            inserir_produto()
        elif escolha == '6':
            atualizar_produto()
        elif escolha == '7':
            deletar_produto()
        elif escolha == '8':
            consultar_produto()
        elif escolha == '9':
            inserir_categoria()
        elif escolha == '10':
            atualizar_categoria()
        elif escolha == '11':
            deletar_categoria()
        elif escolha == '12':
            consultar_categoria()
        elif escolha == '13':
            entrada_saida()
        elif escolha == '14':
            atualizar_entrada_saida()
        elif escolha == '15':
            consultar_entrada_saida()
        elif escolha == '16':
            deletar_entrada_saida()
        elif escolha == '0':
            break




