import qrcode
from PIL import Image

# Configuración
qr_data = "https://womo-solucions.github.io/XCard/"
qr_logo_path = "logo.png"
qr_output_path = "QR_XD.png"
html_output_path = "index.html"

# 1. Generar el código QR
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr.add_data(qr_data)
qr.make(fit=True)

qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

# 2. Procesar el logo con fondo blanco moderado
logo_size = 80  # Tamaño del logo
logo = Image.open(qr_logo_path).convert("RGBA")
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# Crear fondo blanco (solo 10px más grande en cada lado)
bg_size = (logo_size + 20, logo_size + 20)
background = Image.new("RGBA", bg_size, "white")

# Pegar el logo centrado en el fondo
logo_pos = (
    (bg_size[0] - logo_size) // 2,
    (bg_size[1] - logo_size) // 2
)
background.paste(logo, logo_pos, logo)

# 3. Pegar en el QR
qr_pos = (
    (qr_img.size[0] - bg_size[0]) // 2,
    (qr_img.size[1] - bg_size[1]) // 2
)
qr_img.paste(background, qr_pos, background)

# 4. Guardar QR
qr_img.save(qr_output_path)

# 5. HTML ORIGINAL COMPLETO (sin modificaciones)
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>XD</title>
  <link rel="stylesheet" href="./statics/css/styles.css">
  <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
  <div class="vcard">
    <div class="amber-fade"></div>
    <div class="bg-pattern"></div>

    <div class="content">
      <!-- Foto -->
      <div class="photo-frame">
        <img src="./statics/img/foto.jpg" alt="Foto de perfil"
             onerror="this.src='https://via.placeholder.com/400'">
      </div>

      <!-- Info -->
      <div class="info">
        <h1></h1> <!-- Nombre -->
        <h2></h2> <!-- Empresa -->
        <div class="details">
          <p class="cargo"><i class="fas fa-briefcase"></i></p> <!-- Cargo -->
          <p class="ubicacion uni"><i class="fas fa-university"></i></p> <!-- Universidad -->
          <p class="ubicacion direccion"><i class="fas fa-map-marker-alt"></i></p> <!-- Dirección -->
        </div>
      </div>

      <!-- Redes -->
      <div class="social">    
        <a href="#" class="whatsapp" title="WhatsApp"><i class="fab fa-whatsapp"></i></a>
        <a href="#" class="X" title="X.com"><i class="fab fa-x-twitter"></i></a>
        <a href="https://instagram.com/eljuliramirez" title="instagram" class="instagram"><i class="fab fa-instagram"></i></a>
      </div>

      <!-- Mensaje -->
      <div class="mensaje-box">
        <div class="mensaje">
          <p></p>
        </div>
      </div>
        <!-- Guardar contacto -->
        <div class="guardar-contacto">
          <a href="#" id="guardarContacto" title="Guardar contacto">
            <i class="fas fa-address-book"></i>
          </a>
        </div>
    </div>
  </div>

  <!-- Script unificado -->
  <script src="./statics/js/scripts.js"></script>
</body>
</html>
"""

# 6. Guardar HTML
with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ QR, HTML generados.")