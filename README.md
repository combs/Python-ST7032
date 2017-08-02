# Python-ST7032

This is a Python port of [arduino_ST7032](https://github.com/tomozh/arduino_ST7032). It lets you use these devices in I2C mode. Parallel/8bit/4bit and SPI modes are not currently supported.
 
ST7032 is an i2c character display driver, embedded in some fancier character displays. 

## Where to get them

Tested good: [BuyDisplay 16x2 COG](http://www.buydisplay.com/default/display-serial-16x2-cog-lcd-module-pin-connection-white-on-blue)

Many on eBay, [search with description for st7032](https://www.ebay.com/dsc/i.html?_from=R40&_sacat=0&LH_TitleDesc=1&_nkw=st7032&_trksid=p2045573.m570.l1313.TR0.TRC0.H0.TRS0&_odkw=st7032&_osacat=0
)

# Wiring

I2C SDA, SCL to your devices' best pins for these. 

XRESET to VDD. It will not respond without this.

Backlights typically are raw LEDs; the buydisplay white-on-blue expects 3.1v at 15ma, or ~ 120 ohm resistor from 5v.

Enable i2c mode with these pins:

PSB to VDD
PSI2B to GND

Datasheet also says E to VDD, I haven't found this necessary

0.1-4.7uf capacitor across CAP1P (positive) and CAP1N (negative)

VDD to 2.7-5.5V
VSS to GND


# Software usage

```python
device = st7032.ST7032()
device.setContrast(53)
device.clear()
device.write("Hello World!")
device.setCursor(0,1)  # column 0, row 1
device.write("Goodbye")
```

# Params

Pass these to ST7032():

```
    busnum = 0      # i2c bus
    address = 0x3e  # i2c address
    lines = 2       # is this a 1-line, 2-line, 4-line display
    dotsize = 0       # I'm not sure what this does 
```

# Future improvements, bugs

Please file a [GitHub issue](https://github.com/combs/Python-ST7032/issues). Thanks!

