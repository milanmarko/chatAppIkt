function login() {
	const username = $("#usernameInput").val();
	const password = $.md5($("#passwordInput").val());

	var form = new FormData();
	form.append("userName", username);
	form.append("password", password);

	var settings = {
		url: `http://${location.host}/account/login`,
		method: "POST",
		timeout: 0,
		processData: false,
		mimeType: "multipart/form-data",
		contentType: false,
		data: form,
	};

	$.ajax(settings).done(function (response) {
		resp = JSON.parse(response);
		if (resp.sikeresE == true) {
			document.cookie = `username=${username}`;
			document.cookie = `password=${password}`;

			window.location.href = `http://${location.host}/account`;
		}
	});
}
