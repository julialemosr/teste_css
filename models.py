from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base
#configuração base de dados
engine = create_engine('sqlite:///controle_estoque.sqlite3') #nome do banco
db_session = scoped_session(sessionmaker(bind=engine))


#modo declarativo
Base = declarative_base()
Base.query = db_session.query_property()

#Pessoas que tem atividade
class Funcionario(Base):
    __tablename__ = 'TAB_FUNCIONARIO'
    id_funcionario = Column(Integer, primary_key=True)
    CPF = Column(Integer, nullable=False, index=True, unique=True)
    nome_funcionario = Column(String(50), nullable=False, index=True)
    email = Column(String(70), nullable=False, index=True) #string o tamanho dele


    def __repr__(self):
        return '<Funcionario: {} {} {} {}>' .format(self.id_funcionario, self.CPF, self.nome_funcionario, self.email, )


    def save(self) -> object:
        db_session.add(self)
        db_session.commit()

#função para deletar
    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_funcionario(self):
        dados_funcionario = {
            'id_funcionario': self.id_funcionario,
            'CPF': self.CPF,
            'nome_funcionario': self.nome_funcionario,
            'email': self.email,
        }
        return dados_funcionario



class Produto(Base):
    __tablename__ = 'TAB_PRODUTO'
    id_produto = Column(Integer, primary_key=True)
    nome_produto = Column(String(70), nullable=False, index=True)
    valor_produto = Column(Float, nullable=False, index=True)
    data_fabricacao = Column(String(8), nullable=False, index=True)
    iDcategoria = Column(Integer, ForeignKey('TAB_CATEGORIA.id_categoria'))  # string o tamanho dele
    categoria = relationship('Categoria')


    def __repr__(self):
        return '<Produto: {} {} {} {} {}>' .format(self.id_produto, self.nome_produto, self.valor_produto, self.data_fabricacao, self.iDcategoria)

#função para salvar no banco

    def save(self):
        db_session.add(self)#seção de acesso
        db_session.commit() #salva a informação

#função para deletar
    def delete(self):
        db_session.delete(self)#deletar
        db_session.commit()# salvar

    def serialize_produto(self):
        dados_produto = {
            'id_produto': self.id_produto,
            'nome_produto': self.nome_produto,
            'valor_produto': self.valor_produto,
            'data_fabricacao': self.data_fabricacao,
            'iDcategoria': self.iDcategoria,
        }
        return dados_produto



class Categoria(Base):
    __tablename__ = 'TAB_CATEGORIA'
    id_categoria = Column(Integer, primary_key=True)
    nome_categoria = Column(String(30), nullable=False, index=True)


    def __repr__(self):
        return '<Categoria: {} {}>' .format(self.id_categoria, self.nome_categoria)#self ele chama ele mesmo



    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_categoria(self):
        dados_categoria = {
            'id_categoria': self.id_categoria,
            'nome_categoria': self.nome_categoria,
        }
        return dados_categoria


class Entrada_saida(Base):
    __tablename__ = 'TAB_ENTRADA_SAIDA' #nome da tabela
    id_entrada_saida = Column(Integer, primary_key=True) #chave primaria (unico) integer = tipo de dado
    tipo = Column(String(10), nullable=False, index=True) #nullable tem que obrigatoriamente preencher o espaço
    data = Column(String(27), nullable=False, index=True)# index pesquisa
    qtd = Column(Integer, nullable=False, index=True) #string o tamanho dele
    idFuncionario = Column(Integer, ForeignKey('TAB_FUNCIONARIO.id_funcionario'))#string o tamanho dele
    funcionario = relationship('Funcionario')
    id_produtos = Column(Integer, ForeignKey('TAB_PRODUTO.id_produto'))
    produto = relationship('Produto')
    #colum = coluna

    def __repr__(self):
        return '<Entrada_saida: {} {} {} {} {}>' .format(self.id_entrada_saida, self.data, self.qtd, self.tipo, self.idFuncionario, self.id_produtos)#self ele chama ele mesmo

#função para salvar no banco

    def save(self):
        db_session.add(self)#seção de acesso
        db_session.commit() #salva a informação

#função para deletar
    def delete(self):
        db_session.delete(self)#deletar
        db_session.commit()# salvar

    def serialize_entrada_saida(self):
        dados_entrada_saida = {
            'id_entrada_saida': self.id_entrada_saida,
            'tipo': self.tipo,
            'data': self.data,
            'qtd_entrada': self.qtd,
            'idFuncionario': self.idFuncionario,
            'id_produtos': self.id_produtos,

        }
        return dados_entrada_saida


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()