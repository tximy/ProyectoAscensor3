import wiringpi2
import time
# blocks activation pins
io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)

MotorPins = [ 5, 6, 10, 11] # In1, In2, In3, In4  Pines del motor;  Direccion,Pasos,Reset,Velocidad (ms2 0=1/2 y 1=1/8) ms1 +3.3v ms2 pin ms3 0v

Seq1 = [
      #Secuencia de avance simple
      [1,0,0,0], 
      [0,1,0,0], 
      [0,0,1,0], 
      [0,0,0,1], 
];




# Define advanced sequence
# as shown in manufacturers datasheet
StepCount2 = 8
Seq2 = []
Seq2 = range(0, StepCount2)
Seq2[0] = [1,0,0,0]
Seq2[1] = [1,1,0,0]
Seq2[2] = [0,1,0,0]
Seq2[3] = [0,1,1,0]
Seq2[4] = [0,0,1,0]
Seq2[5] = [0,0,1,1]
Seq2[6] = [0,0,0,1]
Seq2[7] = [1,0,0,1]


def Inicializa():
   for n in range(0, len(MotorPins)):
     io.pinMode(MotorPins[n],io.OUTPUT)    
     io.digitalWrite(MotorPins[n],io.LOW)
     
     

#StepPins = [24,25,8,7]
 

def AvanceSencillo(ciclos,WaitTime): # Numero de vueltas y el tiempo de espera 0.5 por ejemplo
  Seq = Seq1 # Choose a sequence to use
  StepCounter = 0
  Ciclo=0 
  # Start main loop
  while Ciclo <= ciclos:
    for pin in range(0, len(MotorPins)):
      xpin = MotorPins[pin]
      if Seq[StepCounter][pin]!=0:
        print " Step %i Enable %i" %(StepCounter,xpin)
        io.digitalWrite(MotorPins[xpin],io.HIGH)
      else:
        io.digitalWrite(MotorPins[xpin],io.LOW)
    StepCounter += 1
    # If we reach the end of the sequence
    # start again
    if (StepCounter==len(Seq)):
      StepCounter = 0
    if (StepCounter<0):
      StepCounter = len(Seq)
    # Wait before moving on
    time.sleep(WaitTime)
    Ciclo +=1
   



def step(dir,steps,Avance,WaitTime):# direccion 0 cw 1 ccw  y pasos entero 1600 ej, Avance 0=1/2 1=1/8 y el tiempo de espera 0.5 por ejemploy el tiempo de espera 0.01 por ejemplo
  io.digitalWrite(MotorPins[0],dir)
  io.digitalWrite(MotorPins[3],Avance)
  io.digitalWrite(MotorPins[2],io.HIGH)
  i=0
  while i < steps :
    #print i
    i+=1
    io.digitalWrite(MotorPins[1],io.HIGH)
    time.sleep(WaitTime)
    io.digitalWrite(MotorPins[1],io.LOW)
    time.sleep(WaitTime)
  io.digitalWrite(MotorPins[2],io.LOW)

