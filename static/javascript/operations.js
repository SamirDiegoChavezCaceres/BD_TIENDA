var control = document.getElementById('controlVenta')
if(control != null){
    window.addEventListener('load', restar);
}
//https://stackoverflow.com/questions/10694661/document-getelementbyid-value-return-undefined-in-chrome
//ctrl + F5 https://stackoverflow.com/questions/52682812/django-css-not-updating
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
function generarPago(){
    var sign = prompt("Ingrese Indice del Pago");
    var indexPago = parseInt(sign);
    console.log(indexPago);
    if (indexPago != null && sign != null) {
        //fecth /crearPagoControl/indexPago
        var url = `/crearPagoControl/${indexPago}`;
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': cookie,
            }
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
            //quita el grabar
        })
        .catch(error => {
            console.log("ERROR"+error)
        }) 
    } else {
        alert("Ingrese un codigo, sino revise la lista de pagos");
    }
}

function generarBoleta(){
    var nombre = prompt("Ingrese nombre");
    console.log(nombre);
    if (nombre != null) {
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
    } else {
        alert("Ingrese un nombre");
    }
}

function generarBoletaArt(){
    var cabCod = document.getElementById("bolCabCod").innerHTML; 
    var n = cabCod.indexOf(" ");

    var length = cabCod.length;
    var index = parseInt(cabCod.slice(n, length));

    var articulo = parseInt(document.getElementById("indexArt").value);
	console.log(index);
    console.log(articulo);
    //fecth /crearBoletaDetArt/index/articulo
    var url = `/crearBoletaDetArt/${index}/${articulo}`;
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
        //quita el grabar
    })
    .catch(error => {
        console.log(error)
    }) 
}

function generarBoletaTra(){
    var cabCod = document.getElementById("bolCabCod").innerHTML; 
    var n = cabCod.indexOf(" ");

    var length = cabCod.length;
    var index = parseInt(cabCod.slice(n, length));

    var transaccion = parseInt(document.getElementById("indexTra").value);
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
        if(status_code != 200) {
            console.log('Error in getting info!')
            return false;
        }
        
        console.log(result);
        return result
    })
    .then(result => {
        main = document.getElementById("main");

        main.innerHTML = result;
    })
    .catch(error => {
        console.log(error)
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