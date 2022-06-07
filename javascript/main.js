window.addEventListener('load', showWelcome);

function showWelcome(fullName){
  let html = '<h2>Bienvenido';
  if(fullName !==  undefined && ! fullName.target){
    html += ' ' + fullName;
  }
  html += "</h2>\n";
  html += `
          <p>Este sistema fue desarrollado por alumnos del primer año de la Escuela Profesional de Ingeniería de Sistemas, de la Universidad Nacional de San Agustín de Arequipa</p>
          <p>El sistema fué desarrollado usando estas tecnologías:</p>
          <ul>
            <li>HTML y CSS</li>
            <li>Perl para el backend</li>
            <li>MariaDB para la base de datos</li>
            <li>Javascript para el frontend</li>
            <li>Las páginas se escriben en lenguaje Markdown</li>
            <li>Se usaron expresiones regulares para el procesamiento del lenguaje Markdown</li>
            <li>La comunicación entre el cliente y el servidor se hizo usando XML de manera asíncrona</li>
          </ul>`;
  document.getElementById('main').innerHTML = html;
  console.log(html);
}

function showLogin(error){
  let html = "<h2>Ingrese sus datos</h2>\n";
  if(error !== undefined){
    html += "<p class='error'>" + error + "</p>\n";
  }
  html += "<label for='user'>Usuario:</label>\n" +
    "<input type='text' name='user' id='user'><br>\n" +
    "<label for='password'>Contraseña:</label>\n" +
    "<input type='password' name='password' id='password'><br>\n" +
    "<button type='button' onclick='doLogin()'>Ingresar</button>\n";
  document.getElementById('main').innerHTML = html;
  console.log(html);
}

function showCreateAccount(){
  let html = `
          <h2>Registre sus datos</h2>
          <p id='errorUserLogin'></p>
          <label for='user'>Usuario:</label>
          <input type='text' name='user' id='user'><br>
          <label for='password'>Contraseña:</label>
          <input type='password' name='password' id='password'><br>
          <label for='firstName'>Nombres:</label>
          <input type='text' name='firstName' id='firstName'><br>
          <label for='lastName'>Apellidos:</label>
          <input type='text' name='lastName' id='lastName'><br>
          <button type='button' onclick='doCreateAccount()'>Registrar</button>`;
  document.getElementById('main').innerHTML = html;
  console.log(html);
}
function showMenuUserLogged(fullName, owner){
  let html = "<p onclick='showWelcome(\"" + fullName + "\")'>Inicio</p>\n"+
    "<p onclick='doList(\"" + owner + "\")'>Lista de Páginas</p>\n"+
    "<p style='float:right' onclick='showNew(\"" + owner + "\")'>Página Nueva</p>\n"
  document.getElementById('menu').innerHTML = html;
  console.log(html);
}
function showNew(owner){
  let html="<div>\n";
  html += "  <label for='title'>Título</label>\n";
  html += "  <input type='text' name='title' id='title'>\n";
  html += "</div>\n";
  html += "<div>\n";
  html += "  <label for='text'>Texto</label>\n";
  html += "  <textarea name='text' id='text'></textarea>\n";
  html += "</div>\n";
  html += "<button onclick='doNew(\"" + owner + "\")'>Enviar</button>\n";
  html += "<button onclick='doList(\"" + owner + "\")'>Cancelar</button>\n";
  document.getElementById('main').innerHTML = html;
  console.log(html);
}

