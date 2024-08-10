# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Teclado numérico de la aplicación

# Importar módulos de PyQt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar la conexión a la base de datos
from modules.conexion import mibanco


# Clase Principal
class DlgTecladoRetiro(QDialog):
    def __init__(self, usuario, cuenta): # Constructor __init__
        super(DlgTecladoRetiro, self).__init__()
        loadUi('./uis/keyboardWithdrawal.ui', self)

        self.usuario = usuario
        self.cuenta = cuenta
        self.txtMonto.setValidator(QIntValidator(0, 999999999, self))

        # Establecer el valor inicial en 0
        self.txtMonto.setText("0")

        # Mostrar el saldo actual
        saldo = self.cuenta['saldo']
        self.lblMessage.setText(f"Su saldo es: ${saldo:9,.2f}")

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
        self.btnBorrar.clicked.connect(self.borrar)
        self.btnAnotacion.clicked.connect(self.anotacion)
        self.btnCancelar.clicked.connect(self.cancelar)

    # Funciones para el teclado numérico
    def cero(self):
        cadenaValor = self.txtMonto.text()
        if len(cadenaValor) != 1:
            self.txtMonto.setText(cadenaValor + str(0))
        elif int(cadenaValor) > 0:
            self.txtMonto.setText(cadenaValor + str(0))

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

    def borrar(self):
        self.txtMonto.setText("0")

    def cancelar(self):
        from modules.cajero import DlgCajero
        self.cajero = DlgCajero(self.usuario, self.cuenta)
        self.cajero.show()
        self.close()

    def anotacion(self):
        sMonto = self.txtMonto.text()

        if sMonto != "" and sMonto != "0":
            monto = int(sMonto)

            if monto <= self.cuenta['saldo']:  # Verificar si el monto es menor o igual al saldo disponible
                nuevoSaldo = self.cuenta['saldo'] - monto  # Realizar la resta para el retiro
                cursor = mibanco.cursor()

                st = (f"UPDATE cuentas SET saldo = {nuevoSaldo} WHERE id_cuenta = {self.cuenta['id_cuenta']}")
                stMvto = (f"INSERT INTO movimientos(movimiento, fecha_mvto, monto, id_cuenta) VALUES (2, CURRENT_TIMESTAMP(), {monto}, {self.cuenta['id_cuenta']})")

                cursor.execute(st)
                cursor.execute(stMvto)
                mibanco.commit()

                self.lblMessage.setText(f"¡Transacción exitosa! Su nuevo saldo es ${nuevoSaldo:9,.2f}")
            else:
                self.lblMessage.setText("Fondos insuficientes para realizar el retiro")
        else:
            self.lblMessage.setText("Por favor ingrese un monto válido")


    def digito(self, dgto):
        cadenaValor = self.txtMonto.text()
        if cadenaValor and (len(cadenaValor) == 1 and int(cadenaValor) == 0):
            self.txtMonto.setText(dgto)
        elif cadenaValor and (int(cadenaValor) > 0):
            self.txtMonto.setText(cadenaValor + dgto)