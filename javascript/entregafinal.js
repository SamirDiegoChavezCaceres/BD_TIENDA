function doLogin(){
	var userName=document.getElementById('user').value;
	var password=document.getElementById("password").value;
	console.log(userName);
	console.log(password);
	var url = "../final/cgi-bin/login.pl?userName="+userName+"&password="+password;
	console.log(url);
	var promise = fetch(url);
	promise.then(response => response.text())
		.then(data => {
			let xml = (new window.DOMParser()).parseFromString(data, "text/xml");
			renderLogin(xml);
		}).catch(error => {
			console.log('Error:', error);
		});
}
function doCreateAccount(){
	var userName=document.getElementById('user').value;
	var password=document.getElementById("password").value;
	var firstName=document.getElementById("firstName").value;
	var lastName=document.getElementById("lastName").value;
	var url = "../final/cgi-bin/register.pl?userName="+userName+"&password="+password+"&firstName="+firstName+"&lastName="+lastName;
	var promise = fetch(url);
	promise.then(response => response.text())
		.then(data => {
			let xml = (new window.DOMParser()).parseFromString(data, "text/xml");
			renderLogin(xml);
		}).catch(error => {
			console.log('Error:', error);
			document.getElementById('errorUserLogin').innerHTML = "Error al momento de crear la cuenta, revise los datos";
		});
}
function doNew(owner){
	var title = document.getElementById("title").value;
	var text = encodeURIComponent(document.getElementById("text").value);
	var url = "../final/cgi-bin/new.pl?owner="+owner+"&title="+title+"&text="+text;
	var promise = fetch(url);
	promise.then(response => response.text())
		.then(data => {
			doList(owner);
		}).catch(error => {
			console.log('Error:', error);
		});
}
function doList(owner){
	var url = "../final/cgi-bin/list.pl?owner="+owner;
	var promise = fetch(url);
	promise.then(response => response.text())
		.then(data => {
			renderList(data);
		}).catch(error => {
			console.log('Error:', error);
		});
}
function doView(owner, title){
	var url = "../final/cgi-bin/view.pl?owner="+owner+"&title="+title;
	var promise = fetch(url);
	promise.then(response => response.text())
		.then(data => {
			renderView(data);
		}).catch(error => {
			console.log('Error:', error);
		});
}
function doDelete(owner, title){
	var url = "../final/cgi-bin/delete.pl?owner="+owner+"&title="+title;
	var promise = fetch(url);
	promise.then(response => response.text())
		.then(data => {
			doList(owner);
		}).catch(error => {
			console.log('Error:', error);
		});
}
function doEdit(owner, title){
	var url = "../final/cgi-bin/article.pl?owner="+owner+"&title="+title;
	var promise = fetch(url);
	promise.then(response => response.text())
		.then(data => {
			let xml = (new window.DOMParser()).parseFromString(data, "text/xml");
			renderEdit(xml);
		}).catch(error => {
			console.log('Error:', error);
		});
}
function doUpdate(owner, title){
	var text = encodeURIComponent(document.getElementById("text").value);
	var url = "../final/cgi-bin/update.pl?owner="+owner+"&title="+title+"&text="+text;
	var promise = fetch(url);
	promise.then(response => response.text())
		.then(data => {
			let xml = (new window.DOMParser()).parseFromString(data, "text/xml");
			renderNew(xml);
		}).catch(error => {
			console.log('Error:', error);
		});
}

