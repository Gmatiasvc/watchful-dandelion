function sendWhatsApp(buttonElement) {
    let telefono = buttonElement.getAttribute('data-telefono');
    let nombre = buttonElement.getAttribute('data-nombre');
    let hashId = buttonElement.getAttribute('data-hash');

    if (telefono) {
        telefono = telefono.replace(/[^0-9+]/g, '');
    }

    if (!telefono) {
        telefono = prompt(`Este usuario no tiene un número de teléfono registrado.\nPor favor, ingresa el número para ${nombre} (incluyendo el código de país, ej. +51...):`);
        if (!telefono) {
            alert("Envío cancelado. Se requiere un número de teléfono.");
            return;
        }
        telefono = telefono.replace(/[^0-9+]/g, '');
    }

    const invitationUrl = window.location.origin + "/invitacion/" + hashId + "/";
    const mensaje = `¡Hola ${nombre}! Aquí tienes tu invitación y código QR de acceso para el evento: ${invitationUrl}`;

    if (confirm("¿Estás seguro de que deseas enviar la invitación por WhatsApp al número " + telefono + "?")) {
        const url = "https://wa.me/" + telefono + "?text=" + encodeURIComponent(mensaje);
        window.open(url, '_blank');
    }
}