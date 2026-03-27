const API = "http://127.0.0.1:5000";

let token = "";
let selectedAgent = 1;

async function signup() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  await fetch(API + "/signup", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({email, password})
  });

  alert("Signup done");
}

async function login() {
  const res = await fetch(API + "/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      email: email.value,
      password: password.value
    })
  });

  const data = await res.json();
  token = data.token;
  alert("Logged in");
}

async function loadAgents() {
  const res = await fetch(API + "/agents");
  const data = await res.json();

  let html = "";
  data.forEach(a => {
    html += `<div onclick="selectAgent(${a.id})">
      <h3>${a.name}</h3>
      <p>${a.premium ? "Premium 🔒" : "Free"}</p>
    </div>`;
  });

  document.getElementById("agents").innerHTML = html;
}

function selectAgent(id) {
  selectedAgent = id;
}

async function runAgent() {
  const res = await fetch(API + "/run-agent", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": token
    },
    body: JSON.stringify({
      agent_id: selectedAgent,
      prompt: prompt.value
    })
  });

  const data = await res.json();
  output.innerText = data.result || data.message;
}

loadAgents();