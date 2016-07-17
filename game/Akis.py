# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Enemy import Enemy
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import BitMask32
from panda3d.bullet import BulletRigidBodyNode, BulletBoxShape

class Akis(Enemy):
  def createCharacter(self):
    self.shape = BulletBoxShape(Vec3(0.4, 0.4, 0.85))
    self.actor = BulletRigidBodyNode('Akis')
    self.actor.setMass(5.0)
    self.np = self.render.attachNewNode(self.actor)
    self.np.node().addShape(self.shape)
    self.np.setPos(self.x, self.y, self.z)
    self.np.setCollideMask(BitMask32.allOn())
    self.world.attachRigidBody(self.np.node())
    
    self.actorModelNP = Actor('models/SecurityGuard/SecurityGuard.egg', {
                     'run': 'models/SecurityGuard/SecurityGuard-run.egg'})
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(0.3048)
    self.actorModelNP.setH(180)
    self.actorModelNP.setPos(0, 0, 0.27)
  
  def move(self, player):
    playerNP = player.getCharacterNP()
    self.np.lookAt(playerNP.getX(), playerNP.getY(), self.np.getZ())
    vec = playerNP.getPos() - self.np.getPos()
    vec.setZ(0)
    dist = vec.length()
    vec.normalize()
    self.np.setPos(self.np.getPos() + vec * dist * 0.01)