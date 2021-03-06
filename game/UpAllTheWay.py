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
from direct.gui.DirectGui import *

class UpAllTheWay(ShowBase):
  def __init__(self):
    ShowBase.__init__(self)
    self.setupLights()
    self.setup()
    
    # Accept the control keys for movement and rotation
    self.accept('escape', self.doExit)
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
    self.collectibleCounter = 0
    self.collectibleTotal = Data.collectibleTotal1
    self.collectibleIndicator = "Level " + str(Data.currentLevel) + ": collectible items - " + str(self.collectibleCounter) + "/" + str(self.collectibleTotal)
    self.timeIndicator = "Time left - " + str(Data.maxTime/Data.frameRate)
    self.helpIndicator = "[F1] - Help"
    self.inst1 = self.addInstructions(0.06, self.collectibleIndicator)
    self.inst2 = self.addInstructions(0.12, self.timeIndicator)
    self.inst3 = self.addInstructions(0.18, self.helpIndicator)
    
    # Help variable
    self.helpOn = False
  
  # Function to put instructions on the screen.
  def addInstructions(self, pos, msg):
    return OnscreenText(text=msg, style=1, fg=(89/255, 255/255, 56/255, 1), 
                        scale=.06, shadow=(0, 0, 0, 1), parent = base.a2dTopLeft, 
                        pos=(0.04, -pos - 0.02), align = TextNode.ALeft)
  
  def addVictoryText(self, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), 
                        scale=.25, shadow=(0, 0, 0, 1), parent = base.a2dTopLeft, 
                        pos=(0.6, -1), align = TextNode.ALeft)
  
  def doExit(self):
    self.cleanup()
    sys.exit(1)

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
      
  def level1Selector(self):
    Data.maxTime = 7200
    Data.detectDistance = 4
    Data.dropRate = 60
    self.collectibleTotal = Data.collectibleTotal1
    self.player.resetCharacter()
    self.level2Music.stop()
    self.level1Music.play()
  
  def level2Selector(self):
    Data.maxTime = 9000
    Data.detectDistance = 5
    Data.dropRate = 30
    self.collectibleTotal = Data.collectibleTotal2
    self.player.resetCharacter()
    self.level1Music.stop()
    self.level2Music.play()
      
  def createMainMenu(self):
    self.v = [0]
    self.myFrame = DirectFrame(frameColor = (0.8, 0.8, 0.8, 1), frameSize = (-0.5, 0.5, -0.3, 0.3), pos = (0, 0, 0))
    self.myLabel = DirectLabel(text = 'MAIN  MENU', scale = 0.1, pos = (0, 0, 0.16))
    self.buttons = [
      DirectRadioButton(text = 'Level 1', variable = self.v, value = [1], scale = 0.1, pos = (-0.2,0,-0.05), command = self.setLevel),
      DirectRadioButton(text = 'Level 2', variable = self.v, value = [2], scale = 0.1, pos = (0.25,0,-0.05), command = self.setLevel)
    ]
    for button in self.buttons:
      button.setOthers(self.buttons)
    self.start = DirectButton(text = "START", scale = 0.1, pos = (-0.2,0,-0.2), command = self.levelStart)
    self.quit = DirectButton(text = "QUIT", scale = 0.1, pos = (0.2,0,-0.2), command = self.doExit)
    
  def setLevel(self):
    Data.currentLevel = self.v[0]
  
  def levelStart(self):
    self.myFrame.destroy()
    self.myLabel.destroy()
    self.buttons[0].destroy()
    self.buttons[1].destroy()
    self.start.destroy()
    self.quit.destroy()
    
    if (Data.currentLevel == 1):
      self.level1Selector()
    else:
      self.level2Selector()
              
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
    if (camdist > 25.0):
      base.camera.setPos(base.camera.getPos() + camvec*(camdist-20))
      camdist = 25.0
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

    # Create starting platforms
    Platform(self.render, self.world, self.loader, 0, 1, 2, 0, 0, -3)
    Platform(self.render, self.world, self.loader, 0, 2, 2, 100, 100, -3)

    # Generate platforms
    PlatformFactory(self.render, self.world, self.loader)
    
    # Create player character
    self.player = Player(self.render, self.world, 0, 0, 0)
    
    # Music and sound
    self.level1Music = base.loader.loadSfx("sounds/level1.mp3")
    self.level1Music.setLoop()
    self.level1Music.setVolume(0.4)
    self.level1Music.play()
    self.level2Music = base.loader.loadSfx("sounds/level2.mp3")
    self.level2Music.setLoop()
    self.level2Music.setVolume(0.4)
    self.winMusic = base.loader.loadSfx("sounds/win.ogg")
    self.winMusic.setLoop()
    self.winMusic.setVolume(0.4)
    self.laughSound = base.loader.loadSfx("sounds/laugh.ogg")
    self.collectSound = base.loader.loadSfx("sounds/collect.mp3")
    
    self.createMainMenu()
  
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
        
    if (len(Data.balls) > 0):
      for ball in Data.balls:
        self.distanceTest(ball)
        
    if (len(Data.magicBox) > 0):
      self.distanceTest(Data.magicBox[0])

  def distanceTest(self, secondObject):
    name = secondObject.getActor().getName()
    distance = self.getDistance(self.player.getCharacterNP(), secondObject.getNP())
    
    if (distance > Data.contactDistance and distance <= Data.detectDistance):
      if ("Akis" in name or "Kang" in name):
        secondObject.move(self.player)
      if ("Kang" in name and Data.maxTime % Data.dropRate == 0):
        secondObject.drop(self.player)
    
    if (distance <= Data.winningDistance):
      if (self.collectibleCounter == self.collectibleTotal):
        if ("Door" in name):
          self.collectibleCounter = 0
          Data.currentLevel = 2
          self.level2Selector()
        elif ("MagicBox" in name):
          taskMgr.remove('updateWorld')
          self.addVictoryText("GRADUATED!")
          self.level2Music.stop()
          self.winMusic.play()
    
    if (distance <= Data.contactDistance):
      if ("Collectible" in name):
        secondObject.killNP()
        secondObject.getActorModelNP().removeNode()
        self.collectSound.play()
        self.collectibleCounter += 1
      elif ("Akis" in name or "Kang" in name or "Ball" in name):
        self.player.resetCharacter()
        self.laughSound.play()
          
  def refreshCollectibleCount(self):
    self.collectibleIndicator = "Level " + str(Data.currentLevel) + ": collectible items - " + str(self.collectibleCounter) + "/" + str(self.collectibleTotal)
    self.inst1.destroy()
    self.inst1 = self.addInstructions(0.06, self.collectibleIndicator)
    
    # refresh time
    self.timeIndicator = "Time left - " + str(Data.maxTime/Data.frameRate)
    self.inst2.destroy()
    self.inst2 = self.addInstructions(0.12, self.timeIndicator)
  
  def countdown(self):
    if (Data.maxTime > 0):
      Data.maxTime -= 1
    elif (Data.maxTime == 0):
      taskMgr.remove('updateWorld')
      self.addVictoryText("YOU LOST!!!")
      
  # UTIL METHODS
  def getDistance(self, one, two):
    vec = one.getPos() - two.getPos()
    return vec.length()

game = UpAllTheWay()
game.run()
