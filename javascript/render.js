function renderLogin(xml){
    if(xml.documentElement.nodeName === 'user'){
    let lastName = xml.getElementsByTagName('lastName')[0]
      .childNodes[0].nodeValue;
    let firstName = xml.getElementsByTagName('firstName')[0]
      .childNodes[0].nodeValue;
    let owner = xml.getElementsByTagName('owner')[0]
      .childNodes[0].nodeValue;

    let fullName = firstName + " " + lastName;
    showWelcome(fullName);
    showMenuUserLogged(fullName, owner);
  } else {
    showLogin('Combinación de usuario contraseña inválida');
  }
}
function renderNew(xml){
  if(xml.documentElement.nodeName === 'article'){
    let title = xml.getElementsByTagName('title')[0]
      .childNodes[0].nodeValue;
    let text = xml.getElementsByTagName('text')[0]
      .childNodes[0].nodeValue;
    let html = "<h1>" + title + "</h1>\n" +
      "<pre>" + text + "</pre>\n" +
      "<hr>\n<h2>Página grabada</h2>\n";
    document.getElementById('main').innerHTML = html;
    console.log(html);
  }
}
function renderList(str){
  xml = (new DOMParser()).parseFromString(str, "application/xml");
	let html = '<h1>Nuestras páginas de wiki</h1>\n';
  if(xml.getElementsByTagName('article')[0] != null){
    let article = xml.getElementsByTagName('article');
    for(let i = 0; i < article.length; i++){
      let title = article[i].getElementsByTagName('title')[0].childNodes[0].nodeValue;
      let owner = article[i].getElementsByTagName('owner')[0].childNodes[0].nodeValue;
      html += "<li>" + title + " ";
      html += "<button onclick='doView(\"" + owner + "\",\"" + title + "\")'>V</button>";
      html += "<button onclick='doDelete(\"" + owner + "\",\"" + title + "\")'>X</button>";
      html += "<button onclick='doEdit(\"" + owner + "\",\"" + title + "\")'>E</button>";
      html += "</li>\n";
    }
  } else {
    html += '<h2>¡Aún no hay Páginas!</h2>';
  }
  document.getElementById('main').innerHTML = html;
  console.log(html);

}
function renderView(data){
  document.getElementById('main').innerHTML = data;
}
function renderEdit(xml){
  if(xml){
    let owner = xml.getElementsByTagName('owner')[0].childNodes[0].nodeValue;
    let title = xml.getElementsByTagName('title')[0].childNodes[0].nodeValue;
    let text = xml.getElementsByTagName('text')[0].childNodes[0].nodeValue;
    let html = "<h1>" + title + "</h1>\n" + 
      "<textarea name='text' id='text'>" + text + "</textarea><br>\n" +
      "<button type='button' onclick='doUpdate(\"" + owner +
      "\", \"" + title +"\")'>Actualizar</button>\n" + 
      "<button type='button' onclick='doList(\"" + owner + "\")'>Cancelar</button>\n";
    document.getElementById('main').innerHTML = html;
    console.log(html);
  }
}

