from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# Nombres que ganan automáticamente si están presentes
GANADORAS_FIJAS = {"Jerika", "Jennifer"}

# Plantilla HTML mejorada
HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Juego de Sorteo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-family: 'Arial', sans-serif;
        }

        .container {
            max-width: 500px;
            background: white;
            color: #333;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            text-align: center;
            animation: fadeIn 1s ease-in-out;
        }

        textarea {
            resize: none;
            height: 120px;
        }

        .btn-custom {
            background-color: #2575fc;
            color: white;
            font-weight: bold;
            transition: 0.3s;
            border-radius: 10px;
        }

        .btn-custom:hover {
            background-color: #1a5adf;
        }

        .resultado {
            margin-top: 20px;
            font-size: 1.3em;
            font-weight: bold;
            color: #2575fc;
            background: #e6f0ff;
            padding: 15px;
            border-radius: 10px;
            animation: fadeIn 0.5s ease-in-out;
        }

        .footer {
            margin-top: 15px;
            font-size: 0.9em;
            color: #ddd;
            text-align: center;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="mb-4">🎲 Juego de Sorteo</h1>
        <p class="text-muted">Ingresa los nombres de los participantes.</p>

        <form method="POST">
            <div class="mb-3">
                <textarea class="form-control" name="nombres" placeholder="Ejemplo:\nPedro\nSofia"></textarea>
            </div>
            <button type="submit" class="btn btn-custom w-100">Sortear</button>
        </form>

        {% if resultado %}
            <div class="resultado">
                {{ resultado }}
            </div>
        {% endif %}

        <div class="footer">
            <p>Desarrollado con ❤️ en Flask</p>
        </div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def sorteo():
    resultado = None
    if request.method == "POST":
        # Obtener nombres ingresados, limpiar espacios y líneas vacías
        nombres = request.form["nombres"].splitlines()
        nombres = [n.strip() for n in nombres if n.strip()]

        if len(nombres) < 2:
            resultado = "⚠️ Necesitas ingresar al menos dos nombres para el sorteo."
        else:
            # Verificar si Jerika y Jennifer están en la lista
            if GANADORAS_FIJAS.issubset(nombres):
                ganadores = list(GANADORAS_FIJAS)
                resultado = f"🎉 ¡Ganadoras automáticas! {ganadores[0]} y {ganadores[1]}."
            else:
                # Seleccionar dos ganadores aleatorios diferentes
                ganadores = random.sample(nombres, 2)
                resultado = f"🎉 Los ganadores al azar son: {ganadores[0]} y {ganadores[1]}."

    return render_template_string(HTML, resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
