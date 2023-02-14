function login() {
	const username = $("#usernameInput");
	const password = $("#passwordInput");
	var settings = {
		url: "http://localhost:5000/account/login",
		method: "POST",
		timeout: 0,
		processData: false,
		mimeType: "multipart/form-data",
		contentType: false,
		data: {
			userName: username,
			password: password,
		},
	};

	$.ajax(settings).done(function (response) {
		console.log(response);
	});
}
