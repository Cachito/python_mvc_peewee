"""
Módulo model.py
"""
import re
import pymysql
import peewee
import modulos.constant as constants
from modulos.clases import *

class CmpModel:
    """
    Clase Model
    Obtiene y guarda en base de datos.
    """
    def create_db(self):
        """
        crea la base de datos carro_maier
        si existe, la elimina
        - peewee no puede crear una base de datos MtSQL.
        - por esto uso pymysql
        """
        db_conn = pymysql.connect(host='localhost', user='root', password='')
        sql_drop = "DROP DATABASE IF EXISTS carro_maier_peewee"
        sql_create = "CREATE DATABASE carro_maier_peewee"

        try:
            db_conn.cursor().execute(sql_drop)
            db_conn.cursor().execute(sql_create)

            db_conn.commit()

        except Exception as e:
            raise Exception(f'Error al crear base de datos (model): {str(e)}') from e

        finally:
            db_conn.close()

    def create_tables(self):
        """
        crea las tablas
        - noticias
        - medios
        - secciones
        si existe, la elimina
        """
        try:
            cm_pw_db.connect()

            models = [Seccion, Medio, Noticia]
            cm_pw_db.drop_tables(models)
            cm_pw_db.create_tables(models)

        except Exception as e:
            raise Exception(f'Error al crear tablas (model): {str(e)}') from e

        finally:
            cm_pw_db.close()

    def populate_tables(self):
        """
        carga registros las tablas
        - medios
        - secciones
        si existen, los elimina
        """
        try:
            medio = self.get_or_add_medio(32, 'Ámbito Financiero')
            self.get_or_add_seccion(medio, 145, 'Ámbito Nacional')
            self.get_or_add_seccion(medio, 411, 'Cuerpo Principal')

            medio = self.get_or_add_medio(36, 'BAE')
            self.get_or_add_seccion(medio, 80, 'Política Económica')
            self.get_or_add_seccion(medio, 81, 'BAE inversor')
            self.get_or_add_seccion(medio, 82, 'Empresas & Negocios')

            medio = self.get_or_add_medio(299, 'Buenos Aires Herald')
            self.get_or_add_seccion(medio, 415, 'Argentina')
            self.get_or_add_seccion(medio, 422, 'Day by Day')

            medio = self.get_or_add_medio(38, 'Clarín')
            self.get_or_add_seccion(medio, 93, 'Sociedad')
            self.get_or_add_seccion(medio, 94, 'Cultura')
            self.get_or_add_seccion(medio, 96, 'Policiales')

            medio = self.get_or_add_medio(221, 'Página 12 Online')
            self.get_or_add_seccion(medio, 871, 'Supl. - Cash')
            self.get_or_add_seccion(medio, 136, 'Supl. - Las 12')
            self.get_or_add_seccion(medio, 103, 'Espectáculos')

        except Exception as e:
            raise Exception(f'Error al insertar registros (model): {str(e)}') from e

    def get_or_add_medio(self, id_medio, descripcion):
        """
        intenta obtener un medio
        """
        if not cm_pw_db.is_closed():
            cm_pw_db.close()

        cm_pw_db.connect()
        medio = Medio()

        try:
            medio = Medio.select().where(Medio.Id == id_medio).get()

        except peewee.DoesNotExist:
            medio = Medio.create(Id = id_medio, Descripcion = descripcion)

        finally:
            cm_pw_db.close()

        return medio

    def get_or_add_seccion(self, medio, id_seccion, descripcion):
        """
        intenta obtener una seccion
        """
        if not cm_pw_db.is_closed():
            cm_pw_db.close()

        cm_pw_db.connect()
        seccion = Seccion()

        try:
            seccion = Seccion.select().where(Seccion.Id == id_seccion).get()

        except peewee.DoesNotExist:
            seccion = Seccion.create(Id = id_seccion, Medio = medio, Descripcion = descripcion)

        finally:
            cm_pw_db.close()

        return seccion

    def get_medios(self):
        """
        devuelve todos los registros
        de la tabla medios
        ordenados por descripción
        """
        m_list = []

        try:
            if not cm_pw_db.is_closed():
                cm_pw_db.close()

            cm_pw_db.connect()

            m_list = list(Medio.select().order_by(Medio.Descripcion))

        except Exception as e:
            raise Exception(f'Error al obtener medios (model): {str(e)}') from e

        finally:
            cm_pw_db.close()

        return m_list

    def get_secciones(self, id_medio):
        """
        devuelve todos los registros
        de la tabla secciones
        según id_medio indicado
        ordenados por descripción
        """
        s_list = []

        try:
            if not cm_pw_db.is_closed():
                cm_pw_db.close()

            cm_pw_db.connect()

            medio = Medio.select().where(Medio.Id == id_medio).get()

            s_list = list(Seccion.select().where(Seccion.Medio == medio).order_by(Seccion.Descripcion))

        except Exception as e:
            raise Exception(f'Error al obtener secciones (model): {str(e)}') from e

        finally:
            cm_pw_db.close()

        return s_list

    def get_noticia(self, search_id):
        """
        devuelve un registro según search_id
        si lo encuentra
        """
        try:
            if not cm_pw_db.is_closed():
                cm_pw_db.close()

            cm_pw_db.connect()

            noticia = Noticia.select().where(Noticia.Id == search_id).get()

            cm_pw_db.close()

        except peewee.DoesNotExist:
            raise Exception(f'La noticia id {search_id} no existe (model)')

        except Exception as e:
            raise Exception(f'Error al obtener noticia (model): {str(e)}') from e

        finally:
            cm_pw_db.close()

        return noticia

    def get_noticias(self):
        """
        devuelve todos los registros
        de la tabla noticias
        ordenados por fecha
        """
        try:
            if not cm_pw_db.is_closed():
                cm_pw_db.close()

            cm_pw_db.connect()

            noticias = Noticia.select()

            cm_pw_db.close()

            return noticias

        except Exception as e:
            raise Exception(f'Error al obtener noticias (model): {str(e)}') from e

        finally:
            cm_pw_db.close()

    def save_data(self, noticia):
        """
        guarda una noticia
        """

        titulo = re.sub("[\"']", r"", noticia[constants.TITULO])
        cuerpo = re.sub("[\"']", r"", noticia[constants.CUERPO])

        try:
            if not cm_pw_db.is_closed():
                cm_pw_db.close()

            cm_pw_db.connect()

            medio = Medio.select().where(Medio.Id == noticia[constants.ID_MEDIO]).get()
            seccion = Seccion.select().where(Seccion.Id == noticia[constants.ID_SECCION]).get()

            if noticia[constants.ID_NOTICIA] == 0: \
                Noticia.create(Fecha = noticia[constants.FECHA], Medio = medio, Seccion = seccion, \
                Titulo = titulo, Cuerpo = cuerpo)

            else:
                noticia_data = Noticia.select().where(Noticia.Id == noticia[constants.ID_NOTICIA]).get()

                noticia_data.Fecha = noticia[constants.FECHA]
                noticia_data.Medio = medio
                noticia_data.Seccion = seccion
                noticia_data.Titulo = titulo
                noticia_data.Cuerpo = cuerpo

                noticia_data.save()

            cm_pw_db.close()

        except Exception as e:
            raise Exception(f'Error al guardar noticia (model): {str(e)}') from e

        finally:
            cm_pw_db.close()

    def delete_data(self, search_id):
        """
        elimina un registro según search_id
        si lo encuentra
        """
        try:
            if not cm_pw_db.is_closed():
                cm_pw_db.close()

            cm_pw_db.connect()

            query = Noticia.delete().where (Noticia.Id == search_id)
            query.execute()

            #noticia = Noticia.select(Noticia.Id == search_id).get()
            #noticia.delete_instance()

            cm_pw_db.close()

        except peewee.DoesNotExist:
            raise Exception(f'La noticia id {search_id} no existe (model)')

        except Exception as e:
            raise Exception(f'Error al eliminar noticia (model): {str(e)}') from e

        finally:
            cm_pw_db.close()
