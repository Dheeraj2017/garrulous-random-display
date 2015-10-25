from PyQt5 import QtCore, QtWidgets

class EntropyMonitor(QtWidgets.QDialog):
    """Monitor /proc/sys/kernel/random/entropy_avail."""

    def __init__(self):
  
        super().__init__()
        self.setWindowTitle("Entropy Display")
        self._get_poolsize()
        vbox = QtWidgets.QVBoxLayout()
        self._create_progress(vbox)
        self._create_labels(vbox)
        self._create_button(vbox)
        self.setLayout(vbox)
        self._create_timer()

    def _get_poolsize(self):
        
        with open('/proc/sys/kernel/random/poolsize', 'r') as f:
            self._poolsize = int(f.read())

    def _create_progress(self, vbox):
      
        self._amount = QtWidgets.QProgressBar()
        self._amount.setMaximum(self._poolsize)
        vbox.addWidget(self._amount)

    def _create_labels(self, vbox):
        grid = QtWidgets.QGridLayout()
        grid.addWidget(QtWidgets.QLabel("Total Available:"), 0, 0)
        grid.addWidget(QtWidgets.QLabel("Total Poolsize:"), 1, 0)
        self._available = QtWidgets.QLabel()
        self._available.setAlignment(QtCore.Qt.AlignRight)
        poolsize = QtWidgets.QLabel(str(self._poolsize))
        poolsize.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(self._available, 0, 1)
        grid.addWidget(poolsize, 1, 1)
        vbox.addLayout(grid)

    def _create_button(self, vbox):
        quit = QtWidgets.QPushButton("END")
        quit.clicked.connect(self.accept)
        vbox.addWidget(quit)

    def _create_timer(self):
        timer = QtCore.QTimer(self)
        timer.setInterval(500)
        timer.timeout.connect(self._timeout)
        timer.start()

    def _timeout(self):
        with open('/proc/sys/kernel/random/entropy_avail', 'r') as f:
            value = int(f.read())
            self._amount.setValue(value)
            self._available.setText(str(value))

if __name__ == '__main__':
    a = QtWidgets.QApplication([])
    EntropyMonitor().exec()
