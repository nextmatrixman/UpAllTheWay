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
    self.lastSide = 2
    self.currentX = 0
    self.currentY = 0
    self.currentZ = -3
    self.zOffset = 3
    
    # call methods
    self.generatePlatform()
    self.insertCollectable()
    self.createPlatform()
    
  # Create the data that's needed to generate the platforms
  def generatePlatform(self):
    self.platformList = []
    
    for i in range(self.platformCount):
      self.currentSide = random.randint(1, 4)
      self.tempOffset = self.lastSide + self.currentSide + 2
      self.currentX = self.currentX + random.choice([self.tempOffset, 0, -self.tempOffset])
      self.currentY = self.currentY + self.tempOffset
      self.currentZ = self.currentZ + self.zOffset
      self.lastSide = self.currentSide
      
      # [collectable, side, x, y, z]
      self.platformList.append([0, self.currentSide, self.currentX, self.currentY, self.currentZ])
  
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
        Platform(self.render, self.world, self.loader, self.platformList[i][0], str(i), self.platformList[i][1], self.platformList[i][2], self.platformList[i][3], self.platformList[i][4])
