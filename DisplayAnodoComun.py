
import wiringpi2
# cambiada la inicializacion e impresion para anodo comun 
# segment representation of each digit
# The original table was for some C library but I can't find it anywhere
# to give credit to the author. If you recognize it, leave me a comment please.

#  --a--
# |     |
# f     b
# |     |
#  --g--
# |     |
# e     c
# |     |
#  --d--  p

Segmentos = [
    #a b c d e f g p Segmentos
    [1, 1, 1, 1, 1, 1, 0, 0], # 0
    [0, 1, 1, 0, 0, 0, 0, 0], # 1
    [1, 1, 0, 1, 1, 0, 1, 0], # 2
    [1, 1, 1, 1, 0, 0, 1, 0], # 3
    [0, 1, 1, 0, 0, 1, 1, 0], # 4
    [1, 0, 1, 1, 0, 1, 1, 0], # 5
    [1, 0, 1, 1, 1, 1, 1, 0], # 6
    [1, 1, 1, 0, 0, 0, 0, 0], # 7
    [1, 1, 1, 1, 1, 1, 1, 0], # 8
    [1, 1, 1, 1, 0, 1, 1, 0], # 9
    [1, 1, 1, 0, 1, 1, 1, 0], # A
    [0, 0, 1, 1, 1, 1, 1, 0], # b
    [1, 0, 0, 1, 1, 1, 0, 0], # C
    [0, 1, 1, 1, 1, 0, 1, 0], # d
    [1, 0, 0, 1, 1, 1, 1, 0], # E
    [1, 0, 0, 0, 1, 1, 1, 0], # F
    [0, 0, 0, 0, 0, 0, 0, 0], # blank
];



io = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_PINS)
PinDeSegmento = [ 1, 2, 3, 4, 0, 13, 12 ]

def Inicializa(): 
  for i in range(0, len(PinDeSegmento)):
    io.pinMode(PinDeSegmento[i],io.OUTPUT)    
    io.digitalWrite(PinDeSegmento[i],io.HIGH)



    
    
def Enciende(char):
 ActivarSegmentos = Segmentos[int(char)]
 for Led in range(0, 7):
    val = bool(ActivarSegmentos[Led])
    io.digitalWrite(PinDeSegmento[Led],not val)
    #print str(PinDeSegmento[led])+' '+str(not val)
   

#Inicializa()
#Enciende(8)
