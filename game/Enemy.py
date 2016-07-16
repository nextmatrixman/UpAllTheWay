# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

class Enemy(object):
  def __init__(self, render, world, id, x, y, z):
    self.render = render
    self.world = world
    self.id = id
    self.x = x
    self.y = y
    self.z = z
    
    self.createCharacter()
  
  def getActor(self):
    return self.actor
  
  def getNP(self):
    return self.np