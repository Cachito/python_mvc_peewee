"""
Módulo controller.py
"""
import datetime
import traceback
from modulos.clases import *
import modulos.constant as constants

class Controller:
    """
    Clase Controller
    Intermediario entre la vista y el modelo.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def create_db(self):
        """
        crea la base de datos carro_maier_peewee
        """
        try:
            self.model.create_db()
            self.model.create_tables()
            self.view.salta_violeta("Carro-Maier", "Base de datos carro_maier_peewee y tablas creados con éxito")

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al crear base o tablas (controller): {str(e)}")

    def populate_tables(self):
        """
        inserta registros en las tablas
        - medios
        - secciones
        """
        try:
            self.model.populate_tables()
            self.view.salta_violeta(
                "Carro-Maier", "Registros insertados con éxito en tablas `Medios` y `Secciones`.")

        except Exception as e:
            self.view.salta_violeta(
                "Error Carro-Maier", f"error al insertar registros (controller): {str(e)}")

    def get_medios(self):
        """
        devuelve una lista con los medios en
        base de datos
        """
        try:
            return self.model.get_medios()

        except Exception as e:
            self.view.salta_violeta(
                "Error Carro-Maier", f"error al intentar obtener medios (controller): {str(e)}")

    def get_secciones(self, id_medio):
        """
        devuelve una lista con las secciones en
        base de datos según el id_medio indicado
        """
        try:
            return self.model.get_secciones(id_medio)

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al intentar obtener secciones (controller): {str(e)}")

    def get_noticia(self, search_id):
        """
        Args:
            search_id (entero): is de la noticia a buscar
        Returns:
            Noticia: La noticia completa según el search_id recibido
        """
        if not search_id:
            self.view.salta_violeta("Carro-Maier", "Debe seleccionar algo")
            return

        try:
            noticia = self.model.get_noticia(search_id)
            data = noticia.Id, noticia.Fecha, f'{noticia.Medio.Descripcion} - ({noticia.Medio.Id})', \
                f'{noticia.Seccion.Descripcion} - ({noticia.Seccion.Id})', noticia.Titulo, noticia.Cuerpo, \
                noticia.Medio.Id, noticia.Seccion.Id

            self.view.set_noticia(data)

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al obtener noticia (controller): {str(e)}")

    def get_noticias(self):
        """
        devuelve todas las noticias
        """
        noticias = []

        try:
            data = self.model.get_noticias()
            for n in data:
                fecha = n.Fecha.strftime("%Y-%m-%d")
                id_nota = str(n.Id)
                id_medio = str(n.Medio.Id)
                id_seccion = str(n.Seccion.Id)
                n_dto = id_nota, fecha, n.Medio.Descripcion, n.Seccion.Descripcion, n.Titulo, n.Cuerpo, id_medio, id_seccion
                noticias.append(n_dto)

            return noticias

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al obtener noticias (controller): {str(e)}")

    def save_data(self, noticia):
        """
        recibe un objeto Noticia
        valida los datos en el objeto recibido
        invoca al modelo para guardar
        actualiza la vista
        limpia los campso de carga
        """
        try:
            if self.valida(noticia):
                self.model.save_data(noticia)
                self.view.salta_violeta("Carro-Maier", \
                    f"registro {'insertado' if noticia[constants.ID_NOTICIA] == 0 else f'{noticia[constants.ID_NOTICIA]} actualizado'} con éxito")
                self.view.refresh()
                self.view.clear_data()

        except Exception as e:
            traceback.print_exc()
            self.view.salta_violeta("Error Carro-Maier", f"error al guardar noticia (controller): {str(e)}")

    def delete_data(self, search_id):
        """
        recibe un entero
        comprueba el valor
        invoca eliminación
        actualiza la vista
        limpa los campos
        """
        if not search_id or search_id == 0:
            self.view.salta_violeta("Carro-Maier", "Debe seleccionar algo")
            return

        try:
            self.model.delete_data(search_id)
            self.view.salta_violeta("Carro-Maier", f"Registro id:{search_id} eliminado")
            self.view.refresh()
            self.view.clear_data()

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al eliminar noticia (controller): {str(e)}")

    def valida(self, noticia):
        """
        Args:
            noticia (Noticia): Objeto noticia a validar
        Returns:
            bool: True si todo está bien
        """
        msj_error = ""

        if not noticia[constants.FECHA]:
            msj_error = " fecha "
        else:
            try:
                datetime.datetime.strptime(noticia[constants.FECHA], '%Y-%m-%d')
            except ValueError:
                msj_error = " el formato de la fecha debe ser YYYY-MM-dd"

        if not noticia[constants.ID_MEDIO] or noticia[constants.ID_MEDIO] == 0:
            msj_error = f"{msj_error} medio "

        if not noticia[constants.ID_SECCION] or noticia[constants.ID_SECCION] == 0:
            msj_error = f"{msj_error} seccion "

        if not noticia[constants.TITULO]:
            msj_error = f"{msj_error} título "

        if not noticia[constants.CUERPO]:
            msj_error = f"{msj_error} cuerpo "

        if msj_error:
            self.view.salta_violeta("Carro-Maier", f"debe ingresar: {msj_error}")
            return False
        else:
            return True
