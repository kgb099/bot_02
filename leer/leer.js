// ==UserScript==
// @name         Leer texto en voz alta
// @namespace    http://tampermonkey.net/
// @version      10.0
// @description  Agrega un botón para leer texto seleccionado en voz alta
// @author       ChatGPT
// @match        *://*/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    console.log("iniciando");

    let speakBtn;
    let botonActivo = 0; // Variable para controlar el estado del botón
    const synth = window.speechSynthesis;

    function removeSpeakButton() {
        if (botonActivo === 0) {
            const btn = document.getElementById("speakBtn");
            if (btn) {
                btn.remove();
            }
            speakBtn = null;
        }
    }

    function leerTexto(text) {
        if (!synth) {
            alert('Tu navegador no soporta la síntesis de voz.');
            return;
        }
        if (!text || text.length === 0) {
            alert('No hay texto seleccionado para leer.');
            return;
        }
        synth.cancel();
        console.warn("cancelando lectura");
        botonActivo = 0; // Aumenta cuando se crea el botón y se va a leer
        removeSpeakButton();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'es-ES'; // Voz en español
        utterance.rate = 1; // Velocidad normal
        utterance.pitch = 1; // Tono normal
        utterance.onstart = function() {
            console.log('comenzando hablar');
        };
        utterance.onend = function() {
            console.warn("termino de hablar borro boton")
            botonActivo = 0; // Vuelve al valor original cuando termina de leer
            removeSpeakButton();
        };
        synth.speak(utterance);
        botonActivo = 0; // Aumenta cuando se crea el botón y se va a leer
    }

    function createSpeakButton(text, x, y) {
        removeSpeakButton();
        botonActivo = 1; // Aumenta cuando se crea el botón y se va a leer
        speakBtn = document.createElement('button');
        speakBtn.id = "speakBtn";
        speakBtn.innerText = '🔊 Leer';
        speakBtn.style.position = 'absolute';
        speakBtn.style.top = `${y + 10}px`;
        speakBtn.style.left = `${x + 10}px`;
        speakBtn.style.zIndex = '9999';
        speakBtn.style.padding = '6px 10px';
        speakBtn.style.fontSize = '14px';
        speakBtn.style.border = 'none';
        speakBtn.style.borderRadius = '5px';
        speakBtn.style.background = '#007bff';
        speakBtn.style.color = '#fff';
        speakBtn.style.cursor = 'pointer';
        speakBtn.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';

        speakBtn.addEventListener('click', () => {
            console.log("comenzando a leer");

            leerTexto(text);
        });
        document.body.appendChild(speakBtn);
    }

    document.addEventListener('mouseup', (e) => {
        const selection = window.getSelection();
        const selectedText = selection.toString().trim();

        if (selectedText.length > 0) {
            const rect = selection.getRangeAt(0).getBoundingClientRect();
            createSpeakButton(selectedText, rect.left + window.scrollX, rect.top + window.scrollY);
        } else {
            botonActivo = 0; // Aumenta cuando se crea el botón y se va a leer
            removeSpeakButton();
        }
    });

    document.addEventListener('scroll', removeSpeakButton);
})();