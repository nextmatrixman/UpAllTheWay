# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from panda3d.core import BitMask32
from panda3d.bullet import BulletSphereShape, BulletRigidBodyNode

class Ball(object):
  def __init__(self, render, world, player, id, x, y, z):
    self.render = render
    self.world = world
    self.player = player
    self.id = id
    self.x = x
    self.y = y
    self.z = z
    
    self.createItem()
  
  def createItem(self):
    self.collisionShape = BulletSphereShape(1)
    self.actor = BulletRigidBodyNode('Ball' + self.id)
    self.actor.addShape(self.collisionShape)
    self.np = self.render.attachNewNode(self.actor)
    self.np.setCollideMask(BitMask32.allOff())
    self.np.setPos(self.x, self.y, self.z + 0.5)
    self.world.attachRigidBody(self.actor)
    
    self.actorModelNP = self.loader.loadModel('models/sphere/ball.egg')
    self.actorModelNP.reparentTo(self.np)
    self.actorModelNP.setScale(0.07)
    self.actorModelNP.setPos(0, 0, -0.2)

  def getActor(self):
    return self.actor
  
  def getNP(self):
    return self.np