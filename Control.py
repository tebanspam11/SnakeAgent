import keyboard

class Control:
    def __init__(self):
        """
            Initialize the control handler for simulating keyboard input.
        """

        pass

    def makeMove(self, move):
        """
            Send a keyboard command to move the snake.

            :param move: String ('up', 'down', 'left', 'right') representing the movement direction.
        """

        keyboard.press_and_release(move)

    def start(self):
        """
            Start the game by sending the 'space' key press.
        """
        
        keyboard.press_and_release("space")