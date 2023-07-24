import pygame as pg
import time

#-------------Engine Code---------------#
# Player data
playerx = 50
playery = 350

score = 0
lives = 10

# Game state data
bulletList = [] 
targetList = []

gameOver = False

fpsDisplay = False

mousePosition = 0

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, deltaTime):
        self.x += 250 * deltaTime

class Target:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, deltaTime):
        self.y += 100 * deltaTime

class Spawner:
    def __init__(self):
        self.elapsedTime = 0

    def Spawn(self, deltaTime):
        self.elapsedTime += deltaTime
        if (self.elapsedTime > 2):
            print("Spawned")
            targetList.append(Target(300, 0))
            self.elapsedTime = 0

#-------------Main Driver Code---------------#

# Initialize pygame
pg.init()
screen = pg.display.set_mode((400, 400))
clock = pg.time.Clock()
initialTime = time.time()

# Set the scene
pg.draw.rect(screen, pg.Color(255, 255, 255), pg.Rect(playerx, playery, 50, 50))
spawner = Spawner()
myfont = pg.font.SysFont("monospace", 20)

# Game Loop
running = True
while (running):
    # Calculate deltatime
    finalTime = time.time()
    deltaTime = finalTime - initialTime
    initialTime = finalTime

    # Check for events
    for event in pg.event.get():
        if (event.type == pg.QUIT):
            print(event)
            running = False
        elif (event.type == pg.KEYUP):
            if (event.key == pg.K_SPACE):
                print(event)
                bulletList.append(Bullet(playerx, playery))
            elif (event.key == pg.K_TAB):
                fpsDisplay = True
                print("FPS displayed.")
        elif pg.mouse.get_pressed()[0]:
                mousePosition = pg.mouse.get_pos()
                if gameOver == True:
                    if pg.Rect(100, 100, 100, 50).collidepoint(mousePosition):
                        gameOver = False
                        lives = 10
                        print("Button Clicked!")

    # Update Engine State
    clock.tick(60)
    fps = clock.get_fps()
    if gameOver == False:
        spawner.Spawn(deltaTime)
        for bullet in bulletList:
            bullet.update(deltaTime)
        for target in targetList:
            target.update(deltaTime)
        # Check collisions
        for bullet in bulletList:
            for target in targetList:
                if pg.draw.circle(screen, pg.Color(255, 255, 255), (bullet.x, bullet.y), 10).contains(pg.draw.rect(screen, pg.Color(255, 255, 255), pg.Rect(target.x, target.y, 10, 10))):
                    targetList.remove(target)
                    score += 1
                    print("collision")
        # Destroy targets that are out of bound
        for target in targetList:
            if (target.y > 400):
                targetList.remove(target)
                lives -= 1
        for bullet in bulletList:
            if (bullet.x > 400):
                bulletList.remove(bullet)
        # Check game over
        if lives <= 9:
            gameOver = True
            print("Game Over Event.")
 

    # Clear and Render screen
    if gameOver == False:
        screen.fill((0, 0, 0))
        pg.draw.rect(screen, pg.Color(255, 255, 255), pg.Rect(playerx, playery, 50, 50))
        for target in targetList:
            pg.draw.rect(screen, pg.Color(255, 255, 255), pg.Rect(target.x, target.y, 10, 10))
        for bullet in bulletList:
            pg.draw.circle(screen, pg.Color(255, 255, 255), (bullet.x, bullet.y), 10)
        label = myfont.render("Score: " + str(score), 1, (255, 255, 255))
        label2 = myfont.render("Lives: " + str(lives), 1, (255, 255, 255))
        screen.blit(label, (20, 10))
        screen.blit(label2, (270, 10))
        if fpsDisplay == True:
            label3 = myfont.render("FPS: " + str(int(fps)), 1, (255, 255, 255))
            screen.blit(label3, (145, 10))
        pg.display.flip()
    else:
        screen.fill((0, 0, 0))
        # Display button
        pg.draw.rect(screen, pg.Color(255, 255, 255), pg.Rect(100, 100, 100, 50))
        btnLabel = myfont.render("Replay!", 1, (0, 0, 255))
        screen.blit(btnLabel, (100, 100))
        # Display scores
        label = myfont.render("Score: " + str(score), 1, (255, 255, 255))
        label2 = myfont.render("Lives: " + str(lives), 1, (255, 255, 255))
        screen.blit(label, (20, 10))
        screen.blit(label2, (270, 10))
        # Refresh the screen
        pg.display.flip()

# Terminate pygame and display ending message
pg.quit()
input("Thank you for playing. Press any key to continue...")