"""
This script runs the game 'snake' using pygame.
Every cubes co-ords and direction are saved in a list.
When an arrow key is pressed, the location of the head of the snake and the direction is added to a list, which is saved within the movement list.
To change direction, it checks if any cubes are in the movement list and if it is, the direction of the turn point is saved to cube_next_dir.
When a cube hits a gridline, the cube_next_dir is saved to dir and the cube moves.
If the last cube passes over the change direction co-ords, it is removed from the list.
"""

# import modules
import os, math, pygame, random
from tkinter import *

difficulty = ''
def select_difficulty(level):
    global fps
    global filename
    if level == 'easy':
        fps = 70
        filename = 'snake_leaderboard_easy.txt'
    if level == 'medium':
        fps = 100
        filename = 'snake_leaderboard_medium.txt'
    if level == 'hard':
        fps = 130
        filename = 'snake_leaderboard_hard.txt'
    first_menu.destroy()

def exit_menu_func():
    global play_again_exit
    first_menu.destroy()
    play_again_exit = False

first_menu = Tk()
first_menu.configure(bg = 'black')
first_menu.geometry('400x100')
first_menu.title('Snake Menu')

welcome_text = Label(text = 'Welcome to snake',fg = 'green',bg = 'black')
welcome_text.config(font = ('fixedsys',20))

button_frame = Frame()
button_frame.place(x=0,y=50)

difficulty_easy_button = Button(button_frame,height = '3',width = '18',bg = 'green',text = 'Easy',command = lambda: select_difficulty('easy'))
difficulty_medium_button = Button(button_frame,height = '3',width = '18',bg = 'orange',text = 'Medium',command = lambda: select_difficulty('medium'))
difficulty_hard_button = Button(button_frame,height = '3',width = '18',bg = 'red',text = 'Hard',command = lambda: select_difficulty('hard'))
exit_button_menu = Button(text = 'Exit',command = exit_menu_func,bg = 'green')

welcome_text.pack()
exit_button_menu.place(x = 30,y=10)
difficulty_easy_button.pack(side = LEFT)
difficulty_medium_button.pack(side = LEFT)
difficulty_hard_button.pack(side = LEFT)

first_menu.mainloop()

# start pygame
pygame.init()
pygame.font.init()

# center window
os.environ['SDL_VIDEO_CENTERED'] = '1'


# set fps
clock = pygame.time.Clock()
# load image
apple_image = pygame.image.load('apple.png')

# variables
# start position
snakex = 780
snakey = 455
# start direction
next_dir = 'left'
score = 0
snake_list = []
movement_list = []
cube_speed = 5
# minimum distance from snake to apple spawn
distance_new_apple = 64
# grid lines with list comprehension
allxcords = [i * 65 for i in range(26)]
allycords = [i * 65 for i in range(17)]
# when False, quits snake window
play_again_exit = True

# load font
font = pygame.font.Font('font.ttf',20)

def easy_mode():
    global snake_body
    global snake_head_up
    global snake_head_left
    global snake_head_down
    global snake_head_right
    global hard_mode_happened
    global easy_mode_happened
    global fps
    snake_body = pygame.image.load('snake_body.png')
    snake_head_up = pygame.image.load('snake_head_up.png')
    snake_head_left = pygame.image.load('snake_head_left.png')
    snake_head_down = pygame.image.load('snake_head_down.png')
    snake_head_right = pygame.image.load('snake_head_right.png')
    hard_mode_happened = False
    easy_mode_happened = True
    fps -= 30

def hard_mode():
    global snake_body
    global snake_head_up
    global snake_head_left
    global snake_head_down
    global snake_head_right
    global hard_mode_happened
    global easy_mode_happened
    global fps
    snake_body = pygame.image.load('snake_body_red.png')
    snake_head_up = pygame.image.load('snake_head_up_red.png')
    snake_head_left = pygame.image.load('snake_head_left_red.png')
    snake_head_down = pygame.image.load('snake_head_down_red.png')
    snake_head_right = pygame.image.load('snake_head_right_red.png')
    hard_mode_happened = True
    easy_mode_happened = False
    fps += 30

easy_mode()

# used to calculate collision using pythagoras : (sqrt(a**2+b**2))
def find_distance(val1x, val1y, val2x, val2y):
    distancex = val2x - val1x
    distancey = val2y - val1y
    distancepoints = math.sqrt(distancex ** 2 + distancey ** 2)
    return distancepoints


# this class stores all the positional and directional data for each cube
class cube:

    def __init__(self, cubex, cubey, dir, cube_next_dir):
        self.cubex = cubex
        self.cubey = cubey
        self.dir = dir
        self.cube_next_dir = cube_next_dir

    @staticmethod
    # this method finds cube in front, gets its direction and makes new cube coordinates behind it. new cube added to snake list
    def add_cube():
        previous_cube = snake_list[-1]
        if previous_cube.cube_next_dir == previous_cube.dir:
            # find previous cube

            new_cubex = previous_cube.cubex
            new_cubey = previous_cube.cubey
            new_dir = previous_cube.dir
            new_cube_next_dir = previous_cube.cube_next_dir

            # new cube coords behind previous cube
            if previous_cube.dir == 'left':
                new_cubex = previous_cube.cubex + 65
            if previous_cube.dir == 'right':
                new_cubex = previous_cube.cubex - 65
            if previous_cube.dir == 'up':
                new_cubey = previous_cube.cubey + 65
            if previous_cube.dir == 'down':
                new_cubey = previous_cube.cubey - 65

            # create new cube object
            new_cube = cube(new_cubex, new_cubey, new_dir, new_cube_next_dir)
            snake_list.append(new_cube)


# add first cube
first_cube = cube(snakex, snakey, next_dir, next_dir)
snake_list.append(first_cube)
# add second cube
cube.add_cube()


# this class handles movement of cubes and whole snake
class snake():
    snakex_change = 0
    snakey_change = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(next_dir):
        # iterate through every cube in snake list
        for i in snake_list:
            current_cube = i

            # check if location is move location, if it is, change direction
            for i in range(len(movement_list)):
                i -= 1
                # if co-ords of any movement points are == to the current cubes co=ords, current cubes direction change
                # [0] is the x co-ord, [1] is the y co-ord, [2] is the direction change
                if movement_list[i][0] == current_cube.cubex and movement_list[i][1] == current_cube.cubey:
                    current_cube.cube_next_dir = movement_list[i][2]
                    # if the current cube is the last in the snake, remove the turn point
                    if snake_list[-1] == current_cube:
                        movement_list.pop(i)

            # current_cube.dir is the cubes current direction.
            # current_cube.cube_next_dir is the direction to go when the cube hits a gridline
            # when the cube hits gridline, current_cube.dir changes to current_cube.cube_next_dir
            if current_cube.dir == 'left' or current_cube.dir == 'right':
                for i in allxcords:
                    if i == current_cube.cubex:
                        current_cube.dir = current_cube.cube_next_dir

            if current_cube.dir == 'up' or current_cube.dir == 'down':
                for i in allycords:
                    if i == current_cube.cubey:
                        current_cube.dir = current_cube.cube_next_dir

            # snake change var is the speed and direction to move the cube. it is added to the co-ords of the cubes
            reset_change()
            if current_cube.dir == 'left':
                snake.snakex_change = -cube_speed
            if current_cube.dir == 'right':
                snake.snakex_change = cube_speed
            if current_cube.dir == 'up':
                snake.snakey_change = -cube_speed
            if current_cube.dir == 'down':
                snake.snakey_change = cube_speed

            # update co-ords with change var
            current_cube.cubey += snake.snakey_change
            current_cube.cubex += snake.snakex_change

            # draw cube in updated position
            if current_cube == first_cube:
                # draw head in correct orientation
                if current_cube.dir == 'left':
                    window.blit(snake_head_left, (current_cube.cubex, current_cube.cubey))
                if current_cube.dir == 'right':
                    window.blit(snake_head_right, (current_cube.cubex, current_cube.cubey))
                if current_cube.dir == 'up':
                    window.blit(snake_head_up, (current_cube.cubex, current_cube.cubey))
                if current_cube.dir == 'down':
                    window.blit(snake_head_down, (current_cube.cubex, current_cube.cubey))
            else:
                window.blit(snake_body, (current_cube.cubex, current_cube.cubey))

    # method for checking collision with snake
    def collision_with_snake(self):
        is_collision = False
        for i in snake_list:
            if i != snake_list[0] and i != snake_list[1]:
                if len(snake_list) > 2:
                    distance = find_distance(first_cube.cubex, first_cube.cubey, i.cubex, i.cubey)
                    if distance < 64:
                        is_collision = True

        if is_collision:
            return True
        else:
            return False

    # method for checking collision with walls
    def collision_with_wall(self):
        if first_cube.cubex <= -1 or first_cube.cubex >= 1561 or first_cube.cubey <= -1 or first_cube.cubey >= 976:
            return True
        else:
            return False

class apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def new_apple(self):
        xcoord_grid = random.randint(2, 24)
        ycoord_grid = random.randint(2, 15)
        self.x = xcoord_grid * 65 + 16
        self.y = ycoord_grid * 65 + 16
        for i in snake_list:
            distance = find_distance(self.x,self.y,i.cubex,i.cubey)
            if distance < distance_new_apple:
                apple.new_apple()

    def apple_collision(self):
        apple_distance = find_distance(self.x, self.y, first_cube.cubex, first_cube.cubey)
        if apple_distance < 40:
            cube.add_cube()
            apple.new_apple()
            return True
        else:
            window.blit(apple_image, (self.x, self.y))
            return False


apple = apple(random.randint(2, 24) * 65 + 16, random.randint(2, 15) * 65 + 16)

# resets change to stop diagonal movement, called in move method of snake class
def reset_change():
    snake.snakex_change = 0
    snake.snakey_change = 0

exit_var = True

while play_again_exit:
    # create window
    window = pygame.display.set_mode((1825, 1040))
    score_above_10 = False
    while exit_var:
        # set fps
        clock.tick(fps)
        # fill background
        window.fill((0, 0, 0))
        # draw grid
        for i in allxcords:
            pygame.draw.line(window, (0, 255, 0), (i, 0), (i, 1040), 1)
        for i in allycords:
            pygame.draw.line(window, (0, 255, 0), (0, i), (1625, i), 1)


        #draw score text
        text = ('Score: ' + str(score))
        font_surface = font.render(text, False, (255, 255, 255))
        window.blit(font_surface,(1650,500))
        # iterate through events
        for event in pygame.event.get():
            # check for quit
            if event.type == pygame.QUIT:
                exit_var = False
            # check for keypresses
            if event.type == pygame.KEYDOWN:
                # if keypress is found, filters out arrow keys and changes direction var
                if first_cube.dir != 'right':
                    if event.key == pygame.K_LEFT:
                        next_dir = 'left'
                if first_cube.dir != 'left':
                    if event.key == pygame.K_RIGHT:
                        next_dir = 'right'
                if first_cube.dir != 'down':
                    if event.key == pygame.K_UP:
                        next_dir = 'up'
                if first_cube.dir != 'up':
                    if event.key == pygame.K_DOWN:
                        next_dir = 'down'
                # adds list in format [turn point x co-ord, turn point y co-ord, direction of turn point to the movement list
                movement_list.append([first_cube.cubex, first_cube.cubey, next_dir])
        # moves movement
        snake.move(next_dir)
        # check collision with itself and wall
        collision_happened_snake = snake.collision_with_snake(None)
        if collision_happened_snake:
            print(1)
            break
        collision_happened_wall = snake.collision_with_wall(None)
        if collision_happened_wall:
            print(2)
            break
        # check apple collision
        collision_happened_apple = apple.apple_collision()
        if collision_happened_apple:
            score+=1

        if score != 0:
            if score % 10 == 0 and not hard_mode_happened:
                hard_mode()

        if score % 10 != 0 and not easy_mode_happened:
            easy_mode()

        pygame.display.update()

    leaderboard = open(filename,'r')
    leaderboard_contents = (leaderboard.read())
    if score > int(leaderboard_contents):
        leaderboard = open(filename,'w')
        leaderboard.write(str(score))

    leaderboard = open(filename,'r')
    print(('The high score is ',leaderboard.read()))
    print('Your score was ',score)

    end_window = Tk()
    end_window.config(bg = 'black')

    def exit_end_window():
        global play_again_exit
        play_again_exit = False
        end_window.destroy()

    play_again_button = Button(height = 3,text='Play Again?', command=end_window.destroy,bg = 'green')
    exit_button_end = Button(height = 3,text='Exit', command=exit_end_window,bg = 'red')
    play_again_button.pack(fill = 'x')
    exit_button_end.pack(fill = 'x')
    end_window.mainloop()

    snake_list = []
    movement_list = []
    first_cube = cube(snakex, snakey, next_dir, next_dir)
    snake_list.append(first_cube)
    cube.add_cube()
    score = 0

    leaderboard.close()

