# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Platform import Platform
import random

class PlatformFactory(object):
  def __init__(self, render, world, loader, platformCount, collectableCount):
    self.render = render
    self.world = world
    self.loader = loader
    self.platformCount = platformCount
    self.collectableCount = collectableCount
    self.zStep = 3
    self.generatePlatform()
    self.insertCollectable()
    self.createPlatform()
    
  # Create the data that's needed to generate the platforms
  def generatePlatform(self):
    self.platformList = []
    
    for i in range(self.platformCount):
      self.side = random.randint(1, 4)
      
      # [collectable, side, x, y]
      self.platformList.append([0, self.side, -(i*4+6), -(i*4+6)])
  
  def insertCollectable(self):
    if (self.collectableCount > 0):
      self.selected = random.randint(0, self.platformCount - 1)
      self.selectedList = [self.selected]
      
      for i in range(self.collectableCount - 1):
        while (self.selected in self.selectedList):
          self.selected = random.randint(0, self.platformCount - 1)
        self.selectedList.append(self.selected)
      
      for i in range(len(self.selectedList)):
        self.platformList[self.selectedList[i]][0] = 1
  
  # Create the platforms using the generated data
  # Platform(render, world, loader, collectable, id, side, x, y, z)
  def createPlatform(self):
    if (len(self.platformList) > 0):
      for i in range(len(self.platformList)):
        Platform(self.render, self.world, self.loader, self.platformList[i][0], str(i), self.platformList[i][1], self.platformList[i][2], self.platformList[i][3], i*self.zStep)