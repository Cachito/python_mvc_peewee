"""
módulo de clases.
"""

from peewee import *

cm_pw_db = MySQLDatabase('carro_maier_peewee', user='root', passwd='')

class MySQLModel(Model):
    """
    A base model that will use our MySQL database
    """
    class Meta:
        """
        metadata
        """
        database = cm_pw_db

class Medio(MySQLModel):
    """
    representa un medio
    """
    class Meta:
        """
        metadata
        """
        Database = cm_pw_db
        table_name = "Medios"

    Id = IntegerField(primary_key=True, unique=True)
    Descripcion = FixedCharField(max_length=128)

class Seccion(MySQLModel):
    """
    representa una sección/suplemento
    en un medio
    """
    class Meta:
        """
        metadata
        """
        Database = cm_pw_db
        table_name = "Secciones"

    Id = IntegerField(primary_key=True, unique=True)
    #IdMedio = ForeignKeyField(Medio, backref='Medios', field="IdMedio", to_field="Id")
    #IdMedio = ForeignKeyField(column_name = "IdMedio", model = Medio)
    Medio = ForeignKeyField(Medio, backref = 'Medios')
    Descripcion = FixedCharField(max_length=128)

class Noticia(MySQLModel):
    """
    representa una Noticia.
    """
    class Meta:
        """
        metadata
        """
        Database = cm_pw_db
        table_name = "Noticias"

    Id =  IntegerField(primary_key=True, unique=True, constraints=[SQL('AUTO_INCREMENT')]) #PrimaryKeyField()
    Fecha = DateField()
    #IdMedio = ForeignKeyField(Medio, backref='Medios', field="IdMedio", to_field="Id")
    #IdMedio = ForeignKeyField(column_name = "IdMedio", model = Medio)
    Medio = ForeignKeyField(Medio, backref = 'Medios')
    #IdSeccion = ForeignKeyField(Seccion, backref='Secciones', field="IdSeccion", to_field="Id")
    #IdSeccion = ForeignKeyField(column_name = "IdSeccion", model = Seccion)
    Seccion = ForeignKeyField(Seccion, backref = 'Secciones')
    Titulo = FixedCharField(max_length=128)
    Cuerpo = CharField()

class NoticiaDto:
    def __init__(self, id_nota, fecha, id_medio, id_seccion, titulo, cuerpo, medio, seccion):
        self.id_nota = id_nota
        self.fecha = fecha
        self.id_medio = id_medio
        self.id_seccion = id_seccion
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.medio = medio
        self.seccion = seccion