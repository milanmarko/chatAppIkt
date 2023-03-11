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

const sendMessage = () => {
	const message = $("#messageInput").val();
	$("#messageInput").val("");
	socket.emit("messageSent", { sender: cookieGetter("username"), roomID: cookieGetter("roomCode"), message: message });
};

const leaveRoom = () => {
	if (confirm("Biztos vagy benne?")) {
		var form = new FormData();
		form.append("roomID", cookieGetter("roomCode"));

		var settings = {
			url: `http://${location.host}/rooms/leaveRoom`,
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
				location.href = `http://${location.host}/account`;
			}
		});
	}
};

// document.title = `Szoba: ${cookieGetter("roomCode")}`;
const socket = io();
socket.emit("joinRoom", { roomID: cookieGetter("roomCode") });
socket.on("messageReceivedByServer", (message) => {
	const messageDate = new Date();
	var date = "";

	if (messageDate.getHours() < 10) {
		date += "0" + messageDate.getHours().toString();
	} else {
		date += messageDate.getHours().toString();
	}
	if (messageDate.getMinutes < 10) {
		date += ":0" + messageDate.getMinutes().toString();
	} else {
		date += ":" + messageDate.getMinutes().toString();
	}
	var align = "left-msg";
	if (message.sender === cookieGetter("username")) {
		align = "right-msg";
	}

	$("#messenger").append(
		`<div class="msg ${align}"><div class="msg-img"></div><div class="msg-bubble"><div class="msg-info"><div class="msg-info-name">${message.sender}</div><div class="msg-info-time">${date}</div></div><div class="msg-text">${message.message}</div></div></div>`
	);
});
