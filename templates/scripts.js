function validateForm(event) {
  event.preventDefault();
  const name = document.getElementById("fullname").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (name === "" || email === "" || password === "") {
    alert("Please fill in all fields.");
    return false;
  }

  fetch('/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name, email, password })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message);
    if (data.success) window.location.href = "/login";
  });

  return false;
}

function validateLoginForm(event) {
  event.preventDefault();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (email === "" || password === "") {
    alert("Please fill in all fields.");
    return false;
  }

  fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      window.location.href = "/dashboard";
    } else {
      alert(data.message);
    }
  });

  return false;
}