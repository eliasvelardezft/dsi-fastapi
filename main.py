from datetime import datetime

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "asd"}


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

    def esEnCurso(self):
        return self.getEstado().esEnCurso()

    def esFinalizada(self):
        return self.getEstado().esFinalizada()


class OpcionValidacion:
    def getDescripcion(self) -> str:
        return self.descripcion

    def esCorrecta(self, respuesta: str) -> bool:
        return respuesta == self.getDescripcion()


class InformacionCliente:
    def __init__(self, datoAValidar: str):
        self.setDatoAValidar(datoAValidar)

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
    def getNombre(self) -> str:
        return self.nombre


class Validacion:
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
    def __init__(self, nombre: str):
        self.setNombre(nombre)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre

    def getValidaciones(self) -> list[Validacion]:
        return self.validaciones


class OpcionLlamada:
    def __init__(self, nombre: str):
        self.setNombre(nombre)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre


class Llamada:
    def __init__(
        self,
        subOpcionLlamada: SubOpcionLlamada,
        cliente: Cliente,
    ):
        self.setSubOpcionLlamada(subOpcionLlamada)
        self.setCliente(cliente)
        self.cambiosDeEstado = []
        self.crearCambioEstado(Estado("enCurso"), datetime.now())

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



class PantallaOperador:
    def getHtml(self) -> str:
        return self.html
    
    def setHtml(self, html: str):
        self.html = html

    def mostrarDatosLlamada(self, datosLlamada: dict):
        html = '<h3>Datos de la llamada</h3>'
        for dato in datosLlamada:
            html += f'<p>{dato}</p>'

        self.setHtml(self, html)
        self.habilitarVentana()

    def mostrarValidaciones(self, validaciones: list[Validacion]):
        html = '<h3>Validaciones</h3>'
        for validacion in validaciones:
            html += f'<p>{validacion.getNombre()}</p>'
        
        html = self.getHtml() + html
        self.setHtml(self, html)
    
        self.habilitarVentana()

    def pedirRespuestaValidacion(self, validacion: Validacion):
        html = f"""
            <form action="/tomar-respuesta-validacion" method="POST" style="margin: 25px" target="_blank">
                <h3>Validacion: {validacion.getNombre()}</h3>
                <div>
                    <input type="text" name="respuesta">
                    <input type="submit" style="margin-left: 25px" value="Validar">
                </div>
            </form>
        """
        html += '<input type="text" name="respuestaValidacion" />'

        self.setHtml(self, html)
        self.habilitarVentana()

    @app.get("/tomar-respuesta-validacion")
    def tomarRespuestaValidacion(self, respuesta: str):
        self.validarRespuesta(respuesta)
        GestorRegistrarRespuestaOperador.tomarRespuestaValidacion(respuesta)
        return JSONResponse(content={"message": "Respuesta validacion tomada"}, status_code=200)

    def pedirRespuesta(self):
        html = f"""
            <form action="/tomar-respuesta" method="POST" style="margin: 25px" target="_blank">
                <h3>Respuesta a la consulta del cliente</h3>
                <div>
                    <input type="text" name="respuesta">
                    <input type="submit" style="margin-left: 25px" value="Enviar">
                </div>
            </form>
        """
        html += '<input type="text" name="respuesta" />'

        self.setHtml(self, html)
        self.habilitarVentana()

    def informarExitoRegistroAccionRequerida(self):
        html = '<h3>Se registro la accion requerida correctamente</h3>'
        self.setHtml(self, html)
        self.habilitarVentana()

    @app.get("/tomar-respuesta")
    def tomarRespuesta(self, respuesta: str):
        GestorRegistrarRespuestaOperador.tomarRespuesta(respuesta)
        return JSONResponse(content={"message": "Respuesta tomada"}, status_code=200)

    @app.get("/pantalla-operador")
    def habilitarVentana(self):
        return HTMLResponse(content=self.getHtml())

class Accion:
    def __init__(self, nombre: str):
        self.setNombre(nombre)

    def setNombre(self, nombre: str):
        self.nombre = nombre

    def getNombre(self) -> str:
        return self.nombre

    def getDescripcion(self) -> str:
        return self.descripcion


class GestorRegistrarAccionRequerida:
    def iniciarCU(self, accion: Accion):
        # aca devolvemos true porque fue exitosa la ejecucion del CU 28 - Registrar accion requerida
        return True


class GestorRegistrarRespuestaOperador:
    def __init__(self, pantallaOperador: PantallaOperador):
        self.setPantallaOperador(pantallaOperador)
        self.acciones = [
            Accion("Cancelar tarjeta"),
            Accion("Reintegrar dinero"),
        ]
        self.informacionesCliente = [
            InformacionCliente("Fecha de nacimiento"),
            InformacionCliente("Cantidad de hijos"),
        ]
        self.estados = [
            Estado("iniciada"),
            Estado("enCurso"),
            Estado("finalizada"),
        ]

    def getEstados(self) -> list[Estado]:
        return self.estados
    
    def getInformacionesCliente(self) -> list[InformacionCliente]:
        return self.informacionesCliente
    
    def getAcciones(self) -> list[Accion]:
        return self.acciones

    def setPantallaOperador(self, pantallaOperador: PantallaOperador):
        self.pantallaOperador = pantallaOperador

    def getPantallaOperador(self) -> PantallaOperador:
        return self.pantallaOperador

    def setLlamada(self, llamada: Llamada):
        self.llamada = llamada

    def setCategoriaLlamada(self, categoriaLlamada: CategoriaLlamada):
        self.categoriaLlamada = categoriaLlamada

    def setSubOpcionLlamada(self, subOpcionllamada: SubOpcionLlamada):
        self.subOpcionllamada = subOpcionllamada

    def setOpcionLlamada(self, opcionllamada: OpcionLlamada):
        self.opcionllamada = opcionllamada

    def getLlamada(self) -> Llamada:
        return self.llamada
    
    def getCategoriaLlamada(self) -> CategoriaLlamada:
        return self.categoriaLlamada
    
    def getSubOpcionLlamada(self) -> SubOpcionLlamada:
        return self.subOpcionllamada
    
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

    def tomarRespuestaValidacion(self, respuesta: str):
        self.setUltimaRespuestaValidacion(respuesta)

    def setDescripcionOperador(self, respuesta: str):
        self.descripcionOperador = respuesta

    def tomarRespuesta(self, respuesta: str):
        self.setDescripcionOperador(respuesta)

    def getDescripcionOperador(self) -> str:
        return self.descripcionOperador

    def validarRespuesta(self, validacion: Validacion, respuesta: str):
        return validacion.validarRespuesta(respuesta)

    def buscarAcciones(self) -> list[Accion]:
        return [accion.getDescripcion() for accion in self.getAcciones()]

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
        pantallaOperador.informarExitoRegistroAccionRequerida()

        estadoFinalizada = self.buscarEstadoParaAsignar("Finalizada")
        fechaHoraActual = self.obtenerFechaHoraActual()
        llamada = self.getLlamada()

        llamada.crearCambioEstado(estadoFinalizada, fechaHoraActual)

        llamada.setOpcionSeleccionada(self.getOpcionLlamada())
        llamada.setSubOpcionSeleccionada(self.getSubOpcionLlamada())
        llamada.setDescripcionOperador(self.getDescripcionOperador())

        duracion = llamada.calcularDuracion()
        llamada.setDuracion(duracion)

    def finCu():
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

        pantallaOperador.mostrarDatosLlamada(datosLlamada)

        validacionesOrdenadas = self.ordernarValidaciones(validaciones)
        pantallaOperador.mostrarValidaciones(validacionesOrdenadas)

        for validacion in validacionesOrdenadas:
            pantallaOperador.pedirRespuestaValidacion(validacion)
            if not self.validarRespuesta(self.getUltimaRespuestaValidacion()):
                raise Exception(
                    "Respuesta invalida",
                    nombreValidacion=validacion.getNombre()
                )
        
        pantallaOperador.pedirRespuesta()

        acciones = self.buscarAcciones()
        
        pantallaOperador.pedirSeleccionAccionRequerida(acciones)
        pantallaOperador.solicitarConfirmacion()

        self.registrarFinLlamada()

        self.finCu()


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



# if __name__ == "__main__":
#     pantallaOperador = PantallaOperador()
#     gestorRegistrarRespuestaOperador = GestorRegistrarRespuestaOperador(pantallaOperador)

#     # agregar parametros
#     llamada = Llamada()
#     categoriaLlamada = CategoriaLlamada()
#     opcionLlamada = OpcionLlamada()
#     subOpcionLlamada = SubOpcionLlamada()

#     gestorRegistrarRespuestaOperador.comunicarseConOperador(
#         llamada=llamada,
#         categoriaLlamada=categoriaLlamada,
#         opcionLlamada=opcionLlamada,
#         subOpcionLlamada=subOpcionLlamada
#     )

@app.get("/")
def main():
    pantallaOperador = PantallaOperador()
    gestorRegistrarRespuestaOperador = GestorRegistrarRespuestaOperador(pantallaOperador)

    # agregar parametros
    llamada = Llamada()
    categoriaLlamada = CategoriaLlamada()
    opcionLlamada = OpcionLlamada()
    subOpcionLlamada = SubOpcionLlamada()

    gestorRegistrarRespuestaOperador.comunicarseConOperador(
        llamada=llamada,
        categoriaLlamada=categoriaLlamada,
        opcionLlamada=opcionLlamada,
        subOpcionLlamada=subOpcionLlamada
    )