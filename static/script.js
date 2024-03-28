document.getElementById("signupForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;
    const confirmpassword = document.getElementById("confirmPassword").value;

    if (password == confirmpassword){
        const response = await fetch("/add-data", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        window.location.href = "/dashboard.html";
        

        const data = await response.json();
        document.getElementById("message").textContent = data.message;

    }
});

document.getElementById("signinForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    
    const email = document.getElementById("signinEmail").value;
    const password = document.getElementById("signinPassword").value;
    
    const response = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email,password })
    });
    window.location.href = "/dashboard.html";
    const data = await response.json();
    document.getElementById("message").textContent = data.message;
})