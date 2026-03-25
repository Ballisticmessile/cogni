let currentUser = null;
let quizState = {
  subjectId: null,
  subjectName: null,
  questions: [],
  currentQuestionIndex: 0,
  answers: {},
  startTime: null
};

// Theme Management
function toggleTheme() {
  const body = document.body;
  const isDarkMode = body.classList.contains('dark-mode');
  
  if (isDarkMode) {
    body.classList.remove('dark-mode');
    body.classList.add('light-mode');
    localStorage.setItem('theme', 'light');
  } else {
    body.classList.remove('light-mode');
    body.classList.add('dark-mode');
    localStorage.setItem('theme', 'dark');
  }
  
  updateThemeIcon();
}

function updateThemeIcon() {
  const icon = document.querySelector('.theme-icon');
  const isDarkMode = document.body.classList.contains('dark-mode');
  icon.textContent = isDarkMode ? '☀️' : '🌙';
}

// Initialize theme from localStorage
function initializeTheme() {
  const savedTheme = localStorage.getItem('theme') || 'light';
  const body = document.body;
  
  body.classList.remove('light-mode', 'dark-mode');
  body.classList.add(savedTheme + '-mode');
  updateThemeIcon();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initializeTheme);

function toggleAuth() {
  const loginForm = document.getElementById("loginForm");
  const signupForm = document.getElementById("signupForm");
  
  loginForm.classList.toggle("active");
  signupForm.classList.toggle("active");
  
  // Clear form fields
  document.getElementById("username").value = "";
  document.getElementById("password").value = "";
  document.getElementById("signupName").value = "";
  document.getElementById("signupUsername").value = "";
  document.getElementById("signupPassword").value = "";
}

function handleLogin(event) {
  event.preventDefault();
  login();
}

function handleSignup(event) {
  event.preventDefault();
  signup();
}

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    alert("Please fill all fields");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();

    if (res.ok) {
      currentUser = data;
      alert("Login successful!");
      showDashboard();
    } else {
      alert(data.error || "Login failed");
    }
  } catch (error) {
    alert("Connection error: " + error.message);
  }
}

async function signup() {
  const name = document.getElementById("signupName").value;
  const username = document.getElementById("signupUsername").value;
  const password = document.getElementById("signupPassword").value;

  if (!name || !username || !password) {
    alert("Please fill all fields");
    return;
  }

  // Prevent signup with username "admin"
  if (username.toLowerCase() === "admin") {
    alert("Username 'admin' is reserved and cannot be created");
    return;
  }

  if (password.length < 6) {
    alert("Password must be at least 6 characters");
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/register", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ name, username, password })
    });

    const data = await res.json();

    if (res.ok) {
      alert("Account created successfully! Please login.");
      toggleAuth();
      // Clear signup form
      document.getElementById("signupName").value = "";
      document.getElementById("signupUsername").value = "";
      document.getElementById("signupPassword").value = "";
    } else {
      // Provide specific error message
      if (data.error && data.error.includes("exists")) {
        alert("This username already exists. Please choose a different one.");
      } else {
        alert(data.error || "Signup failed");
      }
    }
  } catch (error) {
    alert("Connection error: " + error.message);
  }
}

function showDashboard() {
  document.querySelector(".auth-container").style.display = "none";
  document.getElementById("dashboard").style.display = "block";
  document.getElementById("quizContainer").style.display = "none";
  document.getElementById("adminPanel").style.display = "none";
  loadSubjects();
  initializeAdmin();
}

function logout() {
  currentUser = null;
  quizState = {
    subjectId: null,
    subjectName: null,
    questions: [],
    currentQuestionIndex: 0,
    answers: {},
    startTime: null
  };
  document.querySelector(".auth-container").style.display = "grid";
  document.getElementById("dashboard").style.display = "none";
  document.getElementById("quizContainer").style.display = "none";
  
  // Reset forms to login
  document.getElementById("loginForm").classList.add("active");
  document.getElementById("signupForm").classList.remove("active");
  
  // Clear all fields
  document.getElementById("username").value = "";
  document.getElementById("password").value = "";
  document.getElementById("signupName").value = "";
  document.getElementById("signupUsername").value = "";
  document.getElementById("signupPassword").value = "";
}

async function loadSubjects() {
  try {
    const res = await fetch("http://127.0.0.1:5000/subjects");
    const data = await res.json();

    const ul = document.getElementById("subjects");
    ul.innerHTML = "";

    if (data.length === 0) {
      ul.innerHTML = "<li style='padding: 20px; text-align: center; color: #999;'>No subjects available</li>";
      return;
    }

    data.forEach(s => {
      const li = document.createElement("li");
      li.innerHTML = `
        <span>${s.icon} ${s.name}</span>
        <div class="subject-item-actions">
          <button class="btn btn-primary" onclick="startQuiz(${s.id}, '${s.name}')">Start Quiz</button>
        </div>
      `;
      ul.appendChild(li);
    });
  } catch (error) {
    alert("Error loading subjects: " + error.message);
  }
}

async function startQuiz(subjectId, subjectName) {
  try {
    const res = await fetch(`http://127.0.0.1:5000/questions/${subjectId}`);
    const questions = await res.json();

    if (questions.length === 0) {
      alert("No questions available for this subject");
      return;
    }

    quizState.subjectId = subjectId;
    quizState.subjectName = subjectName;
    quizState.questions = questions;
    quizState.currentQuestionIndex = 0;
    quizState.answers = {};
    quizState.startTime = new Date();

    document.getElementById("quizTitle").textContent = `Quiz: ${subjectName}`;
    document.getElementById("dashboard").style.display = "none";
    document.getElementById("quizContainer").style.display = "block";
    document.getElementById("quizSummary").style.display = "none";

    displayQuestion();
  } catch (error) {
    alert("Error loading quiz: " + error.message);
  }
}

function displayQuestion() {
  const question = quizState.questions[quizState.currentQuestionIndex];
  const totalQuestions = quizState.questions.length;
  const progressPercent = ((quizState.currentQuestionIndex + 1) / totalQuestions) * 100;

  // Update progress
  document.getElementById("progressFill").style.width = progressPercent + "%";
  document.getElementById("questionCounter").textContent = `Question ${quizState.currentQuestionIndex + 1} of ${totalQuestions}`;

  // Display question - ensure it's always visible
  const questionElement = document.getElementById("questionText");
  questionElement.textContent = question.text || "Question text unavailable";
  questionElement.style.display = "block";

  // Display options
  const optionsContainer = document.getElementById("optionsContainer");
  optionsContainer.innerHTML = "";

  const options = question.options;
  options.forEach((option, index) => {
    const button = document.createElement("button");
    button.className = "option-btn";
    button.textContent = option;
    button.onclick = () => selectAnswer(index);

    // Highlight previously selected answer
    if (quizState.answers[quizState.currentQuestionIndex] === index) {
      button.classList.add("selected");
    }

    optionsContainer.appendChild(button);
  });

  // Update navigation buttons
  document.getElementById("prevBtn").style.display = quizState.currentQuestionIndex > 0 ? "block" : "none";
  document.getElementById("nextBtn").textContent = quizState.currentQuestionIndex === totalQuestions - 1 ? "Submit Quiz" : "Next Question";
}

function selectAnswer(optionIndex) {
  quizState.answers[quizState.currentQuestionIndex] = optionIndex;

  // Highlight selected option
  const options = document.querySelectorAll(".option-btn");
  options.forEach((btn, idx) => {
    if (idx === optionIndex) {
      btn.classList.add("selected");
    } else {
      btn.classList.remove("selected");
    }
  });
}

function nextQuestion() {
  if (quizState.currentQuestionIndex === quizState.questions.length - 1) {
    // Submit quiz
    submitQuiz();
  } else {
    quizState.currentQuestionIndex++;
    displayQuestion();
    window.scrollTo(0, 0);
  }
}

function previousQuestion() {
  if (quizState.currentQuestionIndex > 0) {
    quizState.currentQuestionIndex--;
    displayQuestion();
    window.scrollTo(0, 0);
  }
}

async function submitQuiz() {
  // Calculate score
  let score = 0;
  quizState.questions.forEach((question, index) => {
    if (quizState.answers[index] === question.correct) {
      score++;
    }
  });

  // Calculate time taken
  const endTime = new Date();
  const timeTaken = Math.floor((endTime - quizState.startTime) / 1000); // in seconds

  // Display summary
  document.getElementById("scoreText").textContent = `Your Score: ${score}/${quizState.questions.length}`;
  const percentage = Math.round((score / quizState.questions.length) * 100);
  document.getElementById("percentageText").textContent = `Percentage: ${percentage}%`;

  // Save result to backend
  try {
    const res = await fetch("http://127.0.0.1:5000/submit", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        user_id: currentUser.id,
        subject_id: quizState.subjectId,
        score: score,
        total: quizState.questions.length,
        time_taken: timeTaken,
        date: new Date().toISOString()
      })
    });

    if (res.ok) {
      document.getElementById("quizSummary").style.display = "block";
      document.querySelector(".quiz-wrapper").style.display = "none";
    }
  } catch (error) {
    alert("Error saving result: " + error.message);
  }
}

function exitQuiz() {
  if (confirm("Are you sure you want to exit the quiz? Your progress will not be saved.")) {
    backToDashboard();
  }
}

function backToDashboard() {
  quizState = {
    subjectId: null,
    subjectName: null,
    questions: [],
    currentQuestionIndex: 0,
    answers: {},
    startTime: null
  };
  document.getElementById("quizContainer").style.display = "none";
  document.getElementById("adminPanel").style.display = "none";
  document.getElementById("dashboard").style.display = "block";
  document.querySelector(".quiz-wrapper").style.display = "block";
  document.getElementById("quizSummary").style.display = "none";
}

// Admin Panel Functions
async function loadSubjectsForAdmin() {
  try {
    const res = await fetch("http://127.0.0.1:5000/subjects");
    const subjects = await res.json();
    
    const select = document.getElementById("questionSubject");
    select.innerHTML = '<option value="">Select a subject</option>';
    
    subjects.forEach(subject => {
      const option = document.createElement("option");
      option.value = subject.id;
      option.textContent = `${subject.icon} ${subject.name}`;
      select.appendChild(option);
    });
  } catch (error) {
    console.error("Error loading subjects:", error);
  }
}

function showAdminPanel() {
  // Check if user is admin
  if (!currentUser || currentUser.username !== "admin") {
    alert("Access Denied! Only admins can access the admin panel.");
    return;
  }
  
  document.getElementById("dashboard").style.display = "none";
  document.getElementById("adminPanel").style.display = "block";
  loadSubjectsForAdmin();
  loadManageData();
}

function switchAdminTab(tabName) {
  // Hide all tabs
  const tabs = document.querySelectorAll(".admin-tab-content");
  tabs.forEach(tab => tab.classList.remove("active"));
  
  const buttons = document.querySelectorAll(".admin-tab-btn");
  buttons.forEach(btn => btn.classList.remove("active"));
  
  // Show selected tab
  document.getElementById(tabName + "-tab").classList.add("active");
  event.target.classList.add("active");
  
  if (tabName === "manage") {
    loadManageData();
  }
}

async function handleAddQuestion(event) {
  event.preventDefault();
  
  // Verify admin access
  if (!currentUser || currentUser.username !== "admin") {
    showMessage("addQuestionMessage", "✗ Access Denied! Only admins can add questions.", "error");
    return;
  }
  
  const subjectId = document.getElementById("questionSubject").value;
  const text = document.getElementById("questionText").value;
  const option1 = document.getElementById("option1").value;
  const option2 = document.getElementById("option2").value;
  const option3 = document.getElementById("option3").value;
  const option4 = document.getElementById("option4").value;
  const correctOption = parseInt(document.getElementById("correctOption").value);
  const difficulty = document.getElementById("difficulty").value;
  
  if (!subjectId) {
    showMessage("addQuestionMessage", "Please select a subject", "error");
    return;
  }
  
  try {
    const res = await fetch("http://127.0.0.1:5000/add-question", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        admin_username: currentUser.username,
        subject_id: subjectId,
        text: text,
        option1: option1,
        option2: option2,
        option3: option3,
        option4: option4,
        correct_option: correctOption,
        difficulty: difficulty
      })
    });
    
    const data = await res.json();
    
    if (res.ok) {
      showMessage("addQuestionMessage", "✓ Question added successfully!", "success");
      event.target.reset();
      loadManageData();
    } else {
      showMessage("addQuestionMessage", "✗ Error: " + data.error, "error");
    }
  } catch (error) {
    showMessage("addQuestionMessage", "✗ Error: " + error.message, "error");
  }
}

async function handleAddSubject(event) {
  event.preventDefault();
  
  // Verify admin access
  if (!currentUser || currentUser.username !== "admin") {
    showMessage("addSubjectMessage", "✗ Access Denied! Only admins can add subjects.", "error");
    return;
  }
  
  const name = document.getElementById("subjectName").value;
  const icon = document.getElementById("subjectIcon").value;
  const category = document.getElementById("subjectCategory").value;
  
  try {
    const res = await fetch("http://127.0.0.1:5000/add-subject", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        admin_username: currentUser.username,
        name: name,
        icon: icon,
        category: category
      })
    });
    
    const data = await res.json();
    
    if (res.ok) {
      showMessage("addSubjectMessage", "✓ Subject added successfully!", "success");
      event.target.reset();
      loadSubjectsForAdmin();
      loadManageData();
    } else {
      showMessage("addSubjectMessage", "✗ Error: " + data.error, "error");
    }
  } catch (error) {
    showMessage("addSubjectMessage", "✗ Error: " + error.message, "error");
  }
}

function showMessage(elementId, message, type) {
  const messageDiv = document.getElementById(elementId);
  messageDiv.textContent = message;
  messageDiv.className = "message " + type;
  
  setTimeout(() => {
    messageDiv.className = "message";
  }, 5000);
}

async function loadManageData() {
  try {
    const subjectsRes = await fetch("http://127.0.0.1:5000/subjects");
    const subjects = await subjectsRes.json();
    
    let totalQuestions = 0;
    for (let subject of subjects) {
      const questionsRes = await fetch(`http://127.0.0.1:5000/questions/${subject.id}`);
      const questions = await questionsRes.json();
      totalQuestions += questions.length;
    }
    
    document.getElementById("totalSubjects").textContent = subjects.length;
    document.getElementById("totalQuestions").textContent = totalQuestions;
  } catch (error) {
    console.error("Error loading manage data:", error);
  }
}

// Initialize admin on dashboard load
function initializeAdmin() {
  if (currentUser && currentUser.username === "admin") {
    document.getElementById("adminToggleBtn").style.display = "block";
  }
}