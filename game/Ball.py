# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from panda3d.core import BitMask32
from panda3d.bullet import BulletSphereShape, BulletRigidBodyNode

class Ball(object):
  def __init__(self, render, world, loader, player):
    self.render = render
    self.world = world
    self.loader = loader
    self.player = player
    self.dropHeight = 5
    self.createItem()
  
  def createItem(self):
    self.collisionShape = BulletSphereShape(0.5)
    self.actor = BulletRigidBodyNode('Ball')
    self.actor.setMass(5.0)
    self.actor.addShape(self.collisionShape)
    self.np = self.render.attachNewNode(self.actor)
    self.np.setCollideMask(BitMask32.allOff())
    
    self.x = self.player.getCharacterNP().getX()
    self.y = self.player.getCharacterNP().getY()
    self.z = self.player.getCharacterNP().getZ() + self.dropHeight
    
    self.np.setPos(self.x, self.y, self.z)
    self.world.attachRigidBody(self.actor)
    
    self.actorModelNP = self.loader.loadModel('models/sphere/ball.egg')
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(0.5)
    self.actorModelNP.setPos(0, 0, 0)

  def getActor(self):
    return self.actor
  
  def getNP(self):
    return self.np
