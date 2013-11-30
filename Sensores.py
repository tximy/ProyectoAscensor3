
import wiringpi2
io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
Entradas=[0,0,0,0,0,0,0,0,0,0,0,0]
blockActivationPins = [ 16, 17]  # Bloque Plantas ,  Bloque Cabina
PinsDeEntrada = [ 7, 8, 9, 14, 15, 20] # 0,1,2,3,4, Sensor de Calibracion (plantas baja y alta)

def Inicializa():
  contador=0
  for i in range(0, len(blockActivationPins)):
    io.pinMode(blockActivationPins[i],io.OUTPUT)    
    io.digitalWrite(blockActivationPins[i],io.HIGH)
    for n in range(0, len(PinsDeEntrada)):
      io.pinMode(PinsDeEntrada[n],io.INPUT)    
      io.pullUpDnControl(PinsDeEntrada[n],io.PUD_UP)
      Entradas[contador]=0
      contador+=1



def Leer():
  contador=0
  for i in range(0, len(blockActivationPins)):
    io.digitalWrite(blockActivationPins[i],io.LOW)
    for n in range(0, len(PinsDeEntrada)):
      x=io.digitalRead(PinsDeEntrada[n])
      if x==io.LOW:
        Entradas[contador]=1
      else :
        Entradas[contador]=0
      contador+=1
    io.digitalWrite(blockActivationPins[i],io.HIGH)
  return Entradas
