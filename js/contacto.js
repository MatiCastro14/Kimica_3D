const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input');

const expresiones = {
	usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	comentarios: /^.{1,500}$/,
	telefono: /^\d{7,14}$/ // 7 a 14 numeros. // De 1 a 500 caracteres
}

const campos = {
	nombre: false,
	correo: false,
	comentarios: false,
	telefono: false

}

const validarFormulario = (e) => {
	switch (e.target.name) {
		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'nombre');
		break;
		case "correo":
			validarCampo(expresiones.correo, e.target, 'correo');
		break;
		case "comentarios":
			validarCampo(expresiones.comentarios, e.target, 'texto');
		break;
		case "telefono":
			validarCampo(expresiones.telefono, e.target, 'telefono');
		break;
	}
}

const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-check-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-times-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.remove('formulario__input-error-activo');
		campos[campo] = true;
	} else {
		document.getElementById(`grupo__${campo}`).classList.add('formulario__grupo-incorrecto');
		document.getElementById(`grupo__${campo}`).classList.remove('formulario__grupo-correcto');
		document.querySelector(`#grupo__${campo} i`).classList.add('fa-times-circle');
		document.querySelector(`#grupo__${campo} i`).classList.remove('fa-check-circle');
		document.querySelector(`#grupo__${campo} .formulario__input-error`).classList.add('formulario__input-error-activo');
		campos[campo] = false;
	}
}


inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});





//const URL = "http://127.0.0.1:5000/"

//Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
const URL = "https://mcastro.pythonanywhere.com/"


// Capturamos el evento de envío del formulario
document.getElementById('formulario').addEventListener('submit', function (event) {
	event.preventDefault(); // Evitamos que se envie el form 

	var formData = new FormData(this);

	// Realizamos la solicitud POST al servidor
	fetch(URL + 'consultas', {
		method: 'POST',
		body: formData // Aquí enviamos formData. Dado que formData puede contener archivos, no se utiliza JSON.
	})

	//Después de realizar la solicitud POST, se utiliza el método then() para manejar la respuesta del servidor.
	.then(function (response) {
			if (response.ok) { 
				//Si la respuesta es exitosa, convierte los datos de la respuesta a formato JSON.
				return response.json(); 
			} else {
				// Si hubo un error, lanzar explícitamente una excepción
				// para ser "catcheada" más adelante
				throw new Error('Error al agregar la consulta.');
			}
	})

		//Respuesta OK, muestra una alerta informando que el consulta se agregó correctamente y limpia los campos del formulario para que puedan ser utilizados para un nuevo consulta.
		.then(function (data) {
			alert('consulta agregada correctamente.');
		})

		// En caso de error, mostramos una alerta con un mensaje de error.
		.catch(function (error) {
			alert('Error al agregar la consulta.');
		});
})


formulario.addEventListener('submit', (e) => {
	e.preventDefault();

	const terminos = document.getElementById('terminos');
	if(campos.nombre && campos.comentarios && campos.correo && campos.telefono && terminos.checked ){
		formulario.reset();

		document.getElementById('formulario__mensaje-exito').classList.add('formulario__mensaje-exito-activo');
		setTimeout(() => {
			document.getElementById('formulario__mensaje-exito').classList.remove('formulario__mensaje-exito-activo');
		}, 5000);

		document.querySelectorAll('.formulario__grupo-correcto').forEach((icono) => {
			icono.classList.remove('formulario__grupo-correcto');
		});
	} else {
		document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
	}
});








// Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
//const URL = "https://USUARIO.pythonanywhere.com/"


// Realizamos la solicitud GET al servidor para obtener todos los productos.
fetch(URL + 'consultas')
	.then(function (response) {
		if (response.ok) {
			//Si la respuesta es exitosa (response.ok), convierte el cuerpo de la respuesta de formato JSON a un objeto JavaScript y pasa estos datos a la siguiente promesa then.
			return response.json(); 
	} else {
			// Si hubo un error, lanzar explícitamente una excepción para ser "catcheada" más adelante
			throw new Error('Error al obtener las consultas.');
		}
	})

	//Esta función maneja los datos convertidos del JSON.
	.then(function (data) {
		let tablaConsulta = document.getElementById('tablaconsulta'); //Selecciona el elemento del DOM donde se mostrarán los productos.

		// Iteramos sobre cada producto y agregamos filas a la tabla
		for (let consulta of data) {
			let fila = document.createElement('tr'); //Crea una nueva fila de tabla (<tr>) para cada producto.
			fila.innerHTML = '<td>' + consulta.id + '</td>' +
				'<td>' + consulta.nombre + '</td>' +
				'<td align="right">' + consulta.correo + '</td>' +
				'<td align="right">' + consulta.telefono + '</td>' +
				'<td>' + consulta.preferencia + '</td>' +
				'<td>' + consulta.motivo + '</td>' +
				'<td>' + consulta.comentario + '</td>' +

				// Mostrar miniatura de la imagen
				//'<td><img src=./static/imagenes/' + producto.imagen_url +' alt="Imagen del producto" style="width: 100px;"></td>' + '<td align="right">' + producto.proveedor + '</td>';
				
				//Al subir al servidor, deberá utilizarse la siguiente ruta. USUARIO debe ser reemplazado por el nombre de usuario de Pythonanywhere
				'<td><img src=https://www.pythonanywhere.com/user/mcastro/files/home/mcastro/mysite/static/imagenes/' + producto.imagen_url +' alt="Imagen del producto" style="width: 100px;"></td>' + '<td align="right">' + producto.proveedor + '</td>';
			
			//Una vez que se crea la fila con el contenido del producto, se agrega a la tabla utilizando el método appendChild del elemento tablaProductos.
			tablaConsulta.appendChild(fila);
		}
	})

	//Captura y maneja errores, mostrando una alerta en caso de error al obtener los productos.
	.catch(function (error) {
		// Código para manejar errores
		alert('Error al obtener los productos.');
	});