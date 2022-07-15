# Pygame
import pygame
from pygame.locals import *

# PGU
from pgu import engine

# Mòduls propis
import conf
from boat import Boat
from background import Background
from garbage import Garbage
import itertools
from garbage import *
from functions import *

import random
import time
import csv
import numpy as np
import matplotlib.pyplot as plt


starttime = time.time()
grid_resolution = 10

# Classe joc (in englsih "game")
class Joc(engine.Game):

    # Initialize screen, pygame modules, clock... and states.
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE)
        self.crono = pygame.time.Clock()
        self._init_state_machine()
        

    # Creates and stores all states as attributes
    def _init_state_machine(self):
        self.jugant = Jugant(self)

    # Calls the main loop with the initial state.
    def run(self): 
        super().run(self.jugant, self.screen)

    # Tick is called once per frame. It shoud control timing.
    def tick(self):
        self.crono.tick(conf.fps)   # Limits the maximum FPS
    

    
# A state may subclass engine.State. Jugant in english "Player"
class Jugant(engine.State):
    # The init method should load data, etc.  The __init__ method
    # should do nothing but record the parameters.  If the init method
    # returns a value, it becomes the new state.
    def init(self):
        n=5
        self.grup = pygame.sprite.Group() # group of Sprites
        self.bg=Background('sea.png',[0,0])
        self.grup.add(self.bg)
        self.new=False
        Garbage.gen(1000)
        for i in range (len(Garbage.patches)):
            self.grup.add(Garbage.patches[i])

        imc = pygame.image.load('boat.png')
        self.g=Garbage('garbage.png', (1,1))
        
        #boat instance construction
        self.energy_left = 60
        self.b = Boat(imc, 20, 0,3,Garbage.patches)
        '''self.grup.add(self.b)'''
        
        self.all_sprites = self.grup
        self.wind = [
            [[1,1],[1,1],[1,1],[1,1],[1,1]],
            [[1,1],[1,1],[1,1],[1,1],[1,1]],
            [[1,1],[1,1],[1,1],[1,1],[1,1]],
            [[1,1],[1,1],[1,1],[1,1],[1,1]],
            [[1,1],[1,1],[1,1],[1,1],[1,1]],
        ]
        self.gyre2 = [
            [[1,1],[1,0],[1,1],[1,1],[0,1],[1,1],[1,1],[1,0],[1,1],[0,1]],
            [[1,-1],[1,-1],[1,0],[1,0],[1,1],[1,1],[1,1],[0,1],[1,1],[0,1]],
            [[0,-1],[1,-1],[1,-1],[1,-1],[1,0],[0,0],[-1,0],[-1,1],[-1,1],[-1,1]],
            [[1,-1],[0,-1],[0,-1],[-1,-1],[-1,0],[-1,-1],[-1,-1],[-1,-1],[-1,1],[-1,1]],
            [[0,-1],[0,-1],[-1,-1],[-1,-1],[-1,0],[-1,-1],[-1,-1],[-1,0],[-1,-1],[-1,-1]],
        ]
        
        self.combined_gyre = matrix_combinator(self.gyre2, self.gyre2)
        self.scaled_wind = [[[1,1],]*grid_resolution,]*grid_resolution
        self.scaled_gyre = gyre_generator(grid_resolution, self.combined_gyre)
        self.final_matrix = matrix_combinator(self.scaled_gyre, self.scaled_wind)
        self.heatmap_pos=[]
        self.counter_heatmap=time.time()
        self.heatmap_x=[]
        self.heatmap_y=[]
    def dynamicWind(self):
        wind = self.scaled_wind
        scale = 1
        for c,i in enumerate(wind):
            for e,j in enumerate(wind[c]):
                a = random.randint(-1*scale, 1*scale)
                b = random.randint(-1*scale, 1*scale)
                wind[c][e] = [a,b]
            
        self.scaled_wind = wind 

 
    # The paint method is called once.  If you call repaint(), it
    # will be called again.
    def paint(self,screen):
        screen.fill(conf.color_fons)        

    # Loop is called once a frame.  It should contain all the logic.
    # If the loop method returns a value it will become the new state.
    def loop(self):
        self.all_sprites.update(self.final_matrix)
        self.g.update(self.final_matrix)
        
        
        self.dynamicWind()
        #print(self.scaled_wind)
        self.final_matrix = matrix_combinator(self.scaled_gyre, self.scaled_wind)
        
        #a = self.final_matrix
       # print(numpy.shape(a))
        
       
        
        #print(self.final_matrix)
        

    # Update is called once a frame.  It should update the display.
    
    
                
    def update(self, screen):
        screen.fill(conf.color_fons)
        self.all_sprites.draw(screen)
        heatmap_counter=time.time()-starttime
               
        
        #Text overlay of garbage entities        
        color = (0, 0, 0)
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.Font('freesansbold.ttf', 20)
        # create a text surface object,
        # on which text is drawn on it.
        text = font.render('Garbage entities collected: {}'.format(self.b.collectedGarbage), False, color)  
        
        self.energy_left = 60-round((time.time()+self.b.collectedGarbage)-starttime)
        text2 = font.render('Energy capacity: {}'.format(self.energy_left), False, color)     
        
        text3 = font.render('Wind/water effect ratio: 50 % ', False, color)    
        # to the display surface object
        # at the center coordinate.
        screen.blit(text, (0,0)) 
        screen.blit(text2, (0,40)) 
        screen.blit(text3, (0,80)) 

        GG=Garbage('Garbage.png',(1,1))

        

        if self.g.new==True:
            self.g.gen_new(40)
            for i in range(len(self.g.patches_new)):
                self.grup.add(self.g.patches_new[i])

        


        for i in range (len(self.g.patches_new)):
            hits2=pygame.sprite.collide_mask(self.b,self.g.patches_new[i])
            if hits2 is not None:
                pygame.sprite.Sprite.kill(self.g.patches_new[i])
        
        if self.energy_left == 0:
            record = ['h_2', grid_resolution, self.b.collectedGarbage, 60]
            filename = "simulation_results.csv"
            with open(filename, 'a', newline='') as csvfile:  
                csvwriter = csv.writer(csvfile)  
                csvwriter.writerow(record)
            pygame.quit()
            quit()
        
        pygame.display.flip()
        
        
        if self.b.rect.right>1400:
            pygame.quit()
            quit()

        for i in range (len(Garbage.patches)):
            if Garbage.patches[i].disappear==True:
                pygame.sprite.Sprite.kill(Garbage.patches[i])

        if heatmap_counter>=22 and heatmap_counter<22.05:
            for i in range(len(Garbage.patches)):
                self.heatmap_pos.append((Garbage.patches[i].rect.x,Garbage.patches[i].rect.y))
            for i in range(len(self.g.patches_new)):
                self.heatmap_pos.append((self.g.patches_new[i].rect.x,self.g.patches_new[i].rect.y))
            for i in range(len(self.heatmap_pos)):
                self.heatmap_x.append(self.heatmap_pos[i][0]) 
                self.heatmap_y.append(self.heatmap_pos[i][1])
            
            x=np.array(self.heatmap_x)
            y=np.array(self.heatmap_y)
            
            print(self.heatmap_x,self.heatmap_y)
            
            
                


        
        

        

        

         
         
# Programa principal
def main():
    game = Joc()
    game.run()
    
# Crida el programa principal només si s'executa el mòdul:
#
#   python3 main_barra.py
#
# o bé
#
#   python3 -m main_barra
#
# Importa les funcions i les classes, però no executa el programa
# principal si s'importa el mòdul:
#
#   import joc
if __name__ == "__main__":
    main()
