let contratoId = document.querySelector("#id_contrato").value;
let monto_total = document.querySelector("#id_monto_total");


fetch(`/proyectos/contratos/json/${contratoId}`)
    .then((resp) => resp.json())
    .then((json) => {
        monto_total.value = json[0].monto;
    });