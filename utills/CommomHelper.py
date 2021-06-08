class CommonHelper:
  def __init__(self):
    pass

  @staticmethod
  def readQss(style):
    with open(style, 'a+') as f:
      return f.read()