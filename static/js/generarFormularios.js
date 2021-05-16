let addForm = document.getElementById("add_form");
let formOculto = document.getElementById("form_oculto");
let formContainer = document.getElementById("forms_container");

addForm.addEventListener("submit", function (event) {
    event.preventDefault();
    let cantidadForms = Number(document.getElementById("number_forms").value);
    
    for (i = 0; i < cantidadForms; i++) {
        let clonado = formOculto.cloneNode(true);
        clonado.classList.remove("d-none");
        formContainer.appendChild(clonado);
    }
});
