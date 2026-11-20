class Vec2 {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }

    add(v) {
        return new Vec2(this.x + v.x, this.y + v.y);
    }

    sub(v) {
        return new Vec2(this.x - v.x, this.y - v.y);
    }

    mul(scalar) {
        return new Vec2(this.x * scalar, this.y * scalar);
    }

    div(scalar) {
        return new Vec2(this.x / scalar, this.y / scalar);
    }

    length() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    normalize() {
        const len = this.length();
        if (len === 0) return new Vec2(0, 0);
        return this.div(len);
    }
}

var naviPos = new Vec2(0, 0);
var targetPos = new Vec2(0, 0);
var targetShadow = new Vec2(0, 0);
var shadowBase = new Vec2(0, 0);

const distrobution = 11.5;
const generalSpread = 50;
const accelerationRate = 2;
const velocityMax = 5;
const accelerationMax = 5;

var direction = new Vec2(0, 0);
var normal = new Vec2(0, 0);

function distance(a, b) {
    return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2);
}

function minabs(x, y) {
    return Math.min(Math.abs(x), y) * Math.sign(x);
}

function spread(x) {
    const exponent = (-0.5 * distrobution) + (distrobution * x);
    const numerator = 1 + (Math.E ** -exponent);
    return (2 / numerator) - 1;
}

function createShadow() {
    shadowBase = new Vec2(Math.random(), Math.random());
    shadowBase = new Vec2(
        generalSpread * spread(shadowBase.x / shadowBase.length()),
        generalSpread * spread(shadowBase.y / shadowBase.length())
    );
}

createShadow();

function updateShadow() {
    if (distance(naviPos, targetPos) < 10) {
        targetShadow = new Vec2(
            targetPos.x + shadowBase.x,
            targetPos.y + shadowBase.y
        );
    }

    function update() {
        updateShadow();
        direction = targetShadow.sub(naviPos);
        normal = direction.normalize();
        const acceleration = minabs(direction.length() * accelerationRate, accelerationMax);
        const velocity = minabs(acceleration, velocityMax);
        naviPos = naviPos.add(normal.mul(velocity));
        if (distance(naviPos, targetShadow) < 10) {
            createShadow();
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        const naviCanvas = document.getElementById('naviCanvas');
        if (!(naviCanvas instanceof HTMLCanvasElement)) {
            throw new Error('Navigation canvas was not found.');
        }

        const ctx = naviCanvas.getContext('2d');
        if (!ctx) {
            throw new Error('Navigation canvas does not support 2D rendering.');
        }

        function resizeCanvas() {
            const pixelRatio = window.devicePixelRatio || 1;
            naviCanvas.width = window.innerWidth * pixelRatio;
            naviCanvas.height = window.innerHeight * pixelRatio;
            naviCanvas.style.width = `${window.innerWidth}px`;
            naviCanvas.style.height = `${window.innerHeight}px`;
            ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
        }

        function clearCanvas() {
            ctx.clearRect(0, 0, window.innerWidth, window.innerHeight);
        }

        function circle(x, y, radius, color) {
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();
        }

        resizeCanvas();
        window.addEventListener('resize', () => {
            resizeCanvas();
            clearCanvas();
        });

        document.addEventListener("mousemove", (event) => {
            targetPos = new Vec2(event.clientX, event.clientY);
        });

        function timedLoop() {
            updateShadow();
            update();
            clearCanvas();
            circle(naviPos.x, naviPos.y, 10, 'rgba(0, 0, 255, 0.5)');
            circle(targetPos.x, targetPos.y, 10, 'rgba(0, 255, 0, 0.5)');
            circle(targetShadow.x, targetShadow.y, 10, 'rgba(255, 255, 0, 0.5)');
            setTimeout(timedLoop, 1);
        }

        timedLoop();
    })
};