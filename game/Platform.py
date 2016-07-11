# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Tran import Tran
from Akis import Akis
from Kang import Kang
from Collectable import Collectable
from Door import Door
import random
from MagicBox import MagicBox
from panda3d.core import BitMask32
from panda3d.core import Vec3
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode

class Platform(object):
  def __init__(self, render, world, loader, collectable, id, side, x, y, z):
    self.render = render
    self.world = world
    self.loader = loader
    self.collectable = collectable
    self.id = id
    self.side = side
    self.thing = -1
    
    if (self.side == 3):
      self.thing = random.randint(0, 1)
    elif (self.side > 3):
      self.thing = 2
    
    self.x = x
    self.y = y
    self.z = z
    self.createPlatform()
    self.zOffset = 1
    self.xYOffset = self.side/10*5
    
    if (self.thing > -1):
      self.addThing()
    
    if (self.collectable == 1):
      self.addItem()
  
  def createPlatform(self):
    platformShape = BulletBoxShape(Vec3(self.side, self.side, 0.2))
    platformNP = self.render.attachNewNode(BulletRigidBodyNode('Platform' + self.id))
    platformNP.node().addShape(platformShape)
    platformNP.setPos(self.x, self.y, self.z)
    platformNP.setCollideMask(BitMask32.allOn())
    self.world.attachRigidBody(platformNP.node())
    
    platformModel = self.loader.loadModel("models/stone-cube/stone")
    platformModel.setScale(self.side*2, self.side*2, 0.2*2)
    platformModel.setPos(self.x, self.y, self.z-0.2) # z is offset by 0.5
    platformModel.reparentTo(self.render)
    
  def addThing(self):
    if (self.thing == 0):
      Tran(self.render, self.world, self.id, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset)
    elif (self.thing == 1):
      Akis(self.render, self.world, self.id, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset)
    elif (self.thing == 2):
      Kang(self.render, self.world, self.id, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset)
    elif (self.thing == 3):
      Door(self.render, self.world, self.loader, self.id, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset)
    elif (self.thing == 4):
      MagicBox(self.render, self.world, self.loader, self.id, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset)
  
  def addItem(self):
    Collectable(self.render, self.world, self.loader, self.id, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset)
