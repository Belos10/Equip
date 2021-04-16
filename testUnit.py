class testUnit():
    def __init__(self, id, name, shangid):
        super(testUnit).__init__()
        self.id = id
        self.name = name
        self.shangid = shangid

    def getShangid(self):
        return self.shangid

    def getId(self):
        return self.id

    def getName(self):
        return self.name