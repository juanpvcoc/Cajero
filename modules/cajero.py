# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Módulo principal de opciones del cajero

# Importar módulos propios de Python
import sys

# Importar módulos de PyQt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


# Clase Principal
class DlgCajero(QDialog):
    def __init__(self, usuario, cuenta): # Constructor __init__
        super(DlgCajero, self).__init__()
        loadUi('./uis/cajero.ui', self)

        self.usuario = usuario # Define el atributo 'usuario' en el constructor para enviarlo a los demás módulos
        self.cuenta = cuenta

        self.lblUser.setText(f"Bienvenido {usuario["usuario"]}")

        self.btnDepositar.clicked.connect(self.depositar)
        self.btnRetirar.clicked.connect(self.retirar)
        self.btnTransferir.clicked.connect(self.transferir)
        self.btnConsultarSaldo.clicked.connect(self.consultarSaldo)
        self.btnCambiarClave.clicked.connect(self.cambiarClave)
        self.btnAdminUsers.clicked.connect(self.adminUsers)
        self.btnSalir.clicked.connect(self.salir)

    def depositar(self):
        from modules.depositar import DlgDepositar
        self.deposit = DlgDepositar(self.usuario, self.cuenta)
        self.deposit.show()
        self.close()

    def retirar(self):
        from modules.retirar import DlgRetirar
        self.whitdrawals = DlgRetirar(self.usuario, self.cuenta)
        self.whitdrawals.show()
        self.close()

    def transferir(self):
        from modules.transferir import DlgTransferir
        self.transfer = DlgTransferir(self.usuario, self.cuenta)
        self.transfer.show()
        self.close()

    def consultarSaldo(self):
        from modules.consultarSaldo import DlgConsultarSaldo
        self.checkBalance = DlgConsultarSaldo(self.usuario, self.cuenta)
        self.checkBalance.show()
        self.close()

    def cambiarClave(self):
        from modules.cambiarClave import DlgCambiarClave
        self.changePass = DlgCambiarClave(self.usuario, self.cuenta)
        self.changePass.show()
        self.close()
    
    def adminUsers(self):
        from modules.crud import DlgCRUD
        self.crud = DlgCRUD(self.usuario, self.cuenta)
        self.crud.show()
        self.close()

    def salir(self):
        # from principal import DlgIniciar
        # self.principal = DlgIniciar(self.usuario)
        # self.principal.show()
        self.close() # Cerrar el programa