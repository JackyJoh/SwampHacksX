

const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

let progress = { lesson1: 0, lesson2: 0 };
let mode = "";
let currentLetter = "";
let currentIndex = 0;
let correctAnswers = 0;
let totalAttempts = 0;

// Elements
const lesson1Button = document.getElementById("lesson1");
const lesson2Button = document.getElementById("lesson2");
const sidebar = document.getElementById("sidebar");
const testingModeButton = document.getElementById("testingMode");
const learningModeButton = document.getElementById("learningMode");
const modeDisplay = document.getElementById("modeDisplay");
const wordDisplay = document.getElementById("wordDisplay");
const progressBar = document.getElementById("progressBar");
const bottomDisplay = document.getElementById("bottomDisplay");
const imageDisplay = document.createElement("img");
const resultDisplay = document.createElement("div");
bottomDisplay.appendChild(imageDisplay);
bottomDisplay.appendChild(resultDisplay);

// Click event for ABC's (Lesson 1)
lesson1Button.addEventListener("click", function() {
    sidebar.style.display = "flex";
    bottomDisplay.style.display = "block"; // Show bottom display
    currentWord = "Letter: ";
    currentIndex = 0;
    correctAnswers = 0;
    totalAttempts = 0;
    updateBottomDisplay();
    displayNextLetter();
});

// Click event for Common English Words (Lesson 2)
lesson2Button.addEventListener("click", function() {
    sidebar.style.display = "flex";
    bottomDisplay.style.display = "block"; // Show bottom display
    currentWord = "Word: ";
    currentIndex = 0;
    correctAnswers = 0;
    totalAttempts = 0;
    updateBottomDisplay();
    displayNextWord();
});

// Click event for Testing Mode
testingModeButton.addEventListener("click", function() {
    mode = "Testing Mode";
    updateBottomDisplay();
});

// Click event for Learning Mode
learningModeButton.addEventListener("click", function() {
    mode = "Learning Mode";
    updateBottomDisplay();
    displayImage();
});

// Function to update bottom display
function updateBottomDisplay() {
    modeDisplay.textContent = "Mode: " + mode;
    wordDisplay.textContent = currentWord;
    updateProgress();
}

// Function to update progress bar
function updateProgress() {
    let lessonProgress = (correctAnswers / totalAttempts) * 100;
    progressBar.style.width = lessonProgress + "%";
    progressBar.textContent = lessonProgress.toFixed(0) + "%";
}

// Function to display next letter
function displayNextLetter() {
    if (currentIndex < alphabet.length) {
        currentLetter = alphabet[currentIndex];
        wordDisplay.textContent = "Letter: " + currentLetter;
        if (mode === "Learning Mode") {
            displayImage();
        }
    } else {
        // Restart or end lesson
        currentIndex = 0;
        displayNextLetter();
    }
}

// Function to display next word
function displayNextWord() {
    if (currentIndex < commonWords.length) {
        currentWord = commonWords[currentIndex];
        wordDisplay.textContent = "Word: " + currentWord;
        if (mode === "Learning Mode") {
            displayImage();
        }
    } else {
        // Restart or end lesson
        currentIndex = 0;
        displayNextWord();
    }
}

// Function to display image for learning mode
function displayImage() {
    if (mode === "Learning Mode") {
        let imagePath = "";
        if (currentWord.startsWith("Letter: ")) {
            imagePath = `images/letters/${currentLetter}.png`;
        } else if (currentWord.startsWith("Word: ")) {
            imagePath = `images/words/${currentWord}.png`;
        }
        imageDisplay.src = imagePath;
        imageDisplay.alt = currentWord;
    }
}

// Function to handle user input and update progress
function handleUserInput() {
    const userInput = answerInput.value.trim().toLowerCase();
    let isCorrect = false;
    if (currentWord.startsWith("Letter: ")) {
        isCorrect = userInput === currentLetter.toLowerCase();
    } else if (currentWord.startsWith("Word: ")) {
        isCorrect = userInput === currentWord.toLowerCase();
    }
    if (currentWord.startsWith("Letter: ")) {
        totalAttempts.lesson1++;
        if (isCorrect) {
            correctAnswers.lesson1++;
        }
    } else if (currentWord.startsWith("Word: ")) {
        totalAttempts.lesson2++;
        if (isCorrect) {
            correctAnswers.lesson2++;
        }
    }
    resultDisplay.textContent = isCorrect ? "Correct!" : "Wrong! Try again.";
    resultDisplay.style.color = isCorrect ? "green" : "red";
    updateProgress();
    if (isCorrect) {
        if (currentWord.startsWith("Letter: ")) {
            currentIndex++;
            displayNextLetter();
        } else if (currentWord.startsWith("Word: ")) {
            currentIndex++;
            displayNextWord();
        }
    }
    answerInput.value = "";
}

const express = require('express');
const app = express();
const port = 3000;

currentLetter = 'A';

app.use(express.json());

app.post('/check-input', (req, res) => {
    const userInput = req.body.input.toUpperCase();
    if (userInput === currentLetter) {
        moveToNextLetter();
        res.json({ success: true, nextLetter: currentLetter });
    } else {
        res.json({ success: false });
    }
});

function moveToNextLetter() {
    if (currentLetter < 'Z') {
        currentLetter = String.fromCharCode(currentLetter.charCodeAt(0) + 1);
    }
}

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
