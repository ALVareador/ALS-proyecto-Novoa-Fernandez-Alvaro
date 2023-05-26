class publicacionDto:
    """
    Clase que representa a una publicación.

    Atributos
    ----------

    email : str
        email del usuario que escribió la publicación
    usuario : str
        nombre del usuario que escribió la publicación
    id : int
        id de la publicación
    texto : str, optional
        texto de la publlicación
    imagen : optional
        imagen de la publicación
    puntuacion : int
        Puntuación de la publicación
    comentarios : list
        Comentarios en la publicación
    """

    def __init__(self, email : str, usuario : str, idPublicacion : int, texto : str, imagen : str) -> None:
        self.__email = email
        self.__usuario = usuario
        self.__id = idPublicacion
        self.__texto = texto
        self.__imagen = imagen
        self.__puntuacion = 0
        self.__comentarios = []

    @property
    def id(self):
        return self.__id
    
    @property
    def email(self):
        return self.__email
    
    @property
    def texto(self):
        return self.__texto
    
    @property
    def imagen(self):
        return self.__imagen
    
    @property
    def usuario(self):
        return self.__usuario
    
    @property
    def puntuacion(self):
        return self.__puntuacion
    
    @property
    def comentarios(self):
        return self.__comentarios
    
    def puntuacionMas(self):
        self.__puntuacion = self.__puntuacion + 1

    def puntuacionMenos(self):
        self.__puntuacion = self.__puntuacion - 1

    def anhadirComentario(self, comentario : str):
        self.__comentarios.append(comentario)
