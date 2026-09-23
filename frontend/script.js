/**
 * script.js
 *
 * Reimplementação em JavaScript puro do mesmo algoritmo de BFS que existe
 * em src/delivery_zone_mapper/pathfinder.py — decisão de arquitetura:
 * manter essa demo 100% client-side (sem backend) simplifica o deploy
 * (basta abrir o index.html) ao custo de duplicar a lógica em duas
 * linguagens. Para um produto real eu manteria as duas em sincronia com
 * testes; aqui é uma troca aceitável para uma vitrine visual.
 *
 * Nota: usamos Array.shift() como fila, que é O(n) em JS (assim como
 * list.pop(0) em Python). Para uma grade deste tamanho (algumas centenas
 * de células) isso é irrelevante na prática; no núcleo em Python optamos
 * por collections.deque exatamente para evitar esse custo em mapas maiores.
 */

const ROWS = 12;
const COLS = 18;

const FREE = 0;
const OBSTACLE = 1;

let grid = createEmptyGrid();
let restaurant = { r: 2, c: 2 };
let client = { r: ROWS - 3, c: COLS - 3 };
let mode = "obstacle";
let isAnimating = false;

const gridEl = document.getElementById("grid");
const statusEl = document.getElementById("status");
const statDistanceEl = document.getElementById("stat-distance");
const statVisitedEl = document.getElementById("stat-visited");

function createEmptyGrid() {
  return Array.from({ length: ROWS }, () => Array(COLS).fill(FREE));
}

function cellKey(r, c) {
  return `${r},${c}`;
}

function render() {
  gridEl.style.gridTemplateColumns = `repeat(${COLS}, 1fr)`;
  gridEl.innerHTML = "";

  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const cell = document.createElement("button");
      cell.type = "button";
      cell.className = "cell";
      cell.dataset.r = String(r);
      cell.dataset.c = String(c);
      cell.setAttribute("aria-label", `Célula linha ${r + 1}, coluna ${c + 1}`);

      if (r === restaurant.r && c === restaurant.c) {
        cell.classList.add("restaurant");
      } else if (r === client.r && c === client.c) {
        cell.classList.add("client");
      } else if (grid[r][c] === OBSTACLE) {
        cell.classList.add("obstacle");
      }

      cell.addEventListener("click", () => handleCellClick(r, c));
      gridEl.appendChild(cell);
    }
  }
}

function handleCellClick(r, c) {
  if (isAnimating) return;

  if (mode === "restaurant") {
    if (r === client.r && c === client.c) return;
    restaurant = { r, c };
    grid[r][c] = FREE;
  } else if (mode === "client") {
    if (r === restaurant.r && c === restaurant.c) return;
    client = { r, c };
    grid[r][c] = FREE;
  } else {
    const isEndpoint = (r === restaurant.r && c === restaurant.c) || (r === client.r && c === client.c);
    if (isEndpoint) return;
    grid[r][c] = grid[r][c] === FREE ? OBSTACLE : FREE;
  }

  setStatus("Mapa editado. Clique em Calcular rota quando estiver pronto.");
  render();
}

/* --- BFS (equivalente ao pathfinder.py) ------------------------------ */

function neighbors(r, c) {
  const deltas = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1],
  ];
  const result = [];
  for (const [dr, dc] of deltas) {
    const nr = r + dr;
    const nc = c + dc;
    if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS && grid[nr][nc] === FREE) {
      result.push([nr, nc]);
    }
  }
  return result;
}

function bfs(start, goal) {
  const queue = [[start.r, start.c]];
  const cameFrom = new Map([[cellKey(start.r, start.c), null]]);
  const visitedOrder = [];

  while (queue.length > 0) {
    const current = queue.shift();
    visitedOrder.push(current);

    if (current[0] === goal.r && current[1] === goal.c) {
      return { path: reconstructPath(cameFrom, current), visitedOrder };
    }

    for (const [nr, nc] of neighbors(current[0], current[1])) {
      const key = cellKey(nr, nc);
      if (!cameFrom.has(key)) {
        cameFrom.set(key, current);
        queue.push([nr, nc]);
      }
    }
  }

  return { path: null, visitedOrder };
}

function reconstructPath(cameFrom, goal) {
  const path = [goal];
  let current = goal;
  while (cameFrom.get(cellKey(current[0], current[1])) !== null) {
    current = cameFrom.get(cellKey(current[0], current[1]));
    path.push(current);
  }
  return path.reverse();
}

/* --- Execução e animação ---------------------------------------------- */

function getCellEl(r, c) {
  return gridEl.querySelector(`[data-r="${r}"][data-c="${c}"]`);
}

function clearHighlights() {
  gridEl.querySelectorAll(".visited, .path").forEach((el) => el.classList.remove("visited", "path"));
}

function setStatus(text) {
  statusEl.textContent = text;
}

function runSearch() {
  if (isAnimating) return;

  clearHighlights();
  statDistanceEl.textContent = "—";
  statVisitedEl.textContent = "—";

  const { path, visitedOrder } = bfs(restaurant, client);
  const delay = Math.max(4, Math.min(18, Math.floor(500 / Math.max(visitedOrder.length, 1))));

  isAnimating = true;
  setStatus("Calculando rota com BFS...");

  visitedOrder.forEach(([r, c], i) => {
    setTimeout(() => {
      const cell = getCellEl(r, c);
      if (cell && !cell.classList.contains("restaurant") && !cell.classList.contains("client")) {
        cell.classList.add("visited");
      }
      statVisitedEl.textContent = String(i + 1);
    }, i * delay);
  });

  setTimeout(() => {
    if (!path) {
      isAnimating = false;
      setStatus("Não existe rota entre o restaurante e o cliente — remova um obstáculo para conectar as duas zonas.");
      return;
    }

    path.forEach(([r, c], i) => {
      setTimeout(() => {
        const cell = getCellEl(r, c);
        if (cell && !cell.classList.contains("restaurant") && !cell.classList.contains("client")) {
          cell.classList.add("path");
        }

        if (i === path.length - 1) {
          isAnimating = false;
          statDistanceEl.textContent = String(path.length - 1);
          setStatus(`Rota calculada — ${path.length - 1} passos.`);
        }
      }, i * delay);
    });
  }, visitedOrder.length * delay + 60);
}

/* --- Ações do toolbar --------------------------------------------------- */

document.querySelectorAll(".tool").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tool").forEach((b) => b.setAttribute("aria-pressed", "false"));
    btn.setAttribute("aria-pressed", "true");
    mode = btn.dataset.mode;
  });
});

document.getElementById("btn-random").addEventListener("click", () => {
  if (isAnimating) return;
  grid = createEmptyGrid();
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      if (Math.random() < 0.22) grid[r][c] = OBSTACLE;
    }
  }
  grid[restaurant.r][restaurant.c] = FREE;
  grid[client.r][client.c] = FREE;
  clearHighlights();
  statDistanceEl.textContent = "—";
  statVisitedEl.textContent = "—";
  setStatus("Mapa aleatório gerado. Clique em Calcular rota para ver o BFS em ação.");
  render();
});

document.getElementById("btn-clear").addEventListener("click", () => {
  if (isAnimating) return;
  grid = createEmptyGrid();
  clearHighlights();
  statDistanceEl.textContent = "—";
  statVisitedEl.textContent = "—";
  setStatus("Mapa limpo. Clique num modo acima e depois numa célula do mapa para editar.");
  render();
});

document.getElementById("btn-run").addEventListener("click", runSearch);

render();
