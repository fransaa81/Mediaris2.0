let botStep = 0;
let userName = "";
let userTema = "";

function abrirBotDialog() {
  document.getElementById('bot-dialog-modal').style.display = 'flex';
  setTimeout(() => {
    document.getElementById('bot-dialog-modal').classList.add('modal-visible');
  }, 10);
  iniciarChatBot();
}

function cerrarBotDialog() {
  document.getElementById('bot-dialog-modal').classList.remove('modal-visible');
  setTimeout(() => {
    document.getElementById('bot-dialog-modal').style.display = 'none';
  }, 300);
}

function iniciarChatBot() {
  botStep = 0;
  userName = "";
  userTema = "";
  const chat = document.getElementById('bot-chat-window');
  chat.innerHTML = '';
  agregarMensajeBot("Bienvenido a Mediaris. Por favor, indícanos tu nombre y apellido.");
  document.getElementById('bot-input').value = '';
  document.getElementById('bot-input').focus();
}

function agregarMensajeBot(texto) {
  const chat = document.getElementById('bot-chat-window');
  const div = document.createElement('div');
  div.className = 'bot-bubble';
  div.innerText = texto;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function agregarMensajeUsuario(texto) {
  const chat = document.getElementById('bot-chat-window');
  const div = document.createElement('div');
  div.className = 'user-bubble';
  div.innerText = texto;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

document.addEventListener('DOMContentLoaded', function() {
  var abrirBot = document.getElementById('abrir-bot-dialogo');
  if (abrirBot) {
    abrirBot.addEventListener('click', function(e) {
      e.preventDefault();
      abrirBotDialog();
    });
  }

  // Cerrar con la X
  var cerrarBot = document.getElementById('cerrar-bot-dialog');
  if (cerrarBot) {
    cerrarBot.addEventListener('click', function(e) {
      e.preventDefault();
      cerrarBotDialog();
    });
  }

  // Manejo del formulario de chat
  const botForm = document.getElementById('bot-input-form');
  if (botForm) {
    botForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const input = document.getElementById('bot-input');
      const texto = input.value.trim();
      if (!texto) return;
      agregarMensajeUsuario(texto);
      input.value = '';
      manejarPasoBot(texto);
    });
  }
});

function manejarPasoBot(texto) {
  if (botStep === 0) {
    // El usuario responde su nombre.
    userName = texto;
    setTimeout(() => {
      agregarMensajeBot("¿Cuéntanos qué tema te gustaría conversar?");
      botStep = 1;
    }, 400);
  } else if (botStep === 1) {
    // El usuario responde el tema.
    userTopic = texto;
    setTimeout(() => {
      agregarMensajeBot("¿Quieres agregar algún detalle o mensaje adicional sobre tu situación?");
      botStep = 2;
    }, 400);
  } else if (botStep === 2) {
    // El usuario responde los detalles.
    setTimeout(() => {
      agregarMensajeBot("Se comunicará con ud un especialista en el tema para abordar.");
      botStep = 3;
    }, 400);
  } else if (botStep === 3) {
    // Una vez que se han contestado las preguntas por defecto, se inicia la conversación
    setTimeout(() => {
      iniciarAgenteOpenia(userName, userTopic);
      botStep = 4;
    }, 400);
  }
}

function iniciarAgenteOpenia(userName, userTopic) {
  agregarMensajeBot("Conectando con el agente IA...");
  
  fetch('/start_agent', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ userName: userName, userTopic: userTopic })
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'success') {
      // Se espera que la API devuelva un mensaje en data.data.response
      let responseMessage = data.data.response || "El agente ya está en línea. Continúa la conversación.";
      agregarMensajeBot(responseMessage);
    } else {
      agregarMensajeBot("Error al conectar con el agente: " + data.message);
    }
  })
  .catch(error => {
    agregarMensajeBot("Error al conectar con el agente: " + error);
  });
}