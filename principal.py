# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Programa principal de la aplicación de escritorio. Ventana para inicio de sesión

# Importar módulos propios de Python
import sys

# Importar módulos de PyQt
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

# Importar módulos
from modules.cajero import DlgCajero
# from modules.crud import DlgCRUD

# Importar la conexión a la base de datos
from modules.conexion import mibanco


# Clase Principal
class DlgIniciar(QDialog):
    def __init__(self): # Constructor __init__
        super(DlgIniciar, self).__init__()
        loadUi('./uis/login.ui', self)
        self.btnIniciar.clicked.connect(self.iniciarSesion)
        # self.btnCrearCuenta.clicked.connect(self.irACrearCuenta)

    def iniciarSesion(self):
        txtUser = self.txtUser.text()
        txtPass = self.txtPass.text()

        st = (f"SELECT id_usuario, usuario, clave, correo FROM usuarios WHERE usuario = '{txtUser}' AND clave = '{txtPass}'")
        cursor = mibanco.cursor()
        cursor.execute(st)
        registro = cursor.fetchall()

        if registro:
            # user = registro[0][0]
            # clave = registro[0][1]
            # correo = registro[0][2]

            usuario = {
                'id_usuario': registro[0][0],
                'usuario': registro[0][1], 
                'clave': registro[0][2], 
                'correo': registro[0][3]
            }

            # self.lblMessage.setText("Usuario: " + usuario["usuario"] + ", Correo: " + usuario["correo"] + ", Clave: " + usuario["usuario"])
            st = (f"SELECT id_cuenta, nro_cuenta, saldo FROM cuentas WHERE id_usuario = {usuario['id_usuario']}") # Sentencia para consultar el saldo del usuario
            cursor.execute(st)
            cuenta = cursor.fetchall()
            cuenta = {
                'id_cuenta' : cuenta[0][0],
                'nro_cuenta' : cuenta[0][1],
                'saldo' : cuenta[0][2]
            }
            
            self.cajero = DlgCajero(usuario, cuenta)
            self.cajero.show()
            # self.crud = DlgCRUD(usuario)
            # self.crud.show()
            dlgIniciar.close()

        else:
            self.lblMessage.setText("Usuario o contraseña incorrectos")


# Programa principal de ejecución.
app = QApplication(sys.argv) # Crea una instancia de QApplication
dlgIniciar = DlgIniciar()

dlgIniciar.show()
sys.exit(app.exec_()) # Inicia el ciclo de eventos de la aplicación

# Este condicional asegura de que al volver a la ventana principal no se va a iniciar una nueva instancia de QApplication
# if __name__ == "__main__":
#     app = QApplication(sys.argv)  # Crea una instancia de QApplication
#     dlgIniciar = DlgIniciar()
#     dlgIniciar.show()
#     sys.exit(app.exec_())
