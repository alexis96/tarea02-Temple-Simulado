#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nreinas.py
------------

Ejemplo de las n_reinas con búsquedas locales

"""

__author__ = 'juliowaissman'


import blocales
from random import shuffle
from random import sample
from itertools import combinations
import time
import math
class ProblemaNreinas(blocales.Problema):
    """
    Las N reinas en forma de búsqueda local se inicializa como

    entorno = ProblemaNreinas(n) donde n es el número de reinas a colocar

    Por default son las clásicas 8 reinas.

    """
    def __init__(self, n=8):
        self.n = n

    def estado_aleatorio(self):
        estado = list(range(self.n))
        shuffle(estado)
        return tuple(estado)

    def vecinos(self, estado):
        """
        Generador vecinos de un estado, todas las 2 permutaciones

        @param estado: una tupla que describe un estado.

        @return: un generador de estados vecinos.

        """
        edo_lista = list(estado)
        for i, j in combinations(range(self.n), 2):
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]
            yield tuple(edo_lista)
            edo_lista[i], edo_lista[j] = edo_lista[j], edo_lista[i]

    def vecino_aleatorio(self, estado):
        """
        Genera un vecino de un estado intercambiando dos posiciones
        en forma aleatoria.

        @param estado: Una tupla que describe un estado

        @return: Una tupla con un estado vecino.

        """
        vecino = list(estado)
        i, j = sample(range(self.n), 2)
        vecino[i], vecino[j] = vecino[j], vecino[i]
        return tuple(vecino)

    def costo(self, estado):
        """
        Calcula el costo de un estado por el número de conflictos entre reinas

        @param estado: Una tupla que describe un estado

        @return: Un valor numérico, mientras más pequeño, mejor es el estado.

        """
        return sum([1 for (i, j) in combinations(range(self.n), 2)
                    if abs(estado[i] - estado[j]) == abs(i - j)])


def prueba_descenso_colinas(problema=ProblemaNreinas(8), repeticiones=10):
    """ Prueba el algoritmo de descenso de colinas con n repeticiones """
    print(" Prueba el algoritmo de descenso de colinas con n repeticiones")
    print("\n\n" + "intento".center(10) +
          "estado".center(60) + "costo".center(10))
    for intento in range(repeticiones):
        solucion = blocales.descenso_colinas(problema)
        print(str(intento).center(10) +
              str(solucion).center(60) +
              str(problema.costo(solucion)).center(10))


def prueba_temple_simulado(problema=ProblemaNreinas(8)):
    
    costos = [problema.costo(problema.estado_aleatorio())
                  for _ in range(10 * len(problema.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 2 * (maximo - minimo)
    calendarizador1 = (T_ini * math.exp(.0005 * -i) for i in range(int(1e10)))
    calendarizador2 = (T_ini/(i*math.log10(1 + i)+1) for i in range(int(1e10)))
    print("T_ini = {} \n".format(T_ini) )
    
    
    """ Prueba el algoritmo de temple simulado calendarizador None  """
    inicio_de_tiempo = time.time()
    solucion = blocales.temple_simulado(problema,tol=.01)
    print("\n\nTemple simulado con calendarización To/(1 + i).")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - inicio_de_tiempo
    print ("\nTomo {} segundos.".format(tiempo_transcurrido))
    
    """ Prueba el algoritmo de temple simulado calendarizador exp(-i) """
    inicio_de_tiempo = time.time()
    solucion = blocales.temple_simulado(problema,calendarizador=calendarizador1)
    print("\n\nTemple simulado con calendarización To * exp.")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - inicio_de_tiempo
    print ("\nTomo {} segundos.".format(tiempo_transcurrido))
    
    """ Prueba el algoritmo de temple simulado calendarizador log( i+1 ) """
    inicio_de_tiempo = time.time()
    solucion = blocales.temple_simulado(problema,calendarizador=calendarizador2)
    print("\n\nTemple simulado con calendarización To/(i*(log(1 + i)+1) .")
    print("Costo de la solución: ", problema.costo(solucion))
    print("Y la solución es: ")
    print(solucion)
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - inicio_de_tiempo
    print ("\nTomo {} segundos.".format(tiempo_transcurrido))
    
    
if __name__ == "__main__":
    """
    inicio_de_tiempo = time.time()
    prueba_descenso_colinas(ProblemaNreinas(128), 10)
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - inicio_de_tiempo
    print ("\nTomo {} segundos.".format(tiempo_transcurrido))
"""
    
    inicio_de_tiempo = time.time()
    prueba_temple_simulado(ProblemaNreinas(128))
    tiempo_final = time.time()
    tiempo_transcurrido = tiempo_final - inicio_de_tiempo
    print ("\nTomo {} segundos.".format(tiempo_transcurrido))
    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    #
    # ¿Cual es el máximo número de reinas que se puede resolver en
    # tiempo aceptable con el método de 10 reinicios aleatorios?
    #   
    #   El maximo numero de reinas que pude resolver fue de 128 en un 
    #   tiempo aprox de 1 hora 40 minutos. 
    #
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan? ¿Cual es el mejor ajuste para el temple simulado
    # y hasta cuantas reinas puede resolver en un tiempo aceptable?
    #  
    #   un tiempo aceptable fue con 300 reinas en 46 minutos 
    #   uno seria la temperatura inicial , otro seria la tolerancia dependiendo del problema.
    #   y la calendarizacion
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizar/probar diferentes metodos de
    # calendarización, prueba al menos otros dos métodos sencillos de
    # calendarización y ajusta los parámetros para que funcionen de la
    # mejor manera
    #
    # Escribe aqui tus conclusiones
    #
    # Obviamente para este problema el temple simulado fue mucho mejor los
    # el tiempo de 128 reinas no es tan aceptable pero como fui doblando el numero
    # con 64 dio muy poco y al doblarlo se fue hasta ese tiempo y ya no me regrese 
    #
    # para el temple simulado cambie la tol y bajo bastante los tiempos y me encontro
    # la solucion con costo cero y con la calendarizacion de T0 * exp(-.0005 * i) 
    # obtuve muy buenos resultados mejor que con los otros dos(default,logaritmicaModificada).
    #
