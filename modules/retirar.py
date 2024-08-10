# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Módulo para retirar

# Importar módulos de PyQt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar la conexión a la base de datos
from modules.conexion import mibanco


# Clase Principal
class DlgRetirar(QDialog):
    def __init__(self, usuario, cuenta): # Constructor __init__
        super(DlgRetirar, self).__init__()
        loadUi('./uis/withdrawals.ui', self)

        self.usuario = usuario
        self.cuenta = cuenta

        # Mostrar el saldo actual
        saldo = self.cuenta['saldo']
        self.lblMessage.setText(f"Su saldo es: ${saldo:9,.2f}")

        self.btnRetirar10.clicked.connect(self.retirar10)
        self.btnRetirar20.clicked.connect(self.retirar20)
        self.btnRetirar50.clicked.connect(self.retirar50)
        self.btnRetirar100.clicked.connect(self.retirar100)
        self.btnRetirar200.clicked.connect(self.retirar200)
        self.btnRetirar500.clicked.connect(self.retirar500)
        self.btnOtroValor.clicked.connect(self.otroValor)
        self.btnCancelar.clicked.connect(self.cancelar)

    def retirar10(self):
        monto = 10000
        # self.txtMonto.setText(str(monto))  # Establecer el monto en el campo de texto
        self.anotacion(monto)

    def retirar20(self):
        monto = 20000
        # self.txtMonto.setText(str(monto))
        self.anotacion(monto)

    def retirar50(self):
        monto = 50000
        # self.txtMonto.setText(str(monto))
        self.anotacion(monto)

    def retirar100(self):
        monto = 100000
        # self.txtMonto.setText(str(monto))
        self.anotacion(monto)

    def retirar200(self):
        monto = 200000
        # self.txtMonto.setText(str(monto))
        self.anotacion(monto)

    def retirar500(self):
        monto = 500000
        # self.txtMonto.setText(str(monto))
        self.anotacion(monto)

    def anotacion(self, monto):  # Ajustar para recibir el parámetro 'monto'
        monto = int(monto)  # Convertir el monto a entero

        if monto <= self.cuenta['saldo']:  
            nuevoSaldo = self.cuenta['saldo'] - monto  
            cursor = mibanco.cursor()

            st = f"UPDATE cuentas SET saldo = {nuevoSaldo} WHERE id_cuenta = {self.cuenta['id_cuenta']}"
            stMvto = f"INSERT INTO movimientos(movimiento, fecha_mvto, monto, id_cuenta) VALUES (2, CURRENT_TIMESTAMP(), {monto}, {self.cuenta['id_cuenta']})"

            cursor.execute(st)
            cursor.execute(stMvto)
            mibanco.commit()

            self.lblMessage.setText(f"¡Transacción exitosa! Su nuevo saldo es ${nuevoSaldo:9,.2f}")
        else:
            self.lblMessage.setText("Fondos insuficientes para realizar el retiro")


    def otroValor(self):
        from modules.tecladoRetiro import DlgTecladoRetiro
        self.tecladoRetiro = DlgTecladoRetiro(self.usuario, self.cuenta)
        self.tecladoRetiro.show()
        self.close() 

    def cancelar(self):
        from modules.cajero import DlgCajero
        self.cajero = DlgCajero(self.usuario, self.cuenta)
        self.cajero.show()
        self.close()