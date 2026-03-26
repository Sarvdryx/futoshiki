from PyQt6.QtCore import QObject, pyqtSignal

class Worker(QObject):
    finished = pyqtSignal(object)   
    error = pyqtSignal(str)
    progress = pyqtSignal(str)  

    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        try:
            # truyền callback progress vào function
            result = self.func(*self.args, progress_callback=self.progress.emit)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))