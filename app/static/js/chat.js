var client_id = currentUserId
document.querySelector("#ws-id").textContent = client_id;
var ws = new WebSocket(`ws://127.0.0.1/ws/${client_id}`);
ws.onmessage = function(event) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(event.data)
    message.appendChild(content)
    messages.appendChild(message)
};
function sendMessage(event) {
    var input = document.getElementById("messageText")
    var recipient = document.getElementById("recipientId")
    ws.send(recipient.value + " " + input.value)
    input.value = ''
    event.preventDefault()
}
