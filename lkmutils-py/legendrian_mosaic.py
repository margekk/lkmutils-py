from PIL import Image, ImageDraw
import os


class Mosaic:

    def __init__(self, input_matrix):
        # [Mosaic.Tile(num) for num in row in input_matrix] 
        # This feels hacky, the above works but doesn't allow us to keep track of position as easily
        self.size = len(input_matrix)
        self.matrix = input_matrix
        for i in range(self.size):
            for j in range(self.size): 
                self.matrix[i][j] = Tile(self.matrix[i][j], i, j)
        self.up_cusps = 0
        self.down_cusps = 0
        self.pos_crossings = 0
        self.neg_crossings = 0
        self.connected = self.trace()
        self.satisfied = True
        for row in self.matrix:
            for tile in row:
                if not tile.satisfied:
                    print(f"not satisfied: {tile.num}")
                    self.satisfied = False
                    break
                else:
                    continue
            break
        
    def display(self):
        print(f"Size: {self.size}")
        print(f"A Knot?: {self.connected and self.satisfied}")
        if self.connected and self.satisfied:
            print(f"Crossings: {self.pos_crossings + self.neg_crossings}")
            print(f"Cusps: {self.down_cusps + self.up_cusps}")
            print(f"Thurston-Bennquin Number: {self.tb()}")
            print(f"Rotation Number: {self.rot()}")
        
        
    def trace(self):
        for row in self.matrix:
            for tile in row:
                if (tile.num != 0):
                    self.starting_tile = tile
                    break
                else:
                    continue
            break
        try:
            for i in range(4):
                for conn in self.starting_tile.valid_connections:
                    if conn[0] == i:
                        #Debug:
                        #print("starting trace")
                        self.trace_through(self.starting_tile,i)
                        break
                    else:
                        continue
                break
        except: 
            return False

        return True

    def trace_through(self, tile, in_face):
        #Debug:
        #print(f"trace tile: {tile.num}")
        # Recursion stops when we return to the starting tile
        if (tile == self.starting_tile and tile.satisfied):
            return

        for conn in tile.valid_connections:
            if conn[0] == in_face:
                # Manipulating current tile and updating counts:
                tile.made_connections.add(conn)    
                if (len(tile.made_connections) == len(tile.valid_connections) // 2):
                    tile.satisfied = True
                    #Debug:
                    #print(f"{tile.num} satisfied")
                if conn in [(0,3),(1,2)]:
                    self.down_cusps += 1
                if (conn == (3,0) or conn == (1,2)):    
                    self.up_cusps += 1
                if (tile.satisfied and tile.num == 10):
                    # Match doesn't work with sets, so this is a bit clunky
                        if tile.made_connections == {(0,2), (1,3)}:
                            self.neg_crossings += 1
                        elif tile.made_connections == {(0,2), (3,1)}:
                            self.pos_crossings += 1
                        elif tile.made_connections == {(2,0), (1,3)}:
                            self.pos_crossings += 1
                        elif tile.made_connections == {(2,0), (3,1)}:
                            self.neg_crossings += 1
                        else :
                            print(f"set equality doesn't work for crossings")
                
                out_face = conn[1]
                match out_face:
                    case 0:
                        self.trace_through(self.matrix[tile.row][tile.col+1], (out_face + 2) % 4)
                    case 1:
                        self.trace_through(self.matrix[tile.row-1][tile.col], (out_face + 2) % 4)
                    case 2:
                        self.trace_through(self.matrix[tile.row][tile.col-1], (out_face + 2) % 4)
                    case 3:
                        self.trace_through(self.matrix[tile.row+1][tile.col], (out_face + 2) % 4)
                return

        # Raises an exception if there are no valid connections.
        raise Exception("Not connected.")


    def tb(self):
        return (self.pos_crossings - self.neg_crossings) - ((self.down_cusps + self.up_cusps) // 2)

    def rot(self):
        return (self.down_cusps - self.up_cusps) // 2

    def to_png(self, output_filename):
        tile_size = 115
        border_size = 4
        border_color = (196, 196, 196, 255)

        tile_images = {}
        for num in range(11):
            if num != 9:
                file_name = f"tiles/{num}.png"
                try:
                    tile_images[num] = Image.open(file_name).convert("RGBA")
                except FileNotFoundError:
                    print(f"Failed to load image {file_name}")

        mosaic_width = self.size * tile_size + 2 * border_size
        mosaic = Image.new("RGBA", (mosaic_width, mosaic_width), border_color)
        draw = ImageDraw.Draw(mosaic)

        for i, row in enumerate(self.matrix):
            for j, tile in enumerate(row):
                if tile.num in tile_images:
                    img_tile = tile_images[tile.num]
                    for y in range(tile_size):
                        for x in range(tile_size):
                            pixel = img_tile.getpixel((x, y))
                            mosaic.putpixel((j * tile_size + x + border_size, i * tile_size + y + border_size), pixel)

        rotated_mosaic = mosaic.rotate(45, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))

        rotated_mosaic.save(output_filename)
        print(f"Mosaic saved as {output_filename}")

class Tile:
    def __init__(self, n, r, c):
        self.num = n
        self.row = r
        self.col = c
        self.satisfied = False
        self.made_connections = set() 
        match n:
            case 0:
                self.valid_connections = set()
                self.satisfied = True
            case 1:
                self.valid_connections = {(2, 3), (3, 2)}
            case 2: # Cusp
                self.valid_connections = {(0, 3), (3, 0)}
            case 3:
                self.valid_connections = {(0, 1), (1, 0)}
            case 4: # Cusp
                self.valid_connections = {(1, 2), (2, 1)}
            case 5:
                self.valid_connections = {(0, 2), (2, 0)}
            case 6:
                self.valid_connections = {(1, 3), (3, 1)}
            case 7:
                self.valid_connections = {(0, 1), (1, 0), (2, 3), (3, 2)}
            case 8: # Double cusp
                self.valid_connections = {(0, 3), (3, 0), (1, 2), (2, 1)}
            case 10: # Crossing
                self.valid_connections = {(0, 2), (2, 0), (1, 3), (3, 1)}

