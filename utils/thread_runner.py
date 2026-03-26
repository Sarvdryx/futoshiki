from PyQt6.QtCore import QThread
from worker.worker import Worker

def run_in_thread(parent, func, *args, on_done=None):
    thread = QThread()
    worker = Worker(func, *args)

    worker.moveToThread(thread)

    thread.started.connect(worker.run)

    worker.progress.connect(parent.footer.setText)

    if on_done:
        worker.finished.connect(on_done)

    worker.error.connect(lambda e: parent.footer.setText("Error: " + e))

    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(thread.deleteLater)

    thread.start()

    return thread, worker