# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp

class Player(object):
  def __init__(self, render, world, x, y, z):
    self.render = render
    self.world = world
    self.x = x
    self.y = y
    self.z = z
    # Game state variables
    self.isMoving = False
    self.isJumping = False
    
    # This is used to store which keys are currently pressed.
    self.keyMap = {"left": 0, "right": 0, "forward": 0, "reverse": 0}
    
    # Defining sound effects
    self.jumpSound = base.loader.loadSfx("sounds/jumping.wav")
    self.runSound = base.loader.loadSfx("sounds/running.ogg")
    
    self.createPlayer()
    
  def createPlayer(self):
    h = 1.75
    w = 0.4
    shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

    self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
    #    self.character.setMass(1.0)
    self.characterNP = self.render.attachNewNode(self.character)
    self.characterNP.setPos(self.x, self.y, self.z)
    self.characterNP.setH(45)
    self.characterNP.setCollideMask(BitMask32.allOn())
    self.world.attachCharacter(self.character)

    self.actorNP = Actor('models/Bricker/Bricker3.egg', {
                     'run': 'models/Bricker/Bricker-run.egg',
                     'jump': 'models/Bricker/Bricker-jump.egg'})

    self.actorNP.reparentTo(self.characterNP)
    self.actorNP.setScale(0.3048)
    self.actorNP.setH(180)
    self.actorNP.setPos(self.x, self.y, self.z + 0.3)
    
  def setKey(self, key, value):
    self.keyMap[key] = value
  
  def doJump(self):
    self.character.setMaxJumpHeight(5.0)
    self.character.setJumpSpeed(8.5)
    self.character.doJump()
    self.actorNP.play("jump")
    self.jumpSound.play()
  
  def move(self, dt):
    speed = Vec3(0, 0, 0)
    omega = 0.0
    
    if self.keyMap["left"]:
      omega =  120.0
    if self.keyMap["right"]:
      omega = -120.0
    if self.keyMap["forward"]:
      speed.setY(4.0)
    if self.keyMap["reverse"]:
      speed.setY(-4.0)
      
    self.character.setAngularMovement(omega)
    self.character.setLinearMovement(speed, True)
    
    if self.keyMap["forward"] or self.keyMap["left"] or self.keyMap["right"] or self.keyMap["reverse"]:
      if self.isMoving is False:
        self.actorNP.loop("run")
        self.runSound.play()
        self.isMoving = True
    else:
      if self.isMoving:
        self.actorNP.stop()
        self.runSound.stop()
        self.isMoving = False
  
  def getCharacterNP(self):
    return self.characterNP