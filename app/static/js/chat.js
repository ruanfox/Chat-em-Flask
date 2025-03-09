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
      method: "POST", // Use o método correto conforme seu backend (GET ou POST)
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin", // Enviar cookies de sessão
    })
    .then(response => {
      if (response.ok) {
        window.location.href = "/"; // Redireciona para a página inicial ou de login
      } else {
        alert("Erro ao sair da sala.");
      }
    })
    .catch(error => console.error("Erro:", error));
  });
});

// função para listar as salas
document.addEventListener("DOMContentLoaded", async function () {
  const roomList = document.getElementById("room-list");

  try {
      const response = await fetch("/api/rooms"); // Substitua pelo endpoint correto
      const data = await response.json();

      if (data.rooms) {
          data.rooms.forEach(room => {
              const roomItem = document.createElement("div");
              roomItem.classList.add("room-list-container");
              roomItem.innerHTML = `
                  <p>${room.nome}</p>
                  <i class="bi bi-trash" onclick="deleteRoom(${room.id})"></i>
              `;
              roomList.appendChild(roomItem);
          });
      }
  } catch (error) {
      console.error("Erro ao buscar salas:", error);
  }
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
