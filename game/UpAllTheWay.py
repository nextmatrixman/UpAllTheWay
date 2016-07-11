# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

import sys
from Platform import Platform
from Player import Player
from PlatformFactory import PlatformFactory
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import NodePath
from panda3d.core import PandaNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode

class UpAllTheWay(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    self.setupLights()
    self.setup()
    
    # Accept the control keys for movement and rotation
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f3', self.toggleDebug)
    self.accept('space', self.player.doJump)
    self.accept("a", self.player.setKey, ["left", True])
    self.accept("a-up", self.player.setKey, ["left", False])
    self.accept("d", self.player.setKey, ["right", True])
    self.accept("d-up", self.player.setKey, ["right", False])
    self.accept("w", self.player.setKey, ["forward", True])
    self.accept("w-up", self.player.setKey, ["forward", False])
    self.accept("s", self.player.setKey, ["reverse", True])
    self.accept("s-up", self.player.setKey, ["reverse", False])

    # Task
    taskMgr.add(self.update, 'updateWorld')

    base.setBackgroundColor(0.1, 0.1, 0.8, 1)
    base.setFrameRateMeter(True)
#     base.disableMouse()
    base.camera.setPos(self.player.getCharacterNP().getPos())
    base.camera.setHpr(self.player.getCharacterNP().getHpr())
    base.camera.lookAt(self.player.getCharacterNP())
    # Create a floater object. We use the "floater" as a temporary
    # variable in a variety of calculations.
    self.floater = NodePath(PandaNode("floater"))
    self.floater.reparentTo(render)
    
    # Add sound effects
    self.gameMusic = base.loader.loadSfx("sounds/level1.mp3")
    self.gameMusic.setLoop()
    self.gameMusic.setVolume(0.4)
    self.gameMusic.play()
    
    # Add environment
    self.env = self.loader.loadModel("models/env/PeachSky")
    self.env.reparentTo(render)
  
  def doExit(self):
    self.cleanup()
    sys.exit(1)

  def doReset(self):
    self.cleanup()
    self.setup()

  def toggleDebug(self):
    if self.debugNP.isHidden():
      self.debugNP.show()
    else:
      self.debugNP.hide()
              
  def update(self, task):
    dt = globalClock.getDt()
    self.player.move(dt)
    self.world.doPhysics(dt, 4, 1./240.)

    camvec = self.player.getCharacterNP().getPos() - base.camera.getPos()
    camvec.setZ(0)
    camdist = camvec.length()
    camvec.normalize()
    # If the camera is too far from Di, move it closer.
    if (camdist > 20.0):
      base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
      camdist = 20.0
    # If the camera is too close to Di, move it farther.
    if (camdist < 5.0):
      base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
      camdist = 5.0

    self.floater.setPos(self.player.getCharacterNP().getPos())
    self.floater.setZ(self.player.getCharacterNP().getZ() + 2.0)
    
    if (self.floater.getZ() > -20.0):
      base.camera.setZ(self.floater.getZ() + 20.0)
    else:
      base.camera.setZ(0.0)
    
    base.camera.lookAt(self.floater)
    
    if (self.player.getCharacterNP().getZ() < -60):
      self.player.resetCharacter()

    return task.cont

  def cleanup(self):
    self.world = None
    self.render.removeNode()

  def setupLights(self):
    # Light
    alight = AmbientLight('ambientLight')
    alight.setColor(Vec4(0.5, 0.5, 0.5, 1))
    alightNP = render.attachNewNode(alight)

    dlight = DirectionalLight('directionalLight')
    dlight.setDirection(Vec3(1, 1, -1))
    dlight.setColor(Vec4(0.7, 0.7, 0.7, 1))
    dlightNP = render.attachNewNode(dlight)

    self.render.clearLight()
    self.render.setLight(alightNP)
    self.render.setLight(dlightNP)

  def setup(self):
    # World
    self.debugNP = self.render.attachNewNode(BulletDebugNode('Debug'))
    self.debugNP.show()

    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
    self.world.setDebugNode(self.debugNP.node())

    # Floor
    Platform(self.render, self.world, self.loader, 0, str(-1), 2, 0, 0, -3)

    # Platforms
    PlatformFactory(self.render, self.world, self.loader, 30, 5)
    
    # Player character
    self.player = Player(self.render, self.world, 0, 0, 0)

game = UpAllTheWay()
game.run()
