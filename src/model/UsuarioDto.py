import sirope
import flask_login
import werkzeug.security as safe
from model.publicacionDto import publicacionDto

class UsuarioDto(flask_login.UserMixin):
    """
    Clase que representa a un usuario.

    Atributos
    ----------

    nombreUsuario :
        nombre del usuario
    email :
        email del usuario
    _password : 
        contraseña del usuario

    Métodos
    -------
    get_id()
        Devuelve el id (email) del usuario.

    anhadir_publicacion(texto, imagen)
        Crea y añade una publicación a la lista de publicaciones del usuario.

    ultima_publicacion()
        Devuelve la última publicación del usuario.

    ultimas_publicaciones()
        Devuleve las 5 últimas publicaciones del usuario.

    publicaciones()
        Devuleve todas las publicaciones del usuario.

    chk_password(pswd)
        Comprueba si "pswd" y _password coinciden.

    change_password(pswd)
        Cambia el valor de _password por "pswd".

    current_user()
        Devuelve el usuario que está actualmente logeado.

    find(s: sirope.Sirope, email: str)
        Comprueba si existe el usuario con el atributo "email" usando sirope "s".
    """
    
    def __init__(self, nombreUsuario, email, password):
        self.__nombreUsuario = nombreUsuario
        self._email = email
        self._password = safe.generate_password_hash(password)
        self.__publicaciones = []

    @property
    def email(self):
        return self._email
    
    @property
    def nombreUsuario(self):
        return self.__nombreUsuario
    
    @nombreUsuario.setter
    def nombreUsuario(self, nuevoNombre):
        self.__nombreUsuario = nuevoNombre
    
    def get_id(self):
        return self.email

    def anhadir_publicacion(self, texto : str, imagen : str):
        lista = []
        lista.count
        id = self.ultima_publicacion() + 1
        publicacion = publicacionDto(self._email, self.__nombreUsuario, id, texto, imagen)
        self.__publicaciones.append(id)
        return publicacion

    def ultima_publicacion(self):
        if self.__publicaciones == []:
            return 0
        else:
            return self.__publicaciones[-1]

    def ultimas_publicaciones(self):
        return self.__publicaciones[-5:]
    
    def publicaciones(self):
        return self.__publicaciones
    
    def chk_password(self, pswd : str):
        return safe.check_password_hash(self._password, pswd)
    
    def change_password(self, pswd : str):
        self._password = safe.generate_password_hash(pswd)
    
    @staticmethod
    def current_user():
        usr = flask_login.current_user
        return usr

    @staticmethod
    def find(s: sirope.Sirope, email: str) -> "UsuarioDto":
        return s.find_first(UsuarioDto, lambda u: u.email == email)