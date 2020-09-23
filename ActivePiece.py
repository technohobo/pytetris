class ActivePiece():
    def __init__(self, pctype,length):
    
        self.name = pctype
        self.data = []
        self.rot = 0

        if pctype == "T":
            self.data = [(length/2-1,0),(length/2,0),(length/2+1,0),(length/2,1)]

            self.firstv = [1,-1]
            self.lastv = [-1,-1]
            self.firststep = [[0,2],[-2,0]]
            self.laststep = [[2,0],[0,2]]

        elif pctype == "O":
            self.data = [(length/2-1,0),(length/2,0),(length/2-1,1),(length/2,1)]
        elif pctype == "I":
            for i in range(4):
                self.data.append((length/2-1,i))

            self.transforms = [[-2,2],[-1,1],[0,0],[1,-1]]

        elif pctype == "L":
            for i in range(3):
                self.data.append((length/2,i))
            self.data.append((length/2+1,2))

            self.firstv = [1,1]
            self.lastv = [-2,0]
            self.firststep = [[-2,0],[0,-2]]
            self.laststep = [[2,-2],[2,2]]

        elif pctype == "J":
            for i in range(3):
                self.data.append((length/2,i))
            self.data.append((length/2-1,2))

            self.firstv = [1,1]
            self.lastv = [0,-2]
            self.firststep = [[-2,0],[0,-2]]
            self.laststep = [[2,2],[-2,2]]

        elif pctype == "Z":
            self.data = [(length/2-1,0),(length/2,0),(length/2,1),(length/2+1,1)]
            self.transforms = [[2,-1],[1,0],[0,-1],[-1,0]]
        elif pctype == "S":
            self.data = [(length/2-1,1),(length/2,1),(length/2,0),(length/2+1,0)]
            self.transforms = [[1,-2],[0,-1],[1,0],[0,1]]

        for i in range(len(self.data)):
            x = int(self.data[i][0])
            y = int(self.data[i][1])
            self.data[i] = (x, y)
