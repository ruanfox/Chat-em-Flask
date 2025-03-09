document.getElementById("login-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Evita o reload da página

    const data = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    console.log("Enviando dados:", data); // Debug no console

    try {
        const response = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Login realizado com sucesso!");
            window.location.href = "/"
        } else {
            document.getElementById("erro").innerText = result.error || "Erro ao fazer login.";
        }
    } catch (error) {
        console.error("Erro:", error);
        document.getElementById("erro").innerText = "Erro na requisição.";
    }
});
