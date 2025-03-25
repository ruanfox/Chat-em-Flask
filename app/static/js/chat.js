const socket = io(); // Conecta ao servidor

// Variável global para armazenar o ID da sala
let selectedRoomId = null; 

// Variável global para armazenar o nickname do usuário
let globalUserId = null;
let globalNickname = null;

document.addEventListener("DOMContentLoaded", async function () {
    const roomList = document.getElementById("room-list");

    try {
        const response = await fetch("/api/rooms");
        const data = await response.json();

        if (data.rooms) {
            data.rooms.forEach(room => {
                const roomItem = document.createElement("div");
                roomItem.classList.add("room-list-container");
                roomItem.setAttribute("data-room-id", room.id); // Define o ID da sala
                roomItem.innerHTML = `
                    <p>${room.nome}</p>
                    <i class="bi bi-trash" onclick="deleteRoom(${room.id})"></i>
                `;

                // Evento para capturar o ID da sala selecionada
                roomItem.addEventListener("click", function () {
                    selectedRoomId = room.id;
                    sessionStorage.setItem("selectedRoomId", room.id); // Salva no sessionStorage

                    // Destacar a sala selecionada
                    document.querySelectorAll(".room-list-container").forEach(el => el.classList.remove("active"));
                    roomItem.classList.add("active");

                    // Carregar mensagens da sala selecionada
                    loadMessages(selectedRoomId);
                });

                roomList.appendChild(roomItem);
            });
        }
    } catch (error) {
        console.error("Erro ao buscar salas:", error);
    }
});


// Entra na sala ao selecionar uma sala
document.addEventListener("DOMContentLoaded", function () {
    const roomList = document.getElementById("room-list");

    roomList.addEventListener("click", function (event) {
        const roomItem = event.target.closest(".room-list-container");
        if (roomItem) {
            const roomId = roomItem.getAttribute("data-room-id");
            selectedRoomId = roomId;  // Atualiza a sala selecionada
            sessionStorage.setItem("selectedRoomId", roomId);  // Salva no sessionStorage
            socket.emit('join_room', { room_id: roomId });  // Entra na sala
            loadMessages(roomId);  // Carrega as mensagens da sala
        }
    });
});

// função para capturar o id e o nickname
async function fetchUserSession() {
    try {
        const response = await fetch('/api/user_session', {
            method: 'GET',
            credentials: 'same-origin'// Garante o envio dos cookies da sessão
        });
        
        if (response.ok) {
            const data = await response.json();
            globalUserId = data.user_id;
            globalNickname = data.nickname;
            // Também podemos salvar no sessionStorage se desejado:
            sessionStorage.setItem('user_id', globalUserId);
            sessionStorage.setItem('nickname', globalNickname);
        } else {
            console.error("Erro ao buscar sessão:", response.statusText);
        }
    } catch (error) {
        console.error("Erro na requisição da sessão:", error);
    }
}

// Chama a função ao carregar o chat
document.addEventListener("DOMContentLoaded", function () {
    fetchUserSession();
});

// Função para enviar mensagem
document.getElementById("message-form").addEventListener("submit", async function (event) {
    event.preventDefault();

    const messageInput = document.getElementById("message-input");
    const messageContent = messageInput.value.trim();
    const roomId = selectedRoomId || sessionStorage.getItem("selectedRoomId");

    // Usa as variáveis globais obtidas pela rota de sessão
    if (!globalUserId || !globalNickname) {
        alert("Você precisa estar logado para enviar mensagens.");
        return;
    }

    if (!messageContent) {
        alert("Digite uma mensagem antes de enviar.");
        return;
    }

    if (!roomId) {
        alert("Selecione uma sala antes de enviar mensagens!");
        return;
    }

    // Envia a mensagem via WebSocket
    socket.emit("send_message", {
        room_id: roomId,
        message: messageContent,
        author: globalNickname,
        user_id: globalUserId
    });

    // Limpa o campo de entrada
    messageInput.value = '';
});


// Recebe uma mensagem em tempo real
socket.on('receive_message', function (data) {
    const currentRoomId = selectedRoomId || sessionStorage.getItem("selectedRoomId");
    if (data.room_id.toString() !== currentRoomId.toString()) return;  // Filtra mensagens de outras salas

    // Adiciona a mensagem ao DOM
    const messageContainer = document.querySelector(".list-message");
    const newMessage = document.createElement("li");
    newMessage.classList.add("message");
    newMessage.innerHTML = `
        <p class="nickname">@${data.author}</p>
        <p class="message-text">${data.message}</p>
        <p class="data_envio">${new Date(data.timestamp).toLocaleTimeString()}</p>
    `;
    messageContainer.prepend(newMessage);
});

// Carrega as mensagens da sala
async function loadMessages(roomId) {
    const messageContainer = document.querySelector(".list-message");
    messageContainer.innerHTML = "";  // Limpa as mensagens atuais

    try {
        const response = await fetch(`/api/messages/${roomId}`);
        const data = await response.json();

        if (data.messages) {
            data.messages.forEach(msg => {
                const newMessage = document.createElement("li");
                newMessage.classList.add("message");
                newMessage.innerHTML = `
                    <p class="nickname">@${msg.author}</p>
                    <p class="message-text">${msg.content}</p>
                    <p class="data_envio">${new Date(msg.timestamp).toLocaleTimeString()}</p>
                `;
                messageContainer.prepend(newMessage);
            });
        }
    } catch (error) {
        console.error("Erro ao carregar mensagens:", error);
    }
}

// Função para deletar uma sala
async function deleteRoom(roomId) {
    if (!confirm("Tem certeza que deseja excluir esta sala?")) return;

    try {
        const response = await fetch(`/api/rooms/${roomId}`, {
            method: "DELETE",
        });
        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error);
        }
    } catch (error) {
        console.error("Erro ao excluir sala:", error);
    }
}

// Exibe o card ao clicar no botão "new-room-btn"
document.getElementById("new-room-btn").addEventListener("click", function() {
    document.getElementById("new-room-card").style.display = "block";
});

// Esconde o card ao clicar no botão "Cancelar"
document.getElementById("cancel-room").addEventListener("click", function() {
    document.getElementById("new-room-card").style.display = "none";
});

// Função para logout
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("leave-room-btn").addEventListener("click", function () {
        fetch("/api/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            credentials: "same-origin",
        })
        .then(response => {
            if (response.ok) {
                window.location.href = "/"; // Redireciona para a página inicial
            } else {
                alert("Erro ao sair da sala.");
            }
        })
        .catch(error => console.error("Erro:", error));
    });
});