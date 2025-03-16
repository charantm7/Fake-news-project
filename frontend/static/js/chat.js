let loc = window.location;

let wsStart = "ws://";

if (location.protocol === "https:") {
  wsStart = "wss://";
}

let endpoint = wsStart + loc.host + loc.pathname;

var socket = new WebSocket(endpoint);

socket.onopen = function (e) {
  console.log("open", e);
};

socket.onmessage = function (e) {
  console.log("message", e);
};

socket.onerror = function (e) {
  console.log("error", e);
};

socket.onclose = function (e) {
  console.log("close", e);
};
