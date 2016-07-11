# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Item import Item
from direct.actor.Actor import Actor
from panda3d.core import BitMask32
from panda3d.bullet import BulletGhostNode, BulletBoxShape
from panda3d.core import Vec3

class Collectable(Item):
  def createItem(self):
    self.collisionShape = BulletBoxShape(Vec3(0.5, 0.1, 0.5))
    self.ghostNode = BulletGhostNode('Collectable' + self.id)
    self.ghostNode.addShape(self.collisionShape)
    self.np = self.render.attachNewNode(self.ghostNode)
    self.np.setCollideMask(BitMask32.allOff())
    self.np.setPos(self.x, self.y, self.z-3.3)
    self.world.attachGhost(self.ghostNode)
    
    self.actorModelNP = Actor('models/book/Book.egg')
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(1.0)
    self.actorModelNP.setH(180)
    self.actorModelNP.setPos(-0.3, 0, -0.5)
