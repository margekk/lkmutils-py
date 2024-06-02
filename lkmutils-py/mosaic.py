class Mosaic:
    class Tile:
        def __init__(self, id):
            self.id = id
            self.satisfied = False
            match id:
                case 0:
                    self.connections = []
                case 1:
                    self.connections = [[3,4]]
                case 2: #Cusp
                    self.connections = [[1,4]]
                case 3:
                    self.connections = [[1,2]]
                case 4: #Cusp
                    self.connections = [[2,3]]
                case 5:
                    self.connections = [[1,3]]
                case 6:
                    self.connections = [[2,4]]
                case 7:
                    self.connections = [[1,2],[3,4]]
                case 8: #Double cusp
                    self.connections = [[1,4],[2,3]]
                case 10: #Crossing
                    self.connections = [[1,3],[2,4]]

    def __init__(self, input_matrix):
        [Mosaic.Tile(num) for num in row in input_matrix] #Converts every number in inmat to the appropriate tile
        

