# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Módulo para consultar el saldo de la cuenta

# Importar módulos propios de Python
import sys

# Importar módulos de PyQt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar la conexión a la base de datos
from modules.conexion import mibanco


# Clase Principal
class DlgConsultarSaldo(QDialog):
    def __init__(self, usuario, cuenta): # Constructor __init__
        super(DlgConsultarSaldo, self).__init__()
        loadUi('./uis/checkBalance.ui', self)

        self.usuario = usuario
        self.cuenta = cuenta
        saldo = cuenta['saldo']

        self.lblSaldo.setText(f"${saldo:9,.2f}")
        self.btnVolver.clicked.connect(self.volver)


    def volver(self):
        from modules.cajero import DlgCajero
        self.cajero = DlgCajero(self.usuario, self.cuenta)
        self.cajero.show()
        self.close() 