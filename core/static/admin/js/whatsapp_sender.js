function sendWhatsApp(buttonElement) {
    let telefono = buttonElement.getAttribute('data-telefono');
    let mensaje = buttonElement.getAttribute('data-mensaje');

    // Remove any spaces or special characters from the phone number just in case
    if (telefono) {
        telefono = telefono.replace(/[^0-9+]/g, '');
    }

    if (!telefono) {
        // Prompt for phone number if missing
        telefono = prompt("Este usuario no tiene un número de teléfono registrado.\nPor favor, ingresa el número (incluyendo el código de país, ej. +51...):");
        if (!telefono) {
            alert("Envío cancelado. Se requiere un número de teléfono.");
            return;
        }
        // Basic clean up of prompted input
        telefono = telefono.replace(/[^0-9+]/g, '');
    }

    // Confirm sending
    if (confirm("¿Estás seguro de que deseas enviar la invitación por WhatsApp al número " + telefono + "?")) {
        const url = "https://wa.me/" + telefono + "?text=" + mensaje;
        window.open(url, '_blank');
    }
}