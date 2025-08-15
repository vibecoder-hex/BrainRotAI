const button_change = function(btn, state) {
            switch (state) {
                case "loading":
                    btn.disabled = true;
                    btn.style.opacity = "0.7";
                    btn.innerHTML = "Generating...";
                    break;
                case "done":
                    btn.disabled = false;
                    btn.style.opacity = "1";
                    btn.innerHTML = "Generate";
                    break;
            }
        }
        
        const generate_form = document.getElementById("prompt_form");
        const submit_btn = document.getElementById("submit_btn");

        generate_form.onsubmit = async (e) => {

            e.preventDefault();

            button_change(submit_btn, "loading");
            
            const token = localStorage.getItem("token")
            const prompt_text = document.getElementById("prompt_input").value;
            const image_ratio = document.getElementById("image_ratio").value;

            try {
                const response = await fetch(`http://127.0.0.1:8000/generate/`, {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({"prompt": prompt_text, "image_ratio": image_ratio.split(":")}),
                });
                if (!response.ok) {
                    throw new Error(response.status)
                }
                const response_result = await response.json()
                document.getElementById("result_image").innerHTML = `
                <img src="data:image/png;base64,${response_result.result}" width="500"/>
                <br>
                <button type="submit" id="clear_button" onclick="clear_result()">Clear</button>
                `
            }
            catch (error) {
                if (error.status === 401) {
                    window.location.href = 'login.html'
                }   
            }
            finally {
                button_change(submit_btn, "done");
            }
        };
        
        const clear_result = function() {
            document.getElementById("result_image").innerHTML = "";
        }