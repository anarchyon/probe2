const ADD_TITLE = "Добавление нового сотрудника";
const EDIT_TITLE = "Редактирование сотрудника";
const DELETE_TITLE = "Подтвердите удаление сотрудника";
const ADD_ACTION = "/add";
const EDIT_ACTION = "/update/";
const DELETE_ACTION = "/delete/";
const ADD_BUTTON = "Добавить сотрудника";
const EDIT_BUTTON = "Обновить информацию";
const DELETE_BUTTON = "Удалить сотрудника";
const urlForGetStaff = "/get-staff/";
const urlForGet = "/get/";
const attrStaffId = 'staff_id';
const attrFirstName = 'first_name';
const attrLastName = 'last_name';
const attrAddress = 'address';
const attrBirthdate = 'birthdate';
const alertEmptyValue = 'Обязательные поля должны быть заполнены';
const alertWrongAge = 'Сотрудник должен быть совершеннолетним';
const add = 'add';
const update = 'update';
const deleteAction = 'delete';
const labelSortUp = '\u21e7';
const labelSortDown = '\u21e9';

let isSortOrderAsc = false;
let sortColumn = attrStaffId;
let pathSort = '';

let actualAction = '';
let pathAction = '';
// let previousSort = '';

function enableFields() {
    document.getElementById(attrFirstName).disabled = false;
    document.getElementById(attrLastName).disabled = false;
    document.getElementById(attrAddress).disabled = false;
    document.getElementById(attrBirthdate).disabled = false;
}

function disableFields() {
    document.getElementById(attrFirstName).disabled = true;
    document.getElementById(attrLastName).disabled = true;
    document.getElementById(attrAddress).disabled = true;
    document.getElementById(attrBirthdate).disabled = true;
}

function fillModalWindow(title, buttonText, employee) {
    document.getElementById("modalTitle").innerText=title
    document.getElementById("buttonAccept").innerText = buttonText;
    if(employee === null) {
        document.getElementById(attrFirstName).value = "";
        document.getElementById(attrLastName).value = "";
        document.getElementById(attrAddress).value = "";
        document.getElementById(attrBirthdate).value = "";
    } else {
        document.getElementById(attrFirstName).value = employee.first_name;
        document.getElementById(attrLastName).value = employee.last_name;
        document.getElementById(attrAddress).value = employee.address;
        document.getElementById(attrBirthdate).value = employee.birthdate;
        }
}

async function getEmployee(staff_id){
    return fetch(urlForGet + staff_id).then(response => {
        return response.json();
    })
}

function addEmployee() {
    actualAction = add;
    pathAction = ADD_ACTION;
    fillModalWindow(ADD_TITLE, ADD_BUTTON, null);
    enableFields();
}

async function editEmployee(staff_id) {
    actualAction = update;
    pathAction = EDIT_ACTION  + staff_id;
    getEmployee(staff_id)
        .then(employee => {
            fillModalWindow(EDIT_TITLE, EDIT_BUTTON, employee);
        })
    enableFields();
}

async function deleteEmployee(staff_id) {
    actualAction = deleteAction;
    pathAction = DELETE_ACTION + staff_id;
    getEmployee(staff_id)
        .then(employee => {
            fillModalWindow(DELETE_TITLE, DELETE_BUTTON, employee);
        });
    disableFields();
}

function setSortParams(orderBy) {
    if (orderBy) {
        if (orderBy !== sortColumn) {
            sortColumn = orderBy;
            isSortOrderAsc = true;
        } else {
            isSortOrderAsc = !isSortOrderAsc;
        }
    }
    pathSort = urlForGetStaff + '?sort_column=' + sortColumn + '&is_sort_order_asc=' + isSortOrderAsc;
}

function clearSortHeaders() {
    let tableHeaders = document.querySelectorAll('td[id\u005e="sort_"]')
    tableHeaders.forEach(element => element.innerHTML = '')
}

async function getStaff(orderBy) {
    setSortParams(orderBy);
    fetch(pathSort)
        .then(response => response.text())
        .then(html => document.getElementById('staff_content').innerHTML = html)
        .then(() => {
            let hereLabelSort = document.querySelector('#sort_'+sortColumn);
            if (isSortOrderAsc) {
                hereLabelSort.innerHTML = labelSortUp;
            } else {
                hereLabelSort.innerHTML = labelSortDown;
            }
        })
}

function checkdata(data) {
    let isDataOk = true;
    for(const key in data) {
        switch(key) {
            case attrFirstName:
                if(data[key].trim() === '') {
                    alert(alertEmptyValue);
                    isDataOk = false;
                }
                break;
            case attrLastName:
                if(data[key].trim() === '') {
                    alert(alertEmptyValue);
                    isDataOk = false;
                }
                break;
            case attrBirthdate:
                if (data[key] !== '') {
                    birthdateEmployee = new Date(data[key]);
                    currentDate = new Date();
                    back18Years = new Date(currentDate.setFullYear(currentDate.getFullYear() - 18));
                    if(birthdateEmployee > back18Years) {
                        alert(alertWrongAge);
                        isDataOk = false;
                    }
                }
                break;
        }
            if(isDataOk) {
                continue;
            } else {
                break;
            }
    }
    return isDataOk;
}

async function sendData(data) {
    return await fetch(pathAction, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: data,
    })
}

function giveAlert() {
    switch(actualAction) {
        case add:
            alert('Сотрудник успешно добавлен в базу');
            break;
        case update:
            alert('Информация о сотруднике успешно обновлена');
            break;
        case deleteAction:
            alert('Сотрудник успешно удален из базы');
            break;
    }
}

async function handleActionSubmit(event){
    event.preventDefault();

    let {elements} = form;
    let data = {};
    Array.from(elements)
        .filter(item => !!item.name)
        .map(element => {
            data[element.name] = element.value;
        })
    if(checkdata(data)) {
        const response = await sendData(JSON.stringify(data));
        if(response.ok) {
            giveAlert();
        } else {
            alert('Произошла ошибка');
        }
        document.getElementById('modalClose').click();
        getStaff();
    }
}

let form = document.getElementById('action');
form.addEventListener('submit', handleActionSubmit);

function sendSearchData(pathSearch) {
    fetch(pathSearch)
        .then(response => response.text())
        .then(html => document.getElementById('staff_content').innerHTML = html);
    
}

function createSearchPath(searchData) {
    let pathSearch = '/search';
    let i = 0;
    for(const searchKey in searchData) {
        if(i === 0) {
            pathSearch += "?";
        } else {
            pathSearch += "&";
        }
        i++;
        pathSearch += searchKey + "=" + searchData[searchKey];
    }
    return pathSearch;
}

function clearFormFields() {
    document.getElementById('fname').value = '';
    document.getElementById('lname').value = '';
    document.getElementById('addr').value = '';
}

function handleSearchSubmit(event) {
    event.preventDefault();

    let { elements } = formSearch;
    let searchData = {};
    Array.from(elements)
        .filter(item => !!item.name)
        .map(element => {
            searchData[element.name] = element.value;
        })
    let pathSearch = createSearchPath(searchData)
    sendSearchData(pathSearch);
    clearFormFields();
    document.getElementById('modalClose2').click();
}

let formSearch = document.getElementById('search');
formSearch.addEventListener('submit', handleSearchSubmit);