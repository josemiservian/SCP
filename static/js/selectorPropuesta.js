let selectorPropuesta = document.querySelector("#id_propuesta");
let nombre = document.querySelector("#id_nombre");
let monto = document.querySelector("#id_monto");
let horas_presupuestadas = document.querySelector("#id_horas_presupuestadas");

selectorPropuesta.addEventListener("change", (event) => {
    let propuestaId = event.currentTarget.value;

    fetch(`/proyectos/propuestas/json/${propuestaId}`)
        .then((resp) => resp.json())
        .then((json) => {
            nombre.value = json[0].nombre;
            horas_presupuestadas.value = json[0].horas_totales;
            monto.value = json[0].ganancia_esperada;
        });
});