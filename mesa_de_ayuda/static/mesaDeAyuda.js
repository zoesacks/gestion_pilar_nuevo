//Inicializamos variables de tarjetas
let cantTickets = 0;
let sol_finalizadas = 0;
let proceso = 0;
let solPendientes = 0;
let trSeleccionado;
let url = window.location.origin


//Declaramos la lista de datos

async function obtenerTickets() {
    const response = await fetch(`${url}/api/solicitud-mesa-ayuda`)
    tickets = await response.json()
    mostrarTarjetas(tickets)
    mostrarTickets(tickets)
}

obtenerTickets()

function mostrarTickets(tickets) {
    //Tomamos la tabla del dom
    const container = document.querySelector('#dataTable')

    eliminarTicketsDelDOM()

    //Recorremos los tickets para agregar las filas de la tabla
    tickets.forEach(ticket => {

        //Insertamos la fila
        let row = container.insertRow()
        row.id = ticket.id
        //Insertamos las celdas
        const fechaCell = row.insertCell(0);
        fechaCell.textContent = ticket.fecha.substring(0, 10);
        fechaCell.classList.add("d-none")
        fechaCell.classList.add("d-sm-table-cell") 

        const asuntoCell = row.insertCell(1);
        asuntoCell.textContent = ticket.titulo;

        const asignadoCell = row.insertCell(2);
        asignadoCell.classList.add("d-none")
        asignadoCell.classList.add("d-sm-table-cell")

        ticket.desarrollador ? asignadoCell.textContent = ticket.desarrollador.username : asignadoCell.textContent = "No asignado"
        

        const estadoCell = row.insertCell(3);
        estadoCell.innerHTML = agregarEstado(ticket.estado);
        

        const comentarioCell = row.insertCell(4)
        ticket.comentarios.length ? comentarioCell.textContent = formatRelativeTime(ticket.comentarios.pop().fecha) : comentarioCell.textContent = "No hay comentarios"
        comentarioCell.classList.add("d-none")
        comentarioCell.classList.add("d-sm-table-cell")

        const botonesCell = row.insertCell(5)
        botonesCell.innerHTML += `
        <button type="button" class="btn btn-primary ver-ticket-boton" data-bs-toggle="modal" data-bs-target="#verTicketModal">
         <i class="fa fa-eye" aria-hidden="true"></i>
         </button>
         `
    })
    agregarEventListenerBotones()
}



function agregarEstado(estado) {
    let color = "red"
    if (estado === "Terminado") {
        color = "green"
    } else if (estado === "En proceso") {
        color = "blue"
    }

    return `<span class="badge badge-pill badge-primary" style="background-color: ${color};" >${estado}</span>`
}


function mostrarTarjetas(tickets) {

    cantTickets = 0;
    solPendientes = 0;
    proceso = 0;
    sol_finalizadas = 0;

    //Asignamos la cantidad de tickets
    cantTickets = tickets.length

    //Recorremos los tickets y actualizamos variables 
    tickets.forEach(ticket => {
        
        if (ticket.estado === "Pendiente") {
            solPendientes += 1
        } else if (ticket.estado === "En proceso") {
            proceso += 1
        } else {
            sol_finalizadas += 1
        }

    })

    //Tomamos los elementos del dom
    const divTotalTickets = document.querySelector('#solicitudes-totales')
    const divPendientes = document.querySelector('#sol-pendientes')
    const divproceso = document.querySelector('#proceso')
    const divsol_finalizadas = document.querySelector('#sol_finalizadas')

    //Actualizamos el texto de los divs con la cantidad de tickets y su estado
    divTotalTickets.textContent = cantTickets
    divPendientes.textContent = solPendientes
    divproceso.textContent = proceso
    divsol_finalizadas.textContent = sol_finalizadas
}

/*Agregar ticket*/

let formularioTransferirTicket = document.querySelector(".enviar-ticket-formulario")

formularioTransferirTicket.addEventListener('submit', (e) => {

    e.preventDefault()

})

let botonEnviarTicket = document.querySelector("#boton-enviar-ticket")

document.querySelector(".input-asunto").addEventListener('input', (e) => {
    if (e.target.value) {
        botonEnviarTicket.disabled = false;
    } else {
        botonEnviarTicket.disabled = true;
    }
})

botonEnviarTicket.addEventListener('click', () => {
    capturarDatos()
})

function capturarDatos() {
    const titulo = document.querySelector(".input-asunto").value
    const detalle = document.querySelector(".textarea-descripcion").value
    agregarTicket({ titulo: titulo, detalle: detalle })
}

function eliminarTicketsDelDOM() {
    const container = document.querySelector('.tickets-container')
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
}

function agregarTicket(data) {

    // Obtener el valor del token CSRF del documento
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

    fetch(`${url}/api/solicitud-mesa-ayuda/`, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Agregar el token CSRF al encabezado
        },
        body: JSON.stringify(data)
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            obtenerTickets()
        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });

}


/*Obtener unico ticket*/

function agregarEventListenerBotones() {
    [...document.querySelectorAll('.ver-ticket-boton')].forEach(function (item) {
        item.addEventListener('click', function () {
            trSeleccionado = item.parentElement.parentElement
            obtenerTicket(item.parentElement.parentElement.id)
        });
    });
}


async function obtenerTicket(id) {
    console.log(`${url}/api/solicitud-mesa-ayuda/${id}`)
    const response = await fetch(`${url}/api/solicitud-mesa-ayuda/${id}/`)
    ticket = await response.json()
    mostrarDatosTicket(ticket)
}

const modalComentarios = document.querySelector(".modal-comentarios")

function mostrarDatosTicket(ticket){
    
    const modalComentarios = document.querySelector(".modal-comentarios")
    modalComentarios.innerHTML = ""

    const modalVerTicket = document.querySelector(".modal-ver-ticket")
    modalVerTicket.id = ticket.id
    modalVerTicket.innerHTML = `
    <div class="container">
    <div class="card border-0">
        <div class="card-body">
            <div class="section">
                        <p><b class="text-primary text-uppercase">Descripcion: </b>${ticket.detalle ? ticket.detalle : 'No hay descripcion'}
                        <p><b class="text-primary text-uppercase">Comentarios: </b>${ticket.comentarios ? '': 'No hay comentarios'}
                        
            </div>
        </div>
    </div>
    <div>
    </div>
    
</div>
    `

    ticket.comentarios.forEach(comentario => {
        
        let estilo
    
        if (ticket.usuario != comentario.usuario.id) {
            estilo = "ajeno"
        } else {
            estilo = "propio"
        }

        modalComentarios.innerHTML += `
        <div class="mensaje ${estilo}">
                    
                        <h6 class="card-subtitle mb-2 small ">${comentario.usuario.username}</h6>
                        <p class="card-text">${comentario.comentario}</p>
                        <p class="card-text small ">${formatRelativeTime(comentario.fecha)}</p>
                    
        </div>`

        modalComentarios.lastChild.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    })

}


/*Añadir comentario*/

let formularioEnviarComentario = document.querySelector(".enviar-comentario-formulario")

formularioEnviarComentario.addEventListener('submit', (e) => {
    e.preventDefault()
    const inputMensaje = document.querySelector(".formulario-mensaje")
    const inputFoto = document.querySelector('input[type="file"]')
    var data = new FormData()
    //data.append('foto', inputFoto.files[0])
    data.append('comentario', inputMensaje.value)
    //console.log({ foto: data.get('foto'), comentario: data.get('comentario') })
    agregarComentario(document.querySelector(".modal-ver-ticket").id, data)
    inputMensaje.value = ""
})



function agregarComentario(id, comentario) {
    // Obtener el valor del token CSRF del documento
    var csrfToken = document.querySelector('input[name=csrfmiddlewaretoken]').value;


    fetch(`${url}/api/solicitud-mesa-ayuda/${id}/nuevo-comentario/`, {
        method: "PUT",
        headers: {
            'X-CSRFToken': csrfToken  // Agregar el token CSRF al encabezado
        },
        body: comentario
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            return response.json();
        })
        .then((data) => {

          console.log(data)
            
            modalComentarios.innerHTML += `
            <div class="mensaje propio">
                            <h6 class="card-subtitle mb-2 small ">${data.comentario.usuario.username}</h6>
                            <p class="card-text">${data.comentario.comentario}</p>
                            <p class="card-text small ">${formatRelativeTime(data.comentario.fecha)}</p>         
            </div>`

   

            modalComentarios.lastChild.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
           const tr = trSeleccionado
           tr.children[4].textContent = formatRelativeTime(data.comentario.fecha)
        })
        .catch((error) => {
            console.error('There was a problem with the fetch operation:', error);
        });

}


/*Agregar imagen*/

const input = document.querySelector('input[type="file"]')


/*input.addEventListener('change', (e) => {
    var data = new FormData()
    data.append('file', e.target.files[0])
    console.log(e.target.files[0])
    
})*/




/*Funciones auxiliares*/

function formatRelativeTime(dateString) {
    const currentDate = new Date();
    const date = new Date(dateString);
    const diffInMilliseconds = currentDate - date;

    const rtf = new Intl.RelativeTimeFormat('es', { numeric: 'auto' });

    if (Math.abs(diffInMilliseconds) < 1000) {
        return 'justo ahora';
    }

    const seconds = Math.floor(diffInMilliseconds / 1000);
    if (seconds < 60) {
        return rtf.format(-seconds, 'second');
    }

    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) {
        return rtf.format(-minutes, 'minute');
    }

    const hours = Math.floor(minutes / 60);
    if (hours < 24) {
        return rtf.format(-hours, 'hour');
    }

    const days = Math.floor(hours / 24);
    if (days < 30) {
        return rtf.format(-days, 'day');
    }

    const months = Math.floor(days / 30);
    if (months < 12) {
        return rtf.format(-months, 'month');
    }

    const years = Math.floor(months / 12);
    return rtf.format(-years, 'year');
}






