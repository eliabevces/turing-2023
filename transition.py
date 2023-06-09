class Transition:
    
  def __init__(self, fromState: str, read: str, toState: str, write: str, direction: str) -> None:
    self.fromState = fromState
    self.toState = toState
    self.read = read
    self.write = write
    self.direction = direction


  def getFromState(self) -> str:
    return self.fromState
  

  def getToState(self) -> str :
    return self.toState
  

  def getRead(self) -> str :
    return self.read
  

  def getWrite(self) -> str :
    return self.write
  

  def getDirection(self) -> str :
    return self.direction;
  