import random

"""Agent acting in some environment"""
class Agent(object):

  def __init__(self):
    return

  # this method is called on the start of the new environment
  # override it to initialise the agent
  def start(self):
    print("start called")
    return

  # this method is called on each time step of the environment
  # it needs to return the action the agent wants to execute as as string
  def next_action(self, percepts):
    print("next_action called")
    return "NOOP"

  # this method is called when the environment has reached a terminal state
  # override it to reset the agent
  def cleanup(self, percepts):
    print("cleanup called")
    return


"""A random Agent for the VacuumCleaner world

 RandomAgent sends actions uniformly at random. In particular, it does not check
 whether an action is actually useful or legal in the current state.
 """
class RandomAgent(Agent):

  def next_action(self, percepts):
    print("perceiving: " + str(percepts))
    actions = ["TURN_ON", "TURN_OFF", "TURN_RIGHT", "TURN_LEFT", "GO", "SUCK"]
    action = random.choice(actions)
    print("selected action: " + action)
    return action

"""MyAgent is a more intelligen agent than the random agent

  It is able to clean up each dirt and go back home using three simple steps:
  1. Find corner (go forward until bumping into a wall turn righ and go forward until bumping again)
  2. Do snake mode/sik sak (swipe accross the whole room until it reaches the other corner)
  3 . Go back home
 """

class MyAgent(Agent):
  isTurnedOn = False
  backHome = False
  x, y = 0,0
  orientation = 0
  bumped = False

  # phases
  findCorner = True
  snakeMode = False
  goHome = False

  # snake mode
  forward = True
  left = False



  def next_action(self, percepts):
    print("perceiving: " + str(percepts))
    #["TURN_ON", "TURN_OFF", "TURN_RIGHT", "TURN_LEFT", "GO", "SUCK"]

    if (not self.isTurnedOn and not self.backHome):
      self.isTurnedOn = True
      return "TURN_ON"

    if "DIRT" in percepts:
      return "SUCK"

    
    if self.findCorner:

      if "BUMP" in percepts:
        self.go_backwards()

        if self.bumped:
          self.findCorner = False
          self.snakeMode = True
          self.bumped = False
        else:
          self.bumped = True

        return self.turn_right()
      else:
        return self.go_forward()

    elif self.snakeMode:

      if "BUMP" in percepts:
        self.go_backwards()

        self.forward = True

        if self.bumped:
          self.snakeMode = False
          self.goHome = True
          return self.turn_right()
        else:
          self.bumped = True
        

        if self.left: 
          return self.turn_left()
        else: 
          return self.turn_right()

      elif self.bumped:
        self.bumped = False

        if self.forward:
          self.bumped = True
          self.forward = False
          return self.go_forward()
        
        if self.left:
          self.left = False
          return self.turn_left()
        else:
          self.left = True
          return self.turn_right()
      
      else:
        return self.go_forward()
      
    elif self.goHome:
      if self.x != 0:
        if self.x > 0 and self.orientation != 3:
          return self.turn_left()
        elif self.x < 0 and self.orientation != 1:
          return self.turn_left()
        return self.go_forward()
      
      elif self.y != 0:
        if self.y > 0 and self.orientation != 2:
          return self.turn_left()
        elif self.y < 0 and self.orientation != 0:
          return self.turn_left()
        return self.go_forward()
      
      else:
        self.backHome = True
        return "TURN_OFF"

  ### HELPER FUNCTIONS ###

  def turn_left(self):
    if self.orientation == 0:
      self.orientation = 3
    else:
      self.orientation -= 1
    
    return "TURN_LEFT"
  

  def turn_right(self):
    if self.orientation == 3:
      self.orientation = 0
    else:
      self.orientation += 1
    
    return "TURN_RIGHT"
  

  def go_forward(self):
    if self.orientation == 0:
      self.y += 1
    elif self.orientation == 1:
      self.x += 1
    elif self.orientation == 2:
      self.y -= 1
    else:
      self.x -= 1
    
    return "GO"
  
  def go_backwards(self):
    if self.orientation == 0:
      self.y -= 1
    elif self.orientation == 1:
      self.x -= 1
    elif self.orientation == 2:
      self.y += 1
    else:
      self.x += 1