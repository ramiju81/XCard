
document.addEventListener("DOMContentLoaded", function () {
  // 1. Verificar CSS
  const stylesheets = Array.from(document.styleSheets || []);
  const cssLoaded = stylesheets.some(sheet => sheet.href && sheet.href.includes('styles.css'));
  if (!cssLoaded) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = './statics/css/styles.css';
    document.head.appendChild(link);
  }

  // 2. Cargar VCF
  fetch("./statics/XD.vcf")
    .then(res => res.text())
    .then(data => {
      const getValue = (key) => {
        const regex = new RegExp(`${key}:(.*)`, "i");
        const match = data.match(regex);
        return match ? match[1].trim() : "";
      };

      const nombre = getValue("FN");
      const telefono = getValue("TEL");
      const direccionRaw = getValue("ADR;TYPE=home");
      const direccion = direccionRaw ? direccionRaw.split(";").filter(Boolean).join(" ").trim() : "";
      const nota = getValue("NOTE");

      const urls = data.match(/URL:(.*)/gi)?.map(u => u.replace(/URL:/i, "").trim()) || [];

      // Escribe en DOM con checks (evitamos errores si falta elemento)
      const elName = document.querySelector("h1");
      const elH2 = document.querySelector("h2");
      const elCargo = document.querySelector(".cargo");
      const elUni = document.querySelector(".ubicacion.uni");
      const elDireccion = document.querySelector(".ubicacion.direccion");
      const elMensaje = document.querySelector(".mensaje p");
      const aWhats = document.querySelector(".whatsapp");
      const aX = document.querySelector(".X");

      if (elName) elName.textContent = nombre || "";
      if (elH2) elH2.textContent = "";
      if (elCargo) elCargo.innerHTML = "";
      if (elUni) elUni.innerHTML = "";
      if (elDireccion) elDireccion.innerHTML = `<i class="fas fa-map-marker-alt"></i> ${direccion || ""}`;
      if (elMensaje) elMensaje.textContent = nota || "";

      // WhatsApp -> limpiar teléfono dejando solo dígitos
      const phoneDigits = telefono ? telefono.replace(/\D/g, "") : "";
      if (aWhats) {
        if (phoneDigits) {
          aWhats.href = `https://wa.me/${phoneDigits}`;
          aWhats.style.display = ""; // mostrar si estaba oculto
        } else {
          aWhats.style.display = "none";
        }
      }

      // Buscar URL de X/Twitter sin depender del orden
      const xRegex = /https?:\/\/(www\.)?(x\.com|twitter\.com)\/\S*/i;
      const xMatch = urls.map(u => u.match(xRegex)).find(m => m);
      if (aX) {
        if (xMatch) {
          // encontrar la url original que cumpla
          const xUrl = urls.find(u => xRegex.test(u));
          aX.href = xUrl;
          aX.style.display = "";
        } else {
          aX.style.display = "none";
        }
      }
    })
    .catch(err => console.error("Error cargando datos del VCF:", err));

  // 3. Guardar contacto (descarga del .vcf)
  const guardarBtn = document.getElementById("guardarContacto");
  if (guardarBtn) {
    guardarBtn.addEventListener("click", function (e) {
      e.preventDefault();
      const vcfUrl = "./statics/XD.vcf";
      const link = document.createElement("a");
      link.href = vcfUrl;
      link.download = "Julian_R.vcf";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  }
});