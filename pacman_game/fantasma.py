import cocos
import pyglet
import random
import sys
import math
import pacman
import posiciones
import pathfantasma
#from pacman import *
from enemigo import *

class Fantasma(Enemigo):
    def __init__(self,laberinto):
        self.atlas=pyglet.image.load("resources/fantasma.png")
        self.animaciones=pyglet.image.ImageGrid(self.atlas,1,16)
        self.frame=0
        self.sprite=cocos.sprite.Sprite(self.animaciones[self.frame])
        self.laberinto=laberinto
        self.movimientos=[[60,0],[0,60],[-60,0],[0,-60]]
        self.fantasma_x=3
        self.fantasma_y=4
        self.cont=0

    def animar(self,px,py):
        self.frame+=1
        self.frame%=2
        self.sprite.image=self.animaciones[self.frame]
        self.mover_aleatorio()

    def movimiento_posible(self,movimiento):
        self.sprite.x+=movimiento[0]
        self.sprite.y+=movimiento[1]
        if self.laberinto.colision(self):
            i,j=self.laberinto.en_celda(self.sprite.x,self.sprite.y)
            objeto=self.laberinto.objeto_en_celda(i,j)
            self.sprite.x-=movimiento[0]
            self.sprite.y-=movimiento[1]
            if isinstance(objeto,pacman.Pacman):
                print("te pille")
                objeto.home()
                return True
            else:
                return False
        else:
            self.sprite.x-=movimiento[0]
            self.sprite.y-=movimiento[1]
            return True

    def mover_aleatorio(self):
        #self.fantasma_posicion.append(self.sprite.x)
        #self.fantasma_posicion.append(self.sprite.y)
        #pac=pacman.Pacman(self.laberinto)
        #posiciones.Posiciones_Busqueda(self.fantasma_posicion,pac.pacman_posicion)
        
        aux_pos_pacman=[]
        
        if(len(posiciones.aux_pacman_coord)!=0):
            aux_pos_pacman+=posiciones.aux_pacman_coord
            pathfantasma.coordenadas=[]
            if(pathfantasma.resolverpath(self.fantasma_x, self.fantasma_y,aux_pos_pacman[0],aux_pos_pacman[1])):
                print("\nPATH RESULTANTE ")
                pathfantasma.coordenadas.reverse()
                print("CORD PACMAN",pathfantasma.coordenadas)
                print("POSICION FANTASMA",aux_pos_pacman[0],",",aux_pos_pacman[1])
                pathfantasma.coordenadas
                largo=len(pathfantasma.coordenadas)
                for i in range(len(pathfantasma.solucion)):
                    for j in range(len(pathfantasma.solucion[i])):
                        if(pathfantasma.solucion[i][j]==1):
                            print("o",end=" ")
                        else:
                            print(".",end=" ")
                    print(" ")
                pathfantasma.solucion = [[0]*9 for _ in range(9)]
                
                
                movimiento=[]
                if pathfantasma.coordenadas[0]=="arriba":
                    movimiento.append(0)
                    movimiento.append(60)
                if pathfantasma.coordenadas[0]=="abajo":
                    movimiento.append(0)
                    movimiento.append(-60)
                if pathfantasma.coordenadas[0]=="derecha":
                    movimiento.append(60)
                    movimiento.append(0)
                if pathfantasma.coordenadas[0]=="izquierda":
                    movimiento.append(-60)
                    movimiento.append(0)
                if(self.movimiento_posible(movimiento)):
                    self.fantasma_x,self.fantasma_y=self.mover(movimiento)
                    
                    return
                
            else:
                print("______ SIN SOLUCION EN PACMAN ________\n")
            
            print("LARG",largo)
           
           
        

    def mover(self,movimiento):
        p=self.laberinto.en_celda(self.sprite.x,self.sprite.y)
        self.laberinto.mapa[p[0]][p[1]]=0
        self.sprite.x+=movimiento[0]
        self.sprite.y+=movimiento[1]
        p=self.laberinto.en_celda(self.sprite.x,self.sprite.y)
        self.laberinto.mapa[p[0]][p[1]]=self
        self.fantasma_x=p[0]
        self.fantasma_y=p[1]
        return self.fantasma_x,self.fantasma_y
