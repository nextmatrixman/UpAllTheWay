# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from direct.actor.Actor import Actor
from panda3d.core import BitMask32
from panda3d.bullet import BulletGhostNode, BulletSphereShape

class Item(object):
  def __init__(self, render, world, id, x, y, z):
    self.render = render
    self.world = world
    self.id = id
    self.x = x
    self.y = y
    self.z = z
    
    self.createItem()
