# Hardware Info

## Heating Control

There are three wires (red, green, white) from the drywall that allows for control of the heater.
[Thermostat Wiring Info](https://dzone.com/articles/how-to-build-your-own-arduino-thermostat)

* Red
  * This is presumed to be a 24V line, this will be used to power the Raspberry Pi
  
* Green
  * This is presumed to be the line to control the indoor fan

* White
  * This is presumed to be the line to control the heating 
  
## Raspberry Pi Control
All control will be from the [GPIO](https://pinout.xyz/#)

### Power
Power will come from tapping into the 24V power line.
* However the Raspberry Pi only requires 5V therefore we need a [regulator](https://www.adafruit.com/product/2164).
* The Pi will be powered through pin #02 (5V) and pin #06 (ground)

### Heat
This is the most important aspect of the project being able to safely control the heater. This will be done through the use of a [relay](https://www.amazon.com/WINGONEER-KY-019-Channel-Module-arduino/dp/B06XHJ2PBJ/ref=sr_1_3?ie=UTF8&qid=1542921769&sr=8-3&keywords=relay)

### Touch Screen
Interacting with the Thermostat will be done through the user interface on the [touch screen](https://www.amazon.com/gp/product/B01IGBDT02/ref=ox_sc_act_title_1?smid=A2E7RYXKRFD586&psc=1)

### Temperature Sensor
We will be using a [temperature sensor](https://www.adafruit.com/product/3251) that I conveniently already wrote a [module](https://github.com/dpengineering/RaspberryPiCommon/tree/master/Libraries/TemperatureSensor) for.

### Thermal Management
In order to prevent components from heating up excessively [heat sinks](https://www.amazon.com/Gadgeter-Aluminum-Raspberry-Thermally-Conductive/dp/B01JB8MQ76/ref=sr_1_10?ie=UTF8&qid=1542921910&sr=8-10&keywords=small+heatsinks) will need to be placed on the CPU, relay, and any other parts that will heat up.