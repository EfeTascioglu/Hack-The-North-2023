import time
import sys
import smbus
import RPi.GPIO as GPIO

class LCD:

    # this device has two I2C addresses
    DISPLAY_RGB_ADDR = 0x62
    DISPLAY_TEXT_ADDR = 0x3e

    def __init__(self):
        self.bus = smbus.SMBus(1)

    # set backlight to (R,G,B) (values from 0..255 for each)
    def set_bg(self, r, g, b):
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 0, 0)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 1, 0)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 0x08, 0xaa)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 4, r)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 3, g)
        self.bus.write_byte_data(self.DISPLAY_RGB_ADDR, 2, b)
    
    def send_cmd(self, cmd):
        self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x80, cmd)
    
    def clear_display(self):
        self.send_cmd(0x01)

    def init_display(self):
        self.clear_display() # clear display
        time.sleep(0.05)
        self.send_cmd(0x08 | 0x04) # display on, no cursor
        self.send_cmd(0x28) # 2 lines
        time.sleep(0.05)
        self.home()
        time.sleep(0.05)
    
    def write_char(self, c):
        self.bus.write_byte_data(self.DISPLAY_TEXT_ADDR, 0x40, ord(c))
    
    def set_cursor(self, row, col):
        if not 0 <= row <= 1 and 0 <= col <= 15:
            return
        col = col | 0x80 if row == 0 else col | 0xc0
        self.send_cmd(col)
    
    def home(self):
        self.send_cmd(0x02)
    
    def write_str(self, s):
        for c in s:
            self.write_char(c)

class ReversedLCD(LCD):
    
    def __init__(self):
        super().__init__()
    
    def write_str_rev(self, s, row, col):
        self.set_cursor(row, ((15 - col) - (len(s) - 1)))
        for c in reversed(s):
            self.write_char(c)

if __name__ == "__main__":
    disp = ReversedLCD()
    disp.init_display()
    disp.set_bg(0, 0, 255)
    disp.write_str_rev("test 1", 0, 3)