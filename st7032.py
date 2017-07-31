# -*- coding: UTF-8 -*-

from constants import *
from smbus2 import SMBus
import time


class ST7032(object):

    busnum = 0
    _displaycontrol = 0
    _displaymode = 0
    _displayfunction = 0
    address = 0x3e
    lines = 2
    dotsize=0
    _numlines = 1
    _currline = 0


    def __del__(self):
        # self.smbus.close()
        pass

    def __init__(self, *args, **kwargs):

        # Flags

        if type (args) is not None:
          for arg in args:
              setattr(self,arg,True)

        # key=value parameters

        if type (kwargs) is not None:
          for key, value in kwargs.iteritems():
              if type(value) is dict:
                  if getattr(self,key):
                        tempdict = getattr(self,key).copy()
                        tempdict.update(value)
                        value = tempdict
              setattr(self,key,value)
              # def begin(self,cols, lines, self.dotsize) :

        self._displayfunction  = LCD_8BITMODE | LCD_1LINE | LCD_5x8DOTS

        if (self.lines > 1) :
            self._displayfunction |= LCD_2LINE

        self._numlines = self.lines
        self._currline = 0
        # for some 1 line displays you can select a 10 pixel high font
        if ((self.dotsize != 0) and (self.lines == 1)) :
            self._displayfunction |= LCD_5x10DOTS

        self.smbus = SMBus(self.busnum)

        # finally, set # lines, font size, etc.
        self.normalFunctionSet()

        self.extendFunctionSet()
        self.command(LCD_EX_SETBIASOSC | LCD_BIAS_1_4 | LCD_OSC_347HZ)          # 1/5bias, OSC=183Hz@3.0V
        self.command(LCD_EX_FOLLOWERCONTROL | LCD_FOLLOWER_ON | LCD_RAB_2_00)     # internal follower circuit is turn on
        time.sleep(0.2)                                 # Wait time >200ms (for power stable)
        self.normalFunctionSet()

        # turn the display on with no cursor or blinking default
        #  display()
        self._displaycontrol  = 0x00 #LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.setDisplayControl(LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF)

        # self.clear it off
        self.clear()

        # Initialize to default text direction (for romance languages)
        #  self.command(LCD_ENTRYMODESET | self._displaymode)
        self._displaymode      = 0x00#LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        self.setEntryMode(LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT)

    def setDisplayControl(self,setBit) :
        self._displaycontrol |= setBit
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)


    def resetDisplayControl(self,resetBit) :
        self._displaycontrol &= ~resetBit
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)


    def setEntryMode(self,setBit) :
        self._displaymode |= setBit
        self.command(LCD_ENTRYMODESET | self._displaymode)


    def resetEntryMode(self,resetBit) :
        self._displaymode &= ~resetBit
        self.command(LCD_ENTRYMODESET | self._displaymode)


    def normalFunctionSet(self) :
        self.command(LCD_FUNCTIONSET | self._displayfunction)


    def extendFunctionSet(self) :
        self.command(LCD_FUNCTIONSET | self._displayfunction | LCD_EX_INSTRUCTION)

    #
    # ST7032::ST7032(int i2c_addr)
    # : self._displaycontrol(0x00)
    # , self._displaymode(0x00)
    # , address((uint8_t)i2c_addr)
    # {
    # #  begin(16, 1)




    def setContrast(self,cont):
        self.extendFunctionSet()
        self.command(LCD_EX_CONTRASTSETL | (cont & 0x0f))                 # Contrast set
        self.command(LCD_EX_POWICONCONTRASTH | LCD_ICON_ON | LCD_BOOST_ON | ((cont >> 4) & 0x03)) # Power, ICON, Contrast control
        self.normalFunctionSet()


    def setIcon(self,addr, bit) :
        self.extendFunctionSet()
        self.command(LCD_EX_SETICONRAMADDR | (addr & 0x0f))                   # ICON address
        write(bit)
        self.normalFunctionSet()


    # /********** high level commands, for the user! */
    def clear(self):
        self.command(LCD_CLEARDISPLAY)  # self.clear display, set cursor position to zero
        time.sleep(0.002)  # this command takes a long time!


    def home(self):
        self.command(LCD_RETURNHOME)  # set cursor position to zero
        time.sleep(0.002)  # this command takes a long time!


    def setCursor(self,col,row):
        row_offsets = [ 0x00, 0x40, 0x14, 0x54 ]

        if ( row > self._numlines ) :
            row = self._numlines-1    # we count rows starting w/0


        self.command(LCD_SETDDRAMADDR | (col + row_offsets[row]))


    # Turn the display on/off (quickly)
    def noDisplay(self) :
        self.resetDisplayControl(LCD_DISPLAYON)

    def display(self) :
        self.setDisplayControl(LCD_DISPLAYON)


    # Turns the underline cursor on/off
    def noCursor(self) :
        self.resetDisplayControl(LCD_CURSORON)

    def cursor(self) :
        self.setDisplayControl(LCD_CURSORON)


    # Turn on and off the blinking cursor
    def noBlink(self) :
        self.resetDisplayControl(LCD_BLINKON)

    def blink(self) :
        self.setDisplayControl(LCD_BLINKON)


    # These commands scroll the display without changing the RAM
    def scrollDisplayLeft(self) :
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)


    def scrollDisplayRight(self) :
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)


    # This is for text that flows Left to Right
    def leftToRight(self) :
        self.setEntryMode(LCD_ENTRYLEFT)


    # This is for text that flows Right to Left
    def rightToLeft(self) :
        self.resetEntryMode(LCD_ENTRYLEFT)


    # This will 'right justify' text from the cursor
    def autoscroll(self) :
        self.setEntryMode(LCD_ENTRYSHIFTINCREMENT)


    # This will 'left justify' text from the cursor
    def noAutoscroll(self) :
        self.resetEntryMode(LCD_ENTRYSHIFTINCREMENT)


    # Allows us to fill the first 8 CGRAM locations
    # with custom characters
    def createChar(self,location, charmap) :
        location &= 0x7 # we only have 8 locations 0-7
        self.command(LCD_SETCGRAMADDR | (location << 3))
        for i in range(0,7):
            self.writeData(charmap[i])



    # /*********** mid level commands, for sending data/cmds */

    def command(self,value) :
        self.smbus.write_byte_data(self.address,0x00,value)


    def writeData(self,value) :
        self.smbus.write_byte_data(self.address,0x40,value)

    def write(self,value):
        for character in value:
            self.writeData(ord(character))


    def println(self,value):
        for character in value:
            self.writeData(ord(character))
        self.writeData(0)



 #
 #  ST7032.cpp - Arduino LiquidCrystal compatible library
 #
 #  Original source is Arduino LiquidCrystal liblary
 #
 #  Author:  tomozh@gmail.com
 #  License: MIT
 #
 #  History:
 #    2014.10.13 コントラスト値のbit7がBONビットに影響する不具合を修正
 #    2014.08.23 コンストラクタでI2Cアドレスを設定可能にした
 #    2013.05.21 1st release
 #
 # ------------------------
 #  Arduino        ST7032i
 # ------------------------
 #  3.3V    --+-- VDD
 #          +-- -RES
 #  A4(SDA) --*-- SDA
 #  A5(SCL) --*-- SCL
 #  GND     ----- GND
 #
 #  *... 10Kohm pull-up
 # ------------------------
 #
