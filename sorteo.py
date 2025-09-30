from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# Ganadores fijos definidos
GANADORES_FIJOS = ["jerika", "jennifer"]
ganadores_mostrados = []  # Para controlar que no se repitan en la misma ronda

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sorteo', methods=['POST'])
def sorteo():
    global ganadores_mostrados

    data = request.get_json()
    participantes = data.get("participantes", [])

    # Normalizar a minúsculas
    participantes = [p.strip().lower() for p in participantes if p.strip()]

    if not participantes:
        return jsonify({"ganador": None})

    # Primero revisamos si los ganadores fijos están en la lista y no han salido aún
    for fijo in GANADORES_FIJOS:
        if fijo in participantes and fijo not in ganadores_mostrados:
            ganadores_mostrados.append(fijo)
            return jsonify({"ganador": fijo.capitalize()})

    # Si no hay fijos pendientes, elegimos al azar entre los que no han salido
    restantes = [p for p in participantes if p not in ganadores_mostrados]
    if not restantes:  # Si ya no quedan, reiniciamos
        ganadores_mostrados = []
        restantes = participantes

    ganador = random.choice(restantes)
    ganadores_mostrados.append(ganador)

    return jsonify({"ganador": ganador.capitalize()})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
