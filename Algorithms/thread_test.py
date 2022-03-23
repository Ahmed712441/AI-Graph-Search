import threading
import time


class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait() # return immediately when it is True, block until the internal flag is True when it is False
            print(time.time())
            time.sleep(1)

    def pause(self):
        self.__flag.clear() # Set to False to block the thread

    def resume(self):
        self.__flag.set() # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set() # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear() # Set to False


if __name__ == "__main__":
    a = Job()
    a.start()
    time.sleep(3)
    a.pause()
    time.sleep(3)
    a.resume()
    time.sleep(3)
    a.pause()
    time.sleep(2)
    a.stop()