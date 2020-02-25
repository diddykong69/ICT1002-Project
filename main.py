import sys
import os
from PyQt5.QtWidgets import *
sys.path.insert(0, os.path.abspath('./controller/'))
from controller.MainWindow import MainWindow

TITLE = "GOTCHA!"

app = QApplication(sys.argv)

# Get screen available size
screen = app.primaryScreen()
available_size = screen.availableSize()
width, height = available_size.width(), available_size.height()

# Size of app: 640 x 480
expected_width, expected_height = 640, 480

# Calculate screen position to
# centralise app
position_x, position_y = (width - expected_width) / 2, (height - expected_height) / 2

# Create the Main Window to add to our
# GUI app
window = MainWindow(TITLE, (position_x, position_y, expected_width, expected_height))

# window = MainWindow()
window.show()

sys.exit(app.exec_())
