let selectorCargo = document.querySelector("#id_cargo");
let tarifa = document.querySelector("#id_tarifa");

selectorCargo.addEventListener("change", (event) => {
    let cargoId = event.currentTarget.value;

    fetch(`/gestion/cargos/json/${cargoId}`)
        .then((resp) => resp.json())
        .then((json) => {
                tarifa.value = json[0].tarifa_gs;
        });
});