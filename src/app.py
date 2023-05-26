import flask
import base64
from flask import json
import sirope
import flask_login
from flask_login import login_manager
import re
from model.UsuarioDto import UsuarioDto
from model.publicacionDto import publicacionDto

def crea_app():
    app = flask.Flask(__name__)
    app.config.from_file("config.json", load= json.load)
    src = sirope.Sirope()
    lm = login_manager.LoginManager()
    lm.init_app(app)
    return src, app, lm

srp, app, lm = crea_app()

@lm.user_loader
def user_loader(email):
    return UsuarioDto.find(srp, email)

@app.route("/", methods=["GET"])
def index():
    """Pantalla principal de la aplicación

    En esta patalla se pueden observar las últimas publicaciones de todos los usuarios,
    además se puede acceder al resto de funcionalidades desde esta.
    """

    # Obtener últimas publicaciones
    lista_publicaciones = srp.load_last(publicacionDto, 10)

    # Obtener últimos publicaciones del usuario actual
    lista_publicaciones_current_usr = []
    if UsuarioDto.current_user().__class__ != flask_login.mixins.AnonymousUserMixin:
        lista_publicaciones_todas = srp.load_all(publicacionDto)

        for publicacion in lista_publicaciones_todas:
            pass
            if publicacion.email == UsuarioDto.current_user().email:
                lista_publicaciones_current_usr.append(publicacion)

    # Guardar publicaciones a visualizar
    datos = {

        "lista_publicaciones": list(lista_publicaciones),
        "lista_publicaciones_current_usr": list(lista_publicaciones_current_usr),
        "usuario_ha_iniciado_sesion": (UsuarioDto.current_user().__class__ != flask_login.mixins.AnonymousUserMixin)

    }

    return flask.render_template("index.html", **datos)

@app.route("/publicar", methods=["POST"])
def publicar():
    """Permite al usuario guardar una nueva publicación

    Este método comprueba que la nueva publicación no estea vacía, 
    y la guarda usando sirope.
    """

    usr = UsuarioDto.current_user()
    if flask.request.method == "POST":

        texto = flask.request.form["edMensaje"].strip()
        imagen = flask.request.files["edImagen"]
        image_b64 = base64.b64encode(imagen.read()).decode('utf-8')  

        # Comprobar publicación
        if not texto and not imagen:
            flask.flash("La publicación no puede estar vacía", "post_warnings")
        else:
            if usr:
                #Guardar publicación
                publicacion = usr.anhadir_publicacion(texto, image_b64)
                srp.save(usr)
                srp.save(publicacion)
                
    return flask.redirect("/")

@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    """Permite al usuario crear una cuenta

    Este método comprueba los datos introducidos por el usuario (nombre de usuario, 
    correo electónico y contraseña) y crea una nueva cuenta.
    """
    if flask.request.method == "POST":

        usuario = flask.request.form["username"]
        email = flask.request.form["email"]
        contrasenha = flask.request.form["password"]

        # Comprobamos que no estean vacíos
        if not email:
            flask.flash("No olvides tu correo electrónico!", "register_email_warning")
            return flask.redirect("/") 
        elif not contrasenha:
            flask.flash("Necesitas una contraseña!", "register_password_warning")
            return flask.redirect("/") 
        elif not usuario:
            flask.flash("Necesitas un usuario!", "register_username_warning")
            return flask.redirect("/") 
        else:
            # Comprobamos el formato
            if not re.match(r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$", email):
                flask.flash("Ese no es un correo válido!", "register_email_warning")
                return flask.redirect("/")
            elif len(contrasenha) < 8:
                flask.flash("Tu contraseña es demasiado corta, debe tener al menos 8 caracteres.", "register_password_warning")
                return flask.redirect("/")
            elif re.search('[0-9]',contrasenha) is None:
                print()
                flask.flash("Tu contraseña debe incluir al menos un numero.", "register_password_warning")
                return flask.redirect("/")
            elif (re.search('[a-z]',contrasenha) is None) and (re.search('[A-Z]',contrasenha) is None):
                flask.flash("Tu contraseña debe incluir al menos una letra.", "register_password_warning")
                return flask.redirect("/")
            else:
                # Comprobamos si ese correo ya está registrado
                usr = UsuarioDto.find(srp, email)
                if not usr:
                    usr = UsuarioDto(usuario , email, contrasenha)
                    srp.save(usr)
                    flask_login.login_user(usr)
                    return flask.redirect("/")
                else:
                    flask.flash("Ese correo electrónico ya está registrado.", "register_email_warning")
                    return flask.redirect("/")
            
    return flask.redirect("/")
    
@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    """Permite al usuario iniciar sesion

    Este método comprueba los datos introducidos por el usuario (correo electónico y contraseña) 
    y si dichos datos son correctos inicia sesion.
    """

    if flask.request.method == "POST":
        email = flask.request.form["email"]
        contrasenha = flask.request.form["password"]

        # Comprobamos que no estean vacíos
        if not email:
            flask.flash("Introduce un usuario", "login_email_warning")
        elif not contrasenha:
            flask.flash("Introduce un contraseña", "login_password_warning")
        else:
            # Comprobamos el formato
            if not re.match(r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$", email):
                flask.flash("Ese no es un correo válido!", "login_email_warning")
                return flask.redirect("/")
            else:
                # Comprobamos si existe el usuario
                usr = UsuarioDto.find(srp, email)
                if not usr or not usr.chk_password(contrasenha):
                    flask.flash("Contraseña incorrecta.", "login_password_warning")
                    return flask.redirect("/")
            
                flask_login.login_user(usr)
                
    return flask.redirect("/")

@app.route("/cerrar_sesion", methods=["POST"])
def cerrar_sesion():
    """Permite al usuario cerrar sesion

    Este método cierra la sesion del usuario actual.
    """

    if UsuarioDto.current_user().__class__ != flask_login.mixins.AnonymousUserMixin:
        flask_login.logout_user()

    return flask.redirect("/")

@app.route("/borrar_cuenta", methods=["POST"])
def borrar_cuenta():
    """Permite al usuario borrar su cuenta

    Este método permite al usuario borrar su cuenta y todas sus publicaciones 
    tras introducir su contraseña.
    """

    contrasenha = flask.request.form["password"]

    # Comprobamos que no estea vacía
    if not contrasenha:
        flask.flash("Introduce un contraseña", "delete_account_password_warnings")
    else:
        # Comprobamos si la contraseña es correcta
        usr = UsuarioDto.find(srp, UsuarioDto.current_user().email)
        if not usr or not usr.chk_password(contrasenha):
            flask.flash("Contraseña incorrecta", "delete_account_password_warnings")
            return flask.redirect("/")

        # Cerramos sesión del usuario
        if UsuarioDto.current_user().__class__ != flask_login.mixins.AnonymousUserMixin:
            flask_login.logout_user()

        # Borrar publicaciones usuario
        lista_publicaciones_todas = srp.load_all(publicacionDto)

        for publicacion in lista_publicaciones_todas:
            if publicacion.email == usr.email:
                srp.delete(publicacion.__oid__)

        # Borrar usuario
        srp.delete(usr.__oid__)

    return flask.redirect("/")

@app.route("/cambiar_contrasenha", methods=["POST"])
def cambiar_contrasenha():
    """Permite al usuario cambiar su contraseña

    Este método permite al usuario cambiar su contraseña por una nueva.
    """

    contrasenha = flask.request.form["password"]
    nueva_contrasenha = flask.request.form["new_password"]

    # Comprobamos que no estea vacía
    if not contrasenha:
        flask.flash("Introduce una contraseña", "change_password_warnings")
    else:
        # Comprobamos que la contraseña sea correcta
        usr = UsuarioDto.find(srp, UsuarioDto.current_user().email)
        if not usr or not usr.chk_password(contrasenha):
            flask.flash("Contraseña incorrecta", "change_password_warnings")
            return flask.redirect("/")
        
        # Comprobamos que no estea vacía
        if not nueva_contrasenha:
            flask.flash("Introduce una contraseña", "change_new_password_warnings")
        else:
            # Comprobamos el formato
            if len(nueva_contrasenha) < 8:
                flask.flash("Tu contraseña es demasiado corta, debe tener al menos 8 caracteres.", "change_new_password_warnings")
                return flask.redirect("/")
            elif re.search('[0-9]',nueva_contrasenha) is None:
                flask.flash("Tu contraseña debe incluir al menos un numero.", "change_new_password_warnings")
                return flask.redirect("/")
            elif ((re.search('[a-z]',nueva_contrasenha) is None) and (re.search('[A-Z]',nueva_contrasenha) is None)):
                flask.flash("Tu contraseña debe incluir al menos una letra.", "change_new_password_warnings")
                return flask.redirect("/")
            else:
                # Cambiamos la contraseña
                usr.change_password(nueva_contrasenha)
                srp.save(usr)

    return flask.redirect("/")

@app.route("/postComment", methods=["POST"])
def comentar():
    """Permite comentar en una publicacion

    Permite comentar en una publicacion.
    """
    usr = UsuarioDto.current_user()
    if flask.request.method == "POST":

        texto = flask.request.form["comment"].strip()
        id = flask.request.form["idPostComment"]
        email = flask.request.form["emailPostComment"]

        # Comprobar publicación
        if not texto:
            flask.flash("La publicación no puede estar vacía", "comment_warnings")
        else:
            if not id and not email:
                flask.flash("La publicación no existe", "comment_warnings")
            else:
                lista_publicaciones_todas = srp.load_all(publicacionDto)
                print("Comentario-------------------------" + email + "-------------------------" + id)
                for publicacion in lista_publicaciones_todas:
                    print("Publicacion" + str(publicacion.id) + publicacion.email)
                    if publicacion.email.strip() == email.strip() and str(publicacion.id).strip() == id.strip():
                        publicacion.anhadirComentario(texto)
                        srp.save(publicacion)
                        
                
    return flask.redirect("/")
    
@app.route("/addPoint", methods=["POST"])
def sumar_punto():
    if flask.request.method == "POST":
        email = flask.request.form["emailAdd"].strip()
        id = flask.request.form["idAdd"]

        lista_publicaciones_todas = srp.load_all(publicacionDto)
        for publicacion in lista_publicaciones_todas:
            if publicacion.email.strip() == email.strip() and str(publicacion.id).strip() == id.strip():
                publicacion.puntuacionMas()
                srp.save(publicacion)
    
    return flask.redirect("/")

@app.route("/substractPoint", methods=["POST"])
def restar_punto():
    if flask.request.method == "POST":
        email = flask.request.form["emailSubstract"].strip()
        id = flask.request.form["idSubstract"]

        lista_publicaciones_todas = srp.load_all(publicacionDto)
        for publicacion in lista_publicaciones_todas:
            if publicacion.email.strip() == email.strip() and str(publicacion.id).strip() == id.strip():
                publicacion.puntuacionMenos()
                srp.save(publicacion)
    
    return flask.redirect("/")