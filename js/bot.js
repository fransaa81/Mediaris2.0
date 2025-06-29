let botStep = 0;
let userName = "Usuario"; // Nombre por defecto
let userTopic = "consulta general"; // Tema por defecto
let userDetails = "";
let additionalInfo = "";
let conversationStarted = false;

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
  conversationStarted = false;
  const chat = document.getElementById('bot-chat-window');
  chat.innerHTML = '';
  agregarMensajeBot("Conectando con el asistente de mediación...");
  document.getElementById('bot-input').value = '';
  document.getElementById('bot-input').focus();
  
  // Conectar directamente con el asistente
  conectarConAsistente();
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

function procesarRespuestaUsuario(input) {
  agregarMensajeUsuario(input);
  
  // Si la conversación ya está activa, enviar mensaje al asistente
  if (conversationStarted) {
    enviarMensajeAlAsistente(input);
  }
}

// Función para enviar mensajes al asistente
async function enviarMensajeAlAsistente(mensaje) {
  try {
    agregarMensajeBot("Procesando tu mensaje...");
    
    const response = await fetch('http://127.0.0.1:5000/send_message', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: mensaje
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Remover el mensaje "Procesando..."
    const chatWindow = document.getElementById('bot-chat-window');
    const lastMessage = chatWindow.lastElementChild;
    if (lastMessage && lastMessage.textContent === "Procesando tu mensaje...") {
      chatWindow.removeChild(lastMessage);
    }

    if (data.status === 'success') {
      agregarMensajeBot(data.data.response);
    } else {
      agregarMensajeBot("Error: " + data.message);
    }
  } catch (error) {
    console.error('Error al enviar mensaje:', error);
    agregarMensajeBot("Error al enviar mensaje: " + error.message);
  }
}

// Función para conectar con el asistente de OpenAI
async function conectarConAsistente() {
  try {
    console.log('Conectando directamente con el asistente...');

    const response = await fetch('http://127.0.0.1:5000/start_assistant', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userName: userName,
        userTopic: userTopic
      })
    });

    console.log('Respuesta del servidor:', response);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('Datos recibidos:', data);

    // Remover el mensaje "Conectando..."
    const chatWindow = document.getElementById('bot-chat-window');
    const lastMessage = chatWindow.lastElementChild;
    if (lastMessage && lastMessage.textContent === "Conectando con el asistente de mediación...") {
      chatWindow.removeChild(lastMessage);
    }

    if (data.status === 'success') {
      agregarMensajeBot(data.data.response);
      // Marcar que la conversación con el asistente ha comenzado
      conversationStarted = true;
    } else {
      agregarMensajeBot("Error: " + data.message);
    }
  } catch (error) {
    console.error('Error al conectar con el agente:', error);
    agregarMensajeBot("Error al conectar con el agente: " + error.message);
  }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  const inputForm = document.getElementById('bot-input-form');
  const userInput = document.getElementById('bot-input');
  const closeBtn = document.getElementById('cerrar-bot-dialog');
  const openBotBtn = document.getElementById('abrir-bot-dialogo');

  // Event listener para el formulario de input
  if (inputForm) {
    inputForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const input = userInput.value.trim();
      if (input) {
        procesarRespuestaUsuario(input);
        userInput.value = '';
      }
    });
  }

  // Event listener para cerrar el diálogo
  if (closeBtn) {
    closeBtn.addEventListener('click', function(e) {
      e.preventDefault();
      cerrarBotDialog();
    });
  }

  // Event listener para abrir el diálogo
  if (openBotBtn) {
    openBotBtn.addEventListener('click', function(e) {
      e.preventDefault();
      abrirBotDialog();
    });
  }

  // Event listener para cerrar al hacer clic fuera del modal
  const botModal = document.getElementById('bot-dialog-modal');
  if (botModal) {
    botModal.addEventListener('click', function(e) {
      if (e.target === botModal) {
        cerrarBotDialog();
      }
    });
  }

  // Event listener para cerrar con la tecla Escape
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
      const modal = document.getElementById('bot-dialog-modal');
      if (modal && modal.style.display !== 'none') {
        cerrarBotDialog();
      }
    }
  });
});