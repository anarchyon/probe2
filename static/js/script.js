async function submitRequest(staff_id){
    let response = await fetch("/get/" + staff_id)
    if(response.ok) {
        let employeeJson = await response.json()
        console.log(employeeJson.birthdate)
    }
}