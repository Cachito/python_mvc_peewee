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

    def __str__(self):
        return f'{self.Descripcion} - ({self.Id})'
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
    Medio = ForeignKeyField(Medio, backref = 'Medios')
    Descripcion = FixedCharField(max_length=128)

    def __str__(self):
        return f'{self.Descripcion} - ({self.Id})'
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
    Medio = ForeignKeyField(Medio, backref = 'Medios')
    Seccion = ForeignKeyField(Seccion, backref = 'Secciones')
    Titulo = FixedCharField(max_length=128)
    Cuerpo = TextField()
