const register = () => {
	const username = $("#usernameInput").val();
	const email = $("#emailInput").val();
	const password = $.md5($("#passwordInput").val());
	if (password !== $.md5($("#passwordAgainInput").val())) {
		alert("A 2 jelszó nem egyezik meg!");
	} else {
		var form = new FormData();
		form.append("userName", username);
		form.append("userEmail", email);
		form.append("password", password);

		var settings = {
			url: `http://${location.host}/account/register`,
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
				alert("Sikeres Regisztráció!");
				window.location.href = `http://${location.host}/login`;
			}
		});
	}
};
