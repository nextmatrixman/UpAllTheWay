# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Item import Item
from panda3d.core import BitMask32
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape
from panda3d.core import Vec3

class MagicBox(Item):
  def createItem(self):
    self.collisionShape = BulletBoxShape(Vec3(0.5, 0.6, 0.5))
    self.actor = BulletRigidBodyNode('MagicBox')
    self.actor.addShape(self.collisionShape)
    self.np = self.render.attachNewNode(self.actor)
    self.np.setCollideMask(BitMask32.allOff())
    self.np.setPos(self.x, self.y, self.z)
    self.world.attachRigidBody(self.actor)
    
    self.actorModelNP = self.loader.loadModel('models/magicbox/ToyBox.egg')
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(0.35)
    self.actorModelNP.setH(180)
    self.actorModelNP.setPos(0, 0, -0.5)
