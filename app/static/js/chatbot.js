const chatbotToggle = document.getElementById("chatbot-toggle");
const headerToggle = document.getElementById("header-toggle");
const chatbot = document.getElementById("chatbot");

const messages = document.getElementById("messages");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");

const LOCAL_API_URL = "http://127.0.0.1:5000/chat";     

// Show chatbot on toggle click
chatbotToggle.onclick = () => {
  chatbot.style.display = "block";
  chatbotToggle.style.display = "none";
};

// Hide chatbot on header toggle click
headerToggle.onclick = () => {
  chatbot.style.display = "none";
  chatbotToggle.style.display = "flex";
};

// Send message when button is clicked
sendButton.onclick = () => handleUserMessage();

// Send message on Enter key press
userInput.addEventListener("keypress", (event) => {
  if (event.key === "Enter") handleUserMessage();
});

// Handle user input and send message
function handleUserMessage() {
  const userMessage = userInput.value.trim();
  if (userMessage) {
    addMessage(userMessage, "question");
    sendMessageToHuggingFace(userMessage);
    userInput.value = ""; // Clear input field
  } else {
    addMessage("Please enter a message.", "message");
  }
}

async function sendMessageToHuggingFace(message) {
  const loadingElement = document.getElementById("loading");
  loadingElement.style.display = "block";  // Show loading

  try {
      const response = await fetch("http://127.0.0.1:5000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: message })
      });

      const result = await response.json();
      loadingElement.style.display = "none";  // Hide loading

      if (result && result.reply) {
          addMessage(result.reply, "message");
      } else {
          addMessage("Error: Unexpected response from AI.", "message");
      }
  } catch (error) {
      loadingElement.style.display = "none";  // Hide loading
      addMessage("Error connecting to AI. Please try again.", "message");
      console.error("API Error:", error);
  }
}



// Function to add messages (both user & bot)
function addMessage(text, type) {
  const messageElement = document.createElement("div");
  messageElement.className = type;
  messageElement.textContent = text;
  messages.appendChild(messageElement);
  messages.scrollTop = messages.scrollHeight; // Auto-scroll to the bottom
}
