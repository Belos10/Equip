class CommonHelper:
  def __init__(self):
    pass

  @staticmethod
  def readQss(style):
    with open(style, 'a+') as f:
      return f.read()
  @staticmethod
  def isNumber(s):
    try:
      float(s)
      return True
    except ValueError:
      pass

    try:
      import unicodedata
      unicodedata.numeric(s)
      return True
    except (TypeError, ValueError):
      pass
    return False