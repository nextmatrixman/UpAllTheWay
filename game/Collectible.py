# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Item import Item
from panda3d.core import BitMask32
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from panda3d.core import Vec3

class Collectible(Item):
  def createItem(self):
    self.shape = BulletBoxShape(Vec3(0.5, 0.1, 0.5))
    self.actor = BulletRigidBodyNode('Collectible')
    self.actor.addShape(self.shape)
    self.np = self.render.attachNewNode(self.actor)
    self.np.setCollideMask(BitMask32.allOff())
    self.np.setPos(self.x + 0.7, self.y + 0.7, self.z)
    self.world.attachRigidBody(self.actor)
    
    self.actorModelNP = self.loader.loadModel('models/book/Book.egg')
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(1.0)
    self.actorModelNP.setH(180)
    self.actorModelNP.setPos(-0.3, 0, -0.5)
  
  def getActorModelNP(self):
    return self.actorModelNP

  def killNP(self):
    self.np.setPos(100, 100, 100)