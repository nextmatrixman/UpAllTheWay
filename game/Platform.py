# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

from Data import Data
from Akis import Akis
from Kang import Kang
from Collectible import Collectible
from Door import Door
from MagicBox import MagicBox
from panda3d.core import BitMask32
from panda3d.core import Vec3
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletRigidBodyNode
from pandac.PandaModules import *

class Platform(object):
  def __init__(self, render, world, loader, collectible, overlay, side, x, y, z):
    self.render = render
    self.world = world
    self.loader = loader
    self.collectible = collectible
    self.overlay = overlay
    self.side = side
    self.thing = -1
    
    # SETUP DIRECTIONAL LIGHT
    self.directionalLight = DirectionalLight( "directionalLight" )
    self.directionalLight.setColor(Vec4( 1, 1, 1, 1 ))
    self.directionalLight.setDirection(Vec3(0, 0, -1))
    self.directionalLightNP = self.render.attachNewNode(self.directionalLight)
    
    if (self.side == 3):
      self.thing = 0
    elif (self.side > 3):
      self.thing = 1
    
    self.x = x
    self.y = y
    self.z = z
    self.createPlatform()
    self.zOffset = 1
    self.xYOffset = self.side/10*5
    
    if (self.thing > -1 and self.collectible < 2):
      self.addThing()
    
    self.addItem()
  
  def createPlatform(self):
    platformShape = BulletBoxShape(Vec3(self.side, self.side, 0.2))
    platformNP = self.render.attachNewNode(BulletRigidBodyNode('Platform'))
    platformNP.node().addShape(platformShape)
    platformNP.setPos(self.x, self.y, self.z)
    platformNP.setCollideMask(BitMask32.allOn())
    self.world.attachRigidBody(platformNP.node())
    
    if (self.overlay == 1):
      platformModel = self.loader.loadModel('models/tile-cube/tile')
      platformModel.setLight(self.directionalLightNP)
       
      # regular texture
      self.tex = self.loader.loadTexture('models/tile-cube/tile.png')
      platformModel.setTexture(self.tex, 1)
  
      # normal-map texture
      self.normal = self.loader.loadTexture('models/tile-cube/tile-normal.png')
      self.ts = TextureStage('ts')
      self.ts.setMode(TextureStage.MNormal)
      platformModel.setTexture(self.ts, self.normal)
      platformModel.setShaderAuto()
    else:
      platformModel = self.loader.loadModel("models/mosaic-cube/mosaic")
      platformModel.setLight(self.directionalLightNP)
       
      # regular texture
      self.tex = self.loader.loadTexture('models/mosaic-cube/mosaic.png')
      platformModel.setTexture(self.tex, 1)
  
      # normal-map texture
      self.normal = self.loader.loadTexture('models/mosaic-cube/mosaic-normal.png')
      self.ts = TextureStage('ts')
      self.ts.setMode(TextureStage.MNormal)
      platformModel.setTexture(self.ts, self.normal)
      platformModel.setShaderAuto()
    
    platformModel.setScale(self.side*2, self.side*2, 0.2*2)
    platformModel.setPos(self.x, self.y, self.z-0.2)
    platformModel.reparentTo(self.render)
    
  def addThing(self):
    if (self.thing == 0):
      Data.akises.append(Akis(self.render, self.world, self.loader, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset))
    elif (self.thing == 1):
      Data.kangs.append(Kang(self.render, self.world, self.loader, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset))
  
  def addItem(self):
    if (self.collectible == 1):
      Data.books.append(Collectible(self.render, self.world, self.loader, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset))
    elif (self.collectible == 2):
      Data.door.append(Door(self.render, self.world, self.loader, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset))
    elif (self.collectible == 3):
      Data.magicBox.append(MagicBox(self.render, self.world, self.loader, self.x + self.xYOffset, self.y + self.xYOffset, self.z + self.zOffset))
