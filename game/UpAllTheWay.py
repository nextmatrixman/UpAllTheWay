# Game Name: Up all the Way
# Author: Di Shen
# CS594 Summer 2016

import sys
from Platform import Platform
from Data import Data
from Player import Player
from PlatformFactory import PlatformFactory
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight
from panda3d.core import Vec3
from panda3d.core import Vec4
from panda3d.core import NodePath
from panda3d.core import PandaNode
from panda3d.core import TextNode
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode
from direct.gui.OnscreenText import OnscreenText

class UpAllTheWay(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)

    self.platformCount = 15
    self.collectibleCounter = 0
    self.collectibleTotal = 5
    self.frameRate = 60
    self.maxTime = 7200
    self.contactDistance = 1
    self.detectDistance = 4
    
    self.setupLights()
    self.setup()
    
    # Accept the control keys for movement and rotation
    self.accept('escape', self.doExit)
    self.accept('r', self.doReset)
    self.accept('f1', self.toggleHelp)
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
    
    # Add environment
    self.env = self.loader.loadModel("models/env/PeachSky")
    self.env.reparentTo(render)
    
    # Add text
    self.collectibleIndicator = "Level 1: collectible items - " + str(self.collectibleCounter) + "/" + str(self.collectibleTotal)
    self.timeIndicator = "Time left - " + str(self.maxTime/self.frameRate)
    self.helpIndicator = "[F1] - Help, [1] - level 1, [2] - level 2"
    self.inst1 = self.addInstructions(0.06, self.collectibleIndicator)
    self.inst2 = self.addInstructions(0.12, self.timeIndicator)
    self.inst3 = self.addInstructions(0.18, self.helpIndicator)
    
    # Help variable
    self.helpOn = False
  
  # Function to put instructions on the screen.
  def addInstructions(self, pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), 
                        scale=.05, shadow=(0, 0, 0, 1), parent = base.a2dTopLeft, 
                        pos=(0.04, -pos - 0.02), align = TextNode.ALeft)
  
  def addVictoryText(self, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), 
                        scale=.25, shadow=(0, 0, 0, 1), parent = base.a2dTopLeft, 
                        pos=(0.75, -1), align = TextNode.ALeft)
  
  def doExit(self):
    self.cleanup()
    sys.exit(1)

  def doReset(self):
    self.cleanup()
    self.setup()

  def toggleHelp(self):
    if (self.helpOn == False):
      self.helpOn = True
      taskMgr.remove('updateWorld')
      self.inst1.destroy()
      self.inst2.destroy()
      self.inst3.destroy()
      self.inst1 = self.addInstructions(0.06, "Game paused")
      self.inst2 = self.addInstructions(0.12, "")
      self.inst3 = self.addInstructions(0.18, "STORY")
      self.inst4 = self.addInstructions(0.24, "Di is a CSULA CS graduate student fighting for his CS MS degree.")
      self.inst5 = self.addInstructions(0.30, "He's on his journey to gain his degree, but it will not be easy.")
      self.inst6 = self.addInstructions(0.36, "He needs to go upward and collect books as knowledge, and avoid professor attacks.")
      self.inst7 = self.addInstructions(0.42, "Eventually he will reach a new height in life and collect his diploma in a magic box!")
      self.inst8 = self.addInstructions(0.48, "")
      self.inst9 = self.addInstructions(0.54, "ACTION KEYS")
      self.inst10 = self.addInstructions(0.60, "[W] - forward, [S] - reverse, [A] - turn left, [D] - turn right, [SPACE] - jump")
    else:
      self.helpOn = False
      taskMgr.add(self.update, 'updateWorld')
      self.inst1.destroy()
      self.inst2.destroy()
      self.inst3.destroy()
      self.inst4.destroy()
      self.inst5.destroy()
      self.inst6.destroy()
      self.inst7.destroy()
      self.inst8.destroy()
      self.inst9.destroy()
      self.inst10.destroy()
      self.inst1 = self.addInstructions(0.06, self.collectibleIndicator)
      self.inst2 = self.addInstructions(0.12, self.timeIndicator)
      self.inst3 = self.addInstructions(0.18, self.helpIndicator)
  
  def toggleDebug(self):
    if self.debugNP.isHidden():
      self.debugNP.show()
    else:
      self.debugNP.hide()
              
  def update(self, task):
    dt = globalClock.getDt()
    self.player.move()
    self.world.doPhysics(dt, 4, 1./240.)
    self.processMovements()
    self.countdown()
    self.refreshCollectibleCount()

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
    
    if (self.player.getCharacterNP().getZ() < -40):
      self.player.resetCharacter()
      self.laughSound.play()

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
    self.debugNP.hide()

    self.world = BulletWorld()
    self.world.setGravity(Vec3(0, 0, -9.81))
    self.world.setDebugNode(self.debugNP.node())

    # Create starting platform
    Platform(self.render, self.world, self.loader, 0, str(-1), 2, 0, 0, -3)

    # Generate platforms
    PlatformFactory(self.render, self.world, self.loader, self.platformCount, self.collectibleTotal)
    
    # Create player character
    self.player = Player(self.render, self.world, 0, 0, 0)
    
    # Music and sound
    self.gameMusic = base.loader.loadSfx("sounds/level1.mp3")
    self.gameMusic.setLoop()
    self.gameMusic.setVolume(0.4)
    self.gameMusic.play()
    self.laughSound = base.loader.loadSfx("sounds/laugh.ogg")
    self.collectSound = base.loader.loadSfx("sounds/collect.mp3")
  
  # Handle contacts
  def processMovements(self):
    if (len(Data.books) > 0):
      for book in Data.books:
        self.distanceTest(book)
    
    if (len(Data.door) > 0):
      self.distanceTest(Data.door[0])
      
    if (len(Data.akises) > 0):
      for akis in Data.akises:
        self.distanceTest(akis)
        
    if (len(Data.kangs) > 0):
      for kang in Data.kangs:
        self.distanceTest(kang)

  def distanceTest(self, secondObject):
    name = secondObject.getActor().getName()
    distance = self.getDistance(self.player.getCharacterNP(), secondObject.getNP())
    
    if (distance > self.contactDistance and distance <= self.detectDistance):
      if ("Akis" in name):
        secondObject.move(self.player)
      elif ("Kang" in name):
        # drop things onto player
        print "something"
    
    if (distance <= self.contactDistance):
      if ("Collectible" in name):
        secondObject.killNP()
        secondObject.getActorModelNP().removeNode()
        self.collectSound.play()
        self.collectibleCounter += 1
      elif ("Door" in name):
        if (self.collectibleCounter == self.collectibleTotal):
          taskMgr.remove('updateWorld')
          self.addVictoryText("YOU WON!!!")
      elif ("Akis" in name):
        self.player.resetCharacter()
        self.laughSound.play()
          
  def refreshCollectibleCount(self):
    self.collectibleIndicator = "Level 1: collectible items - " + str(self.collectibleCounter) + "/" + str(self.collectibleTotal)
    self.inst1.destroy()
    self.inst1 = self.addInstructions(0.06, self.collectibleIndicator)
    
    # refresh time
    self.timeIndicator = "Time left - " + str(self.maxTime/self.frameRate)
    self.inst2.destroy()
    self.inst2 = self.addInstructions(0.12, self.timeIndicator)
  
  def countdown(self):
    if (self.maxTime > 0):
      self.maxTime -= 1
    elif (self.maxTime == 0):
      taskMgr.remove('updateWorld')
      self.addVictoryText("YOU LOST!!")
      
  # UTIL METHODS
  def getDistance(self, one, two):
    vec = one.getPos() - two.getPos()
    return vec.length()

game = UpAllTheWay()
game.run()
