const backgroundColor = getComputedStyle(document.documentElement).getPropertyValue("--background-color");

const canvasElement = document.getElementById("snakeCanvas");
if (!(canvasElement instanceof HTMLCanvasElement)) {
    throw new Error("Snake canvas was not found.");
}
const canvas = canvasElement;

const canvasContext = canvas.getContext("2d");
if (!canvasContext) {
    throw new Error("Snake canvas does not support 2D rendering.");
}
const context = canvasContext;

const gridSize = 15;
const cellSize = canvas.width / gridSize;
let snake = [
    { x: 7, y: 7 },
    { x: 6, y: 7 },
    { x: 5, y: 7 },
];
let direction = { x: 1, y: 0 };
let nextDirection = direction;
let food = { x: 11, y: 7 };

function drawCell(cell, color) {
    context.fillStyle = color;
    context.fillRect(
        cell.x * cellSize + 1,
        cell.y * cellSize + 1,
        cellSize - 2,
        cellSize - 2,
    );
}

function draw() {
    context.fillStyle = backgroundColor; // get css background color
    context.fillRect(0, 0, canvas.width, canvas.height);
    drawCell(food, "#f44336");
    snake.forEach((cell, index) => drawCell(cell, index === 0 ? "#8bc34a" : "#4caf50"));
}

function isSameCell(first, second) {
    return first.x === second.x && first.y === second.y;
}

function placeFood() {
    do {
        food = {
            x: Math.floor(Math.random() * gridSize),
            y: Math.floor(Math.random() * gridSize),
        };
    } while (snake.some((cell) => isSameCell(cell, food)));
}

function resetSnake() {
    snake = [
        { x: 7, y: 7 },
        { x: 6, y: 7 },
        { x: 5, y: 7 },
    ];
    direction = { x: 1, y: 0 };
    nextDirection = direction;
}

function move() {
    direction = nextDirection;
    const head = {
        x: (snake[0].x + direction.x + gridSize) % gridSize,
        y: (snake[0].y + direction.y + gridSize) % gridSize,
    };

    if (snake.some((cell) => isSameCell(cell, head))) {
        resetSnake();
        draw();
        return;
    }

    snake.unshift(head);
    if (isSameCell(head, food)) {
        placeFood();
    } else {
        snake.pop();
    }
    draw();
}

const directions = {
    ArrowUp: { x: 0, y: -1 },
    ArrowDown: { x: 0, y: 1 },
    ArrowLeft: { x: -1, y: 0 },
    ArrowRight: { x: 1, y: 0 },
};

document.addEventListener("keydown", (event) => {
    const requestedDirection = directions[event.key];
    if (
        requestedDirection &&
        requestedDirection.x !== -direction.x &&
        requestedDirection.y !== -direction.y
    ) {
        nextDirection = requestedDirection;
        event.preventDefault();
    }
});

draw();
window.setInterval(move, 150);
