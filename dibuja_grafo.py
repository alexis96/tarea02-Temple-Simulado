#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dibuja_grafo.py
------------

Dibujar un grafo utilizando métodos de optimización

Estos métodos no son los que se utilizan en el dibujo de
gráfos por computadora pero da una idea de la utilidad de los métodos de
optimización en un problema divertido.

Para realizar este problema es necesario contar con el módulo Pillow
instalado (en Anaconda se instala por default. Si no se encuentr instalado, 
desde la termnal se puede instalar utilizando

$pip install pillow

"""

__author__ = 'Escribe aquí tu nombre'

import blocales
import random
import itertools
import math
import time
from PIL import Image, ImageDraw


class problema_grafica_grafo(blocales.Problema):

    """
    Clase para el dibujo de un grafo simple no dirigido

    """

    def __init__(self, vertices, aristas, dimension_imagen=400):
        """
        Un grafo se define como un conjunto de vertices, en forma de
        lista (no conjunto, el orden es importante a la hora de
        graficar), y un conjunto (tambien en forma de lista) de pares
        ordenados de vertices, lo que forman las aristas.

        Igualmente es importante indicar la resolución de la imagen a
        mostrar (por default de 400x400 pixeles).

        @param vertices: Lista con el nombre de los vertices.
        @param aristas: Lista con pares de vertices, los cuales
                        definen las aristas.
        @param dimension_imagen: Entero con la dimension de la imagen
                                 en pixeles (cuadrada por facilidad).

        """
        self.vertices = vertices
        self.aristas = aristas
        self.dim = dimension_imagen

    def estado_aleatorio(self):
        """
        Devuelve un estado aleatorio.

        Un estado para este problema de define como:

           s = [s(1), s(2),..., s(2*len(vertices))],
 
        en donde s(i) \in {10, 11, ..., self.dim - 10} es la posición
        en x del nodo i/2 si i es par, o la posicion en y
        del nodo (i-1)/2 si i es non y(osease las parejas (x,y)).

        @return: Una tupla con las posiciones (x1, y1, x2, y2, ...) de
                 cada vertice en la imagen.

        """
        return tuple(random.randint(10, self.dim - 10) for _ in
                     range(2 * len(self.vertices)))

    def vecino_aleatorio(self, estado, dmax=10):
        """
        Encuentra un vecino en forma aleatoria. En estea primera
        versión lo que hacemos es tomar un valor aleatorio, y
        sumarle o restarle x pixeles al azar.

        Este es un vecino aleatorio muy malo. Por lo que deberás buscar
        como hacer un mejor vecino aleatorio y comparar las ventajas de
        hacer un mejor vecino en el algoritmo de temple simulado.

        @param estado: Una tupla con el estado.
        @param dispersion: Un flotante con el valor de dispersión para el
                           vertice seleccionado

        @return: Una tupla con un estado vecino al estado de entrada.

        """
        vecino = list(estado)
        i = random.randint(0, len(vecino) - 1)
        vecino[i] = max(10,
                        min(self.dim - 10,
                            vecino[i] + random.randint(-dmax,  dmax)))
        return tuple(vecino)

        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # Por supuesto que esta no es la mejor manera de generar vecinos.
        #
        # Propon una manera alternativa de vecino_aleatorio y muestra que
        # con tu propuesta se obtienen resultados mejores o en menor tiempo

    def costo(self, estado):
        """
        Encuentra el costo de un estado. En principio el costo de un estado
        es la cantidad de veces que dos aristas se cruzan cuando se dibujan.

        Esto hace que el dibujo se organice para tener el menor numero
        posible de cruces entre aristas.

        @param: Una tupla con un estado

        @return: Un número flotante con el costo del estado.

        """

        # Inicializa fáctores lineales para los criterios más importantes
        # (default solo cuanta el criterio 1)
        K1 = 1.0
        K2 = 1.0
        K3 = 1.0
        K4 = 0.0

        # Genera un diccionario con el estado y la posición
        estado_dic = self.estado2dic(estado)

        return (K1 * self.numero_de_cruces(estado_dic) +
                K2 * self.separacion_vertices(estado_dic) +
                K3 * self.angulo_aristas(estado_dic) +
                K4 * self.criterio_propio(estado_dic))

        # Como podras ver en los resultados, el costo inicial
        # propuesto no hace figuras particularmente bonitas, y esto es
        # porque lo único que considera es el numero de cruces.
        #
        # Una manera de buscar mejores resultados es incluir en el
        # costo el angulo entre dos aristas conectadas al mismo
        # vertice, dandole un mayor costo si el angulo es muy pequeño
        # (positivo o negativo). Igualemtente se puede penalizar el
        # que dos nodos estén muy cercanos entre si en la gráfica
        #
        # Así, vamos a calcular el costo en trescuatro partes, una es el
        # numero de cruces (ya programada), otra la distancia entre
        # nodos (ya programada) y otro el angulo entre arista de cada
        # nodo (para programar). Por último, un criterio propio
        #
        # Al final, es necesario darle un peso lineal a cada uno de
        # los subcriterios.

    def numero_de_cruces(self, estado_dic):
        """
        Devuelve el numero de veces que dos aristas se cruzan en el grafo
        si se grafica como dice estado_dic

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        total = 0

        # Por cada arista en relacion a las otras (todas las combinaciones de
        # aristas)
        for (aristaA, aristaB) in itertools.combinations(self.aristas, 2):

            # Encuentra los valores de (x0A,y0A), (xFA, yFA) para los
            # vertices de una arista y los valores (x0B,y0B), (x0B,
            # y0B) para los vertices de la otra arista
            (x0A, y0A) = estado_dic[aristaA[0]]
            (xFA, yFA) = estado_dic[aristaA[1]]
            (x0B, y0B) = estado_dic[aristaB[0]]
            (xFB, yFB) = estado_dic[aristaB[1]]

            # Utilizando la clasica formula para encontrar
            # interseccion entre dos lineas cuidando primero de
            # asegurarse que las lineas no son paralelas (para evitar
            # la división por cero)
            den = (xFA - x0A) * (yFB - y0B) - (xFB - x0B) * (yFA - y0A)
            if den == 0:
                continue

            # Y entonces sacamos el largo del cruce, normalizado por
            # den. Esto significa que en 0 se encuentran en la primer
            # arista y en 1 en la última. Si los puntos de cruce de
            # ambas lineas se encuentran en valores entre 0 y 1,
            # significa que se cruzan
            puntoA = ((xFB - x0B) * (y0A - y0B) -
                      (yFB - y0B) * (x0A - x0B)) / den
            puntoB = ((xFA - x0A) * (y0A - y0B) -
                      (yFA - y0A) * (x0A - x0B)) / den
            if 0 < puntoA < 1 and 0 < puntoB < 1:
                total += 1
        return total

    def separacion_vertices(self, estado_dic, min_dist=50):
        """
        A partir de una posicion "estado" devuelve una penalización
        proporcional a cada par de vertices que se encuentren menos
        lejos que min_dist. Si la distancia entre vertices es menor a
        min_dist, entonces calcula una penalización proporcional a
        esta.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.  
        @param min_dist: Mínima distancia aceptable en pixeles entre dos vértices en
                           el dibujo.

        @return: Un número.

        """
        total = 0
        for (v1, v2) in itertools.combinations(self.vertices, 2):
            # Calcula la distancia entre dos vertices
            (x1, y1), (x2, y2) = estado_dic[v1], estado_dic[v2]
            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

            # Penaliza la distancia si es menor a min_dist
            if dist < min_dist:
                total += (1.0 - (dist / min_dist))
        return total

    def angulo_aristas(self, estado_dic):
        """
        A partir de una posicion "estado", devuelve una penalizacion
        proporcional a cada angulo entre aristas menor a pi/6 rad (30
        grados). Los angulos de pi/6 o mayores no llevan ninguna
        penalización, y la penalizacion crece conforme el angulo es
        menor.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # Agrega el método que considere el angulo entre aristas de
        # cada vertice. Dale diferente peso a cada criterio hasta
        # lograr que el sistema realice gráficas "bonitas"
        #
        # ¿Que valores de diste a K1, K2 y K3 respectivamente?
        #

        total = 0
         
        for v in self.vertices:
            lista_aristas = [arista for arista in self.aristas if v in arista]
            (x,y) = estado_dic[v]
            
            for a1,a2 in itertools.combinations(lista_aristas,2):
                # obtengo las coordenadas de los vertices diferentes
                (x1,y1) = estado_dic[a1[0]] if v in a1[1] else estado_dic[a1[1]]
                (x2,y2) = estado_dic[a2[0]] if v in a2[1] else estado_dic[a2[1]]
                # Saco los vectores directores
                (v1x,v1y) = ((x1-x),(y1-y))
                (v2x,v2y) = ((x2-x),(y2-y))
                # obtengo sus normas
                n1 = math.sqrt( (v1x)**2 + (v1y)**2 )
                n2 = math.sqrt( (v2x)**2 + (v2y)**2 )
                # obtengo el angulo
                angulo = math.degrees(math.acos((abs((v1x * v2x) + (v1y * v2y)))/(n1*n2)))
              
                
                if angulo < 30:
                    total += 1 - (angulo/30)
                
        return total

    def criterio_propio(self, estado_dic):
        """
        Implementa y comenta correctamente un criterio de costo que sea
        conveniente para que un grafo luzca bien.

        @param estado_dic: Diccionario cuyas llaves son los vértices
                           del grafo y cuyos valores es una tupla con
                           la posición (x, y) de ese vértice en el
                           dibujo.

        @return: Un número.

        """
        #######################################################################
        #                          20 PUNTOS
        #######################################################################
        # ¿Crees que hubiera sido bueno incluir otro criterio? ¿Cual?
        #
        # Desarrolla un criterio propio y ajusta su importancia en el
        # costo total con K4 ¿Mejora el resultado? ¿En que mejora el
        # resultado final?
        #
        #
        # ------ IMPLEMENTA AQUI TU CÓDIGO ------------------------------------
        #
        return 0

    def estado2dic(self, estado):
        """
        Convierte el estado en forma de tupla a un estado en forma de diccionario

        @param: Una tupla con las posiciones (x1, y1, x2, y2, ...)

        @return: Un diccionario cuyas llaves son el nombre de cada
                 arista y su valor es una tupla (x, y)

        """
        return {self.vertices[i]: (estado[2 * i], estado[2 * i + 1])
                for i in range(len(self.vertices))}

    def dibuja_grafo(self, estado=None, filename="prueba.gif"):
        """
        Dibuja el grafo utilizando el modulo pillow, donde estado es una
        lista de dimensión 2*len(vertices), donde cada valor es la
        posición en x y y respectivamente de cada vertice. dim es la
        dimensión de la figura en pixeles.

        Si no existe una posición, entonces se obtiene una en forma
        aleatoria.

        """
        if not estado:
            estado = self.estado_aleatorio()

        # Diccionario donde lugar[vertice] = (posX, posY)
        lugar = self.estado2dic(estado)

        # Abre una imagen y para dibujar en la imagen
        # Imagen en blanco
        imagen = Image.new('RGB', (self.dim, self.dim), (255, 255, 255))
        dibujar = ImageDraw.ImageDraw(imagen)

        for (v1, v2) in self.aristas:
            dibujar.line((lugar[v1], lugar[v2]), fill=(255, 0, 0))
        for v in self.vertices:
            dibujar.text(lugar[v], v, (0, 0, 0))

        imagen.save(filename)


def main():
    """
    La función principal

    """

    # Vamos a definir un grafo sencillo
    vertices_sencillo = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    aristas_sencillo = [('B', 'G'),
                        ('E', 'F'),
                        ('H', 'E'),
                        ('D', 'B'),
                        ('H', 'G'),
                        ('A', 'E'),
                        ('C', 'F'),
                        ('H', 'B'),
                        ('F', 'A'),
                        ('C', 'B'),
                        ('H', 'F'),
                        ('D','F')]
    dimension = 400
    
    

    # Y vamos a hacer un dibujo del grafo sin decirle como hacer para
    # ajustarlo.
    grafo_sencillo = problema_grafica_grafo(vertices_sencillo,
                                            aristas_sencillo,
                                            dimension)

    estado_aleatorio = grafo_sencillo.estado_aleatorio()
    costo_inicial = grafo_sencillo.costo(estado_aleatorio)
    grafo_sencillo.dibuja_grafo(estado_aleatorio, "prueba_inicial.gif")
    print("Costo del estado aleatorio: {}".format(costo_inicial))

    costos = [grafo_sencillo.costo(grafo_sencillo.estado_aleatorio())
                  for _ in range(10 * len(grafo_sencillo.estado_aleatorio()))]
    minimo,  maximo = min(costos), max(costos)
    T_ini = 2 * (maximo - minimo)
    #calendarizador1 = (T_ini * math.exp(.0005 * -i) for i in range(int(1e10)))
    calendarizador2 = (T_ini/(i*math.log10(1 + i)+1) for i in range(int(1e10)))
    print("T_ini = {} \n".format(T_ini) )
    
    # Ahora vamos a encontrar donde deben de estar los puntos
    t_inicial = time.time()
    solucion = blocales.temple_simulado(grafo_sencillo,calendarizador=calendarizador2,tol=.00001)
    t_final = time.time()
    costo_final = grafo_sencillo.costo(solucion)

    grafo_sencillo.dibuja_grafo(solucion, "prueba_final.gif")
    print("\nUtilizando la calendarización por default")
    print("Costo de la solución encontrada: {}".format(costo_final))
    print("Tiempo de ejecución en segundos: {}".format(t_final - t_inicial))

    ##########################################################################
    #                          20 PUNTOS
    ##########################################################################
    # ¿Que valores para ajustar el temple simulado son los que mejor
    # resultado dan?
    #
    # ¿Que encuentras en los resultados?, ¿Cual es el criterio mas importante?
    #
    # En general para obtener mejores resultados del temple simulado,
    # es necesario utilizar una función de calendarización acorde con
    # el metodo en que se genera el vecino aleatorio.  Existen en la
    # literatura varias combinaciones. Busca en la literatura
    # diferentes métodos de calendarización (al menos uno más
    # diferente al que se encuentra programado) y ajusta los
    # parámetros para que obtenga la mejor solución posible en el
    # menor tiempo posible.
    #
    # Escribe aqui tus conclusiones
    #
    # ------ IMPLEMENTA AQUI TU CÓDIGO ---------------------------------------
    #


if __name__ == '__main__':
    main()
