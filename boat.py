
import pygame
pygame.init()
from garbage import *
from garbage import Garbage
import pygame 
import time
import csv

start=time.time()
class Boat(pygame.sprite.Sprite):
    def __init__(self, im, posv, velh, velv,trash):
        super().__init__()
        self.image =  im
        self.rect = im.get_rect()
        self.rect.top = posv
        self.rect.right = 300
        self.velh = velh
        self.velv = velv
        self.trash=trash
        self.bot=False
        self.top=False
        self.final_right=False
        self.final_right2=False
        self.time_counter = 0
        self.follow_currents = False
        self.counter_up = 0
        self.counter_down = 0
        self.direction = 0 # 0 = down, 1 = up
        self.sedeways_counter = 60
        self.starttime = time.time()
        self.new_one=False

        self.time_now=0
        self.results=0
        
        #Garbage counter
        self.collectedGarbage=0

    def collide(self):
        for i in range (len(Garbage.patches)):
            hits=pygame.sprite.collide_mask(self,Garbage.patches[i])
            if hits!=None and Garbage.patches[i].disappear == False:
                self.collectedGarbage +=1
                self.follow_currents = True
                self.time_counter = 0
                
                Garbage.patches[i].disappear=True

        timer=time.time()
        if timer-start>2:
            for i in range(len(Garbage.patches_new)):
                hits2=pygame.sprite.collide_mask(self,Garbage.patches_new[i])
                if hits2!=None and Garbage.patches_new[i].disappear == False:
                    self.collectedGarbage +=1
                    self.follow_currents = True
                    self.time_counter = 0
                    Garbage.patches_new[i].disappear=True
                                


        '''for i in range (len(self.g.patches_new)):
            hits2=pygame.sprite.collide_mask(self.b,self.g.patches_new[i])
            if hits2!=None and self.g.patches_new[i].disappear==False:
                self.g.patches_new[i].disappear=True
            if self.g.patches_new[i].disappear==True:
                self.b.follow_currents=True
                pygame.sprite.Sprite.kill(self.g.patches_new[i])
                self.g.patches_new[i].disappear=False'''


        time_elapsed = round(time.time()-self.starttime)
        record = ['whatever', 100, self.collectedGarbage, time_elapsed]
        filename = "over_time.csv"
        with open(filename, 'a', newline='') as csvfile:  
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerow(record)
        return True

    def update2(self,matrix):
        self.collide()
        vert=3
        hor=3
        height=pygame.display.get_surface().get_height()
        width=pygame.display.get_surface().get_width()
        
        if self.rect.left+200 >= width:
            self.bot=False
            self.top=False
            self.velv=0
            self.velh=0
        else:
            if self.rect.top+150 >= height:
                self.bot=True
                self.top=False
                self.direction = 1
            if self.rect.top < 10:
                self.top=True
                self.bot=False
                self.direction = 0
            
        if self.bot==True:
            self.counter_down = 0
            self.velv=0
            self.velh=hor
             
            if self.counter_up < self.sedeways_counter:
                self.counter_up += 1
            else:
                self.velv=-vert
                self.velh=0
                self.bot=False
        
        elif self.top==True:
            self.counter_up = 0
            self.velv=0
            self.velh=hor

            if self.counter_down < self.sedeways_counter:
                self.counter_down += 1
            else:
                self.velv=vert
                self.velh=0
                self.top=False
        else:
            pass
                
        self.rect.left = self.rect.left + self.velh
        self.rect.top = self.rect.top + self.velv

        if self.time_now<30:
                self.time_now+=1
                self.new_one=False
                self.collide()
        else:
            
            self.new_one=True
            self.time_now=0
            self.collide()
  
    #def routePlanneralternative
    def update(self, final_matrix):
        self.collide()
        if  not self.follow_currents:
            self.update2(final_matrix)
            
           
        else:
            self.rect.left = self.rect.left + self.velh
            self.rect.top = self.rect.top + self.velv
            
            
            self.collide()
        
            height=pygame.display.get_surface().get_height()
            width=pygame.display.get_surface().get_width()
            
            x_index = round(self.rect.left/(width/len(final_matrix[0])))
            y_index = round(self.rect.top/(height/len(final_matrix)))
            
            if self.time_now<30:
                self.time_now+=1
                self.new_one=False
                self.collide()
            else:
                
                self.new_one=True
                self.time_now=0
                self.collide()
            
            self.velh = final_matrix[y_index][x_index][0]
            self.velv = final_matrix[y_index][x_index][1]
            
                    
            self.rect.left = self.rect.left + self.velh
            self.rect.top = self.rect.top + self.velv
            
            if self.time_counter < 60:
                self.time_counter += 1
            else:
                self.follow_currents = False
                if self.direction == 0:
                    self.top=True
                    self.bot=False
                    self.counter_down = self.sedeways_counter
                else:
                    self.top=False
                    self.bot=True
                    self.counter_up = self.sedeways_counter

            