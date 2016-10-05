"""
 Steve Cooper's Program!
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame, random, time
 
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
WIDTH = 15    # Width of grid square 
HEIGHT = 15   # Height of grid square
MARGIN = 2   # Margin of grid square

# Window size needs to be worked out based on above
WINDOW_SIZE = [500, 359]

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
DOWN_LEFT = 5
DOWN_RIGHT = 6
UP_LEFT = 7
UP_RIGHT = 0
 

# Initial vars
done = False     # Loop until the user clicks the close button.
HiddenSquares = GRID_SIZE * GRID_SIZE
Clicks = 0
Bugs = 0
ProbBlueBug = 0.5
ProbRedBug = 0.1
ProbYellowBug = 0.3
ProbGreenBug = 0.7
H=0


# Some functions...

def CheckEmpty (row, col): # Check if cell is empty
    if grid[row][col]['Hidden'] == True:
        return True
    return False


ColorArray = [GREY, GREEN, YELLOW, BLUE, RED, WHITE, BLACK]
grid = []

for row in range(GRID_SIZE):
    grid.append([])
    for column in range(GRID_SIZE):
        grid[row].append(0)  # Append a cell
        x = random.randint(1, 4)
        grid[row][column] = {'ColorIndex' : x, 'Color' : ColorArray[x], 'Hidden' : True }


# Initialize pygame
pygame.init()                                    # Initialise pygame
screen = pygame.display.set_mode(WINDOW_SIZE)    # Set up screen
pygame.display.set_caption("Bug Sweeper")        # Set display caption
clock = pygame.time.Clock()                      # Used to manage how fast the screen updates
screen.fill(BLACK)                               # Set screen background colour


# -------- Main Program Loop -----------


while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            #pygame.quit()
            #sys.exit() 
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse. Get the position
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            #print(" COL = ", column)
            #print(" ROW = ", row)
            # Change the x/y screen coordinates to grid coordinates if inside the grid
            if (column < GRID_SIZE) and (row < GRID_SIZE):
                # Get the color...
                CurrCol = grid[row][column]['Color']

                # Get Random number floating between 0.0 and 1.0
                Random = random.random()
                if (CurrCol == RED) and (ProbRedBug > Random  ):
                    Bugs = Bugs + 1
                if (CurrCol == BLUE) and (ProbBlueBug > Random  ):
                    Bugs = Bugs + 1
                if (CurrCol == GREEN) and (ProbGreenBug > Random  ):
                    Bugs = Bugs + 1
                if (CurrCol == YELLOW) and (ProbYellowBug > Random  ):
                    Bugs = Bugs + 1

                # Update "clicked" square colour to white
                grid[row][column]['Color'] = WHITE
                Clicks = Clicks + 1

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
            DirValue = 2**DestinationDirection
            DirBitField = DirBitField | DirValue

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
            
            # Check destination is in the grid!
            if  0 <= dest_row < GRID_SIZE and 0 <= dest_col < GRID_SIZE:
                # Check destination square is empty.  I.E middle coords + 1
                if CheckEmpty(dest_row, dest_col):
                    #print("Cell is empty!")
                    grid[dest_row][dest_col]['Hidden'] = False
                    Found = True

                if ((DirBitField & DirBitFieldLen) != 0):
                    #print ("All filled up! ", DirBitField) 
                    CurrRow = dest_row
                    CurrCol = dest_col
            else:
                #print("Destination out of grid!  Resetting to middle!")
                CurrRow = MID_ROW
                CurrCol = MID_COL 
 
    # Draw the grid
    HiddenSquares = 0
    TotalColors = len(ColorArray)
    ColorCount = []
    H = 0 
    for i in range(TotalColors):
        ColorCount.append(0)

    # print ("Starting to draw grid")
    screen.fill(BLACK)
    for row in range(GRID_SIZE-1):
        for column in range(GRID_SIZE-1):

            # = ColorCount[grid[row][column]['ColorIndex']] + 1
            if grid[row][column]['Hidden'] == True:
                HiddenSquares = HiddenSquares + 1
                print("Hidden Squares...",HiddenSquares)
                ColorVar = GREY
                H = H + 1
            else:
                ColorVar = grid[row][column]['Color']
            # print ("ColorVar = " + str(ColorVar))
            pygame.draw.rect(screen,
                             ColorVar,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
            if grid[row][column]['Hidden'] == False:
                i = grid[row][column]['ColorIndex']
                # print (">", row, column,i)
                ColorCount[i] = ColorCount[i] + 1
                # print ColorCount[i]
    print H
    time.sleep(0.1) 
    font = pygame.font.Font(None, 16)

    BugsFoundMsg = 'Bugs found..........' + str(Bugs)
    text = font.render(BugsFoundMsg, 1,WHITE)
    screen.blit(text, (370,100))

    ClickMsg = 'Clicks...' + str(Clicks)
    text = font.render(ClickMsg, 1,WHITE)
    screen.blit(text, (370,20))

    # ColorArray = [GREY, GREEN, YELLOW, BLUE, RED, WHITE, BLACK]
    RedCountMsg = 'Red Squares...' + str(ColorCount[4])
    BlueCountMsg = 'Blue Squares...' + str(ColorCount[3])
    GreenCountMsg = 'Green Squares...' + str(ColorCount[1])
    YellowCountMsg = 'Yellow Squares...' + str(ColorCount[2])
    
    text = font.render(ClickMsg, 1,WHITE)
    screen.blit(text, (370,20))
    
    text = font.render(RedCountMsg, 1, RED)
    screen.blit(text, (370,30))

    text = font.render(BlueCountMsg, 1, BLUE)
    screen.blit(text, (370,40))

    text = font.render(GreenCountMsg, 1, GREEN)
    screen.blit(text, (370,50))

    text = font.render(YellowCountMsg, 1, YELLOW)
    screen.blit(text, (370,60))



    # Limit to 60 fres per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    if HiddenSquares == 0:
        done = True
#        print("Hidden Squares = 0 !!!!")

 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
