# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Item import Item
from direct.actor.Actor import Actor
from panda3d.core import BitMask32
from panda3d.bullet import BulletGhostNode, BulletSphereShape

class Collectable(Item):
  def createItem(self):
    self.collisionShape = BulletSphereShape(0.35)
    self.ghostNode = BulletGhostNode('Collectable' + self.id)
    self.ghostNode.addShape(self.collisionShape)
    self.np = self.render.attachNewNode(self.ghostNode)
    self.np.setCollideMask(BitMask32.allOff())
    self.np.setPos(self.x, self.y, self.z-3.5)
    self.world.attachGhost(self.ghostNode)
    
    self.actorModelNP = Actor('models/sphere/ball.egg')
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(0.34)
    self.actorModelNP.setH(180)
    self.actorModelNP.setPos(0, 0, 0)
