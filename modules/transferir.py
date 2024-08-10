# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Módulo para transferir

# Importar módulos de PyQt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar la conexión a la base de datos
from modules.conexion import mibanco


# Clase Principal
class DlgTransferir(QDialog):
    def __init__(self, usuario, cuenta): # Constructor __init__
        super(DlgTransferir, self).__init__()
        loadUi('./uis/transfer.ui', self)

        self.usuario = usuario
        self.cuenta = cuenta
        self.txtCuentaDestino.setValidator(QIntValidator(0, 999999999, self))
        
        # Establecer el valor inicial en 0
        self.txtCuentaDestino.setText("0")

        # Botones del UI
        self.btn0.clicked.connect(self.cero)
        self.btn1.clicked.connect(self.uno)
        self.btn2.clicked.connect(self.dos)
        self.btn3.clicked.connect(self.tres)
        self.btn4.clicked.connect(self.cuatro)
        self.btn5.clicked.connect(self.cinco)
        self.btn6.clicked.connect(self.seis)
        self.btn7.clicked.connect(self.siete)
        self.btn8.clicked.connect(self.ocho)
        self.btn9.clicked.connect(self.nueve)
        self.btnSiguiente.clicked.connect(self.siguiente)
        self.btnBorrar.clicked.connect(self.borrar)
        self.btnCancelar.clicked.connect(self.cancelar)


    # Funciones para el teclado numérico
    def cero(self):
        cadenaValor = self.txtCuentaDestino.text()
        if len(cadenaValor) != 1:
            self.txtCuentaDestino.setText(cadenaValor + str(0))
        elif int(cadenaValor) > 0:
            self.txtCuentaDestino.setText(cadenaValor + str(0))

    def uno(self):
        self.digito("1")

    def dos(self):
        self.digito("2")

    def tres(self):
        self.digito("3")

    def cuatro(self):
        self.digito("4")

    def cinco(self):
        self.digito("5")

    def seis(self):
        self.digito("6")

    def siete(self):
        self.digito("7")

    def ocho(self):
        self.digito("8")

    def nueve(self):
        self.digito("9")

    def siguiente(self):
        cuentaDestino = self.txtCuentaDestino.text()  # Obtener el número de cuenta destino desde la interfaz

        if self.validarCuentaDestino(cuentaDestino):
            # Si la cuenta destino existe en la base de datos, continua con la transferencia
            from modules.tecladoTransferir import DlgTecladoTransferir
            self.tecladoTransferir = DlgTecladoTransferir(self.usuario, self.cuenta, cuentaDestino)  # Pasa cuentaDestino
            self.tecladoTransferir.show()
            self.close()
        else:
            self.lblMessage.setText("La cuenta destino no existe, por favor ingrese una cuenta válida")


    def validarCuentaDestino(self, cuentaDestino):
        cursor = mibanco.cursor()
        st = f"SELECT id_cuenta, nro_cuenta, saldo FROM cuentas WHERE nro_cuenta = '{cuentaDestino}'"
        cursor.execute(st)
        cuentaExiste = cursor.fetchone()

        if cuentaExiste is not None:
            cuentaExiste = cuentaExiste[0]
            return cuentaExiste > 0  # Devolver True si la cuenta existe, False si no existe
        else:
            return False  # Si no hay resultados, asumimos que la cuenta no existe

    def borrar(self):
        self.txtCuentaDestino.setText("0")

    def cancelar(self):
        from modules.cajero import DlgCajero
        self.cajero = DlgCajero(self.usuario, self.cuenta)
        self.cajero.show()
        self.close()

    def digito(self, dgto):
        cadenaValor = self.txtCuentaDestino.text()
        if cadenaValor and (len(cadenaValor) == 1 and int(cadenaValor) == 0):
            self.txtCuentaDestino.setText(dgto)
        elif cadenaValor and (int(cadenaValor) > 0):
            self.txtCuentaDestino.setText(cadenaValor + dgto)