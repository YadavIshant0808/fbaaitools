document.addEventListener("DOMContentLoaded", function() {
    const body = document.body;
    const modeToggleCheckbox = document.getElementById("modeToggleCheckbox");
    const sidebar = document.getElementById("sidebar");
    const chatBox = document.getElementById("chatBox");
    const userInput = document.getElementById("userInput");
    const sendButton = document.getElementById("sendButton");
    const newConversationBtn = document.getElementById("newConversationBtn");
    const conversationList = document.getElementById("conversationList");
    const sidebarToggleMobile = document.getElementById("sidebarToggleMobile");
  
    // Toggle dark mode
    modeToggleCheckbox.addEventListener("change", function() {
      body.classList.toggle("dark-mode");
    });
  
    // Mobile sidebar close button
    if (sidebarToggleMobile) {
      sidebarToggleMobile.addEventListener("click", function() {
        sidebar.classList.remove("show");
      });
    }
  
    // New conversation button clears the chat and appends a new conversation item
    newConversationBtn.addEventListener("click", function() {
      chatBox.innerHTML = "";
      const newConvItem = document.createElement("a");
      newConvItem.href = "#";
      newConvItem.className = "list-group-item list-group-item-action bg-transparent text-white";
      newConvItem.textContent = "New Conversation";
      conversationList.appendChild(newConvItem);
    });
  
    // Send a message when clicking the button or pressing Enter
    function sendMessage() {
      const message = userInput.value.trim();
      if (message === "") return;
      appendMessage("user", message);
      userInput.value = "";
      getBotResponse(message);
    }
    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keydown", function(e) {
      if (e.key === "Enter") sendMessage();
    });
  
    // Append a chat message to the chatBox
    function appendMessage(sender, message) {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("chat-message", sender === "user" ? "user" : "bot");
      messageDiv.textContent = message;
      chatBox.appendChild(messageDiv);
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  
    // Simulate bot responses based on keywords
    function getBotResponse(message) {
      let response = "";
      const lowerMessage = message.toLowerCase();
      if (lowerMessage.includes("hello")) {
        response = "Hello! How can I help you today?";
      } else if (lowerMessage.includes("time")) {
        response = `The current time is ${new Date().toLocaleTimeString()}`;
      } else if (lowerMessage.includes("date")) {
        response = `Today's date is ${new Date().toLocaleDateString()}`;
      } else if (lowerMessage.includes("joke")) {
        response = "Why did the web developer go broke? Because he used up all his cache!";
      } else {
        response = "I'm here to help!";
      }
      setTimeout(() => appendMessage("bot", response), 500);
    }
  
    // For mobile: Add a fixed toggle button to show the sidebar
    const mobileSidebarToggleBtn = document.createElement("button");
    mobileSidebarToggleBtn.className = "btn btn-primary d-md-none position-fixed";
    mobileSidebarToggleBtn.style.top = "10px";
    mobileSidebarToggleBtn.style.left = "10px";
    mobileSidebarToggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
    document.body.appendChild(mobileSidebarToggleBtn);
    mobileSidebarToggleBtn.addEventListener("click", function() {
      sidebar.classList.toggle("show");
    });
  });
  