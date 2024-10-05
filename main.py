from PyQt5 import QtWidgets
from design import*
import sys, threading, mouse, time, keyboard

sleep_sec = 1

class Clicker:
    def __init__(self):
        self.isClicking = False
        self.thread = None

    def start_clicking(self):
        self.isClicking = True
        self.thread = threading.Thread(target=self.click_loop)
        self.thread.start()

    def stop_clicking(self):
        self.isClicking = False
        if self.thread is not None:
            self.thread.join()

    def click_loop(self):
        next_click_time = time.perf_counter()
        while self.isClicking:
            current_time = time.perf_counter()
            if current_time >= next_click_time:
                mouse.click(button='left')
                next_click_time = current_time + sleep_sec


class MyWin(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.HotKey_Edit.returnPressed.connect(self.change_Hotkey)
        self.ui.KlicksInSecond_Spin.textChanged.connect(self.clicks_in_sec)

        # Создаем экземпляр класса Clicker
        self.clicker = Clicker()

        keyboard.add_hotkey(self.ui.HotKey_Edit.text(), self.toggle_clicker)


    def toggle_clicker(self):
        if self.clicker.isClicking:
            self.clicker.stop_clicking()  # Останавливаем кликер
        else:
            self.clicker.start_clicking()  # Запускаем кликер
    
    def change_Hotkey(self):
        self.ui.HotKey_label.setText(self.ui.HotKey_Edit.text())
        keyboard.remove_hotkey(self.ui.HotKey_Edit.text())
        keyboard.add_hotkey(self.ui.HotKey_Edit.text(), self.toggle_clicker)
    
    def clicks_in_sec(self):
        global sleep_sec
        sleep_sec = 1 / int(self.ui.KlicksInSecond_Spin.text())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()
    sys.exit(app.exec_())
