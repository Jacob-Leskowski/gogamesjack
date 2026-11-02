import * as THREE from 'three';

// 1. Get the canvas element
const canvas: HTMLCanvasElement = document.getElementById("snakeCanvas") as HTMLCanvasElement;
console.log("Canvas:", canvas);

// 2. Create the Three.js Renderer using your canvas (handles the WebGL context automatically)
const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);

// 3. Create a Scene and a Camera
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// 4. Using 2D vectors correctly in Three.js
const snakeDirection = new THREE.Vector2(1, 0); // Moving right
console.log("Direction X:", snakeDirection.x);

// 5. Basic Animation Loop to render the scene
function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}
animate();
