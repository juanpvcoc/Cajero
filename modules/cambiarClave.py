# @autor: Juan Velásquez
# @fecha: 2023/10/27
# @descripción: Módulo para cambiar la clave

# Importar módulos propios de Python
import sys

# Importar módulos de PyQt
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

# Importar la conexión a la base de datos
from modules.conexion import mibanco


# Clase Principal
class DlgCambiarClave(QDialog):
    def __init__(self, usuario, cuenta): # Constructor __init__
        super(DlgCambiarClave, self).__init__()
        loadUi('./uis/changePassword.ui', self)

        self.usuario = usuario
        self.cuenta = cuenta

        self.btnCambiarClave.clicked.connect(self.cambiarClave)
        self.btnCancelar.clicked.connect(self.cancelar)


    def cambiarClave(self):
        claveActual = self.txtClaveActual.text()
        claveNueva = self.txtClaveNueva.text()
        confirmarClave = self.txtConfirmarClave.text()
        id_usuario = self.usuario['id_usuario']

        # Consultar la clave actual del usuario
        st = (f"SELECT clave FROM usuarios WHERE id_usuario = {id_usuario}")
        cursor = mibanco.cursor()
        cursor.execute(st)
        registro = cursor.fetchone()

        if registro:  # Si se encuentra el registro del usuario
            claveGuardada = registro[0]  # Obtener la clave guardada en la base de datos

            # Verificar si los campos de clave nueva y confirmación no están vacíos
            if claveNueva.strip() == "" or confirmarClave.strip() == "":
                self.lblMessage.setText("Por favor, complete todos los campos.")
            else:
                if claveActual == claveGuardada:  # Verificar si la clave actual coincide con la guardada
                    if claveNueva == confirmarClave:  # Verificar si la clave nueva coincide con la confirmación
                        # Actualizar la clave en la base de datos
                        st = (f"UPDATE usuarios SET clave = '{claveNueva}' WHERE id_usuario = {id_usuario}")
                        cursor.execute(st)
                        mibanco.commit()

                        self.lblMessage.setText("Clave actualizada correctamente")

                        # Fragmento para regresar al módulo cajero
                        # from modules.cajero import DlgCajero
                        # self.cajero = DlgCajero(self.usuario, self.cuenta)
                        # self.cajero.show()
                        # self.close() 
                    else:
                        self.lblMessage.setText("Las claves no coinciden")
                else:
                    self.lblMessage.setText("La clave actual es incorrecta")
        else:
            self.lblMessage.setText("Usuario no encontrado")


    def cancelar(self):
        from modules.cajero import DlgCajero
        self.cajero = DlgCajero(self.usuario, self.cuenta)
        self.cajero.show()
        self.close() 