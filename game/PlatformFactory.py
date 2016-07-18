# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Platform import Platform
from Data import Data
import random

class PlatformFactory(object):
  def __init__(self, render, world, loader):
    self.render = render
    self.world = world
    self.loader = loader
    self.lastSide = 2
    self.zOffset = 3
    
    # setup level 1
    self.generatePlatform(Data.platformCount1, 1, 0, 0, -3)
    self.insertCollectable(Data.platformCount1, Data.collectibleTotal1)
    self.addLastPlatform(2, 1)
    self.createPlatform()
    # setup level 2
    self.generatePlatform(Data.platformCount2, 2, 100, 100, -3)
    self.insertCollectable(Data.platformCount2, Data.collectibleTotal2)
    self.addLastPlatform(3, 2)
    self.createPlatform()
    
  # Create the data that's needed to generate the platforms
  def generatePlatform(self, platformCount, overlay, x, y, z):
    self.platformList = []
    self.currentX = x
    self.currentY = y
    self.currentZ = z
    
    for i in range(platformCount - 1):
      self.currentSide = random.randint(1, 4)
      self.tempOffset = self.lastSide + self.currentSide + 2
      self.currentX = self.currentX + random.choice([self.tempOffset, 0, -self.tempOffset])
      self.currentY = self.currentY + self.tempOffset
      self.currentZ = self.currentZ + self.zOffset
      self.lastSide = self.currentSide
       
      # [collectible, overlay, side, x, y, z]
      self.platformList.append([0, overlay, self.currentSide, self.currentX, self.currentY, self.currentZ])
      
  def insertCollectable(self, platformCount, collectibleTotal):
    if (collectibleTotal > 0):
      self.selected = random.randint(0, platformCount - 2)
      self.selectedList = [self.selected]
      
      for i in range(collectibleTotal - 1):
        while (self.selected in self.selectedList):
          self.selected = random.randint(0, platformCount - 2)
        self.selectedList.append(self.selected)
      
      for i in range(len(self.selectedList)):
        self.platformList[self.selectedList[i]][0] = 1
  
  def addLastPlatform(self, lastItem, overlay):
    self.currentSide = 3
    self.tempOffset = self.lastSide + self.currentSide + 2
    self.currentX = self.currentX + random.choice([self.tempOffset, 0, -self.tempOffset])
    self.currentY = self.currentY + self.tempOffset
    self.currentZ = self.currentZ + self.zOffset
    
    self.platformList.append([lastItem, overlay, self.currentSide, self.currentX, self.currentY, self.currentZ])
  
  # Create the platforms using the generated data
  # Platform(render, world, loader, collectible, overlay, side, x, y, z)
  def createPlatform(self):
    if (len(self.platformList) > 0):
      for i in range(len(self.platformList)):
        Platform(self.render, self.world, self.loader, self.platformList[i][0], self.platformList[i][1], self.platformList[i][2], self.platformList[i][3], self.platformList[i][4], self.platformList[i][5])
