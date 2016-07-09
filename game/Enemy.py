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
    
    # Game state variables
    self.isMoving = False
    
    # Defining sound effects
    self.runSound = base.loader.loadSfx("sounds/running.ogg")
    
    self.createCharacter()
  
  def move(self, dt):
    print 'need AI'
    # when distance between player and this is < threashold
    # this.setPos(player pos)
    # this.lookAt player
    # isMoving = true
  
  def getCharacterNP(self):
    return self.characterNP