from PIL import ImageGrab

class Image:
    def __init__(self, rows, columns, tileSize, top, left):
        """
            Initialize the image handler for capturing the game board.

            :param rows: Number of rows in the board.
            :param columns: Number of columns in the board.
            :param tileSize: Size of each tile in pixels.
            :param top: Y-coordinate of the top-left corner of the board.
            :param left: X-coordinate of the top-left corner of the board.
        """

        self.rows = rows
        self.columns = columns

        self.tileSize = tileSize
        self.top = top
        self.left = left
        self.width = self.columns * self.tileSize + self.columns // 2
        self.height = self.rows * self.tileSize + self.rows // 2

    def takeBoardCapture(self):
        """
            Capture the current board image as a PIL image.

            :return: Captured PIL image of the game board.
        """

        boardBox = (self.left, self.top, self.left + self.width, self.top + self.height)
        return ImageGrab.grab(bbox = boardBox)

    def centralPixel(self, i, j):
        """
            Get the coordinates of the central pixel of a given tile.

            :param i: Row index.
            :param j: Column index.
            :return: Tuple (x, y) representing the pixel coordinates.
        """

        return (j * self.tileSize + j // 2 + self.tileSize // 2, i * self.tileSize + i // 2 + self.tileSize // 2)
    
    def findApple(self):
        """
            Locate the apple on the board based on pixel color detection.

            :return: Tuple (row, column) of the apple or None if not found.
        """
        
        board_image = self.takeBoardCapture()

        for i in range(self.rows):
            for j in range(self.columns):
                r, g, b, a = board_image.getpixel(self.centralPixel(i, j))

                if r > g and r > b:
                    return (i, j)
                    
        return None
