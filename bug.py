"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame, random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

# Grid Attributes
GRID_SIZE = 21
MID_ROW = (GRID_SIZE - 1)/2
MID_COL = (GRID_SIZE - 1)/2

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
DOWN_LEFT = 5
DOWN_RIGHT = 6
UP_LEFT = 7
UP_RIGHT = 0
 
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
 
# This sets the margin between each cell
MARGIN = 5

# Initial vars
HiddenSquares = GRID_SIZE * GRID_SIZE



# Some functions...

def CheckEmpty (row, col): # Check if cell is empty
    if overlay[row][col] == 0:
        return True
    return False

# create background
overlay = []
background = []
for row in range(GRID_SIZE):
    background.append([])
    overlay.append([])
    for column in range(GRID_SIZE):
        background[row].append(0)  # Append a cell
        overlay[row].append(0) 
        x = random.randint(1, 4)
        background[row][column] = x
        overlay[row][column] = 0

 
# Set middle cell to "GREY"
overlay[MID_ROW][MID_COL] = 1
 
# Initialize pygame
pygame.init()
 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [255, 255]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Bug Sweeper")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Set the screen background
screen.fill(BLACK)


# -------- Main Program Loop -----------


while not done:
    for event in pygame.event.get():  # User did something
        print ("Current Event = ", event.type)
        if event.type == pygame.QUIT:  # If user clicked close
            print("CLICKED!!!!!!!!!!!!!!!!!!!!!!!!!" + str(event.type))
            #pygame.quit()
            #sys.exit() 
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            # Set that location to 9 (WHITE)
            background[row][column] = 9
#            print("Click ", pos, "Grid coordinates: ", row, column)



    # Update overlay

    # Set current cell to middle
    CurrRow = MID_ROW
    CurrCol = MID_COL
    Radius = 1
    Found = False
    DirBitFieldLen = 0xff
    if HiddenSquares > 0:
        DirBitField = 0
        while Found == False:

        # Get destination direction
            DestinationDirection = random.randint(0, 7)
            #print(DestinationDirection)
            DirValue = 2**DestinationDirection
            #print("Current DirValue ", DirValue)
            DirBitField = DirBitField | DirValue
            #print("Current DirBitField ", DirBitField)

            if DestinationDirection == DOWN: # Down  
                dest_row = CurrRow + Radius 
                dest_col = CurrCol
            if DestinationDirection == UP: # Up
                dest_row = CurrRow - Radius
                dest_col = CurrCol
            if DestinationDirection == LEFT: # left
                dest_row = CurrRow
                dest_col = CurrCol - Radius
            if DestinationDirection == RIGHT: # right
                dest_row = CurrRow
                dest_col = CurrCol + Radius
            if DestinationDirection == DOWN_LEFT: # Down Left  
                dest_row = CurrRow + Radius
                dest_col = CurrCol - Radius
            if DestinationDirection == UP_RIGHT: # Up right
                dest_row = CurrRow - Radius
                dest_col = CurrCol + Radius
            if DestinationDirection == UP_LEFT: # up left
                dest_row = CurrRow - Radius
                dest_col = CurrCol - Radius
            if DestinationDirection == DOWN_RIGHT: # down right
                dest_row = CurrRow + Radius
                dest_col = CurrCol + Radius
            
            #dest_row = 10
#            print("Spawn direction..." + str(DestinationDirection))
            # Check distination is in the grid!
            if  0 <= dest_row < GRID_SIZE and 0 <= dest_col < GRID_SIZE:
                print("Destination valid!")
                # Check destination square is empty.  I.E middle coords + 1
                if CheckEmpty(dest_row, dest_col):
#                   print("Cell is empty!")
                    overlay[dest_row][dest_col] = 1
                    Found = True

                if ((DirBitField & DirBitFieldLen) != 0):
                    print ("All filled up! ", DirBitField) 
                    CurrRow = dest_row
                    CurrCol = dest_col
            else:
                print("Destination out of grid!  Resetting to middle!")
                CurrRow = MID_ROW
                CurrCol = MID_COL 
 
    # Draw the grid
    HiddenSquares = 0
    GreyCount = 0
    BlueCount = 0
    RedCount = 0
    YellowCount = 0
    GreenCount = 0
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            color = WHITE
            # print("current overlay ", overlay[row][column], "current background ", background[row][column])
            squarecol = background[row][column] * overlay[row][column] 
            if squarecol == 0:
                color = GREY
                GreyCount = GreyCount + 1
                HiddenSquares = HiddenSquares + 1
            if squarecol == 1:
                color = BLUE
                BlueCount = BlueCount + 1
            if squarecol == 2:
                color = RED
                RedCount = RedCount + 1
            if squarecol == 3:
                color = YELLOW
                YellowCount = YellowCount + 1
            if squarecol == 4:
                color = GREEN
                GreenCount = GreenCount + 1
            if squarecol == 9:
                color = WHITE
                WhiteCount = WhiteCount + 1

            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])

 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
#pygame.quit()
