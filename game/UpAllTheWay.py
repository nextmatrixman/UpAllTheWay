# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

import sys
from Platform import Platform
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import BitMask32
from panda3d.core import NodePath
from panda3d.core import PandaNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from panda3d.bullet import BulletCapsuleShape
from panda3d.bullet import BulletCharacterControllerNode
from panda3d.bullet import ZUp

class UpAllTheWay(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    self.setupLights()
    
    # This is used to store which keys are currently pressed.
    self.keyMap = {"left": 0, "right": 0, "forward": 0, "reverse": 0}
    
    # Accept the control keys for movement and rotation
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f3', self.toggleDebug)
    self.accept('space', self.doJump)
    self.accept("a", self.setKey, ["left", True])
    self.accept("a-up", self.setKey, ["left", False])
    self.accept("d", self.setKey, ["right", True])
    self.accept("d-up", self.setKey, ["right", False])
    self.accept("w", self.setKey, ["forward", True])
    self.accept("w-up", self.setKey, ["forward", False])
    self.accept("s", self.setKey, ["reverse", True])
    self.accept("s-up", self.setKey, ["reverse", False])
    
    # Game state variables
    self.isMoving = False
    self.isJumping = False

    # Task
    taskMgr.add(self.update, 'updateWorld')

    self.setup()
    base.setBackgroundColor(0.1, 0.1, 0.8, 1)
    base.setFrameRateMeter(True)
    base.disableMouse()
    base.camera.setPos(self.characterNP.getPos())
    base.camera.setHpr(self.characterNP.getHpr())
    base.camera.lookAt(self.characterNP)
    # Create a floater object. We use the "floater" as a temporary
    # variable in a variety of calculations.
    self.floater = NodePath(PandaNode("floater"))
    self.floater.reparentTo(render)
    
    # Add sound effects
    self.gameMusic = base.loader.loadSfx("sounds/level1.mp3")
    self.jumpSound = base.loader.loadSfx("sounds/jumping.wav")
    self.runSound = base.loader.loadSfx("sounds/running.ogg")
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

  def doJump(self):
    self.character.setMaxJumpHeight(5.0)
    self.character.setJumpSpeed(8.5)
    self.character.doJump()
    self.actorNP.play("jump")
    self.jumpSound.play()

  # Records the state of the keys
  def setKey(self, key, value):
    self.keyMap[key] = value
  
  def move(self, dt):
    speed = Vec3(0, 0, 0)
    omega = 0.0
    
    if self.keyMap["left"]:
      omega =  120.0
    if self.keyMap["right"]:
      omega = -120.0
    if self.keyMap["forward"]:
      speed.setY(4.0)
    if self.keyMap["reverse"]:
      speed.setY(-4.0)
      
    self.character.setAngularMovement(omega)
    self.character.setLinearMovement(speed, True)
    
    if self.keyMap["forward"] or self.keyMap["left"] or self.keyMap["right"] or self.keyMap["reverse"]:
      if self.isMoving is False:
        self.actorNP.loop("run")
        self.runSound.play()
        self.isMoving = True
    else:
      if self.isMoving:
        self.actorNP.stop()
        self.runSound.stop()
        self.isMoving = False
              
  def update(self, task):
    dt = globalClock.getDt()
    self.move(dt)
    self.world.doPhysics(dt, 4, 1./240.)

    # If the camera is too far from Di, move it closer.
    # If the camera is too close to Di, move it farther.
    camvec = self.characterNP.getPos() - base.camera.getPos()
    camvec.setZ(0)
    camdist = camvec.length()
    camvec.normalize()
    if (camdist > 15.0):
      base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
      camdist = 15.0
    if (camdist < 5.0):
      base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
      camdist = 5.0

    self.floater.setPos(self.characterNP.getPos())
    self.floater.setZ(self.characterNP.getZ() + 2.0)
    if (self.floater.getZ() > -15.0):
      base.camera.setZ(self.floater.getZ() + 15.0)
    else:
      base.camera.setZ(0.0)
    base.camera.lookAt(self.floater)

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
    floor = Platform(self.render, self.world, self.loader, -1, 5, 0, 0, -3)

    # Character
    h = 1.75
    w = 0.4
    shape = BulletCapsuleShape(w, h - 2 * w, ZUp)

    self.character = BulletCharacterControllerNode(shape, 0.4, 'Player')
    #    self.character.setMass(1.0)
    self.characterNP = self.render.attachNewNode(self.character)
    self.characterNP.setPos(-2, 0, 14)
    self.characterNP.setH(45)
    self.characterNP.setCollideMask(BitMask32.allOn())
    self.world.attachCharacter(self.character)

    self.actorNP = Actor('models/Bricker/Bricker3.egg', {
                     'run' : 'models/Bricker/Bricker-run.egg',
                     'jump' : 'models/Bricker/Bricker-jump.egg'})

    self.actorNP.reparentTo(self.characterNP)
    self.actorNP.setScale(0.3048)
    self.actorNP.setH(180)
    self.actorNP.setPos(0, 0, 0.3)

    for i in range(10):
      platform = Platform(self.render, self.world, self.loader, i, 3, -(i*2+4), -(i*2+4), i*3)

game = UpAllTheWay()
game.run()
