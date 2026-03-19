// Inicializar Librería de Animaciones
AOS.init({ duration: 1000, once: true });

// AJAX Formulario
document.getElementById('quote-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const messageDiv = document.getElementById('form-message');
    
    messageDiv.innerText = "Enviando cotización...";

    fetch('/cotizar', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            messageDiv.style.color = "green";
            messageDiv.innerText = "✅ ¡Listo! Rafael Diaz ha recibido tu solicitud.";
            this.reset(); // Limpia el formulario
        } else {
            messageDiv.style.color = "red";
            messageDiv.innerText = "❌ Error al enviar. Intenta de nuevo.";
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});