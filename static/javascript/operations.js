
//https://stackoverflow.com/questions/10694661/document-getelementbyid-value-return-undefined-in-chrome
//ctrl + F5 https://stackoverflow.com/questions/52682812/django-css-not-updating
function abrirVentana(url) {
    window.open(url, "nuevo", "directories=no, location=no, menubar=no, scrollbars=yes, statusbar=no, tittlebar=no, width=400, height=400");
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
let cookie = getCookie('csrftoken');

function restar(){
    var min = document.getElementById("minuendo").innerHTML.replace(",",".");
    var sus = document.getElementById("sustraendo").innerHTML.replace(",",".");
    console.log(min+"a");
    console.log(sus);

    
    var res = min - sus;
    console.log(res);
    document.getElementById("resultado").innerHTML = res;
}
// https://stackoverflow.com/questions/67188765/using-fetch-with-javascript-and-django


function generarBoleta(){
    var nombre = prompt("Ingrese nombre");
    if (nombre == null || nombre == "") {
        nombre = "Personas Varias";
        console.log(nombre);
    } 
    var dni = prompt("Ingrese dni, puede no ingresarlo", "0");
    console.log(dni);
    if (dni != null) {
        //fecth /crearBoletaCab/nombre/dni
        var url = `/crearBoletaCab/${nombre}/${dni}`;
        fetch(url, {
            method: 'GET',
            credentials: 'include',
        })
        .then(response => {
            result = response.json()
            status_code = response.status;
            if(status_code != 200) {
                console.log('Error in getting info!')
                return false;
            }
            if(response['message']) {
        
            }
            return result
        })
        .then(result => {
            console.log(result);
            main = document.getElementById("main");

            main.innerHTML = result;
            //quita el grabar
        })
        .catch(error => {
            console.log(error)
        }) 
    } else {
        alert("Ingrese un dni o dejelo en 0");
    }
}

function generarBoletaArt(){
    var cabCod = document.getElementById("bolCabCod").innerHTML; 
    var n = cabCod.indexOf(" ");

    var length = cabCod.length;
    var index = parseInt(cabCod.slice(n, length));

    var articulo = parseInt(document.getElementById("indexArt").value);
    if(Number.isNaN(articulo))
        articulo = 99999;
	console.log(index);
    console.log(articulo);
    //fecth /crearBoletaDetArt/index/articulo
    var url = `/crearBoletaDetArt/${index}/${articulo}`;
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        console.log(response);
        result = response.json()
        status_code = response.status;
        if(status_code == 400) {
            throw 1;
        }
        if(status_code != 200) {
            console.log('Error in getting info!')
            return false;
        }
        
        return result
    })
    .then(result => {
        console.log("lis");
        main = document.getElementById("main");
        
        main.innerHTML = result;
        document.getElementById("indexArt").focus();
        //quita el grabar
    })
    .catch(error => {
        console.log(error)
        if(error == 1)
            location.reload();
    }) 
}

function generarBoletaTra(){
    var cabCod = document.getElementById("bolCabCod").innerHTML; 
    var n = cabCod.indexOf(" ");

    var length = cabCod.length;
    var index = parseInt(cabCod.slice(n, length));

    var transaccion = parseInt(document.getElementById("indexTra").value);
	if(transaccion == NaN)
        transaccion = -1;
    console.log(index);
    console.log(transaccion);
    //fecth /crearBoletaDetTra/index/transaccion
    var url = `/crearBoletaDetTra/${index}/${transaccion}`;
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        result = response.json()
        status_code = response.status;
        if(status_code == 400) {
            throw 1;
        }
        if(status_code != 200) {
            console.log('Error in getting info!')
            return false;
        }
        
        console.log("lis");
        return result
    })
    .then(result => {
        main = document.getElementById("main");

        main.innerHTML = result;
        document.getElementById("indexTra").focus();
    })
    .catch(error => {
        console.log(error)
        if(error == 1)
            location.reload();
    }) 
}

function updateBolEleArt(indexArt){
    var cabCod = document.getElementById("bolCabCod").innerHTML; 
    var n = cabCod.indexOf(" ");

    var length = cabCod.length;
    var index = parseInt(cabCod.slice(n, length));

    var indexArt = parseInt(indexArt);
	console.log(index);
    console.log(indexArt);

    var cantidad = prompt("Ingrese Cantidad");
    console.log(cantidad);
    //https://www.youtube.com/watch?v=gXiNGapOJnw&t=0s
    if (cantidad != null) {
        //fecth /updateBoletaDetArt/index/indexArt/cantidad
        var url = `/updateBoletaDetArt/${index}/${indexArt}/${cantidad}`;
        fetch(url, {
            method: 'GET',
        })
        .then(response => {
            result = response.json()
            status_code = response.status;
            if(status_code != 200) {
                console.log('Error in getting info!')
                return false;
            }
            
            return result
        })
        .then(result => {
            console.log(result);
            main = document.getElementById("main");

            main.innerHTML = result;
        })
        .catch(error => {
            console.log(error)
        }) 
    } else {
        alert("Ingrese cantidad valida, por favor");
    }
}

function deleteBolEleArt(indexArt){
    var cabCod = document.getElementById("bolCabCod").innerHTML; 
    var n = cabCod.indexOf(" ");

    var length = cabCod.length;
    var index = parseInt(cabCod.slice(n, length));

    var indexArt = parseInt(indexArt);
	console.log(index);
    console.log(indexArt);
    //fecth /deleteBoletaDetArt/index/indexArt
    var url = `/deleteBoletaDetArt/${index}/${indexArt}`;
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        result = response.json()
        status_code = response.status;
        if(status_code != 200) {
            console.log('Error in getting info!')
            return false;
        }
        
        return result
    })
    .then(result => {
        console.log(result);
        main = document.getElementById("main");

        main.innerHTML = result;
    })
    .catch(error => {
        console.log(error)
    }) 
    
}

function updateBolEleTra(indexTra){
    var cabCod = document.getElementById("bolCabCod").innerHTML; 
    var n = cabCod.indexOf(" ");

    var length = cabCod.length;
    var index = parseInt(cabCod.slice(n, length));

    var indexTra = parseInt(indexTra);
	console.log(index);
    console.log(indexTra);

    var cantidad = prompt("Ingrese Cantidad");
    console.log(cantidad);
    if (cantidad != null) {
        //fecth /updateBoletaDetTra/index/indexTra/cantidad
        if (cantidad != null) {
            var url = `/updateBoletaDetTra/${index}/${indexTra}/${cantidad}`;
            fetch(url, {
                method: 'GET',
            })
            .then(response => {
                result = response.json()
                status_code = response.status;
                if(status_code != 200) {
                    console.log('Error in getting info!')
                    return false;
                }
                
                return result
            })
            .then(result => {
                console.log(result);
                main = document.getElementById("main");

                main.innerHTML = result;
            })
            .catch(error => {
                console.log(error)
            }) 
        } else {
            alert("Ingrese cantidad valida, por favor");
        }
    } else {
        alert("Ingrese cantidad valida, por favor");
    }
}

function deleteBolEleTra(indexTra){
    var cabCod = document.getElementById("bolCabCod").innerHTML; 
    var n = cabCod.indexOf(" ");

    var length = cabCod.length;
    var index = parseInt(cabCod.slice(n, length));
    
    var indexTra = parseInt(indexTra);
	console.log(index);
    console.log(indexTra);
    //fecth /deleteBoletaDetTra/index/indexTra
    var url = `/deleteBoletaDetTra/${index}/${indexTra}`;
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        result = response.json()
        status_code = response.status;
        if(status_code != 200) {
            console.log('Error in getting info!')
            return false;
        }
        
        return result
    })
    .then(result => {
        console.log(result);
        main = document.getElementById("main");

        main.innerHTML = result;
    })
    .catch(error => {
        console.log(error)
    }) 
}

/////////////

(function(document) {
    'use strict';

    var LightTableFilter = (function(Arr) {

      var _input;

      function _onInputEvent(e) {
        _input = e.target;
        var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
        Arr.forEach.call(tables, function(table) {
          Arr.forEach.call(table.tBodies, function(tbody) {
            Arr.forEach.call(tbody.rows, _filter);
          });
        });
      }

      function _filter(row) {
        var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
        row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
      }

      return {
        init: function() {
          var inputs = document.getElementsByClassName('light-table-filter');
          Arr.forEach.call(inputs, function(input) {
            input.oninput = _onInputEvent;
          });
        }
      };
    })(Array.prototype);

    document.addEventListener('readystatechange', function() {
      if (document.readyState === 'complete') {
        LightTableFilter.init();
      }
    });

  })(document);