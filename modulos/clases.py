"""
módulo de clases.
"""

from peewee import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

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

    IdMedio = ForeignKeyField(Medio, backref='Medios')
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

    Fecha = DateField()
    IdMedio = ForeignKeyField(Medio, backref='Medios')
    IdSeccion = ForeignKeyField(Seccion, backref='Secciones')
    Titulo = FixedCharField(max_length=128)
    Cuerpo = CharField()

    #def __init__(self, id_nota, fecha, id_medio, id_seccion, titulo, cuerpo):
    #    self.id = id_nota
    #    self.Fecha = fecha
    #    self.IdMedio = id_medio
    #    self.IdSeccion = id_seccion
    #    self.Titulo = titulo
    #    self.Cuerpo = cuerpo
