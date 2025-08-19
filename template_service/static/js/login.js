let form_for_login = document.getElementById("login_form")
            form_for_login.onsubmit = async (e) => {
                e.preventDefault();

                let login = document.getElementById("login_input").value;
                let password = document.getElementById("password_input").value;

                let formdata = new URLSearchParams();
                formdata.append('username', login);
                formdata.append('password', password);
                try {
                    let response = await fetch("http://127.0.0.1:8001/api/token/", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/x-www-form-urlencoded"
                        },
                        body: formdata
                    });
                    if (!response.ok) {
                        switch (response.status) {
                            case 401:
                                throw new Error("Incorrect username/pasword");
                            case 500:
                                throw new Error("Internal server error")
                            default:
                                throw new Error(`Error with code: ${response.status}`)
                        }
                    }
                    let token_response = await response.json()
                    localStorage.setItem("token", token_response.access_token)
                    window.location.href = '/'
                }
                catch (error) {
                    document.getElementById("status_div").innerHTML = `
                    <h3>Error: ${error.message}</h3>
                    `;
                }
            }