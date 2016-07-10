# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Enemy import Enemy
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape

class Tran(Enemy):
  def createCharacter(self):
    self.shape = BulletBoxShape(Vec3(0.4, 0.4, 0.85))
    self.actor = BulletRigidBodyNode('Enemy' + self.id)
    self.actor.setMass(5.0)
    self.actorNP = self.render.attachNewNode(self.actor)
    self.actorNP.node().addShape(self.shape)
    self.actorNP.setPos(self.x, self.y, self.z)
    self.actorNP.setCollideMask(BitMask32.allOn())
    self.world.attachRigidBody(self.actorNP.node())
    
    self.actorModelNP = Actor('models/Scientist/Scientist.egg', {
                     'run': 'models/Scientist/Scientist-runaway.egg'})
    self.actorModelNP.reparentTo(self.actorNP)
    self.actorModelNP.setScale(0.3048)
    self.actorModelNP.setH(180)
    self.actorModelNP.setPos(0, 0, 0.27)