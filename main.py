import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtGui import QPainter, QPen, QColor, QPolygon
import PySide6.QtCore as qt
import pygame

if getattr(sys, 'frozen', False):  # When the app is frozen (compiled)
    app_path = sys._MEIPASS
else:
    app_path = os.path.dirname(__file__)

music_path = os.path.join(app_path, 'outro_music.mp3')


class ClockWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        # self.play_outro = False
        pygame.mixer.init()
        pygame.mixer.music.load(music_path)
        self.play_outro = False

        
        self.timer = qt.QTimer(self)
        self.timer.timeout.connect(self.update)
        # self.timer.start(50)  # Update every 50 ms
        self.timer.start(1000)  # Update every 50 ms
        self.rotation_angle = 0

        self.setWindowTitle('Clock')
        self.setGeometry(200, 200, 300, 300)
        self.setStyleSheet("background : black;")

        self.countdown_time = None

        self.countdown_hours = 0


    

    def handle_timer_changed(self, new_time):
        tik = qt.QTime.currentTime()

        self.countdown_time = tik.secsTo(new_time)


        if self.countdown_time < 0:
            remaining_seconds_today = tik.secsTo(QtCore.QTime(23, 59, 59)) + 1
            self.countdown_time = remaining_seconds_today + QtCore.QTime(0, 0, 0).secsTo(new_time)
            # print(f"Time set for the next day. Countdown: {countdown_seconds} seconds")



        # print(f"Timer changed to: {new_time.toString('HH:mm:ss')}")

    def paintEvent(self, event):
        rec = min(self.width(), self.height())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(rec / 300, rec / 300)
        painter.setPen(QPen(QColor("white")))


        points = QPolygon([qt.QPoint(0, -60), qt.QPoint(-2, -45), qt.QPoint(2, -45)])
        painter.drawPolygon(points)

        tik = qt.QTime.currentTime()


        # self.rotation_angle = -(tik.second() + tik.msec() / 1000) * 6  
        painter.save()

        if self.countdown_time == 0:

            # print("Shut Down !!")
            if os.name == 'nt':  
                os.system("shutdown /s /f /t 0")
            elif os.name == 'posix': 
                os.system("shutdown now")


        if self.countdown_time is not None:
            if widget.checkbox1.isChecked() == True and self.countdown_time < 28 and not self.play_outro:

                # print("Play Music !!")
                self.play_outro = True
                pygame.mixer.music.play()  


            painter.rotate(6 * (60 - self.countdown_time % 60))
            # print(self.countdown_time//60)
            self.countdown_hours = (self.countdown_time // 3600)

            self.countdown_time -=1


        # Draw the clock ticks
        for i in range(0, 60):
            painter.setPen(QPen(QColor("pink")))
            painter.drawLine(0, -65, 0, -70)
            if (i % 5) == 0:                    
                painter.drawLine(0, -65, 0, -75)
                painter.save()
                if i < 10:
                    painter.translate(-3, -80)
                else:
                    painter.translate(-6, -80)


                painter.drawText(0, 0, f"{i}")
                painter.restore()

            # Rotate the painter for each tick
            painter.rotate(6)  # 360 degrees / 60 ticks

        painter.restore()

        painter.save()

        if self.countdown_time is not None:
            painter.rotate(-6 * (self.countdown_time // 60))

        for i in range(0, 60):
            painter.drawLine(0, -105, 0, -110)
            if (i % 5) == 0:
                painter.drawLine(0, -105, 0, -115)
                painter.save()

                if i < 10:
                    painter.translate(-3, -119)
                else:
                    painter.translate(-6, -119)
                painter.drawText(0, 0, f"{i}")
                painter.restore()

            # Rotate the painter for each tick
            painter.rotate(6)  # 360 degrees / 60 ticks
        
        painter.restore()

        if self.countdown_hours > 0:
            painter.setPen(QPen(QColor("grey")))
            painter.rotate(-15 * (self.countdown_hours))
            for i in range(0,  self.countdown_hours+1):
                painter.drawLine(0, -135, 0, -140)
                painter.drawLine(0, -135, 0, -145)
                painter.save()
                if i < 10:
                    painter.translate(-3, -149)
                else:
                    painter.translate(-6, -149)
                painter.drawText(0, 0, f"{i}")
                painter.restore()

                # Rotate the painter for each tick
                painter.rotate(15)  # 360 degrees / 60 ticks

        painter.end()


class MyWidget(QtWidgets.QWidget):
    timer_changed = QtCore.Signal(QtCore.QTime)

    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)


        self.clock_widget = ClockWidget()
        main_layout.addWidget(self.clock_widget, stretch=5)
        self.timer_changed.connect(self.clock_widget.handle_timer_changed)

        self.title_label = QtWidgets.QLabel("SLEEP TIMER")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont("Courier New", 28, QtGui.QFont.Bold)
        font.setItalic(True)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet("color: #00FF00;")  

        side_controls_layout = QtWidgets.QVBoxLayout()
        side_controls_layout.addStretch()

        side_controls_layout.addWidget(self.title_label)
        # side_controls_layout.addStretch()
        time_control_layout = QtWidgets.QHBoxLayout()


        self.time_edit = QtWidgets.QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm:ss")
        self.time_edit.setTime(QtCore.QTime.currentTime())
        time_control_layout.addWidget(self.time_edit)


        self.button = QtWidgets.QPushButton("Set Sleep Time")
        self.button.clicked.connect(self.on_button_click)
        time_control_layout.addWidget(self.button)


        side_controls_layout.addLayout(time_control_layout)
        self.custom_x = 0
        self.custom_y = 0


        self.message_label = QtWidgets.QLabel("")
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setStyleSheet("color: white;")
        side_controls_layout.addWidget(self.message_label)

        self.dropdown = QtWidgets.QComboBox()
        self.dropdown.addItem("Custom Add Time")
        self.dropdown.addItem("5 min")
        self.dropdown.addItem("10 min")
        self.dropdown.addItem("15 min")
        self.dropdown.addItem("20 min")
        self.dropdown.addItem("30 min")
        self.dropdown.addItem("45 min")
        self.dropdown.addItem("1 hour")
        self.dropdown.addItem("2 hour")
        # self.dropdown.model().item(0).setFlags(self.dropdown.model().item(0).flags() & ~QtCore.Qt.ItemIsSelectable)
        
        self.dropdown.currentTextChanged.connect(self.on_dropdown_change)

        side_controls_layout.addWidget(self.dropdown, alignment=QtCore.Qt.AlignCenter)

        self.checkbox1 = QtWidgets.QCheckBox("Enable Outro Music (last 20 sec)")

        side_controls_layout.addWidget(self.checkbox1, alignment=QtCore.Qt.AlignCenter)


        main_layout.addLayout(side_controls_layout, stretch=2)
        side_controls_layout.addStretch()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.time_edit.timeChanged.connect(self.on_time_changed)


        self.setWindowTitle("Sleep Timer")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background: black;")

    def on_time_changed(self, new_time):
        """Handles the time change while user is editing."""
        # Adjust if the seconds are 0
        if new_time.second() == 0:
            # If seconds are 0, check if minutes are also 0
            if new_time.minute() == 0:
                # If minute is 0 and hour is not 0, decrement the hour by 1 and set seconds to 59
                if new_time.hour() > 0:
                    new_time = QtCore.QTime(new_time.hour() - 1, 59, 59)
                else:
                    # If it's 00:00:00, set to 23:59:59
                    new_time = QtCore.QTime(23, 59, 59)
            else:
                # If minutes are not 0, just set seconds to 59
                new_time = QtCore.QTime(new_time.hour(), new_time.minute() - 1, 59)
        else:
            # If seconds are not 0, just keep the time unchanged
            new_time = new_time

        # Update the time edit widget with the adjusted time
        self.time_edit.setTime(new_time)


    def on_dropdown_change(self):

        selected_time = self.dropdown.currentText()


        current_time = QtCore.QTime.currentTime()


        if selected_time == "5 min":
            new_time = current_time.addSecs(5 * 60)
        elif selected_time == "10 min":
            new_time = current_time.addSecs(10 * 60)
        elif selected_time == "15 min":
            new_time = current_time.addSecs(15 * 60)
        elif selected_time == "20 min":
            new_time = current_time.addSecs(20 * 60)
        elif selected_time == "30 min":
            new_time = current_time.addSecs(30 * 60)
        elif selected_time == "45 min":
            new_time = current_time.addSecs(45 * 60)
        elif selected_time == "1 hour":
            new_time = current_time.addSecs(60 * 60)
        elif selected_time == "2 hour":
            new_time = current_time.addSecs(2 * 60 * 60)
        else:

            new_time = current_time


        self.time_edit.setTime(new_time)

    def on_button_click(self):
        selected_time = self.time_edit.time()
        self.message_label.setText(f"Timer set for {selected_time.toString('HH:mm:ss')}")
        self.timer_changed.emit(selected_time)


    def update_time(self):
        current_time = QtCore.QTime.currentTime()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
