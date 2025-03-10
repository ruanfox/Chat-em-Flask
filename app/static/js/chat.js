let selectedRoomId = null; // Variável global para armazenar o ID da sala

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

                    console.log("Sala selecionada:", selectedRoomId);

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

// Função para carregar mensagens da sala selecionada
async function loadMessages(roomId) {
    const messageContainer = document.querySelector(".list-message");
    messageContainer.innerHTML = ""; // Limpa mensagens atuais

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

// Função para enviar mensagem
document.addEventListener("DOMContentLoaded", function () {
    const messageForm = document.getElementById("message-form");

    messageForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evita o reload da página

        const messageInput = document.getElementById("message-input");
        const messageContent = messageInput.value.trim();
        const roomId = selectedRoomId || sessionStorage.getItem("selectedRoomId");

        if (!messageContent) {
            alert("Digite uma mensagem antes de enviar.");
            return;
        }

        if (!roomId) {
            alert("Selecione uma sala antes de enviar mensagens!");
            return;
        }

        try {
            const response = await fetch("/api/messages", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: new URLSearchParams({
                    conteudo: messageContent,
                    sala_id: roomId,
                }),
            });

            const result = await response.json();

            if (response.ok) {
                // Exibir a mensagem na tela sem recarregar
                const messageContainer = document.querySelector(".list-message");
                const newMessage = document.createElement("li");
                newMessage.classList.add("message");
                newMessage.innerHTML = `
                    <p class="nickname">@Você</p>
                    <p class="message-text">${messageContent}</p>
                    <p class="data_envio">${new Date().toLocaleTimeString()}</p>
                `;
                messageContainer.prepend(newMessage);

                messageInput.value = ""; // Limpa o campo de entrada
            } else {
                alert(result.error || "Erro ao enviar a mensagem.");
            }
        } catch (error) {
            console.error("Erro ao enviar mensagem:", error);
            alert("Erro na requisição.");
        }
    });
});

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
