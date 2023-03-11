$(document).ready(() => {
	var settings = {
		url: `http://${location.host}/rooms/getAll`,
		method: "GET",
		timeout: 0,
		processData: false,
		mimeType: "multipart/form-data",
		contentType: false,
	};

	$.ajax(settings).done(function (response) {
		const tbody = $("#roomTableBody");
		resp = JSON.parse(response);
		resp.rooms.forEach((elem) => {
			tbody.append(
				`<tr><td>${elem[0]}</td><td>${elem[1]}</td><td><input type="button" class=" btn btn-primary" value="Csatlakozás" onclick="joinRoom('${[
					elem[2],
				]}')" /></td></tr>`
			);
		});
	});
});

const joinRoom = (roomCode) => {
	document.cookie = `roomCode=${roomCode}; path=/`;
	location.href = `http://${location.host}/chat`;
};
