# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from panda3d.core import BitMask32
from panda3d.core import Vec3
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode

class Platform(object):
  def __init__(self, render, world, loader, id, side, x, y, z):
    self.render = render
    self.world = world
    self.loader = loader
    self.id = id
    self.side = side
    self.x = x
    self.y = y
    self.z = z
    self.createPlatform()
    
  def createPlatform(self):
    platformShape = BulletBoxShape(Vec3(self.side, self.side, 0.2))
    platformNP = self.render.attachNewNode(BulletRigidBodyNode('Platform' + str(self.id)))
    platformNP.node().addShape(platformShape)
    platformNP.setPos(self.x, self.y, self.z)
    platformNP.setCollideMask(BitMask32.allOn())
    self.world.attachRigidBody(platformNP.node())
    platformModel = self.loader.loadModel("models/stone-cube/stone")
    platformModel.setScale(self.side*2, self.side*2, 0.2*2)
    platformModel.setPos(self.x, self.y, self.z-0.2) # z is offset by 0.5
    platformModel.reparentTo(self.render)
  
  def toString(self):
    print id + ": " + self.side + ", (" + self.x + ", " + self.y + ", " + self.z + ")"
    