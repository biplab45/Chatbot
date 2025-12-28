<!DOCTYPE html>
<html>
<head>
    <title>Jarvis Mobile</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script type="text/javascript" src="/eel.js"></script>
    <style>
        body { background: #0a0b10; color: #00f2ff; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .ui-box { text-align: center; border: 2px solid #00f2ff; padding: 40px; border-radius: 20px; width: 85%; box-shadow: 0 0 20px #00f2ff55; }
        #status { margin: 20px 0; min-height: 50px; font-weight: bold; }
        .btn { background: #00f2ff; color: #000; border: none; padding: 15px 30px; border-radius: 50px; font-weight: bold; cursor: pointer; }
        .listening { animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { box-shadow: 0 0 0px #ff0055; } 50% { box-shadow: 0 0 20px #ff0055; } 100% { box-shadow: 0 0 0px #ff0055; } }
    </style>
</head>
<body>
    <div class="ui-box" id="mainBox">
        <h2>JARVIS SYSTEM</h2>
        <div id="status">Ready</div>
        <button class="btn" id="listenBtn" onclick="toggleListening()">START LISTENING</button>
    </div>

    <script>
        const status = document.getElementById('status');
        const btn = document.getElementById('listenBtn');
        const box = document.getElementById('mainBox');

        // Voice Out (Phone Speakers)
        function speak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            synth.speak(utter);
        }

        // Voice In (Phone Mic)
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        recognition.continuous = true; // Loops automatically

        function toggleListening() {
            recognition.start();
            status.innerText = "Listening...";
            box.classList.add('listening');
        }

        recognition.onresult = async (event) => {
            const command = event.results[event.results.length - 1][0].transcript;
            status.innerText = "You: " + command;

            // Send to Python for Logic
            let response = await eel.process_logic(command)();
            
            status.innerText = response.msg;
            speak(response.msg);

            if (response.action === "open") {
                window.open(response.url, '_blank');
            }
        };

        recognition.onerror = (err) => {
            status.innerText = "Mic Error: " + err.error;
            box.classList.remove('listening');
        };
    </script>
</body>
</html>
