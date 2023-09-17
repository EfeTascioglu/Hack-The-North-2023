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
    def __init__(self, operations: Queue):
        super().__init__()
        self.operations = operations
    
    def run(self):
        lcd = display.ReversedLCD()
        lcd.init_display()
        lcd.set_bg(255, 255, 255)

        blink_cycles = 0
        clear_cycles = 0

        while True:
            try:
                if blink_cycles > 0:
                    blink_cycles -= 1
                    if blink_cycles == 0:
                        lcd.set_bg(255, 255, 255)
                
                if clear_cycles > 0:
                    clear_cycles -= 1
                    if clear_cycles == 0:
                        lcd.clear_display()

                op: DisplayOperation = self.operations.get_nowait()
                if op.type == DisplayOperation.Type.SET_TEXT:
                    lcd.write_str_rev(op.args[0], op.args[1], op.args[2])
                    if len(op.args) > 3:
                        clear_cycles = op.args[3]
                    else:
                        clear_cycles = 0
                elif op.type == DisplayOperation.Type.CLEAR:
                    lcd.clear_display()
                elif op.type == DisplayOperation.Type.BLINK:
                    blink_cycles = 3
                    lcd.set_bg(op.args[0], op.args[1], op.args[2])
            except: # oops we're at a hackathon
                pass
            time.sleep(0.1)
