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
	$("#topH").text(`Bejelentkezve mint: ${cookieGetter("username")}`);
});

const logOut = () => {
	document.cookie = "username=";
	document.cookie = "password=";
	document.cookie = "roomCode=";
	location.href = "../login";
};
