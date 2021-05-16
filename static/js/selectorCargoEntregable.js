let selectorCargo0 = document.querySelector("#id_detalle-0-cargo");
let selectorCargo1 = document.querySelector("#id_detalle-1-cargo");
let selectorCargo2 = document.querySelector("#id_detalle-2-cargo");
let selectorCargo3 = document.querySelector("#id_detalle-3-cargo");
let selectorCargo4 = document.querySelector("#id_detalle-4-cargo");
let horas_servicio_0  = document.querySelector("#id_detalle-0-horas_servicio");
let horas_servicio_1  = document.querySelector("#id_detalle-1-horas_servicio");
let horas_servicio_2  = document.querySelector("#id_detalle-2-horas_servicio");
let horas_servicio_3  = document.querySelector("#id_detalle-3-horas_servicio");
let horas_servicio_4  = document.querySelector("#id_detalle-4-horas_servicio");
let tarifa_gs_0 = document.querySelector("#id_detalle-0-tarifa");
let tarifa_gs_1 = document.querySelector("#id_detalle-1-tarifa");
let tarifa_gs_2 = document.querySelector("#id_detalle-2-tarifa");
let tarifa_gs_3 = document.querySelector("#id_detalle-3-tarifa");
let tarifa_gs_4 = document.querySelector("#id_detalle-4-tarifa");
let total_0 = document.querySelector("#id_detalle-0-total");
let total_1 = document.querySelector("#id_detalle-1-total");
let total_2 = document.querySelector("#id_detalle-2-total");
let total_3 = document.querySelector("#id_detalle-3-total");
let total_4 = document.querySelector("#id_detalle-4-total");

selectorCargo0.addEventListener("change", (event) => {
    let CargoId0 = event.currentTarget.value;

    fetch(`/gestion/cargos/json/${CargoId0}`)
        .then((resp) => resp.json())
        .then((json) => {
            tarifa_gs_0.value = json[0].tarifa_gs;
            total_0.value = tarifa_gs_0.value * horas_servicio_0.value;
            
        });
});
selectorCargo1.addEventListener("change", (event) => {
        let CargoId1 = event.currentTarget.value;
    
        fetch(`/gestion/cargos/json/${CargoId1}`)
            .then((resp) => resp.json())
            .then((json) => {
                tarifa_gs_1.value = json[0].tarifa_gs;
                total_1.value = tarifa_gs_1.value * horas_servicio_1.value;
                
            });
    });
selectorCargo2.addEventListener("change", (event) => {
    let CargoId2 = event.currentTarget.value;

    fetch(`/gestion/cargos/json/${CargoId2}`)
        .then((resp) => resp.json())
        .then((json) => {
            tarifa_gs_2.value = json[0].tarifa_gs;
            total_2.value = tarifa_gs_2.value * horas_servicio_2.value;
            
        });
});
selectorCargo3.addEventListener("change", (event) => {
    let CargoId3 = event.currentTarget.value;

    fetch(`/gestion/cargos/json/${CargoId3}`)
        .then((resp) => resp.json())
        .then((json) => {
            tarifa_gs_3.value = json[0].tarifa_gs;
            total_3.value = tarifa_gs_3.value * horas_servicio_3.value;
            
        });
});
selectorCargo4.addEventListener("change", (event) => {
    let CargoId4 = event.currentTarget.value;

    fetch(`/gestion/cargos/json/${CargoId4}`)
        .then((resp) => resp.json())
        .then((json) => {
            tarifa_gs_4.value = json[0].tarifa_gs;
            total_4.value = tarifa_gs_4.value * horas_servicio_4.value;
            
        });
});