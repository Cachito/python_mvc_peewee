"""
Módulo controller.py
"""
import datetime
import traceback

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
            self.view.salta_violeta("Carro-Maier", "Base de datos carro_maier_peewee creada con éxito")

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al intentar base: {str(e)}")

    def create_tables(self):
        """
        crea las tablas
        - noticias
        - medios
        - secciones
        """
        try:
            self.model.create_tables()
            self.view.salta_violeta(
                "Carro-Maier", "Tablas `Noticias`, `Medios` y `Secciones` creadas con éxito.")

        except Exception as e:
            self.view.salta_violeta(
                "Error Carro-Maier", f"error al intentar crear tablas: {str(e)}")

    def get_medios(self):
        """
        devuelve una lista con los medios en
        base de datos
        """
        try:
            return self.model.get_medios()

        except Exception as e:
            self.view.salta_violeta(
                "Error Carro-Maier", f"error al intentar obtener medios: {str(e)}")

    def get_secciones(self, id_medio):
        """
        devuelve una lista con las secciones en
        base de datos según el id_medio indicado
        """
        try:
            return self.model.get_secciones(id_medio)

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al intentar obtener secciones: {str(e)}")

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
            self.view.set_noticia(noticia)

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al intentar obtener noticia: {str(e)}")

    def get_noticias(self):
        """
        devuelve todas las noticias
        """
        try:
            return self.model.get_noticias()

        except Exception as e:
            self.view.salta_violeta("Error Carro-Maier", f"error al intentar obtener noticias: {str(e)}")

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
                self.view.salta_violeta("Carro-Maier", f"registro {'insertado' if noticia.id == 0 else f'{noticia.id} actualizado'} con éxito")
                self.view.refresh()
                self.view.clear_data()

        except Exception as e:
            traceback.print_exc()
            self.view.salta_violeta("Error Carro-Maier", f"error al intentar guardar noticia: {str(e)}")

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
            self.view.salta_violeta("Error Carro-Maier", f"error al intentar eliminar noticia: {str(e)}")

    def valida(self, noticia):
        """
        Args:
            noticia (Noticia): Objeto noticia a validar
        Returns:
            bool: True si todo está bien
        """
        msj_error = ""

        if not noticia.fecha:
            msj_error = " fecha "
        else:
            try:
                datetime.datetime.strptime(noticia.fecha, '%Y-%m-%d')
            except ValueError:
                msj_error = " el formato de la fecha debe ser YYYY-MM-dd"

        if not noticia.id_medio or noticia.id_medio == 0:
            msj_error = f"{msj_error} medio "

        if not noticia.id_seccion or noticia.id_seccion == 0:
            msj_error = f"{msj_error} seccion "

        if not noticia.titulo:
            msj_error = f"{msj_error} título "

        if not noticia.cuerpo:
            msj_error = f"{msj_error} cuerpo "

        if msj_error:
            self.view.salta_violeta("Carro-Maier", f"debe ingresar: {msj_error}")
            return False
        else:
            return True
