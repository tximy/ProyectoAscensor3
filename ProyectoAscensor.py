##ProyectoAscensor V3
##Este ha sido el primer programa desarrollado en python por Alfredo Rego Diaz con la colaboracion de Luis Gonzalez Perez para el proyecto de la universidad Galileo en el curso de Iniciacion a Raspberry PI
##Este programa es funcional con un control "inteligente/logico" aunque por falta de tiempo aun no se ha optimizado.


import DisplayAnodoComun as Display #Inicializa() y Enciende(0-16)
import IndicadorDeEstado3 as iEstado # Inicializa() y ActivaLeds(Libre,Bajando,Subiendo,Ocupado)
import Sensores # Inicializa() y Leer() una matriz de 12 sensores
import sys
import Motor # Inicializa() y  step direccion 0 cw(subir) 1 ccw(bajar)  y pasos entero 1600 ej, Avance 0=1/2 1=1/8 y el tiempo de espera 0.5 por ejemploy el tiempo de espera 0.01 por ejemplo
import time

Entradas=Sensores
Estado='Ocupado'
ParadasSubiendo=[]
ParadasBajando=[]
PlantaActual=0
PlantaDestino=0


def LeerEntrada(Entrada):
  x=Entradas.Leer()
  #print x
  if Entrada=='FCBajo':
    return x[5]
  elif Entrada=='FCAlto':
    return x[11]
  elif Entrada=='P0': 
    return x[0]
  elif Entrada=='P1':
    return x[1]
  elif Entrada=='P2':
    return x[2]
  elif Entrada=='P3':
    return x[3]
  elif Entrada=='P4':
    return x[4]
  elif Entrada=='A0':
    return x[6]
  elif Entrada=='A1':
    return x[7]
  elif Entrada=='A2':
    return x[8]
  elif Entrada=='A3':
    return x[9]
  elif Entrada=='A4':
    return x[10]

    
    
def InicializaAscensor():
  global Estado
  global PlantaActual
  global PlantaDestino
  iEstado.Inicializa()
  Motor.Inicializa()
  Display.Inicializa()
  Entradas.Inicializa()

  Estado='Ocupado'
  iEstado.ActivaLeds('Bajando')
  Display.Enciende(10)
  while not LeerEntrada('FCBajo'): 
    Motor.step(1,100,1,0.001)
  Estado='Libre'
  iEstado.ActivaLeds(Estado)
  PlantaActual=0
  PlantaDestino=0
  Display.Enciende(PlantaActual)
  
  
def Planta(Accion):
  global Estado
  global PlantaActual
  global PlantaDestino
  global ParadasSubiendo
  global ParadasBajando
  if Estado=='Bajando' and PlantaDestino>PlantaActual:
    Estado='Subiendo'
    Accion='Subir'
  if Estado=='Subiendo' and PlantaDestino<PlantaActual:
    Estado='Bajando'
    Accion='Bajar'
  if Accion=='Subir':
    if (not LeerEntrada('FCAlto')) and (PlantaActual<4) and (PlantaActual<PlantaDestino):
      Estado='Subiendo'
      iEstado.ActivaLeds(Estado)
      s=0
      while (s<10) and (not LeerEntrada('FCAlto')) :
        s+=1
        Motor.step(0,130,1,0.001)
        ActualizarMemorias()
      PlantaActual +=1
      Display.Enciende(PlantaActual)
      if PlantaActual==PlantaDestino:
        iEstado.ActivaLeds('Ocupado')
        for n in range(0,200):
          time.sleep(0.01)
          ActualizarMemorias()
      iEstado.ActivaLeds(Estado)
      while PlantaActual in ParadasSubiendo:
        ParadasSubiendo.remove(PlantaActual)
        while PlantaActual==4 and PlantaActual in ParadasBajando:
          ParadasBajando.remove(PlantaActual)
        if PlantaActual==4 and (len(ParadasBajando)>0):
          Estado='Bajando'
          iEstado.ActivaLeds(Estado)
          PlantaDestino=ParadasBajando[0]
        if PlantaActual==4 and (len(ParadasBajando)==0):
          Estado='Libre'
          iEstado.ActivaLeds(Estado)
        if PlantaActual>0 and (len(ParadasBajando)>0) and (len(ParadasSubiendo)==0):
          if (not(PlantaDestino in ParadasBajando))and (ParadasBajando[0] > PlantaActual): 
            Estado='Subiendo'
            ParadasSubiendo.append(ParadasBajando[0])
            PlantaDestino=ParadasSubiendo[0]
            while PlantaDestino in ParadasBajando:
              ParadasBajando.remove(PlantaDestino)
          elif ParadasBajando[0] == PlantaActual:
            while PlantaDestino in ParadasBajando:
              ParadasBajando.remove(PlantaDestino)
          elif ParadasBajando[0] < PlantaActual:      
            Estado='Bajando'
            iEstado.ActivaLeds(Estado)
            PlantaDestino=ParadasBajando[0]
        if (len(ParadasBajando)==0) and (len(ParadasSubiendo)==0):
          Estado='Libre'
          iEstado.ActivaLeds(Estado)
          
  if Accion=='Bajar':
    if (not LeerEntrada('FCBajo')) and (PlantaActual>0) and (PlantaActual>PlantaDestino):
      Estado='Bajando'
      iEstado.ActivaLeds(Estado)
      b=0
      while (b<10) and (not LeerEntrada('FCBajo')) :
        b+=1
        Motor.step(1,124,1,0.001)
        ActualizarMemorias()
      PlantaActual -=1
      Display.Enciende(PlantaActual)
      if PlantaActual==PlantaDestino:
        iEstado.ActivaLeds('Ocupado')
        for n in range(0,200):
          time.sleep(0.01)
          ActualizarMemorias()
      iEstado.ActivaLeds(Estado)
      while PlantaActual in ParadasBajando:
        ParadasBajando.remove(PlantaActual)
        if PlantaActual==0 and (len(ParadasSubiendo)>0):
          #print ' bajando planta actual 0 y con paradas subiendo'
          Estado='Subiendo'
          iEstado.ActivaLeds(Estado)
          PlantaDestino=ParadasSubiendo[0]
        if PlantaActual==0 and (len(ParadasSubiendo)==0):
          if (len(ParadasBajando)>0):
            if ParadasBajando[0] > 0:
              ParadasSubiendo.append(ParadasBajando[0])
              PlantaDestino=ParadasBajando[0]
              Estado='Subiendo'
              while PlantaDestino in ParadasBajando:
                ParadasBajando.remove(PlantaDestino)
          else:
            #print ' bajando planta actual 0 y sin paradas subiendo'
            Estado='Libre'
            iEstado.ActivaLeds(Estado)
        if PlantaActual<4 and (len(ParadasSubiendo)>0) and (len(ParadasBajando)==0):
          #print ' bajando sin paradas bajando y con paradas subiendo'
          Estado='Subiendo'
          PlantaDestino=ParadasSubiendo[0]
          iEstado.ActivaLeds(Estado)
        if (len(ParadasBajando)==0) and (len(ParadasSubiendo)==0):
          #print ' bajando sin paradas ni subiendo ni bajando'
          Estado='Libre'
          iEstado.ActivaLeds(Estado)


  
def ActualizarMemorias():
  global Estado
  global PlantaActual
  global PlantaDestino
  global ParadasSubiendo
  global ParadasBajando
  if (Estado=='Libre') and (PlantaActual==0) and (LeerEntrada('FCBajo')): # Libre en planta baja
    if LeerEntrada('A1') or LeerEntrada('P1'):
      ParadasSubiendo.append(1)
    if LeerEntrada('A2') or LeerEntrada('P2'):
      ParadasSubiendo.append(2)
    if LeerEntrada('A3') or LeerEntrada('P3'):
      ParadasSubiendo.append(3)
    if LeerEntrada('A4') or LeerEntrada('P4'):
      ParadasSubiendo.append(4)


  if Estado=='Subiendo':
    if (LeerEntrada('A0') or LeerEntrada('P0')) and PlantaActual >0:
      ParadasBajando.append(0)

    if LeerEntrada('A1'):
      if PlantaActual <1:
        ParadasSubiendo.append(1)
      else:
        ParadasBajando.append(1)
    if LeerEntrada('P1'):
      ParadasBajando.append(1)

    if LeerEntrada('A2'):
      if PlantaActual <2:
        ParadasSubiendo.append(2)
      else:
        ParadasBajando.append(2)
    if LeerEntrada('P2'):
      ParadasBajando.append(2)

    if LeerEntrada('A3'):
      if PlantaActual <3:
        ParadasSubiendo.append(3)
      else:
        ParadasBajando.append(3)      
    if LeerEntrada('P3'):
      ParadasBajando.append(3)

    if LeerEntrada('A4'):
      if PlantaActual <4:
        ParadasSubiendo.append(4)
      else:
        ParadasBajando.append(4)      
    if LeerEntrada('P4'):
      ParadasBajando.append(4)

    
  if Estado=='Bajando':
    if (LeerEntrada('A0') or LeerEntrada('P0')) and PlantaActual>0:
      ParadasBajando.append(0)
    if (LeerEntrada('A1') or LeerEntrada('P1')) and PlantaActual>1:
      ParadasBajando.append(1)
    if (LeerEntrada('A1') or LeerEntrada('P1')) and PlantaActual<=1:
      ParadasSubiendo.append(1)
    if LeerEntrada('A2') or LeerEntrada('P2') and PlantaActual>2:
      ParadasBajando.append(2)
    if (LeerEntrada('A2') or LeerEntrada('P2')) and PlantaActual<=2:
      ParadasSubiendo.append(2)      
    if LeerEntrada('A3') or LeerEntrada('P3') and PlantaActual>3:
      ParadasBajando.append(3)
    if (LeerEntrada('A3') or LeerEntrada('P3')) and PlantaActual<=3:
      ParadasSubiendo.append(3)      
    if (LeerEntrada('A4') or LeerEntrada('P4')) and PlantaActual<=4:
      ParadasSubiendo.append(4)     
  if (Estado=='Libre') : # Libre en planta 
    if (LeerEntrada('A0') or LeerEntrada('P0')) and PlantaActual>0:
      ParadasBajando.append(0)
    if (LeerEntrada('A1') or LeerEntrada('P1'))and PlantaActual>1:
      ParadasBajando.append(1)
    if (LeerEntrada('A1') or LeerEntrada('P1'))and PlantaActual<1:
      ParadasSubiendo.append(1)
    if (LeerEntrada('A2') or LeerEntrada('P2'))and PlantaActual >2:
      ParadasBajando.append(2)
    if (LeerEntrada('A2') or LeerEntrada('P2'))and PlantaActual<2:
      ParadasSubiendo.append(2)
    if (LeerEntrada('A3') or LeerEntrada('P3'))and PlantaActual >3:
      ParadasBajando.append(3)
    if (LeerEntrada('A3') or LeerEntrada('P3'))and PlantaActual<3:
      ParadasSubiendo.append(3)
    if (LeerEntrada('A4') or LeerEntrada('P4'))and PlantaActual<4:
      ParadasSubiendo.append(4)
  if (len(ParadasSubiendo)>0):
    ParadasSubiendo.sort()
    if (Estado=='Subiendo' or (len(ParadasBajando)==0))  and PlantaActual<ParadasSubiendo[0]:
      PlantaDestino=ParadasSubiendo[0]
      Estado='Subiendo'
  if (len(ParadasBajando)>0):
    ParadasBajando.sort()
    ParadasBajando.reverse()
    if (Estado=='Bajando' or (len(ParadasSubiendo)==0))  and PlantaActual>ParadasBajando[0]:
      PlantaDestino=ParadasBajando[0]
      Estado='Bajando'
    
  #print 'paradas subiendo '+ str(ParadasSubiendo)+' paradas bajando '+str(ParadasBajando)    
  #print 'planta actual '+ str(PlantaActual)+' planta destino'+str(PlantaDestino)
  #print Estado
      
    
    
    
def Control():
  global Estado
  global PlantaActual
  global PlantaDestino
  global ParadasSubiendo
  global ParadasBajando
  while 1 :
    ActualizarMemorias()
    CiclosLibre=0
    while (len(ParadasBajando)==0) and (len(ParadasSubiendo)==0):
      CiclosLibre+=1
      Estado='Libre'
      iEstado.ActivaLeds(Estado)
      ActualizarMemorias()
      if CiclosLibre>5000 and PlantaActual>0:# Si lleva un rato libre y no esta abajo, baja a la planta 0
        ParadasBajando.append(0)
        PlantaDestino=0
    if (len(ParadasSubiendo)==0) and (len(ParadasBajando)>0):
      if ParadasBajando[0]>PlantaActual:
        PlantaDestino=ParadasBajando[0]
        ParadasSubiendo.append(ParadasBajando[0])
        Estado='Subiendo'
        while PlantaDestino in ParadasBajando:
          ParadasBajando.remove(PlantaDestino)
        #print 'planta destino ' + str(PlantaDestino)
        #while PlantaDestino > PlantaActual:
         # ActualizarMemorias()
          #Estado='Subiendo'
          #Planta('Subir')
    while (PlantaActual==0) and (len(ParadasSubiendo)>0):
      PlantaDestino=ParadasSubiendo[0]
      ActualizarMemorias()
      Estado='Subiendo'
      Planta('Subir')
    while (PlantaActual>0) and (len(ParadasBajando)>0)and (Estado=='Libre' or Estado=='Bajando'):
      if ParadasBajando[0]<PlantaActual:
        PlantaDestino=ParadasBajando[0]
        Estado='Bajando'
        Planta('Bajar')
      else:
        while  ParadasBajando[0]>=PlantaActual:
          ParadasSubiendo.append(ParadasBajando[0])
          ParadasBajando.remove(ParadasBajando[0])
      ActualizarMemorias()

    while (PlantaActual>0) and (len(ParadasSubiendo)>0)and (Estado=='Libre' or Estado=='Subiendo'):
      if ParadasSubiendo[0]>PlantaActual:
        PlantaDestino=ParadasSubiendo[0]
      ActualizarMemorias()
      Estado='Subiendo'
      Planta('Subir')

      
      
    
   
  
  

  

InicializaAscensor()

while 1:
  Control()


