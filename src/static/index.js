/**
 * Comprueba el formato de los parametros en el registro de un nuevo usuario.
 * 
 * @returns Si los campos del formulario son correctos.
 */
function validateRegister(){
    let username = document.forms["frRegistrarse"]["username"].value;
    let email = document.forms["frRegistrarse"]["email"].value;
    let password = document.forms["frRegistrarse"]["password"].value;

    let flag = true;
    if (username == "") {
      document.getElementById("register_username_warnings_p").innerHTML = "Necesitas un usuario!";
      flag = false;
    } else {
      document.getElementById("register_username_warnings_p").innerHTML = "";
    }
    if (email == "") {
      document.getElementById("register_email_warning_p").innerHTML = "No olvides tu correo electrónico!";
      flag = false;
    } else {
      if (!email.match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
        document.getElementById("register_email_warning_p").innerHTML = "Ese no es un correo válido!";
        flag = false;
      } else {
        document.getElementById("register_email_warning_p").innerHTML = "";
      }
    }
    if (password == "") {
      document.getElementById("register_password_warnings_p").innerHTML = "Necesitas una contraseña!";
      flag = false;
    }else {
      if (password.length < 8){
        document.getElementById("register_password_warnings_p").innerHTML = "Tu contraseña es demasiado corta, debe tener al menos 8 caracteres.";
        flag = false;
      } else {
        if (!password.match(/[0-9]/i)){
          document.getElementById("register_password_warnings_p").innerHTML = "Tu contraseña debe incluir al menos un numero.";
          flag = false;
        } else {
          if ((!password.match(/[a-z]/g)) && (!password.match(/[A-Z]/g))){
            document.getElementById("register_password_warnings_p").innerHTML = "Tu contraseña debe incluir al menos una letra.";
            flag = false;
          } else {
            document.getElementById("register_password_warnings_p").innerHTML = "";
          }
        }
      }
    }
    return flag;
}
/**
 * Comprueba el formato de los parametros en el inicio de sesion.
 * 
 * @returns Si los campos del formulario son correctos.
 */
function validateLogin(){
    let email = document.forms["frIniciarSesion"]["email"].value;
    
    let flag = true;
    if (email == "") {
      document.getElementById("login_email_warnings_p").innerHTML = "No olvides tu correo electrónico!";
      flag = false;
    } else {
      if (!email.match(/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)) {
        document.getElementById("login_email_warnings_p").innerHTML = "Ese no es un correo válido!";
        flag = false;
      } else {
        document.getElementById("login_email_warnings_p").innerHTML = "";
      }
    }
    return flag;
}

/**
 * Comprueba el formato de los parametros al cambiar la contraseña.
 * 
 * @returns Si los campos del formulario son correctos.
 */
function validateNewPassword(){
    let password = document.forms["frCambiarContrasenha"]["new_password"].value;

    let flag = true;
    if (password == "") {
      document.getElementById("change_new_password_warnings_p").innerHTML = "Tu contraseña no puede estar vacía.";
      flag = false;
    }else {
      if (password.length < 8){
        document.getElementById("change_new_password_warnings_p").innerHTML = "Tu contraseña es demasiado corta, debe tener al menos 8 caracteres.";
        flag = false;
      } else {
        if (!password.match(/[0-9]/i)){
          document.getElementById("change_new_password_warnings_p").innerHTML = "Tu contraseña debe incluir al menos un numero.";
          flag = false;
        } else {
          if ((!password.match(/[a-z]/g)) && (!password.match(/[A-Z]/g))){
            document.getElementById("change_new_password_warnings_p").innerHTML = "Tu contraseña debe incluir al menos una letra.";
            flag = false;
          } else {
            document.getElementById("change_new_password_warnings_p").innerHTML = "";
          }
        }
      }
    }
    return flag;
}

/**
 * Comprueba si la nueva publicación no está vacía.
 * 
 * @returns Si los campos del formulario no están vacíos.
 */
function validateNewPost(){
    let text = document.forms["frPublicar"]["edMensaje"].value;
    let image = document.forms["frPublicar"]["edImagen"].value;

    let flag = true;
    if (text == "" && image == "") {
      document.getElementById("post_warnings_p").innerHTML = "La publicación no puede estar vacía.";
      flag = false;
    } else {
      document.getElementById("post_warnings_p").innerHTML = "";
    }
    return flag;
}
