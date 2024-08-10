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
class DlgTecladoTransferir(QDialog):
    def __init__(self, usuario, cuenta, cuentaDestino): # Constructor __init__
        super(DlgTecladoTransferir, self).__init__()
        loadUi('./uis/keyboardTransfer.ui', self)

        self.usuario = usuario
        self.cuenta = cuenta
        self.txtMonto.setValidator(QIntValidator(0, 999999999, self))
        self.cuentaDestino = cuentaDestino  # Almacenar cuentaDestino en la instancia de la clase

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

        if sMonto != "" and sMonto != "0" and self.cuentaDestino != "":
            monto = int(sMonto)

            if monto <= self.cuenta['saldo']:  
                nuevoSaldoOrigen = self.cuenta['saldo'] - monto  
                cursor = mibanco.cursor()

                # Actualizar el saldo de la cuenta origen
                stOrigen = f"UPDATE cuentas SET saldo = {nuevoSaldoOrigen} WHERE id_cuenta = {self.cuenta['id_cuenta']}"
                stMvtoOrigen = f"INSERT INTO movimientos(movimiento, fecha_mvto, monto, id_cuenta) VALUES (3, CURRENT_TIMESTAMP(), {monto}, {self.cuenta['id_cuenta']})"
                cursor.execute(stOrigen)
                cursor.execute(stMvtoOrigen)
                
                # Actualizar el saldo de la cuenta destino
                stDestino = f"UPDATE cuentas SET saldo = saldo + {monto} WHERE nro_cuenta = '{self.cuentaDestino}'"
                stMvtoDestino = f"INSERT INTO movimientos(movimiento, fecha_mvto, monto, id_cuenta) VALUES (1, CURRENT_TIMESTAMP(), {monto}, '{self.cuentaDestino}')"
                cursor.execute(stDestino)
                cursor.execute(stMvtoDestino)

                mibanco.commit()

                self.lblMessage.setText(f"¡Transacción exitosa! Nuevo saldo: ${nuevoSaldoOrigen:9,.2f}")
            else:
                self.lblMessage.setText("Fondos insuficientes para realizar la transferencia")
        else:
            self.lblMessage.setText("Por favor ingrese un monto válido y una cuenta de destino")


    def digito(self, dgto):
        cadenaValor = self.txtMonto.text()
        if cadenaValor and (len(cadenaValor) == 1 and int(cadenaValor) == 0):
            self.txtMonto.setText(dgto)
        elif cadenaValor and (int(cadenaValor) > 0):
            self.txtMonto.setText(cadenaValor + dgto)