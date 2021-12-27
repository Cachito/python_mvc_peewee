"""
módulo de clases.
"""

from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class Noticia:
    """
    clase Noticia.
    """
    def __init__(self, id_nota, fecha, id_medio, id_seccion, titulo, cuerpo):
        self.id = id_nota
        self.fecha = fecha
        self.id_medio = id_medio
        self.id_seccion = id_seccion
        self.titulo = titulo
        self.cuerpo = cuerpo
