let horas_asignadas_1 = document.querySelector("#id_entregable_set-0-horas_asignadas");
let horas_asignadas_2 = document.querySelector("#id_entregable_set-1-horas_asignadas");
let horas_asignadas_3 = document.querySelector("#id_entregable_set-2-horas_asignadas");
let horas_asignadas_4 = document.querySelector("#id_entregable_set-3-horas_asignadas");
let horas_asignadas_5 = document.querySelector("#id_entregable_set-4-horas_asignadas");
let boton_crear = document.querySelector("#id_submit");
let contrato = document.querySelector("#id_contrato").value;

console.log(contrato)
boton_crear.addEventListener("onclick", (event) => {
    let suma_horas = horas_asignadas_1.value + horas_asignadas_2.value + horas_asignadas_3.value + horas_asignadas_4.value + horas_asignadas_5;

    fetch(`/proyectos/contratos/json/${contrato}`)
        .then((resp) => resp.json())
        .then((json) => {
            if (suma_horas >= json[0].horas_presupuestadas) {
                alert("Se han asignado a los entregables más horas de las presupuestadas.")
            } else {
                pass;
            }
            
        });
});