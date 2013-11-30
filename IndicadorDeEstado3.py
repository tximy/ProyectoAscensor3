

import wiringpi2
io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
LedPins = [18,19]
Estado = {'Libre':0,'Bajando':1,'Subiendo':2,'Ocupado':3}
LedActive = [
      #Up Down
      [0, 0], # Estado 0  Stoped 
      [0, 1], # Estado 1  Down Direcction
      [1, 0], # Estado 2  Up Direcction
      [1, 1], # Estado 3  Door is Open
];

def Inicializa():
  for i in range(0, len(LedPins)):
      io.pinMode(LedPins[i],io.OUTPUT)    
      io.digitalWrite(LedPins[i],io.LOW)


def ActivaLeds(Modo):
  LedsEncender = LedActive[int(Estado[Modo])]
  for led in range(0,len(LedPins)):
      val = bool(LedsEncender[led])
      io.digitalWrite(LedPins[led],val)
      #print str(LedPins[led])+' '+ str(val)
   
