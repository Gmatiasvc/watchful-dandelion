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

    if (!confirm(`¿Deseas generar y enviar la imagen de la invitación a ${nombre} por WhatsApp? \n\nEl sistema copiará la imagen al portapapeles y abrirá WhatsApp. Solo tendrás que pegar (Ctrl+V) la imagen en el chat y enviar.`)) {
        return;
    }

    // Since we're in the admin, we might not have html2canvas loaded by default.
    // Let's dynamically load it if it's missing.
    if (typeof html2canvas === 'undefined') {
        const script = document.createElement('script');
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js";
        document.head.appendChild(script);

        let originalText = buttonElement.innerHTML;
        buttonElement.innerHTML = 'Cargando librería...';
        buttonElement.disabled = true;

        script.onload = () => {
            buttonElement.innerHTML = originalText;
            buttonElement.disabled = false;
            generateAndSendImage(telefono, nombre, hashId, buttonElement);
        };
        return; // wait for script to load
    } else {
        generateAndSendImage(telefono, nombre, hashId, buttonElement);
    }
}

async function generateAndSendImage(telefono, nombre, hashId, buttonElement) {
    let originalText = buttonElement.innerHTML;
    buttonElement.innerHTML = 'Generando...';
    buttonElement.disabled = true;

    try {
        const response = await fetch(window.location.origin + "/invitacion/" + hashId + "/");
        const htmlText = await response.text();

        const iframe = document.createElement('iframe');
        iframe.style.position = 'absolute';
        iframe.style.width = '600px';
        iframe.style.height = '800px';
        iframe.style.top = '-9999px';
        iframe.style.left = '-9999px';
        document.body.appendChild(iframe);

        iframe.contentDocument.open();
        iframe.contentDocument.write(htmlText);
        iframe.contentDocument.close();

        await new Promise(resolve => {
            iframe.onload = () => {
                setTimeout(resolve, 500);
            };
        });

        const card = iframe.contentDocument.getElementById('invitation-card');

        if (!card) {
            throw new Error("No se pudo encontrar la tarjeta en la invitación.");
        }

        const saved = JSON.parse(localStorage.getItem('invitationConfig'));
        if (saved) {
            if (saved.bg1 && saved.bg2) card.style.background = `linear-gradient(135deg, ${saved.bg1} 0%, ${saved.bg2} 100%)`;
            if (saved.text) {
                Array.from(card.querySelectorAll('.editable-text')).forEach(el => el.style.color = saved.text);
            }
            if (saved.t1) iframe.contentDocument.getElementById('invText1').innerText = saved.t1;
            if (saved.t2) iframe.contentDocument.getElementById('invText2').innerText = saved.t2;
            if (saved.t3) iframe.contentDocument.getElementById('invText3').innerText = saved.t3;
            if (saved.t4) iframe.contentDocument.getElementById('invText4').innerText = saved.t4;
        }

        const canvas = await html2canvas(card, {
            scale: 2,
            useCORS: true,
            backgroundColor: null,
            windowWidth: 600
        });

        document.body.removeChild(iframe);

        canvas.toBlob(async function(blob) {
            try {
                const item = new ClipboardItem({ "image/png": blob });
                await navigator.clipboard.write([item]);

                const url = "https://wa.me/" + telefono;
                window.open(url, '_blank');

                setTimeout(() => {
                    alert("¡Imagen copiada al portapapeles!\n\nSe ha abierto WhatsApp. Solo presiona 'Pegar' (Ctrl+V) en el chat para enviar la imagen.");
                }, 500);

            } catch (err) {
                console.error("Error al copiar al portapapeles:", err);
                alert("No se pudo copiar la imagen al portapapeles automáticamente. Tu navegador podría no soportar esta función.");
            } finally {
                buttonElement.innerHTML = originalText;
                buttonElement.disabled = false;
            }
        }, "image/png");

    } catch (error) {
        console.error(error);
        alert("Error al generar la imagen de la invitación.");
        buttonElement.innerHTML = originalText;
        buttonElement.disabled = false;
    }
}