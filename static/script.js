let nombres = [];
let colores = [];
const canvas = document.getElementById("ruleta");
const ctx = canvas.getContext("2d");
let startAngle = 0;
let arc = Math.PI / 6;
let contadorGanadores = 0;
let ganadores = [];

function actualizarParticipantes() {
  const participantes = document.getElementById("participantes").value
    .split("\n").map(p => p.trim()).filter(p => p);

  nombres = participantes.map(p => p.trim());
  colores = nombres.map(() => "#" + Math.floor(Math.random()*16777215).toString(16));
  drawRouletteWheel();
}

function drawRouletteWheel() {
  let outsideRadius = 180;
  let textRadius = 130;
  let insideRadius = 50;

  ctx.clearRect(0,0,400,400);

  if (nombres.length === 0) {
    ctx.beginPath();
    ctx.arc(200, 200, outsideRadius, 0, 2 * Math.PI);
    ctx.fillStyle = "#ddd";
    ctx.fill();
    ctx.fillStyle = "black";
    ctx.font = "18px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Agrega participantes", 200, 200);
    return;
  }

  arc = Math.PI * 2 / nombres.length;

  for(let i = 0; i < nombres.length; i++) {
    let angle = startAngle + i * arc;
    ctx.fillStyle = colores[i];

    ctx.beginPath();
    ctx.arc(200, 200, outsideRadius, angle, angle + arc, false);
    ctx.arc(200, 200, insideRadius, angle + arc, angle, true);
    ctx.fill();

    ctx.save();
    ctx.fillStyle = "white";
    ctx.font = "bold 20px Arial";
    ctx.textAlign = "center";
    ctx.translate(
      200 + Math.cos(angle + arc/2) * textRadius,
      200 + Math.sin(angle + arc/2) * textRadius
    );
    ctx.rotate(angle + arc/2 + Math.PI/2);
    ctx.fillText(nombres[i], 0, 0);
    ctx.restore();
  }

  // Flecha
  ctx.fillStyle = "black";
  ctx.beginPath();
  ctx.moveTo(200 - 4, 200 - (outsideRadius + 5));
  ctx.lineTo(200 + 4, 200 - (outsideRadius + 5));
  ctx.lineTo(200 + 4, 200 - (outsideRadius - 5));
  ctx.lineTo(200 - 4, 200 - (outsideRadius - 5));
  ctx.fill();
}

function girarRuleta() {
  const participantes = document.getElementById("participantes").value
    .split("\n").map(p => p.trim()).filter(p => p);

  if (participantes.length === 0) {
    alert("Por favor ingresa participantes");
    return;
  }

  fetch("/sorteo", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ participantes })
  })
  .then(res => res.json())
  .then(data => {
    if (data.ganador) {
      spinToWinner(data.ganador);
    }
  });
}

function spinToWinner(winner) {
  const idx = nombres.findIndex(n => n.toUpperCase() === winner.toUpperCase());
  if (idx === -1) return;

  let arcSize = Math.PI * 2 / nombres.length;
  let angle = startAngle + idx * arcSize + arcSize / 2;

  let spinAngle = (Math.PI * 6) - angle + Math.PI/2;
  let spinTime = 0;
  let spinTimeTotal = 4000;

  function rotate() {
    spinTime += 30;
    if (spinTime >= spinTimeTotal) {
      stopRotate(winner);
      return;
    }
    let spinAngleStep = spinAngle * (1 - spinTime/spinTimeTotal);
    startAngle += spinAngleStep;
    drawRouletteWheel();
    requestAnimationFrame(rotate);
  }

  rotate();
}

function stopRotate(winner) {
  contadorGanadores++;
  ganadores.push(winner);

  // Elegir emoji según el contador
  let emoji = contadorGanadores === 1 ? "🥇" : "🥈";

  // Agregar el ganador con el emoji
  document.getElementById("resultado").innerHTML += 
    `<p>${contadorGanadores}° Ganador: ${winner} ${emoji}</p>`;

  if (contadorGanadores >= 2) {
    document.getElementById("btnGirar").disabled = true;
    document.getElementById("btnReiniciar").style.display = "inline-block";
  }
}


function reiniciar() {
  contadorGanadores = 0;
  ganadores = [];
  document.getElementById("resultado").innerHTML = "";
  document.getElementById("btnGirar").disabled = false;
  document.getElementById("btnReiniciar").style.display = "none";
  drawRouletteWheel();
}

// Evento: actualizar en tiempo real mientras escribes
document.getElementById("participantes").addEventListener("input", actualizarParticipantes);

// Dibuja la ruleta vacía al inicio
drawRouletteWheel();

