# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Programa principal de la aplicación de escritorio. Ventana para inicio de sesión

# Importar módulos de PyQt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QHeaderView, QDialog
from PyQt5.uic import loadUi

# Importar la conexión a la base de datos
from modules.conexion import mibanco

# Importar los módulos de ReportLab
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors


# Clase Principal
class DlgCRUD(QDialog):
    def __init__(self, usuario, cuenta): # Constructor __init__
        super(DlgCRUD, self).__init__()
        loadUi('./uis/crud.ui', self)
        self.usuario = usuario
        self.cuenta = cuenta

        nombreColumnas = ['id_usuario', 'usuario', 'clave', 'correo']

        # Establecer el número de columnas
        self.tblCRUD.setColumnCount(len(nombreColumnas))

        # Establecer el nombre de las columnas
        self.tblCRUD.setHorizontalHeaderLabels(nombreColumnas)

        # Adaptar columnas al ancho de la tabla
        self.tblCRUD.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tblCRUD.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.cargarDatos()

        self.btnActualizar.clicked.connect(self.actualizar)
        self.btnInsertar.clicked.connect(self.insertar)
        self.btnEliminar.clicked.connect(self.eliminar)
        self.btnSalir.clicked.connect(self.salir)
        self.tblCRUD.clicked.connect(self.filaElegida)
        self.btnGenerarReporte.clicked.connect(self.generarReporte)


    def cargarDatos(self):
        cursor = mibanco.cursor()
        st = (f"SELECT id_usuario, usuario, clave, correo FROM usuarios")
        cursor.execute(st)
        filas = cursor.fetchall()

        numFilas = len(filas)
        self.tblCRUD.setRowCount(numFilas)
        f = 0

        if filas:
            for fila in filas:
                self.tblCRUD.setItem(f, 0, QtWidgets.QTableWidgetItem(str(fila[0])))
                self.tblCRUD.setItem(f, 1, QtWidgets.QTableWidgetItem(fila[1]))
                self.tblCRUD.setItem(f, 2, QtWidgets.QTableWidgetItem(fila[2]))
                self.tblCRUD.setItem(f, 3, QtWidgets.QTableWidgetItem(fila[3]))
                f += 1

        # Limpiar los campos
            self.txtUser.setText("")
            self.txtPassword.setText("")
            self.txtMail.setText("")


    def filaElegida(self):
        fila = self.tblCRUD.currentRow()
        id_usuario = self.tblCRUD.item(fila, 0)
        usuario = self.tblCRUD.item(fila, 1)
        clave = self.tblCRUD.item(fila, 2)
        correo = self.tblCRUD.item(fila, 3)

        self.spIdUsuario.setValue(int(id_usuario.text()))
        self.txtUser.setText(usuario.text())
        self.txtPassword.setText(clave.text())
        self.txtMail.setText(correo.text())


    def actualizar(self):
        if self.txtUser.text() != "" and self.txtPassword.text() != "" and self.txtMail.text() != "":
            id_usuario = self.spIdUsuario.value()
            usuario = self.txtUser.text()
            clave = self.txtPassword.text()
            correo = self.txtMail.text()

            cursor = mibanco.cursor()
            st = (f"UPDATE usuarios SET usuario = '{usuario}', clave = '{clave}', correo = '{correo}' WHERE id_usuario = {id_usuario}")
            cursor.execute(st)
            mibanco.commit()
            self.cargarDatos()


    def insertar(self):
        usuario = self.txtUser.text()
        clave = self.txtPassword.text()
        correo = self.txtMail.text()

        cursor = mibanco.cursor()
        st = (f"INSERT INTO usuarios (usuario, clave, correo) VALUES ('{usuario}', '{clave}', '{correo}')")
        cursor.execute(st)
        mibanco.commit()
        self.cargarDatos()


    def eliminar(self):
        id_usuario = self.spIdUsuario.value()

        cursor = mibanco.cursor()
        st = (f"DELETE FROM usuarios WHERE id_usuario = {id_usuario}")
        cursor.execute(st)
        mibanco.commit()
        self.cargarDatos()


    def generarReporte(self):
        nombreArchivo = "reporte_usuarios.pdf"
        # imagen = "imagenes/reporte_cajero_automatico_5.png" # Esta línea sirve para cargar una imagen en el reporte
        titulo = "REPORTE DE USUARIOS"
        encabezado = "ID        USUARIO         CORREO"
        lineas = [encabezado]

        cursor = mibanco.cursor()
        st = ("SELECT * FROM usuarios")
        cursor.execute(st)
        registros = cursor.fetchall()

        # Recorrido de las listas
        for registro in registros:
            linea = (f"{registro[0]:2d} {registro[1]:10s} {registro[3]:20s}")
            lineas.append(linea) # .append Adiciona los elementos al final

        # print(f"""
        #         Título: {titulo}
        #         Cuerpo:
        #             {lineas}
        # """)

        pdf = canvas.Canvas(nombreArchivo) # Crea un objeto PDF
        pdf.setTitle(titulo)
        pdf.setFillColorRGB(0, 0, 0) # Color de la fuente
        pdf.setFont("Courier-Bold", 12) # Tipo y tamaño de la fuente
        pdf.drawCentredString(290, 720, titulo)
        pdf.line(30, 710, 550, 710) # Dibuja una línea para separar los datos

        # Crear un texto multilínea utilizando textline y un ciclo for
        text = pdf.beginText(40, 680)
        text.setFont = ("Courier", 10)
        text.setFillColor(colors.black)

        # Recorrido sobre las líneas creadas previamente
        for linea in lineas:
            text.textLine(linea)

        pdf.drawText(text)
        # pdf.drawInlineImage(image, 475, 750) # Dibuja la imagen en la coordenada indicada
        pdf.save() # Guarda el archivo PDF


    def salir(self):
        from modules.cajero import DlgCajero
        self.cajero = DlgCajero(self.usuario, self.cuenta)
        self.cajero.show()
        self.close() # Cerrar el programa