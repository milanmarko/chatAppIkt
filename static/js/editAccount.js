const cookieGetter = (cname) => {
	let name = cname + "=";
	let decodedCookie = decodeURIComponent(document.cookie);
	let ca = decodedCookie.split(";");
	for (let i = 0; i < ca.length; i++) {
		let c = ca[i];
		while (c.charAt(0) == " ") {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
};

$(document).ready(() => {
	document.title = `Bejelentkezve mint ${cookieGetter("username")}`;
	const username = cookieGetter("username");
	const password = cookieGetter("password");
	var form = new FormData();
	form.append("username", username);
	form.append("password", password);

	var settings = {
		url: `http://${location.host}/account/getAccountInfo`,
		method: "POST",
		timeout: 0,
		processData: false,
		mimeType: "multipart/form-data",
		contentType: false,
		data: form,
	};

	$.ajax(settings).done(function (response) {
		resp = JSON.parse(response);
		$("#usernameInput").val(resp.username);
		$("#emailInput").val(resp.email);
	});
});

const editPassword = () => {
	if ($("#passwordOldInput").val() === "") {
		$("#passwordChange").html("");
	} else {
		$("#passwordChange").html(
			`<div class="row mt-5"><div class="d-flex justify-content-center col-12 col-md-6 col-sm-12 mt-3"><span id="label" class="text-center">Új jelszó: </span></div><div class="d-flex justify-content-center col-12 col-md-6 col-sm-12 mt-3"><input class="form-control" type="password" id="passwordNewInput" placeholder="" /></div></div><div class="row mt-5"><div class="d-flex justify-content-center col-12 col-md-6 col-sm-12 mt-3"><span id="label" class="text-center">Új jelszó újra: </span></div><div class="d-flex justify-content-center col-12 col-md-6 col-sm-12 mt-3"><input class="form-control" type="password" id="passwordNewAgainInput" placeholder="" /></div></div>`
		);
	}
};

const editProfile = () => {
	var isUsernameBeingEdited = false;
	var isPasswordBeingChanged = false;
	const oldUsername = cookieGetter("username");
	const newUsername = $("#usernameInput").val();
	if (oldUsername !== newUsername) {
		isUsernameBeingEdited = true;
		document.cookie = `username=${newUsername}`;
	}
	const newEmail = $("#emailInput").val();
	const oldPassword = cookieGetter("password");
	var newPassword = "";
	if ($.md5($("#passwordOldInput").val()) === cookieGetter("password")) {
		if ($.md5($("#passwordNewInput").val()) === $.md5($("#passwordNewAgainInput").val())) {
			newPassword = $.md5($("#passwordNewInput").val());
			document.cookie = `password=${newPassword}`;
			isPasswordBeingChanged = true;
		} else {
			alert("A két új jelszó nem egyezik!");
		}
	}
	var form = new FormData();
	form.append("newEmail", newEmail);
	form.append("newUsername", newUsername);
	form.append("oldUsername", oldUsername);
	form.append("oldPassword", oldPassword);
	form.append("newPassword", newPassword);
	form.append("isUsernameBeingChanged", isUsernameBeingEdited);

	var settings = {
		url: `http://${location.host}/account/editAccountInfo`,
		method: "POST",
		timeout: 0,
		processData: false,
		mimeType: "multipart/form-data",
		contentType: false,
		data: form,
	};

	$.ajax(settings).done(function (response) {
		resp = JSON.parse(response);
		if (isPasswordBeingChanged && resp.sikeresE) {
			alert("Amennyiben a beírt jelszó helyes, a változtatások sikeresek.");
		} else if (resp.sikeresE) {
			alert("Sikeres változtatás");
		}
		location.href = `http://${location.host}/account`;
	});
};
