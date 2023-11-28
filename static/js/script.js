const ADD_TITLE = "Добавление нового сотрудника";
const EDIT_TITLE = "Редактирование сотрудника";
const DELETE_TITLE = "Подтвердите удаление сотрудника";
const ADD_ACTION = "/add/";
const EDIT_ACTION = "/update/";
const DELETE_ACTION = "/delete/";
const ADD_BUTTON = "Добавить сотрудника";
const EDIT_BUTTON = "Обновить информацию";
const DELETE_BUTTON = "Удалить сотрудника";
const GET_STAFF = "/get-staff/"

function enableFields() {
    document.getElementById("first_name").disabled = false;
    document.getElementById("last_name").disabled = false;
    document.getElementById("address").disabled = false;
    document.getElementById("birthdate").disabled = false;
}

function disableFields() {
    document.getElementById("first_name").disabled = true;
    document.getElementById("last_name").disabled = true;
    document.getElementById("address").disabled = true;
    document.getElementById("birthdate").disabled = true;
}

function fillModalWindow(title, stringAction, buttonText, employee) {
    console.log(employee===null)
    document.getElementById("modalTitle").innerText=title
    document.getElementById("action").action = stringAction;
    document.getElementById("buttonAccept").innerText = buttonText;
    if(employee === null) {
        document.getElementById("first_name").value = "";
        document.getElementById("last_name").value = "";
        document.getElementById("address").value = "";
        document.getElementById("birthdate").value = "";
    } else {
        document.getElementById("first_name").value = employee.first_name;
        document.getElementById("last_name").value = employee.last_name;
        document.getElementById("address").value = employee.address;
        document.getElementById("birthdate").value = employee.birthdate;
        }
}

async function getEmployee(staff_id){
    let response = await fetch("/get/" + staff_id);
    if(response.ok) {
        let employeeJson = await response.json();
        console.log(employeeJson.last_name)
        return employeeJson;
    }
}

function addEmployee() {
    fillModalWindow(ADD_TITLE, ADD_ACTION, ADD_BUTTON, null);
    enableFields();
}

async function editEmployee(staff_id) {
    let employee = await getEmployee(staff_id);
    console.log(employee.birthdate)
    let editAction = EDIT_ACTION  + staff_id;
    fillModalWindow(EDIT_TITLE, editAction, EDIT_BUTTON, employee);
    enableFields();
}

async function deleteEmployee(staff_id) {
    let employee = await getEmployee(staff_id);
    console.log(employee.last_name)
    let deleteAction = DELETE_ACTION + staff_id;
    fillModalWindow(DELETE_TITLE, deleteAction, DELETE_BUTTON, employee);
    disableFields();
}

async function getStaff(orderBy) {
    let urlForGet = GET_STAFF + "?order=" + orderBy;
    console.log(urlForGet);
    fetch(urlForGet).then(response => window.location.replace(response.url));
}