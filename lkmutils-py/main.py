from PIL import Image, ImageDraw
import os
import legendrian_mosaic

def main():
    print("Please enter the rows of the knot mosaic, one row per line.")
    print("Each row should contain tile numbers between 0 and 10, excluding 9, separated by spaces.")
    print("Enter an empty line to finish input.")
    
    matrix = []

    while True:
        input_row = input()
        
        if input_row.strip() == "":
            if len(matrix) != len(matrix[0]):
                print("Not a square mosaic! Please start again.")
                matrix = []
            else:
                break
        
        try:
            row = [int(num) for num in input_row.split() if 0 <= int(num) <= 10 and int(num) != 9]
            if len(matrix) > 0 and len(matrix[0]) != len(row):
                print("All rows must have the same number of elements. Please start again.")
                matrix = []
                continue
            matrix.append(row)
        except ValueError:
            print("Invalid input. Please enter a row of integers.")
            continue
    
    mosaic = legendrian_mosaic.Mosaic(matrix)
    
    mosaic.display()
    
    save_confirmation = input("Save to file as .png? (yes/no): ").strip().lower()
    if save_confirmation in ["yes", "y"]:
        save_name = input("Enter file name: ").strip()
        mosaic.to_png(save_name)

def create_knot_mosaic(matrix, output_filename):
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
    
    rows = len(matrix)
    mosaic_width = rows * tile_size + 2 * border_size
    
    mosaic = Image.new("RGBA", (mosaic_width, mosaic_width), border_color)
    draw = ImageDraw.Draw(mosaic)
    
    for i, row in enumerate(matrix):
        for j, num in enumerate(row):
            if num in tile_images:
                tile = tile_images[num]
                for y in range(tile_size):
                    for x in range(tile_size):
                        pixel = tile.getpixel((x, y))
                        mosaic.putpixel((j * tile_size + x + border_size, i * tile_size + y + border_size), pixel)
    
    rotated_mosaic = mosaic.rotate(45, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))

    rotated_mosaic.save(output_filename)
    print(f"Mosaic saved as {output_filename}")

if __name__ == "__main__":
    main()

