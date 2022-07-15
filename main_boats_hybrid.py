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
        Garbage.gen(20)
        for i in range (len(Garbage.patches)):
            self.grup.add(Garbage.patches[i])

        imc = pygame.image.load('boat.png')
        self.g=Garbage('garbage.png', (1,1))
        self.initial_energy=60
        self.energy_left=60
        self.energy_left1=60
        self.energy_left2=60
        #boat instance construction
        
        self.b = Boat(imc, 20, 0,3,Garbage.patches)
        self.grup.add(self.b)
        
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
        
        self.dynamicWind()
        #print(self.scaled_wind)
        self.final_matrix = matrix_combinator(self.scaled_gyre, self.scaled_wind)
        
        #a = self.final_matrix
       # print(numpy.shape(a))
        
       
        
        #print(self.final_matrix)
        

    # Update is called once a frame.  It should update the display.
    
    
                
    def update(self, screen):
        timer=time.time()
        screen.fill(conf.color_fons)
        self.all_sprites.draw(screen)
        
        #Text overlay of garbage entities        
        color = (0, 0, 0)
        # create a font object.
        # 1st parameter is the font file
        # which is present in pygame.
        # 2nd parameter is size of the font
        font = pygame.font.SysFont('didot.ttc', 20)
        # create a text surface object,
        # on which text is drawn on it.
        text = font.render('Garbage entities collected: {}'.format(self.b.collectedGarbage), False, color)  
        

        
            



        self.energy_left = 60-round((time.time()+self.b.collectedGarbage)-starttime)
        if self.b.follow_currents==True:
            self.energy_left =self.energy_left+(0.2*round((time.time()+self.b.collectedGarbage)-starttime))/20

        print(time.time()-starttime)

        text2 = font.render('Energy capacity: {}'.format(self.energy_left), False, color)     

        text3 = font.render('Wind/water effect ratio: 50 % ', False, color)    
        # to the display surface object
        # at the center coordinate.
        screen.blit(text, (0,0)) 
        screen.blit(text2, (0,40)) 
        screen.blit(text3, (0,80)) 

        
        
        if self.b.new_one==True:            
            self.g.gen_new(2)
            self.grup.add(self.g.patches_new[-1])

        else:
            pass


        if self.b.results>30:
            record2 = [self.b.collectedGarbage, self.energy_left]
            filename2 = "energy_vs_trash.csv"
            with open(filename2, 'a', newline='') as csvfile:  
                csvwriter = csv.writer(csvfile)  
                csvwriter.writerow(record2)   
            self.b.results=0
        else:
            self.b.results+=1
             

        
        if self.energy_left <= 0:
            record = [self.b.collectedGarbage, timer-starttime]
            filename = "simulation_results.csv"
            with open(filename, 'a', newline='') as csvfile:  
                csvwriter = csv.writer(csvfile)  
                csvwriter.writerow(record)
            pygame.quit()
            quit()
        
        pygame.display.flip()
        

        for i in range (len(Garbage.patches)):
            if Garbage.patches[i].disappear==True:
                pygame.sprite.Sprite.kill(Garbage.patches[i])
        if timer-starttime>2:
            for i in range (len(Garbage.patches_new)):
                if Garbage.patches_new[i].disappear==True:
                    pygame.sprite.Sprite.kill(Garbage.patches_new[i])
         
         
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
