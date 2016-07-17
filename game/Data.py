class Data(object):
  # GAME PARAMETERS
  currentLevel = 1
  
  if (currentLevel == 1):
    platformCount = 10
    collectibleTotal = 5
    timeAllowed = 120
    detectDistance = 4
    ballDropRate = 1
  else:
    platformCount = 15
    collectibleTotal = 10
    timeAllowed = 120
    detectDistance = 5
    ballDropRate = 0.5
  
  # OTHER PARAMETERS
  contactDistance = 1
  winningDistance = 1.5
  collectibleCounter = 0
  frameRate = 60
  maxTime = timeAllowed * frameRate
  dropRate = ballDropRate * frameRate
  
  books = []
  door = []
  magicBox = []
  akises = []
  kangs = []
  balls = []