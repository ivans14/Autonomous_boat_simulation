import pygame
import numpy
from pygame.locals import *

class Garbage(pygame.sprite.Sprite):
    def __init__(self, image_file,position):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.disappear=False
        self.velh = 0
        self.velv = 0
        self.skip_counter = 0
        self.patches_new=[]
        

    def gen(n):
        
        coordx=numpy.random.randint(400,1000,size=n)
        coordy=numpy.random.randint(100,700,size=n)
        patches=[]
        for i in range(n-1):
            x=coordx[i]
            y=coordy[i]
            a=Garbage('garbage.png', (x,y))
            patches.append(a)
        Garbage.patches=patches
    def gen_new(self,n):
        coord=numpy.random.randint(100,800,size=n)
        for i in range(n-1):
            if coord[i]<500:
                x=coord[i]*1.1
            elif coord[i]>=500:
                x=coord[i]*1.6
            y=coord[i+1]-100
            a=Garbage('garbage.png', (x,y))
            self.patches_new.append(a)
        Garbage.patches_new=self.patches_new
  
    def update(self, final_matrix):
        if self.skip_counter < 1:
            self.skip_counter += 1
        else:
            self.skip_counter = 0
            height=pygame.display.get_surface().get_height()
            width=pygame.display.get_surface().get_width()
        
            x_index = int((self.rect.left+(self.rect.w/2))/(width/len(final_matrix[0])))
            y_index = int((self.rect.top+(self.rect.h/2))/(height/len(final_matrix)))
        
            self.velh = final_matrix[y_index][x_index][0]
            self.velv = final_matrix[y_index][x_index][1]
            
            self.rect.left = self.rect.left + self.velh
            self.rect.top = self.rect.top + self.velv

        

        