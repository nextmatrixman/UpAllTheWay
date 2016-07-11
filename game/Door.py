# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Item import Item
from panda3d.core import BitMask32
from panda3d.bullet import BulletGhostNode, BulletBoxShape
from panda3d.core import Vec3

class Door(Item):
  def createItem(self):
    self.collisionShape = BulletBoxShape(Vec3(1.2, 0.2, 1.2))
    self.ghostNode = BulletGhostNode('Door' + self.id)
    self.ghostNode.addShape(self.collisionShape)
    self.np = self.render.attachNewNode(self.ghostNode)
    self.np.setCollideMask(BitMask32.allOff())
    self.np.setPos(self.x, self.y, self.z - 2.6)
    self.world.attachGhost(self.ghostNode)
    
    self.actorModelNP = self.loader.loadModel('models/door/Doorway.egg')
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(0.07)
    self.actorModelNP.setH(180)
    self.actorModelNP.setPos(0, 0, -0.2)
