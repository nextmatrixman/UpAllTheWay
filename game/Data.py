class Data(object):
  # GAME PARAMETERS
  platformCount = 3
  collectibleTotal = 1
  timeAllowed = 120
  contactDistance = 1
  detectDistance = 4
  ballDropRate = 1
  
  # OTHER PARAMETERS
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