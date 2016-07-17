class Data(object):
  # GAME PARAMETERS
  platformCount = 2
  collectibleTotal = 1
  timeAllowed = 120
  ballDropRate = 1
  
  # OTHER PARAMETERS
  contactDistance = 1
  winningDistance = 1.5
  detectDistance = 4
  collectibleCounter = 0
  frameRate = 60
  maxTime = timeAllowed * frameRate
  dropRate = ballDropRate * frameRate
  currentLevel = 1
  
  books = []
  door = []
  magicBox = []
  akises = []
  kangs = []
  balls = []