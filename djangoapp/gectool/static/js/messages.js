// console.log('WORKINGGGGG....!');

const id = JSON.parse(document.getElementById('json-username').textContent);

const message_username = JSON.parse(document.getElementById('json-message-username').textContent);

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/chat/ws/'
    // + '/ws/'
    + id
    + '/'
);

socket.onopen = function (e) {
    console.log('CONNECTION ESTABLISHED');
}

socket.onclose = function (e) {
    console.log('CONNECTION LOST');
}

socket.onerror = function (e) {
    console.log(e);
}

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data.message);

    if (data.username == message_username) {
        document.querySelector('#chat-body').innerHTML +=
        `<tr>
            <td>
                <p class="msg-send ">
                    ${data.message}<br>
                    <span class="small text-secondary">27 Jun 2023</span>
                </p>
            </td>
        </tr>`;
    }
    else {
        document.querySelector('#chat-body').innerHTML +=
        `<tr>
            <td>
                <p class="msg-recieved ">
                    ${data.message}<br>
                    <span class="small text-secondary">27 Jun 2023</span>
                </p>
            </td>
        </tr>`;
    }
    console.log(e);
}

document.querySelector('#chat-message-submit').onclick = function (e) {
    const message_input = document.querySelector('#message-input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message': message,
        'username': message_username
    }));
    message_input.value = '';
}