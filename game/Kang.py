# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Enemy import Enemy
from Data import Data
from Ball import Ball
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape

class Kang(Enemy):
  def createCharacter(self):
    self.shape = BulletBoxShape(Vec3(0.4, 0.4, 0.85))
    self.actor = BulletRigidBodyNode('Kang')
#     self.actor.setMass(5.0)
    self.np = self.render.attachNewNode(self.actor)
    self.np.node().addShape(self.shape)
    self.np.setPos(self.x, self.y, self.z)
    self.np.setCollideMask(BitMask32.allOn())
    self.world.attachRigidBody(self.np.node())
    
    self.actorModelNP = Actor('models/Eve/eve.egg.pz', {
                     'run': 'models/Eve/eve_run.egg.pz'})
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(0.3048)
    self.actorModelNP.setH(180)
    self.actorModelNP.setPos(0, 0, -0.82)
  
  def move(self, player):
    playerNP = player.getCharacterNP()
    self.np.lookAt(playerNP.getX(), playerNP.getY(), self.np.getZ())
    
  def drop(self, player):
    Data.balls.append(Ball(self.render, self.world, self.loader, player))
    self.falling.play()