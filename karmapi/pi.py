# [Create a window]

import sys
from PyQt5 import QtWidgets as qt

from PyQt5.QtWidgets  import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QGridLayout, QBoxLayout, QHBoxLayout, QVBoxLayout)


def hello():
    
    app = QApplication(sys.argv) #ignore()
    window = QWidget()
    window.setWindowTitle("Hello World")
    window.show()

    # [Add widgets to the widget]

    # Create some widgets (these won't appear immediately):
    nameLabel = QLabel("Name:")
    nameEdit = QLineEdit()
    addressLabel = QLabel("Address:")
    addressEdit = QTextEdit()

    # Put the widgets in a layout (now they start to appear):
    layout = QGridLayout(window)
    layout.addWidget(nameLabel, 0, 0)
    layout.addWidget(nameEdit, 0, 1)
    layout.addWidget(addressLabel, 1, 0)
    layout.addWidget(addressEdit, 1, 1)
    layout.setRowStretch(2, 1)

    # [Resizing the window]

    # Let's resize the window:
    window.resize(480, 160)

    # The widgets are managed by the layout...
    window.resize(320, 180)

    # [Run the application]

    # Start the event loop...
    sys.exit(app.exec_())

def build(recipe, parent=None, row=True):

    if parent is None:
        parent = QVBoxLayout()

    for item in recipe:

        if isinstance(item, dict):
            parent.addWidget(build_widget(item))

        else:
            if row:
                layout = QHBoxLayout(window)
            else:
                layout = QVBoxLayout(window)

            parent.addWidget(window)

            build(item, layout, not row)

    return parent

def build_widget(item):

    return QLabel(item.get(name, 'noname'))


class PiWidget(QWidget):

    def __init__(self, recipe):

        super().__init__()
        
        self.recipe = recipe

    def build(self):

        layout = QVBoxLayout(self)

        build(self.recipe, layout)

        return


def app(recipe, title=None):

    if title is None:
        title = "Hello World"
        
    app = QApplication(sys.argv) #ignore()
    #window = PiWidget(recipe)
    window = QWidget()
    window.setWindowTitle(title)
    window.show()

    return app


if __name__ == '__main__':

    hello()
