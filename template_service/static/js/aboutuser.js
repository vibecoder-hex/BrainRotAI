const getUserData = async () => {
    const token = localStorage.getItem("token")
        const response = await fetch('http://127.0.0.1:8001/api/about_user', {
            method: "GET",
            credentials: 'include',
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
}

getUserData();