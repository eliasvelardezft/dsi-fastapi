from datetime import datetime
from functools import lru_cache
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from typing import Annotated

app = FastAPI()


class Estado:
    def __init__(self, nombre: str):
        self.setNombre(nombre)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getNombre(self):
        return self.nombre

    def getFechaHoraFin(self):
        return self.fechaHoraFin

    def esEnCurso(self):
        return self.getNombre() == "enCurso"

    def esFinalizada(self):
        return self.getNombre() == "finalizada"



class CambioEstado:
    fechaHoraFin: str | None = None

    def __init__(self, nuevoEstado: Estado, fechaHora: datetime):
        self.setEstado(nuevoEstado)
        self.setFechaHoraInicio(fechaHora)

    def setFechaHoraInicio(self, fecha: datetime):
        self.fechaHoraInicio = fecha

    def setFechaHoraFin(self, fecha: datetime):
        self.fechaHoraFin = fecha

    def setEstado(self, nuevoEstado: Estado):
        self.estado = nuevoEstado
    
    def getEstado(self):
        return self.estado
    
    def getFechaHoraFin(self):
        return self.fechaHoraFin

    def getFechaHoraInicio(self):
        return self.fechaHoraInicio

    def esEnCurso(self):
        return self.getEstado().esEnCurso()

    def esFinalizada(self):
        return self.getEstado().esFinalizada()


class OpcionValidacion:
    def __init__(self, descripcion: str, correcta: bool):
        self.setDescripcion(descripcion)
        self.setCorrecta(correcta)

    def setDescripcion(self, descripcion: str):
        self.descripcion = descripcion

    def setCorrecta(self, correcta: bool):
        self.correcta = correcta

    def getDescripcion(self) -> str:
        return self.descripcion

    def esCorrecta(self, respuesta: str) -> bool:
        return respuesta == self.getDescripcion()


class InformacionCliente:
    def __init__(self, datoAValidar: str, validacion, opcionValidacion: OpcionValidacion):
        self.setOpcionValidacion(opcionValidacion)
        self.setValidacion(validacion)
        self.setDatoAValidar(datoAValidar)

    # TODO: REVISAR DONDE PONER ESTO
    @classmethod
    def getTodosLosObjetos(cls):
        return [
            cls(
                "Fecha de nacimiento",
                Validacion("Fecha de nacimiento", 1),
                OpcionValidacion("24/06/1987", True),
            ),
            cls(
                "Cantidad de hijos",
                Validacion("Cantidad de hijos", 2),
                OpcionValidacion("3", True)
            ),
        ]

    def setOpcionValidacion(self, opcionValidacion: OpcionValidacion):
        self.opcionValidacion = opcionValidacion
    
    def setValidacion(self, validacion):
        self.validacion = validacion

    def getValidacion(self):
        return self.validacion

    def esValidacion(self, validacion):
        return self.getValidacion().getNombre() == validacion.getNombre()

    def setDatoAValidar(self, datoAValidar: str):
        self.datoAValidar = datoAValidar

    def getDatoAValidar(self) -> str:
        return self.datoAValidar

    def getOpcionValidacion(self) -> OpcionValidacion:
        return self.opcionValidacion

    def esInformacionCorrecta(self, respuesta: str) -> bool:
        opcionValidacion = self.getOpcionValidacion()
        return opcionValidacion.esCorrecta(respuesta)


class Cliente:
    def __init__(self, nombre: str):
        self.setNombre(nombre)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre


class Validacion:
    def __init__(self, nombre: str, nroOrden: int):
        self.setNombre(nombre)
        self.setNroOrden(nroOrden)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def setNroOrden(self, nroOrden: int):
        self.nroOrden = nroOrden

    def getNroOrden(self) -> int:
        return self.nroOrden

    def getNombre(self) -> str:
        return self.nombre

    def getInformacionCliente(self) -> InformacionCliente:
        for infoCliente in InformacionCliente.getTodosLosObjetos():
            if infoCliente.esValidacion(self):
                return infoCliente

    def validarRespuesta(self, respuesta: str) -> bool:
        informacionCliente = self.getInformacionCliente()
        return informacionCliente.esInformacionCorrecta(respuesta)


class SubOpcionLlamada:
    validaciones: list[Validacion] = []
    def __init__(self, nombre: str, validaciones: list[Validacion]):
        self.setValidaciones(validaciones)
        self.setNombre(nombre)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre

    def setValidaciones(self, validaciones: list[Validacion]):
        self.validaciones = validaciones

    def getValidaciones(self) -> list[Validacion]:
        return self.validaciones

    def getValidacionPorNombre(self, nombre: str) -> Validacion:
        for validacion in self.getValidaciones():
            if validacion.getNombre() == nombre:
                return validacion


class OpcionLlamada:
    def __init__(self, nombre: str):
        self.setNombre(nombre)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre


class Llamada:
    cambiosDeEstado: list[CambioEstado] = [CambioEstado(Estado("iniciada"), datetime.now())]

    def __init__(
        self,
        subOpcionLlamada: SubOpcionLlamada,
        cliente: Cliente,
    ):
        self.setSubOpcionLlamada(subOpcionLlamada)
        self.setCliente(cliente)

    def setSubOpcionLlamada(self, subOpcionLlamada: SubOpcionLlamada):
        self.subOpcionLlamada = subOpcionLlamada

    def setCliente(self, cliente: Cliente):
        self.cliente = cliente

    def getSubOpcionLlamada(self) -> SubOpcionLlamada:
        return self.subOpcionLlamada

    def crearCambioEstado(self, nuevoEstado: Estado, fechaHora: datetime):
        cambioEstadoActual = self.getCambioEstadoActual()
        cambioEstadoActual.setFechaHoraFin(fechaHora)

        # CambioEstado.new()
        nuevoEstado = CambioEstado(nuevoEstado, fechaHora)
        self.appendCambioEstado(nuevoEstado)

    def appendCambioEstado(self, cambioEstado: CambioEstado):
        self.cambiosDeEstado.append(cambioEstado)

    def getCambiosDeEstado(self) -> list[CambioEstado]:
        return self.cambiosDeEstado

    def getCambioEstadoActual(self) -> CambioEstado:
        for estado in self.getCambiosDeEstado():
            if not estado.getFechaHoraFin():
                return estado

    def getCliente(self) -> Cliente:
        return self.cliente

    def getValidaciones(self) -> list[Validacion]:
        return self.getSubOpcionLlamada().getValidaciones()

    def getNombreCliente(self) -> str:
        return self.getCliente().getNombre()

    def setOpcionSeleccionada(self, opcion: OpcionLlamada):
        self.opcionSeleccionada = opcion

    def setSubOpcionSeleccionada(self, subOpcion: SubOpcionLlamada):
        self.subOpcionSeleccionada = subOpcion

    def setDescripcionOperador(self, descripcion: str):
        self.descripcionOperador = descripcion

    def setDuracion(self, duracion: int):
        self.duracion = duracion

    def calcularDuracion(self):
        for cambioEstado in self.getCambiosDeEstado():
            if cambioEstado.esEnCurso():
                cambioEstadoEnCurso = cambioEstado
            elif cambioEstado.esFinalizada():
                cambioEstadoFinalizada = cambioEstado
        return cambioEstadoFinalizada.getFechaHoraInicio() - cambioEstadoEnCurso.getFechaHoraInicio()
        

class CategoriaLlamada:
    def __init__(self, nombre: str):
        self.setNombre(nombre)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre


class Accion:
    def __init__(self, descripcion: str):
        self.setDescripcion(descripcion)

    def setDescripcion(self, descripcion: str):
        self.descripcion = descripcion

    def getDescripcion(self) -> str:
        return self.descripcion


class GestorRegistrarAccionRequerida:
    def iniciarCU(self, accion: Accion):
        # aca devolvemos true porque fue exitosa la ejecucion del CU 28 - Registrar accion requerida
        return True


from fastapi import Form, Body, Request
from fastapi.testclient import TestClient
from typing import Any
import requests

class GestorRegistrarRespuestaOperador:
    accionSeleccionada: Accion | None = None
    descripcionOperador: Accion | None = None

    def __init__(self, pantallaOperador):
        self.setPantallaOperador(pantallaOperador)
        self.acciones = [
            Accion("Cancelar tarjeta"),
            Accion("Reintegrar dinero"),
        ]
        self.setValidacionesValidadas(False)
        self.estados = [
            Estado("iniciada"),
            Estado("enCurso"),
            Estado("finalizada"),
        ]

    def getEstados(self) -> list[Estado]:
        return self.estados
    
    # def getInformacionesCliente(self) -> list[InformacionCliente]:
    #     return self.informacionesCliente
    
    def getAcciones(self) -> list[Accion]:
        return self.acciones

    def setPantallaOperador(self, pantallaOperador):
        self.pantallaOperador = pantallaOperador

    def getPantallaOperador(self):
        return self.pantallaOperador

    def setLlamada(self, llamada: Llamada):
        self.llamada = llamada

    def setCategoriaLlamada(self, categoriaLlamada: CategoriaLlamada):
        self.categoriaLlamada = categoriaLlamada

    def setSubOpcionLlamada(self, subOpcionLlamada: SubOpcionLlamada):
        self.subOpcionLlamada = subOpcionLlamada

    def setOpcionLlamada(self, opcionllamada: OpcionLlamada):
        self.opcionllamada = opcionllamada

    def getLlamada(self) -> Llamada:
        return self.llamada
    
    def getCategoriaLlamada(self) -> CategoriaLlamada:
        return self.categoriaLlamada
    
    def getSubOpcionLlamada(self) -> SubOpcionLlamada:
        return self.subOpcionLlamada
    
    def getOpcionLlamada(self) -> OpcionLlamada:
        return self.opcionllamada

    def ordernarValidaciones(
        self,
        validaciones: list[Validacion]
    ) -> list[Validacion]:
        return sorted(
            validaciones,
            key=lambda validacion: validacion.getNroOrden()
        )

    def setUltimaRespuestaValidacion(self, respuesta: str):
        self.ultimaRespuestaValidacion = respuesta

    def getUltimaRespuestaValidacion(self):
        return self.ultimaRespuestaValidacion

    def tomarRespuestasValidaciones(self, respuestas: dict[str, str]):
        errores = {}
        for respuestaValidacion in respuestas.items():
            errores[respuestaValidacion[0]] = self.validarRespuesta(respuestaValidacion)
        validaciones = self.getSubOpcionLlamada().getValidaciones()
        if all(errores.values()):
            self.setValidacionesValidadas(True)
        return validaciones, errores

    def setValidacionesValidadas(self, validacionesValidadas: bool):
        self.validacionesValidadas = validacionesValidadas

    def getValidacionesValidadas(self) -> bool:
        return self.validacionesValidadas

    def setDescripcionOperador(self, respuesta: str):
        self.descripcionOperador = respuesta

    def tomarRespuesta(self, respuesta: str):
        self.setDescripcionOperador(respuesta)

    def getDescripcionOperador(self) -> str:
        return self.descripcionOperador

    def validarRespuesta(self, respuestaValidacion: dict) -> dict[str, str]:
        validacion = self.getSubOpcionLlamada().getValidacionPorNombre(respuestaValidacion[0])
        esCorrecta = validacion.validarRespuesta(respuestaValidacion[1])
        return esCorrecta

    def getAccionSeleccionada(self) -> Accion:
        return self.accionSeleccionada

    def tomarSeleccionAccionRequerida(self, accionSeleccionada: Accion):
        self.setAccionSeleccionada(accionSeleccionada)

    def setAccionSeleccionada(self, accionSeleccionada: Accion):
        self.accionSeleccionada = accionSeleccionada

    def registrarFinLlamada(self):
        gestorRegistrarAccionRequerida = GestorRegistrarAccionRequerida()
        exitoCURegistrarAccionRequerida = gestorRegistrarAccionRequerida.iniciarCU(
            self.getAccionSeleccionada()
        )

        pantallaOperador = self.getPantallaOperador()
        pantallaOperador.informarExitoRegistroAccionRequerida(exitoCURegistrarAccionRequerida)

        estadoFinalizada = self.buscarEstadoParaAsignar("finalizada")
        fechaHoraActual = self.obtenerFechaHoraActual()
        llamada = self.getLlamada()
        llamada.crearCambioEstado(estadoFinalizada, fechaHoraActual)

        llamada.setOpcionSeleccionada(self.getOpcionLlamada())
        llamada.setSubOpcionSeleccionada(self.getSubOpcionLlamada())
        llamada.setDescripcionOperador(self.getDescripcionOperador())

        duracion = llamada.calcularDuracion()
        llamada.setDuracion(duracion)

    def setValidacionesOrdenadas(self, validacionesOrdenadas: list[Validacion]):
        self.validacionesOrdenadas = validacionesOrdenadas

    def getValidacionesOrdenadas(self) -> list[Validacion]:
        return self.validacionesOrdenadas

    def setConfirmacion(self, confirmacion: bool):
        self.confirmacion = confirmacion

    def tomarConfirmacion(self, confirmacion: bool):
        self.setConfirmacion(confirmacion)

    def finCu(self):
        pass
    
    def comunicarseConOperador(
        self,
        llamada: Llamada,
        categoriaLlamada: CategoriaLlamada,
        opcionLlamada: OpcionLlamada,
        subOpcionLlamada: SubOpcionLlamada
    ):
        self.setLlamada(llamada)
        self.setCategoriaLlamada(categoriaLlamada)
        self.setOpcionLlamada(opcionLlamada)
        self.setSubOpcionLlamada(subOpcionLlamada)

        pantallaOperador = self.getPantallaOperador()

        estadoEnCurso = self.buscarEstadoParaAsignar("enCurso")
        fechaHoraActual = self.obtenerFechaHoraActual()
        llamada.crearCambioEstado(
            nuevoEstado=estadoEnCurso,
            fechaHora=fechaHoraActual
        )

        datosLlamada = self.getDatosLlamada()
        validaciones = llamada.getValidaciones()

        pantallaOperador.mostrarDatosLlamada(datosLlamada, gestor=self)

        validacionesOrdenadas = self.ordernarValidaciones(validaciones)
        self.setValidacionesOrdenadas(validacionesOrdenadas)
        pantallaOperador.mostrarValidaciones(validacionesOrdenadas)

    def getDatosLlamada(self):
        llamada = self.getLlamada()
        categoriaLlamada = self.getCategoriaLlamada()
        opcionLlamada = self.getOpcionLlamada()
        subOpcionLlamada = self.getSubOpcionLlamada()

        nombreCliente = llamada.getNombreCliente()
        nombreCategoriaLlamada = categoriaLlamada.getNombre()
        nombreOpcionLlamada = opcionLlamada.getNombre()
        nombreSubOpcionLlamada = subOpcionLlamada.getNombre()

        return {
            "nombreCliente": nombreCliente,
            "nombreCategoriaLlamada": nombreCategoriaLlamada,
            "nombreOpcionLlamada": nombreOpcionLlamada,
            "nombreSubOpcionLlamada": nombreSubOpcionLlamada,
        }

    def buscarEstadoParaAsignar(self, nombre: str):
        match nombre:
            case "enCurso":
                for estado in self.getEstados():
                    if estado.esEnCurso():
                        return estado
            case "finalizada":
                for estado in self.getEstados():
                    if estado.esFinalizada():
                        return estado

    def obtenerFechaHoraActual(self):
        import datetime
        return datetime.datetime.now()


@lru_cache
def get_gestor():
    pantallaOperador = PantallaOperador()
    return GestorRegistrarRespuestaOperador(pantallaOperador)


class PantallaOperador:
    titulo: str = "<h1>IVR</h1>"
    datosLlamadaHtml: str = "<h1>Datos de la llamada</h1>"
    validacionesHtml: str = "<h1>Validaciones</h1>"
    accionesHtml: str = "<h1>Acciones</h1>"
    respuestaOperadorHtml: str = ""

    def mostrarDatosLlamada(self, datosLlamada: dict, gestor):
        datosLlamadaHtml = f"""
            <ul>
                <li>Nombre del cliente: {datosLlamada["nombreCliente"]}</li>
                <li>Categoria de la llamada: {datosLlamada["nombreCategoriaLlamada"]}</li>
                <li>Opcion de la llamada: {datosLlamada["nombreOpcionLlamada"]}</li>
                <li>Sub opcion de la llamada: {datosLlamada["nombreSubOpcionLlamada"]}</li>
            </ul>"""
        self.datosLlamadaHtml = datosLlamadaHtml

    def mostrarValidaciones(self, validaciones: list[Validacion], errores: dict = {}):
        validacionesHtml = """
            <form action="/tomar-respuesta-validacion" method="POST" 
            style="margin: 25px">
        """
        ambasCorrectas = all(errores.values()) if errores else False
        ambasCorrectasHtml = f"""<p style="color: green">Validado</p>""" if ambasCorrectas else ""
        if ambasCorrectas:
            validacionesHtml = ambasCorrectasHtml
        else:
            for validacion in validaciones:
                esCorrecta = errores.get(validacion.getNombre(), None)
                errorHtml = f"""<p style="color: red">Incorrecta</p>""" if esCorrecta is False else ""
                validacionesHtml += f"""<h3>Validacion: {validacion.getNombre()}</h3>
                        {errorHtml}
                        <input type="text" name="{validacion.getNombre()}" id="{validacion.getNombre()}">
                    """
            validacionesHtml += """<input type="submit" style="margin-left: 25px" value="Validar">
                </form>
            """
        self.validacionesHtml = validacionesHtml

    @app.post("/tomar-respuesta-validacion")
    async def tomarRespuestaValidacion(
        request: Request,
        gestor = Depends(get_gestor)
    ):
        form_data = await request.form()
        respuestas = form_data._dict
        validaciones, errores = gestor.tomarRespuestasValidaciones(respuestas)
        gestor.getPantallaOperador().mostrarValidaciones(validaciones, errores)
        if gestor.getValidacionesValidadas():
            gestor.getPantallaOperador().pedirRespuestaOperador()
        html = (
            gestor.pantallaOperador.titulo +
            gestor.pantallaOperador.datosLlamadaHtml +
            gestor.pantallaOperador.validacionesHtml + 
            gestor.pantallaOperador.respuestaOperadorHtml
        )
        return HTMLResponse(content=html)

    def pedirRespuestaOperador(self, fueTomada = False, gestor = None):
        if not fueTomada:
            respuestaOperadorHtml = """     
                    <form action="/tomar-respuesta-operador" method="POST" style="margin: 25px">
                        <h3>Respuesta del operador:</h3>
                        <input type="text" name="respuestaOperador" id="respuestaOperador">
                        <input type="submit" style="margin-left: 25px" value="Enviar">
                    </form>
                """
        else:
            respuestaOperadorHtml = f"""
                <p style="color: green">Respuesta del operador tomada: {gestor.getDescripcionOperador()}</p>
            """
        self.respuestaOperadorHtml = respuestaOperadorHtml

    @app.post("/tomar-respuesta-operador")
    async def tomarRespuestaOperador(
        request: Request,
        gestor = Depends(get_gestor)
    ):
        form_data = await request.form()
        respuesta = form_data._dict
        gestor.tomarRespuesta(respuesta['respuestaOperador'])
        gestor.getPantallaOperador().pedirRespuestaOperador(True, gestor)
        acciones = gestor.getAcciones()
        gestor.getPantallaOperador().pedirSeleccionAccionRequerida(acciones, False, gestor)
        html = (
            gestor.pantallaOperador.titulo +
            gestor.pantallaOperador.datosLlamadaHtml +
            gestor.pantallaOperador.validacionesHtml + 
            gestor.pantallaOperador.respuestaOperadorHtml +
            gestor.pantallaOperador.accionesHtml
        )
        return HTMLResponse(content=html)

    def pedirSeleccionAccionRequerida(
            self,
            acciones: list[Accion],
            fueSeleccionada: bool = False,
            gestor = None,
        ):
        if not fueSeleccionada:
            accionesHtml = """
                <form action="/tomar-accion-requerida" method="POST" style="margin: 25px">
                    <h3>Seleccione una acción requerida:</h3>
                    <select name="accionSeleccionada">
            """
            for accion in acciones:
                accionesHtml += f'<option value="{accion.getDescripcion()}">{accion.getDescripcion()}</option>'

            accionesHtml += """
                    </select>
                    <input type="submit" style="margin-left: 25px" value="Seleccionar">
                </form>
            """
        else:
            accionesHtml = f"""
                <p style="color: green">Acción requerida seleccionada: {gestor.getAccionSeleccionada()}</p>
            """
        self.accionesHtml = accionesHtml

    @app.post("/tomar-accion-requerida")
    async def tomarAccionRequerida(
        request: Request,
        gestor = Depends(get_gestor)
    ):
        form_data = await request.form()
        accionSeleccionada = form_data._dict["accionSeleccionada"]
        gestor.tomarSeleccionAccionRequerida(accionSeleccionada)
        gestor.getPantallaOperador().pedirSeleccionAccionRequerida(
            gestor.getAcciones(),
            True,
            gestor,
        )
        gestor.getPantallaOperador().solicitarConfirmacion()
        html = (
            gestor.pantallaOperador.titulo +
            gestor.pantallaOperador.datosLlamadaHtml +
            gestor.pantallaOperador.validacionesHtml + 
            gestor.pantallaOperador.respuestaOperadorHtml +
            gestor.pantallaOperador.accionesHtml + 
            gestor.pantallaOperador.confirmacionHtml
        )
        return HTMLResponse(content=html)

    def solicitarConfirmacion(self, confirmada: bool = False):
        if not confirmada:
            confirmacionHtml = """
                <form action="/tomar-confirmacion" method="POST" style="margin: 25px">
                    <button type="submit">Confirmar</button>
                </form>
            """
        else:
            confirmacionHtml = """
                <p style="color: green">Confirmación tomada</p>
            """

        self.confirmacionHtml = confirmacionHtml

    @app.post("/tomar-confirmacion")
    async def tomarConfirmacion(
        request: Request,
        gestor=Depends(get_gestor)
    ):
        gestor.tomarConfirmacion(True)
        gestor.getPantallaOperador().solicitarConfirmacion(True)
        gestor.registrarFinLlamada()
        html = (
            gestor.pantallaOperador.titulo +
            gestor.pantallaOperador.datosLlamadaHtml +
            gestor.pantallaOperador.validacionesHtml + 
            gestor.pantallaOperador.respuestaOperadorHtml +
            gestor.pantallaOperador.accionesHtml + 
            gestor.pantallaOperador.confirmacionHtml + 
            gestor.pantallaOperador.exitoCURegistrarAccionRequeridaHtml
        )
        return HTMLResponse(content=html)

    def informarExitoRegistroAccionRequerida(self, exito: bool = False):
        if exito:
            exitoCURegistrarAccionRequeridaHtml = """
                <p style="color: green">Registro de accion requerida finalizado con exito.</p>
            """
        else:
            exitoCURegistrarAccionRequeridaHtml = ""
        self.exitoCURegistrarAccionRequeridaHtml = exitoCURegistrarAccionRequeridaHtml


@app.get("/")
def main(
    gestor = Depends(get_gestor)
):
    cliente = Cliente(nombre="Lionel Messi")
    validaciones = [
        Validacion(nombre="Fecha de nacimiento", nroOrden=1),
        Validacion(nombre="Cantidad de hijos", nroOrden=2),
    ]
    subOpcionLlamada = SubOpcionLlamada(nombre="Cancelar tarjeta", validaciones=validaciones)
    opcionLlamada = OpcionLlamada(nombre="Tarjetas")
    categoriaLlamada = CategoriaLlamada(nombre="Reclamos")
    llamada = Llamada(cliente=cliente, subOpcionLlamada=subOpcionLlamada)
    gestor.comunicarseConOperador(
        llamada=llamada,
        categoriaLlamada=categoriaLlamada,
        opcionLlamada=opcionLlamada,
        subOpcionLlamada=subOpcionLlamada
    )

    html = (
        gestor.pantallaOperador.titulo +
        gestor.pantallaOperador.datosLlamadaHtml +
        gestor.pantallaOperador.validacionesHtml
    )
    return HTMLResponse(content=html)