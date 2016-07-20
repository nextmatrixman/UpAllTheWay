# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

class Enemy(object):
  def __init__(self, render, world, loader, x, y, z):
    self.render = render
    self.world = world
    self.loader = loader
    self.x = x
    self.y = y
    self.z = z
    
    self.falling = base.loader.loadSfx("sounds/falling.mp3")
    
    self.createCharacter()
  
  def getActor(self):
    return self.actor
  
  def getNP(self):
    return self.np