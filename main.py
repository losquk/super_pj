import sys

from PyQt5.QtWidgets import QApplication

from GUI import GUI
app = QApplication(sys.argv)
window = GUI.GUI()
window.show()  # Показуємо вікно
sys.exit(app.exec_())  # Запускаємо цикл подій PyQt







