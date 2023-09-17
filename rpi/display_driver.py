from threading import Thread
from queue import Queue, Empty
import time
import enum

import display

class DisplayOperation:

    class Type(enum.Enum):
        SET_TEXT = 0
        BLINK = 1
        CLEAR = 2

    def __init__(self, type: Type, *args):
        self.type = type
        self.args = args

class DisplayDriver(Thread):
    def __init__(operations: Queue):
        super().__init__()
    
    def run(self):
        lcd = display.ReversedLCD()
        lcd.init_display()
        lcd.set_bg(255, 255, 255)

        blink_cycles = 0

        while True:
            try:
                if blink_cycles > 0:
                    blink_cycles -= 1
                    if blink_cycles == 0:
                        lcd.set_bg(255, 255, 255)

                op: DisplayOperation = self.operations.get_nowait()
                if op.type == DisplayOperation.Type.SET_TEXT:
                    lcd.write_str_rev(op.args[0], op.args[1], op.args[2])
                elif op.type == DisplayOperation.Type.CLEAR:
                    lcd.clear_display()
                elif op.type == DisplayOperation.Type.BLINK:
                    blink_cycles = 10
                    lcd.set_bg(op.args[0], op.args[1], op.args[2])
            except: # oops we're at a hackathon
                pass
            time.sleep(0.1)

if __name__ == "__main__":
    q = Queue()
    driver = DisplayDriver(q)
    driver.daemon = True
    driver.start()

    time.sleep(5)
    q.put(DisplayOperation(DisplayOperation.Type.SET_TEXT, "Test", 0, 0))

    time.sleep(1)
    q.put(DisplayOperation(DisplayOperation.Type.BLINK, 0, 255, 0))

    q.put(DisplayOperation(DisplayOperation.Type.CLEAR))
    time.sleep(10)
    print("Exit")
