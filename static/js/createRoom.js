const createRoom = () => {
	const roomName = $("#chatRoomNameInput").val();
	const private = document.getElementById("privateCheckInput").checked;

	var form = new FormData();
	form.append("roomName", roomName);
	form.append("private", private);

	var settings = {
		url: `http://${location.host}/rooms/createRoom`,
		method: "POST",
		timeout: 0,
		processData: false,
		mimeType: "multipart/form-data",
		contentType: false,
		data: form,
	};

	$.ajax(settings).done(function (response) {
		resp = JSON.parse(response);
		if (resp.successful) {
			document.cookie = `roomCode=${resp.roomCode}; path=/`;
			alert("Szoba sikeresen létrehozva");
			location.href = `http://${location.host}/chat`;
		}
	});
};
