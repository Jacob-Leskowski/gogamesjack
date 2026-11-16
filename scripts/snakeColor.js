// general information used by both the front and back

console.log("Script loaded successfully.");

class int2 {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    toString() {
        return `(${this.x}, ${this.y})`;
    }

    length() {
        return Math.sqrt((this.x ** 2) + (this.y ** 2));
    }

    copy() {
        return int2(this.x, this.y);
    }

    *[Symbol.iterator]() {
        index = 0;
        while (true) {
            yield [this.x, this.y][index];
            index = 1 - index;
        }
    }

    add(other) {
        if (typeof other === "number") {
            return new int2(this.x + other, this.y + other);
        }
        return new int2(this.x + other.x, this.y + other.y);
    }

    add(other) {
        if (typeof other === "number") {
            return new int2(this.x + other, this.y + other);
        }
        return new int2(this.x + other.x, this.y + other.y);
    }

    sub(other) {
        if (typeof other === "number") {
            return new int2(this.x - other, this.y - other);
        }
        return new int2(this.x - other.x, this.y - other.y);
    }

    mul(other) {
        if (typeof other === "number") {
            return new int2(this.x * other, this.y * other);
        }
        return new int2(this.x * other.x, this.y * other.y);
    }

    div(other) {
        if (typeof other === "number") {
            return new int2(this.x / other, this.y / other);
        }
        return new int2(this.x / other.x, this.y / other.y);
    }


    fdiv(other) {
        if (typeof other === "number") {
            return new int2(~~(this.x / other), ~~(this.y / other));
        }
        return new int2(~~(this.x / other.x), ~~(this.y / other.y));
    }
}

const boardSize = new int2(10, 8);

// backend information used by the backend

class Snake {
    constructor() {
        this.head = boardSize.fdiv(2);
        this.length = 3;
        this.body = [this.head.sub(new int2(1, 0)), this.head.sub(new int2(2, 0))];
        this.direction = new int2(1, 0);
        this.controls = ["w", "a", "s", "d"];
    }

    update() {
        this.body.unshift(this.head.copy());
        this.head = this.head.add(direction);
        if (len(this.body) > this.length) {
            this.body.pop()
        }
    }
}

const snake = new Snake();

document.addEventListener('keydown', (event) => {
    if (event.code === 'W') {
        snake.direction = new int2(0, 1);
    }
    if (event.code === 'A') {
        snake.direction = new int2(-1, 0);
    }
    if (event.code === 'S') {
        snake.direction = new int2(0, -1);
    }
    if (event.code === 'D') {
        snake.direction = new int2(1, 0);
    }
    console.log(`Key pressed: ${event.key} | Code: ${event.code}`);
});

// frontend information used by the frontend

// canvas
//const canvasElement = document.getElementById("snakeCanvas");

class Color {
    constructor(r = "#00000000", g = null, b = null, a = null) {
        this.r = r;
        this.g = g;
        this.b = b;
        if (a === null) {
            this.a = 255;
        } else {
            this.a = a;
        }
        if (typeof r === 'string') {
            if (r[0] === '#') {
                r = r.slice(1);
            }
            this.r = parseInt(r.slice(0, 2), 16);
            if (g === null) {
                this.g = parseInt(r.slice(2, 4), 16);
            }
            if (b === null) {
                this.b = parseInt(r.slice(4, 6), 16);
            }
            if (a === null) {
                if (len(r) <= 6) {
                    this.a = 255;
                } else {
                    this.a = parseInt(r.slice(6, 8), 16);
                }
            }
        }
    }

    toString() {
        if (this.a === 256) {
            return `(${this.r.toString(16)}, ${this.g.toString(16)}, ${this.b.toString(16)})`;
        }
        return `(${this.r.toString(16)}, ${this.g.toString(16)}, ${this.b.toString(16)}, ${this.a.toString(16)})`;
    }


}

function render(player, apple) {

    // make board sizes
    var board = [];
    var row = [];
    for (var i = 0; i < boardSize.x; i++) {
        row = [];
        for (var j = 0; j < boardSize.y; j++) {
            row.push(0);
        }
        board.push(row);
    }
}

window.addEventListener("resize", () => {
    const width = window.innerWidth;
    const height = window.innerHeight;

    console.log(`Width: ${width}px, Height: ${height}px`);
});
