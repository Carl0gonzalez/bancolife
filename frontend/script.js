// Configuración de la API
const API_BASE_URL = "http://localhost:5000";

// Función para verificar el estado de la API
async function checkApiStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (response.ok) {
      document.getElementById("api-status").className =
        "status-indicator status-online";
      document.getElementById("api-text").textContent = "Conectado";
    } else {
      throw new Error("API no responde correctamente");
    }
  } catch (error) {
    document.getElementById("api-status").className =
      "status-indicator status-offline";
    document.getElementById("api-text").textContent = "Desconectado";
  }
}

// Función para mostrar respuestas
function mostrarRespuesta(elementId, data, tipo = "info") {
  const element = document.getElementById(elementId);
  element.style.display = "block";
  element.className = `response ${tipo}`;

  if (typeof data === "object") {
    element.textContent = JSON.stringify(data, null, 2);
  } else {
    element.textContent = data;
  }
}

// Función para ocultar respuestas
function ocultarRespuesta(elementId) {
  document.getElementById(elementId).style.display = "none";
}

// Función para hacer peticiones a la API
async function apiRequest(endpoint, method = "GET", data = null) {
  try {
    const options = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Error en la petición");
    }

    return result;
  } catch (error) {
    throw new Error(`Error de conexión: ${error.message}`);
  }
}

// ===== GESTIÓN DE CLIENTES =====

// Crear cliente
document
  .getElementById("clienteForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const clienteData = {
      nombre: formData.get("nombre"),
      correo: formData.get("correo"),
    };

    try {
      const result = await apiRequest("/clientes", "POST", clienteData);
      mostrarRespuesta("clientesResponse", result, "success");
      this.reset();
    } catch (error) {
      mostrarRespuesta("clientesResponse", error.message, "error");
    }
  });

// Cargar clientes
async function cargarClientes() {
  try {
    const clientes = await apiRequest("/clientes");
    mostrarRespuesta("clientesResponse", clientes, "info");
  } catch (error) {
    mostrarRespuesta("clientesResponse", error.message, "error");
  }
}

// ===== GESTIÓN DE CUENTAS =====

// Crear cuenta
document
  .getElementById("cuentaForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const cuentaData = {
      cliente_id: parseInt(formData.get("cliente_id")),
      saldo: parseFloat(formData.get("saldo_inicial") || 0),
    };

    try {
      const result = await apiRequest("/cuentas", "POST", cuentaData);
      mostrarRespuesta("cuentasResponse", result, "success");
      this.reset();
    } catch (error) {
      mostrarRespuesta("cuentasResponse", error.message, "error");
    }
  });

// Cargar cuentas
async function cargarCuentas() {
  try {
    const cuentas = await apiRequest("/cuentas");
    mostrarRespuesta("cuentasResponse", cuentas, "info");
  } catch (error) {
    mostrarRespuesta("cuentasResponse", error.message, "error");
  }
}

// ===== GESTIÓN DE TRANSFERENCIAS =====

// Realizar transferencia
document
  .getElementById("transferenciaForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const transferenciaData = {
      cuenta_origen: parseInt(formData.get("cuenta_origen")),
      cuenta_destino: parseInt(formData.get("cuenta_destino")),
      monto: parseFloat(formData.get("monto")),
    };

    try {
      const result = await apiRequest(
        "/transferencias",
        "POST",
        transferenciaData
      );
      mostrarRespuesta("transferenciasResponse", result, "success");
      this.reset();
    } catch (error) {
      mostrarRespuesta("transferenciasResponse", error.message, "error");
    }
  });

// Cargar transferencias
async function cargarTransferencias() {
  try {
    const transferencias = await apiRequest("/transferencias");
    mostrarRespuesta("transferenciasResponse", transferencias, "info");
  } catch (error) {
    mostrarRespuesta("transferenciasResponse", error.message, "error");
  }
}

// ===== FUNCIONES AUXILIARES =====

// Función para limpiar todas las respuestas
function limpiarRespuestas() {
  ocultarRespuesta("clientesResponse");
  ocultarRespuesta("cuentasResponse");
  ocultarRespuesta("transferenciasResponse");
}

// Función para formatear fechas
function formatearFecha(fechaString) {
  const fecha = new Date(fechaString);
  return fecha.toLocaleString("es-ES");
}

// Función para formatear moneda
function formatearMoneda(monto) {
  return new Intl.NumberFormat("es-ES", {
    style: "currency",
    currency: "USD",
  }).format(monto);
}

// ===== INICIALIZACIÓN =====

// Verificar estado de la API al cargar la página
document.addEventListener("DOMContentLoaded", function () {
  checkApiStatus();

  // Verificar estado cada 30 segundos
  setInterval(checkApiStatus, 30000);

  console.log("BancoLite Frontend cargado correctamente");
  console.log("API Base URL:", API_BASE_URL);
});

// Función para mostrar información de ayuda
function mostrarAyuda() {
  const ayuda = `
=== BancoLite - Guía de Uso ===

1. GESTIÓN DE CLIENTES:
   - Crear cliente: Completa nombre y correo
   - Cargar clientes: Ver todos los clientes registrados

2. GESTIÓN DE CUENTAS:
   - Crear cuenta: Necesitas el ID del cliente
   - Cargar cuentas: Ver todas las cuentas

3. TRANSFERENCIAS:
   - Realizar transferencia: Usa IDs de cuenta origen y destino
   - Cargar transferencias: Ver historial de transferencias

NOTAS:
- Los IDs se generan automáticamente
- Las transferencias requieren saldo suficiente
- No se puede transferir a la misma cuenta
- Todos los montos deben ser positivos
    `;

  alert(ayuda);
}

// Agregar botón de ayuda al header
document.addEventListener("DOMContentLoaded", function () {
  const header = document.querySelector(".header");
  const ayudaButton = document.createElement("button");
  ayudaButton.textContent = "❓ Ayuda";
  ayudaButton.style.cssText = `
        position: absolute;
        top: 20px;
        right: 20px;
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
    `;
  ayudaButton.onclick = mostrarAyuda;
  header.style.position = "relative";
  header.appendChild(ayudaButton);
});
