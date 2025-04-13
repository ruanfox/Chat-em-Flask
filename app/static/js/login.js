document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const form = document.getElementById("login-form");
    const formData = new FormData(form);

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            body: formData, // Envia os dados como form data
            credentials: "same-origin"
        });
        
        const result = await response.json();

        if (response.ok) {
            // Salva os dados do usuário no sessionStorage
            sessionStorage.setItem('nickname', result.nickname);  // Salva o nickname
            sessionStorage.setItem('user_id', result.user_id);       // Salva o user_id

            alert("Login realizado com sucesso!");
            window.location.href = "/chat";
        } else {
            document.getElementById("erro").innerText = result.error || "Erro ao fazer login.";
        }
    } catch (error) {
        console.error("Erro:", error);
        document.getElementById("erro").innerText = "Erro na requisição.";
    }
});
