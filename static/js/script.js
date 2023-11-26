async function submitRequest(staff_id){
    let response = await fetch("/get/" + staff_id, {nethod: "POST"})
    if(response.ok) {
        let myJson = await response.json()
        alert(myJson)
    }
}