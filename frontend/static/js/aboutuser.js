const getUserData = async () => {
    const token = localStorage.getItem("token")
    try {
        const response = await fetch('http://127.0.0.1:8000/about_user', {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        })
        const user_data = await response.json()
        let userdata_list = document.createElement('ul')
        userdata_list.id = 'userdata_list'
        for (let elem in user_data) {
            let li_elem = document.createElement('li')
            li_elem.innerText = `${elem} : ${user_data[elem]}`
            userdata_list.append(li_elem)
        }
        document.body.append(userdata_list)

        if (!response.ok) {
            throw {"status": response.status}
        }
    }
    catch (error) {
        if (error.status === 401) {
            window.location.href = "login.html"
        }
    }

}

getUserData();