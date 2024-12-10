


from cmu_graphics import *
pygame = cmu_graphics.pygame
import time
import math
import random

# Global constants for colors and sizes
BACKGROUND_COLOR = 'black'
TITLE_COLOR = 'white'
BUTTON_COLOR = 'blue'
BUTTON_TEXT_COLOR = 'white'
BUTTON_HOVER_COLOR = 'darkBlue'
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 20

goFullScreen = time.time() + 2
inFullScreenMode = False

class GameState:
    MENU = 'menu'
    PONG = 'pong'
    BREAKOUT = 'breakout'
    SNAKE = 'snake'
    PACMAN = 'pacman'
    ASTEROIDS = 'asteroids'

def onAppStart(app):
    app.state = GameState.MENU
    app.stepsCount = 0
    app.heldKeys = set()
    app.stepsPerSecond = 60
    app.framesPerSecond = 1
    
    # Menu buttons
    app.buttons = [
        {'text': 'PONG', 'state': GameState.PONG, 'y': 200},
        {'text': 'BREAKOUT', 'state': GameState.BREAKOUT, 'y': 270},
        {'text': 'SNAKE', 'state': GameState.SNAKE, 'y': 340},
        {'text': 'PAC-MAN', 'state': GameState.PACMAN, 'y': 410},
        {'text': 'ASTEROIDS', 'state': GameState.ASTEROIDS, 'y': 480},
    ]
    
    # Initialize hover state
    app.hoverIndex = -1
    
    # Initialize Pong variables
    initPong(app)
    
    # Initialize Breakout variables
    initBreakout(app)
    
    # Initialize Snake variables
    initSnake(app)
    
    # Initialize Pac-Man variables
    initPacman(app)
    
    # Initialize Asteroids variables
    initAsteroids(app)

def initPong(app):
    app.paddle1Y = app.height // 2
    app.paddle2Y = app.height // 2
    app.paddleHeight = 60
    app.paddleWidth = 10
    app.ballX = app.width // 2
    app.ballY = app.height // 2
    app.ballRadius = 10
    app.ballSpeedX = 5
    app.ballSpeedY = 5
    app.score1 = 0
    app.score2 = 0

def initBreakout(app):
    # Paddle properties
    app.breakoutPaddleWidth = 100
    app.breakoutPaddleHeight = 15
    app.breakoutPaddleY = app.height - 40
    app.breakoutPaddleX = app.width // 2
    app.paddleSpeed = 8  # Speed for keyboard controls
    
    # Ball properties
    app.breakoutBallRadius = 8
    app.breakoutBallX = app.width // 2
    app.breakoutBallY = app.height - 60
    app.breakoutBallSpeedX = 5
    app.breakoutBallSpeedY = -5
    
    # Brick properties
    app.brickRows = 6
    app.brickCols = 10
    app.brickWidth = (app.width - 100) // app.brickCols
    app.brickHeight = 25
    app.brickMarginX = 50
    app.brickColors = ['crimson', 'orange', 'gold', 'limeGreen', 'deepSkyBlue', 'mediumPurple']
    app.bricks = []
    
    # Visual effects
    app.particles = []
    app.glowEffect = 0
    app.gameOverTimer = 0
    
    # Initialize bricks with margin
    for row in range(app.brickRows):
        for col in range(app.brickCols):
            brick = {
                'x': col * app.brickWidth + app.brickMarginX,
                'y': row * app.brickHeight + 50,
                'color': app.brickColors[row],
                'visible': True,
                'strength': app.brickRows - row 
            }
            app.bricks.append(brick)
    
    # Game state
    app.breakoutScore = 0
    app.gameOver = False
    app.won = False

def initSnake(app):
    # Grid properties
    app.gridSize = 20
    app.rows = app.height // app.gridSize
    app.cols = app.width // app.gridSize
    
    # Snake properties
    app.snake = [(app.cols//2, app.rows//2)]  
    app.direction = (1, 0)
    app.nextDirection = (1, 0)
    app.snakeColor = 'limeGreen'
    app.moveCounter = 0 
    app.moveDelay = 4 
    
    # Food properties
    app.food = None
    app.foodColor = 'red'
    spawnFood(app)
    
    # Game state
    app.snakeScore = 0
    app.gameOver = False
    app.gameOverTimer = 0

def initPacman(app):
    # Grid properties
    app.cellSize = 20
    app.pacmanRows = app.height // app.cellSize
    app.pacmanCols = app.width // app.cellSize
    
    # Pac-Man maze layout (1 = wall, 0 = path, 2 = power pellet, 3 = ghost house door)
    app.maze = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,2,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,2,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
        [1,0,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,1,1,1,3,3,3,3,3,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,0,1,1,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,0,1,1,0,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,0,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1],
        [1,2,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,2,1],
        [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
        [1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,1],
        [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
    
    # Pacman properties
    app.pacmanX = 14 * app.cellSize 
    app.pacmanY = 23 * app.cellSize  
    app.pacmanDirection = (0, 0) 
    app.nextPacmanDirection = (0, 0) 
    app.pacmanMouthAngle = 45 
    app.pacmanMouthOpen = True 
    
    # Ghost properties (Blinky, Pinky, Inky, Clyde)
    app.ghosts = [
        {'x': 13 * app.cellSize, 'y': 14 * app.cellSize, 'color': 'red', 'direction': (-1, 0), 'released': True, 'exiting': False},
        {'x': 14 * app.cellSize, 'y': 14 * app.cellSize, 'color': 'pink', 'direction': (1, 0), 'released': False, 'exiting': False},
        {'x': 15 * app.cellSize, 'y': 14 * app.cellSize, 'color': 'cyan', 'direction': (0, -1), 'released': False, 'exiting': False},
        {'x': 16 * app.cellSize, 'y': 14 * app.cellSize, 'color': 'orange', 'direction': (0, 1), 'released': False, 'exiting': False}
    ]
    app.ghostMode = 'scatter' 
    app.ghostTimer = 0
    app.frightenedTimer = 0
    app.ghostReleaseTimer = 0
    
    # Game state
    app.pacmanScore = 0
    app.gameOver = False
    app.gameOverTimer = 0
    # Only count dots in valid positions (not in ghost house)
    app.dotsLeft = sum(1 for row in range(len(app.maze)) 
                      for col in range(len(app.maze[0])) 
                      if app.maze[row][col] == 0)
    app.powerPelletsLeft = sum(1 for row in range(len(app.maze)) 
                             for col in range(len(app.maze[0])) 
                             if app.maze[row][col] == 2)
    app.frozen = False  

def initAsteroids(app):
    # Ship properties
    app.shipX = app.width // 2
    app.shipY = app.height // 2
    app.shipAngle = 0  
    app.shipSpeed = 0
    app.shipDX = 0
    app.shipDY = 0
    app.thrustPower = 0.5
    app.friction = 0.99  
    app.rotateSpeed = 5
    app.shipRadius = 15
    app.invincible = False
    app.invincibleTimer = 0
    
    # Trail effect
    app.shipTrail = []  # List of {x, y, time} for trail points
    app.trailLifetime = 15  # 0.5 seconds at 30 FPS
    
    # Bullets
    app.bullets = []  
    app.bulletSpeed = 10
    app.bulletLifetime = 60  
    
    # Asteroids
    app.asteroids = []  
    app.asteroidSpeeds = {
        'large': 2,
        'medium': 3,
        'small': 4
    }
    app.asteroidSizes = {
        'large': 40,
        'medium': 20,
        'small': 10
    }
    # Spawn initial asteroids
    for _ in range(4):
        # Spawn at edges
        if random.random() < 0.5:
            x = random.choice([0, app.width])
            y = random.randint(0, app.height)
        else:
            x = random.randint(0, app.width)
            y = random.choice([0, app.height])
        
        dx = random.uniform(-2, 2)
        dy = random.uniform(-2, 2)
        app.asteroids.append({
            'x': x, 'y': y,
            'dx': dx, 'dy': dy,
            'size': 'large'
        })
    
    # Game state
    app.asteroidScore = 0
    app.gameOver = False
    app.gameOverTimer = 0
    app.lives = 3

def spawnFood(app):
    while True:
        x = random.randint(0, app.cols-1)
        y = random.randint(0, app.rows-1)
        if (x, y) not in app.snake:
            app.food = (x, y)
            break

def createParticles(app, x, y, color):
    for _ in range(10):
        particle = {
            'x': x,
            'y': y,
            'dx': random.uniform(-3, 3),
            'dy': random.uniform(-3, 3),
            'life': 1.0,
            'color': color,
            'size': random.randint(4, 8) 
        }
        app.particles.append(particle)

def redrawAll(app):
    if app.state == GameState.MENU:
        drawMenu(app)
    elif app.state == GameState.PONG:
        drawPong(app)
    elif app.state == GameState.BREAKOUT:
        drawBreakout(app)
    elif app.state == GameState.SNAKE:
        drawSnake(app)
    elif app.state == GameState.PACMAN:
        drawPacman(app)
    elif app.state == GameState.ASTEROIDS:
        drawAsteroids(app)
    # Other game states will be added here

def drawMenu(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    
    # Draw title
    drawLabel('ARCADE GAMES', app.width//2, 100, 
             fill='white', size=36, bold=True)
    
    # Draw buttons
    for button in app.buttons:
        buttonY = button['y']
        drawRect(app.width//2 - BUTTON_WIDTH//2, buttonY,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                fill='darkGray')
        drawLabel(button['text'], app.width//2, buttonY + BUTTON_HEIGHT//2,
                 fill='white', size=20)

def drawPong(app):
    # Draw background
    drawRect(0, 0, app.width, app.height, fill='black')
    
    # Draw center line
    drawLine(app.width//2, 0, app.width//2, app.height, 
             fill='white', lineWidth=2, dashes=True)
    
    # Draw paddles
    drawRect(30, app.paddle1Y - app.paddleHeight//2, 
             app.paddleWidth, app.paddleHeight, fill='white')
    drawRect(app.width - 30 - app.paddleWidth, 
             app.paddle2Y - app.paddleHeight//2,
             app.paddleWidth, app.paddleHeight, fill='white')
    
    # Draw ball
    drawCircle(app.ballX, app.ballY, app.ballRadius, fill='white')
    
    # Draw scores
    drawLabel(str(app.score1), app.width//4, 50, 
             fill='white', size=40, bold=True)
    drawLabel(str(app.score2), 3*app.width//4, 50, 
             fill='white', size=40, bold=True)
    
    # Draw back button
    drawRect(10, 10, 60, 30, fill='red')
    drawLabel('BACK', 40, 25, fill='white', bold=True)

def drawBreakout(app):
    # Draw background with gradient effect
    gradientSteps = 20
    for i in range(gradientSteps):
        y = i * (app.height / gradientSteps)
        height = app.height / gradientSteps
        progress = i / gradientSteps
        r = 10 + progress * 20
        g = 10 + progress * 20
        b = 40 + progress * 20
        drawRect(0, y, app.width, height + 1, fill=rgb(r, g, b))
    
    # Draw back button
    drawRect(10, 10, 60, 30, fill='red')
    drawLabel('BACK', 40, 25, fill='white', bold=True)
    
    # Draw score on the right
    drawLabel(f'Score: {app.breakoutScore}', app.width - 70, 25,
             fill='white', size=24, bold=True)
    
    # Draw particles
    for particle in app.particles:
        size = max(2, int(particle['size'] * particle['life']))  
        drawCircle(particle['x'], particle['y'], 
                  size, 
                  fill=rgb(255, 255, 255), opacity=int(particle['life'] * 100))
    
    # Draw paddle with glow effect
    paddleGlow = 20 + 5 * math.sin(app.glowEffect)
    drawCircle(app.breakoutPaddleX, app.breakoutPaddleY + app.breakoutPaddleHeight/2, 
              paddleGlow, fill=rgb(100, 200, 255), opacity=20)
    drawRect(app.breakoutPaddleX - app.breakoutPaddleWidth//2,
             app.breakoutPaddleY,
             app.breakoutPaddleWidth, app.breakoutPaddleHeight,
             fill='white', border=None)
    
    # Draw ball with trail effect
    drawCircle(app.breakoutBallX, app.breakoutBallY,
              app.breakoutBallRadius + 2, fill=rgb(255, 255, 255), opacity=40)
    drawCircle(app.breakoutBallX, app.breakoutBallY,
              app.breakoutBallRadius, fill='white')
    
    # Draw bricks with 3D effect
    for brick in app.bricks:
        if brick['visible']:
            # Draw brick shadow
            drawRect(brick['x']+2, brick['y']+2,
                    app.brickWidth-4, app.brickHeight-4,
                    fill=rgb(0, 0, 0), opacity=20)
            # Draw main brick
            drawRect(brick['x'], brick['y'],
                    app.brickWidth-4, app.brickHeight-4,
                    fill=brick['color'], border='white')
            # Draw strength number
            drawLabel(str(brick['strength']), 
                     brick['x'] + app.brickWidth//2, 
                     brick['y'] + app.brickHeight//2,
                     size=20, bold=True, 
                     fill='white')
    
    # Draw game over or win message
    if app.gameOver or app.won:
        message = 'Game Over!' if app.gameOver else 'You Won!'
        # Draw shadow
        drawLabel(message, app.width//2 + 2, app.height//2 + 2,
                 fill=rgb(0, 0, 0), opacity=60, size=50, bold=True)
        # Draw text
        drawLabel(message, app.width//2, app.height//2,
                 fill='white', size=50, bold=True)
        # Draw countdown message
        secondsLeft = max(1, 4 - int(app.gameOverTimer / 30))  
        drawLabel(f'Restarting in {secondsLeft}...', app.width//2, app.height//2 + 50,
                 fill='white', size=20)

def drawSnake(app):
    # Draw background
    drawRect(0, 0, app.width, app.height, fill='black')
    
    # Draw grid (more subtle)
    for row in range(app.rows):
        for col in range(app.cols):
            drawRect(col * app.gridSize, row * app.gridSize,
                    app.gridSize, app.gridSize,
                    fill=None, border=rgb(50, 50, 50))
    
    # Draw snake
    for i, (x, y) in enumerate(app.snake):
        # Calculate color gradient from head to tail
        progress = i / max(1, len(app.snake)-1)
        r = 0 + progress * 50
        g = 255 - progress * 100
        b = 0 + progress * 50
        
        # Draw segment with rounded corners
        centerX = x * app.gridSize + app.gridSize//2
        centerY = y * app.gridSize + app.gridSize//2
        radius = app.gridSize//2 - 2
        drawCircle(centerX, centerY, radius, fill=rgb(r, g, b))
        
        # Draw eyes on head
        if i == 0:
            # Determine eye positions based on direction
            dx, dy = app.direction
            eyeOffset = app.gridSize//4
            leftEye = (centerX - dy*eyeOffset, centerY + dx*eyeOffset)
            rightEye = (centerX + dy*eyeOffset, centerY - dx*eyeOffset)
            drawCircle(leftEye[0], leftEye[1], 3, fill='white')
            drawCircle(rightEye[0], rightEye[1], 3, fill='white')
    
    # Draw food with glow effect
    if app.food:
        foodX = app.food[0] * app.gridSize + app.gridSize//2
        foodY = app.food[1] * app.gridSize + app.gridSize//2
        # Glow
        glowSize = 3 + math.sin(app.gameOverTimer * 0.2) * 2
        drawCircle(foodX, foodY, app.gridSize//2 + glowSize, 
                  fill=rgb(255, 0, 0), opacity=20)
        # Food
        drawCircle(foodX, foodY, app.gridSize//2 - 2, fill='red')
    
    # Draw back button (on top of everything)
    drawRect(10, 10, 60, 30, fill='red')
    drawLabel('BACK', 40, 25, fill='white', bold=True)
    
    # Draw score
    drawLabel(f'Score: {app.snakeScore}', app.width - 70, 25,
             fill='white', size=24, bold=True)
    
    # Draw game over message
    if app.gameOver:
        # Draw shadow
        drawLabel('Game Over!', app.width//2 + 2, app.height//2 + 2,
                 fill=rgb(0, 0, 0), opacity=60, size=50, bold=True)
        # Draw text
        drawLabel('Game Over!', app.width//2, app.height//2,
                 fill='white', size=50, bold=True)
        # Draw countdown
        secondsLeft = max(1, 4 - int(app.gameOverTimer / 30))  
        drawLabel(f'Restarting in {secondsLeft}...', app.width//2, app.height//2 + 50,
                 fill='white', size=20)

def drawPacman(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    
    # Draw maze
    for row in range(len(app.maze)):
        for col in range(len(app.maze[0])):
            x = col * app.cellSize
            y = row * app.cellSize
            if app.maze[row][col] == 1:
                drawRect(x, y, app.cellSize, app.cellSize, fill='blue')
            elif app.maze[row][col] == 0: 
                drawCircle(x + app.cellSize//2, y + app.cellSize//2, 2, fill='white')
            elif app.maze[row][col] == 2:
                drawCircle(x + app.cellSize//2, y + app.cellSize//2, 6, fill='white')
            elif app.maze[row][col] == 3:
                drawRect(x, y, app.cellSize, app.cellSize, fill='black')
    
    # Draw Pac-Man
    mouthAngle = app.pacmanMouthAngle if app.pacmanMouthOpen else 5
    startAngle = mouthAngle/2
    sweepAngle = 360 - mouthAngle
    
    # Rotate based on direction
    if app.pacmanDirection == (1, 0):
        rotateAngle = 0
    elif app.pacmanDirection == (-1, 0):
        rotateAngle = 180
    elif app.pacmanDirection == (0, -1):
        rotateAngle = 90
    elif app.pacmanDirection == (0, 1):
        rotateAngle = 270
    else:
        rotateAngle = 0
    
    # Draw Pac-Man body with rotation
    drawArc(app.pacmanX + app.cellSize//2, app.pacmanY + app.cellSize//2, 
            app.cellSize - 4, app.cellSize - 4, 
            rotateAngle + startAngle, sweepAngle, fill='yellow')
    
    # Draw ghosts
    for ghost in app.ghosts:
        if app.ghostMode == 'frightened':
            color = 'blue'
        else:
            color = ghost['color']
        
        # Ghost body
        drawCircle(ghost['x'] + app.cellSize//2, ghost['y'] + app.cellSize//2 - 2,
                  app.cellSize//2 - 2, fill=color)
        drawRect(ghost['x'], ghost['y'] + app.cellSize//2 - 2,
                app.cellSize, app.cellSize//2, fill=color)
        
        # Ghost eyes
        eyeColor = 'white' if app.ghostMode != 'frightened' else 'white'
        pupilColor = 'blue' if app.ghostMode != 'frightened' else 'white'
        
        # Left eye
        drawCircle(ghost['x'] + app.cellSize//3, ghost['y'] + app.cellSize//2 - 2,
                  3, fill=eyeColor)
        drawCircle(ghost['x'] + app.cellSize//3, ghost['y'] + app.cellSize//2 - 2,
                  1.5, fill=pupilColor)
        
        # Right eye
        drawCircle(ghost['x'] + 2*app.cellSize//3, ghost['y'] + app.cellSize//2 - 2,
                  3, fill=eyeColor)
        drawCircle(ghost['x'] + 2*app.cellSize//3, ghost['y'] + app.cellSize//2 - 2,
                  1.5, fill=pupilColor)
    
    # Draw score and remaining dots
    drawLabel(f'Score: {app.pacmanScore}', app.width - 50, 20,
             fill='white', size=16)
    drawLabel(f'Dots Left: {app.dotsLeft}', app.width - 50, 40,
             fill='white', size=16)
    
    # Draw back button
    drawRect(10, 10, 60, 30, fill='darkGray')
    drawLabel('BACK', 40, 25, fill='white', size=14)
    
    # Draw game over or win
    if app.gameOver:
        message = 'You Win!' if app.dotsLeft == 0 else 'Game Over!'
        drawLabel(message, app.width//2, app.height//2,
                 fill='red' if message == 'Game Over!' else 'green', 
                 size=50, bold=True)
        secondsLeft = max(1, 4 - int(app.gameOverTimer / 30))
        drawLabel(f'Restarting in {secondsLeft}...', app.width//2, app.height//2 + 50,
                 fill='white', size=20)

def drawAsteroids(app):
    drawRect(0, 0, app.width, app.height, fill='black')
    
    # Draw ship if not game over
    if not app.gameOver:
        # Draw trail
        for point in app.shipTrail:
            age = app.stepsCount - point['time']
            if age < app.trailLifetime:
                size = 3 * (1 - (age / app.trailLifetime))  # Shrink from 3 to 0
                drawCircle(point['x'], point['y'], size,
                          fill='white')
        
        # Ship is a triangle
        angle = math.radians(app.shipAngle)
        tip = (app.shipX + app.shipRadius * math.sin(angle),
               app.shipY - app.shipRadius * math.cos(angle))
        left = (app.shipX + app.shipRadius * math.sin(angle + 2.6),
                app.shipY - app.shipRadius * math.cos(angle + 2.6))
        right = (app.shipX + app.shipRadius * math.sin(angle - 2.6),
                 app.shipY - app.shipRadius * math.cos(angle - 2.6))
        
        # Flash when invincible
        color = 'white' if not app.invincible or app.invincibleTimer % 10 < 5 else None
        if color:
            drawPolygon(tip[0], tip[1], left[0], left[1], right[0], right[1],
                       fill=None, border=color, borderWidth=2)
    
    # Draw bullets
    for bullet in app.bullets:
        drawCircle(bullet['x'], bullet['y'], 2, fill='white')
    
    # Draw asteroids
    for asteroid in app.asteroids:
        radius = app.asteroidSizes[asteroid['size']]
        drawCircle(asteroid['x'], asteroid['y'], radius, 
                  fill=None, border='white', borderWidth=2)
    
    # Draw score and lives
    drawLabel(f'Score: {app.asteroidScore}', app.width - 50, 20,
             fill='white', size=16)
    drawLabel(f'Lives: {app.lives}', app.width - 50, 40,
             fill='white', size=16)
    
    # Draw back button
    drawRect(10, 10, 60, 30, fill='darkGray')
    drawLabel('BACK', 40, 25, fill='white', size=14)
    
    # Draw game over
    if app.gameOver:
        drawLabel('Game Over!', app.width//2, app.height//2,
                 fill='red', size=50, bold=True)
        secondsLeft = max(1, 4 - int(app.gameOverTimer / 30))
        drawLabel(f'Restarting in {secondsLeft}...', app.width//2, app.height//2 + 50,
                 fill='white', size=20)

def onStep(app):
    global inFullScreenMode
    if (not inFullScreenMode and time.time() > goFullScreen):
        pygame.display. toggle_fullscreen()
        inFullScreenMode = True
    app.stepsCount += 1
    if app.state == GameState.PONG:
        # Move the ball
        app.ballX += app.ballSpeedX
        app.ballY += app.ballSpeedY
        
        # Ball collision with top and bottom
        if app.ballY - app.ballRadius <= 0 or app.ballY + app.ballRadius >= app.height:
            app.ballSpeedY = -app.ballSpeedY
        
        # Ball collision with paddles
        if (app.ballX - app.ballRadius <= 40 and 
            app.paddle1Y - app.paddleHeight//2 <= app.ballY <= app.paddle1Y + app.paddleHeight//2):
            app.ballSpeedX = -app.ballSpeedX
        
        if (app.ballX + app.ballRadius >= app.width - 40 and 
            app.paddle2Y - app.paddleHeight//2 <= app.ballY <= app.paddle2Y + app.paddleHeight//2):
            app.ballSpeedX = -app.ballSpeedX
        
        # Score points
        if app.ballX - app.ballRadius <= 0:
            app.score2 += 1
            resetBall(app)
        elif app.ballX + app.ballRadius >= app.width:
            app.score1 += 1
            resetBall(app)
    
    elif app.state == GameState.BREAKOUT:
        if app.gameOver or app.won:
            app.gameOverTimer += 1
            if app.gameOverTimer >= 90:
                initBreakout(app)
                return
        
        if not app.gameOver and not app.won:
            # Store previous position for collision detection
            prevX = app.breakoutBallX
            prevY = app.breakoutBallY
            
            # Update ball position
            app.breakoutBallX += app.breakoutBallSpeedX
            app.breakoutBallY += app.breakoutBallSpeedY
            
            # Update visual effects
            app.glowEffect += 0.1
            
            # Update particles
            for particle in app.particles[:]:
                particle['x'] += particle['dx']
                particle['y'] += particle['dy']
                particle['life'] -= 0.02
                if particle['life'] <= 0:
                    app.particles.remove(particle)
            
            # Ball collision with walls
            if (app.breakoutBallX - app.breakoutBallRadius <= 0 or
                app.breakoutBallX + app.breakoutBallRadius >= app.width):
                app.breakoutBallSpeedX = -app.breakoutBallSpeedX
            
            if app.breakoutBallY - app.breakoutBallRadius <= 0:
                app.breakoutBallSpeedY = -app.breakoutBallSpeedY
            
            # Ball collision with paddle
            if (app.breakoutBallY + app.breakoutBallRadius >= app.breakoutPaddleY and
                app.breakoutBallY - app.breakoutBallRadius <= app.breakoutPaddleY + app.breakoutPaddleHeight and
                app.breakoutPaddleX - app.breakoutPaddleWidth//2 <= app.breakoutBallX <= 
                app.breakoutPaddleX + app.breakoutPaddleWidth//2):
                app.breakoutBallSpeedY = -abs(app.breakoutBallSpeedY)
                # Adjust ball direction based on where it hits the paddle
                hitPos = (app.breakoutBallX - (app.breakoutPaddleX - app.breakoutPaddleWidth//2)) / app.breakoutPaddleWidth
                app.breakoutBallSpeedX = 8 * (hitPos - 0.5)
                createParticles(app, app.breakoutBallX, app.breakoutBallY, 'white')
            
            # Ball collision with bricks
            for brick in app.bricks:
                if brick['visible']:
                    brickLeft = brick['x']
                    brickRight = brick['x'] + app.brickWidth
                    brickTop = brick['y']
                    brickBottom = brick['y'] + app.brickHeight
                    ballLeft = app.breakoutBallX - app.breakoutBallRadius
                    ballRight = app.breakoutBallX + app.breakoutBallRadius
                    ballTop = app.breakoutBallY - app.breakoutBallRadius
                    ballBottom = app.breakoutBallY + app.breakoutBallRadius
                    
                    # Check if ball overlaps with brick
                    if (ballRight >= brickLeft and ballLeft <= brickRight and
                        ballBottom >= brickTop and ballTop <= brickBottom):
                        
                        # Determine which side of the brick was hit
                        prevRight = prevX + app.breakoutBallRadius
                        prevLeft = prevX - app.breakoutBallRadius
                        prevTop = prevY - app.breakoutBallRadius
                        prevBottom = prevY + app.breakoutBallRadius
                        
                        # Hit from left or right
                        if (prevRight <= brickLeft or prevLeft >= brickRight):
                            app.breakoutBallSpeedX = -app.breakoutBallSpeedX
                        # Hit from top or bottom
                        else:
                            app.breakoutBallSpeedY = -app.breakoutBallSpeedY
                        
                        # Handle brick damage and destruction
                        brick['strength'] -= 1
                        if brick['strength'] <= 0:
                            brick['visible'] = False
                            createParticles(app, app.breakoutBallX, app.breakoutBallY, brick['color'])
                            app.breakoutScore += 10
                        break  # Only handle one brick collision per frame
            
            # Check for game over
            if app.breakoutBallY + app.breakoutBallRadius >= app.height:
                app.gameOver = True
                app.gameOverTimer = 0
            
            # Check for win
            if all(not brick['visible'] for brick in app.bricks):
                app.won = True
                app.gameOverTimer = 0
    
    elif app.state == GameState.SNAKE:
        if app.gameOver:
            app.gameOverTimer += 1
            if app.gameOverTimer >= 90:
                initSnake(app)
                return
        
        if not app.gameOver:
            # Update food glow animation
            app.gameOverTimer += 1
            
            # Slow down snake movement
            app.moveCounter += 1
            if app.moveCounter < app.moveDelay:
                return
            app.moveCounter = 0
            
            # Update direction
            app.direction = app.nextDirection
            
            # Get new head position
            oldHead = app.snake[0]
            newHead = (oldHead[0] + app.direction[0],
                      oldHead[1] + app.direction[1])
            
            # Check for collisions with walls
            if (newHead[0] < 0 or newHead[0] >= app.cols or
                newHead[1] < 0 or newHead[1] >= app.rows):
                app.gameOver = True
                app.gameOverTimer = 0
                return
            
            # Check for collisions with self
            if newHead in app.snake:
                app.gameOver = True
                app.gameOverTimer = 0
                return
            
            # Move snake
            app.snake.insert(0, newHead)
            
            # Check for food
            if newHead == app.food:
                app.snakeScore += 10
                spawnFood(app)
            else:
                app.snake.pop()

    elif app.state == GameState.PACMAN:
        if app.gameOver:
            app.gameOverTimer += 1
            if app.gameOverTimer >= 90:
                initPacman(app)
                return
            if app.frozen:
                return
        
        # Animate Pac-Man's mouth
        if app.pacmanMouthOpen:
            app.pacmanMouthAngle += 5
            if app.pacmanMouthAngle >= 45:
                app.pacmanMouthOpen = False
        else:
            app.pacmanMouthAngle -= 5
            if app.pacmanMouthAngle <= 5:
                app.pacmanMouthOpen = True
        
        # Release ghosts one by one
        app.ghostReleaseTimer += 1
        if app.ghostReleaseTimer >= 180:
            app.ghostReleaseTimer = 0
            # Find next unreleased ghost
            for ghost in app.ghosts:
                if not ghost['released']:
                    ghost['released'] = True
                    ghost['exiting'] = True
                    ghost['direction'] = (0, -1)
                    break
        
        # Move Pac-Man
        newX = app.pacmanX + app.pacmanDirection[0] * app.cellSize
        newY = app.pacmanY + app.pacmanDirection[1] * app.cellSize
        
        # Handle tunnel teleportation
        if newX < 0:
            newX = (len(app.maze[0]) - 1) * app.cellSize
        elif newX >= len(app.maze[0]) * app.cellSize:
            newX = 0
        elif newY < 0:
            newY = (len(app.maze) - 1) * app.cellSize
        elif newY >= len(app.maze) * app.cellSize:
            newY = 0
        
        # Check if new position is valid (not wall or ghost house door)
        gridX = int(newX / app.cellSize)
        gridY = int(newY / app.cellSize)
        
        if 0 <= gridX < len(app.maze[0]) and 0 <= gridY < len(app.maze):
            if app.maze[gridY][gridX] != 1 and app.maze[gridY][gridX] != 3:
                app.pacmanX = newX
                app.pacmanY = newY
                
                # Check for dot collection
                if app.maze[gridY][gridX] == 0:
                    app.maze[gridY][gridX] = -1
                    app.pacmanScore += 10
                    app.dotsLeft -= 1
                elif app.maze[gridY][gridX] == 2:
                    app.maze[gridY][gridX] = -1
                    app.pacmanScore += 50
                    app.powerPelletsLeft -= 1
                    app.ghostMode = 'frightened'
                    app.frightenedTimer = 0
        
        # Move ghosts
        for ghost in app.ghosts:
            if not ghost['released']:
                continue
            
            if ghost['exiting']:
                # Guide ghost out of the house
                if ghost['y'] > 11 * app.cellSize:
                    ghost['y'] -= app.cellSize
                else:
                    ghost['exiting'] = False
                    ghost['direction'] = (-1, 0)
                continue
            
            # Normal ghost movement
            newX = ghost['x'] + ghost['direction'][0] * app.cellSize
            newY = ghost['y'] + ghost['direction'][1] * app.cellSize
            
            # Handle ghost tunnel teleportation
            if newX < 0:
                newX = (len(app.maze[0]) - 1) * app.cellSize
            elif newX >= len(app.maze[0]) * app.cellSize:
                newX = 0
            elif newY < 0:
                newY = (len(app.maze) - 1) * app.cellSize
            elif newY >= len(app.maze) * app.cellSize:
                newY = 0
            
            gridX = int(newX / app.cellSize)
            gridY = int(newY / app.cellSize)
            
            if (0 <= gridX < len(app.maze[0]) and 0 <= gridY < len(app.maze) and
                app.maze[gridY][gridX] != 1 and
                (app.maze[gridY][gridX] != 3 or not ghost['released'])):
                ghost['x'] = newX
                ghost['y'] = newY
            else:
                # Change direction randomly if hit wall
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                ghost['direction'] = random.choice(directions)
        
        # Check for collision with ghosts
        for ghost in app.ghosts:
            if (abs(ghost['x'] - app.pacmanX) < app.cellSize and
                abs(ghost['y'] - app.pacmanY) < app.cellSize):
                if app.ghostMode == 'frightened':
                    # Reset ghost position
                    ghost['x'] = 14 * app.cellSize
                    ghost['y'] = 14 * app.cellSize
                    ghost['released'] = False
                    app.pacmanScore += 200
                else:
                    app.gameOver = True
                    app.frozen = True
                    return
        
        # Update ghost mode
        if app.ghostMode == 'frightened':
            app.frightenedTimer += 1
            if app.frightenedTimer >= 150:
                app.ghostMode = 'scatter'
                app.frightenedTimer = 0
        
        # Check win condition
        if app.dotsLeft == 0 and app.powerPelletsLeft == 0:
            app.gameOver = True
            app.frozen = True 

    elif app.state == GameState.ASTEROIDS:
        if app.gameOver:
            app.gameOverTimer += 1
            if app.gameOverTimer >= 90: 
                initAsteroids(app)
                return
        
        # Update ship position
        app.shipX += app.shipDX
        app.shipY += app.shipDY
        
        # Wrap around screen
        app.shipX = app.shipX % app.width
        app.shipY = app.shipY % app.height
        
        # Apply friction
        app.shipDX *= app.friction
        app.shipDY *= app.friction
        
        # Update invincibility
        if app.invincible:
            app.invincibleTimer += 1
            if app.invincibleTimer >= 90: 
                app.invincible = False
                app.invincibleTimer = 0
        
        # Update bullets
        for bullet in app.bullets[:]:  
            bullet['x'] += bullet['dx']
            bullet['y'] += bullet['dy']
            bullet['x'] = bullet['x'] % app.width
            bullet['y'] = bullet['y'] % app.height
            bullet['age'] += 1
            if bullet['age'] >= app.bulletLifetime:
                app.bullets.remove(bullet)
        
        # Update asteroids
        for asteroid in app.asteroids[:]:  
            asteroid['x'] += asteroid['dx']
            asteroid['y'] += asteroid['dy']
            asteroid['x'] = asteroid['x'] % app.width
            asteroid['y'] = asteroid['y'] % app.height
            
            # Check collision with bullets
            for bullet in app.bullets[:]:
                if (distance(bullet['x'], bullet['y'], 
                           asteroid['x'], asteroid['y']) < 
                    app.asteroidSizes[asteroid['size']]):
                    app.bullets.remove(bullet)
                    app.asteroids.remove(asteroid)
                    
                    # Add score based on size
                    if asteroid['size'] == 'large':
                        app.asteroidScore += 20
                    elif asteroid['size'] == 'medium':
                        app.asteroidScore += 50
                    else: 
                        app.asteroidScore += 100
                    
                    # Split asteroid if not smallest
                    if asteroid['size'] != 'small':
                        newSize = 'medium' if asteroid['size'] == 'large' else 'small'
                        speed = app.asteroidSpeeds[newSize]
                        # Create two smaller asteroids
                        for _ in range(2):
                            angle = random.uniform(0, math.pi * 2)
                            app.asteroids.append({
                                'x': asteroid['x'],
                                'y': asteroid['y'],
                                'dx': speed * math.cos(angle),
                                'dy': speed * math.sin(angle),
                                'size': newSize
                            })
                    break
            
            # Check collision with ship
            if not app.invincible and not app.gameOver:
                if (distance(app.shipX, app.shipY,
                           asteroid['x'], asteroid['y']) <
                    app.asteroidSizes[asteroid['size']] + app.shipRadius):
                    app.lives -= 1
                    if app.lives <= 0:
                        app.gameOver = True
                    else:
                        # Reset ship position and make invincible
                        app.shipX = app.width // 2
                        app.shipY = app.height // 2
                        app.shipDX = 0
                        app.shipDY = 0
                        app.invincible = True
                        app.invincibleTimer = 0
        
        # Spawn new asteroids if none left
        if len(app.asteroids) == 0:
            for _ in range(4):
                if random.random() < 0.5:
                    x = random.choice([0, app.width])
                    y = random.randint(0, app.height)
                else:
                    x = random.randint(0, app.width)
                    y = random.choice([0, app.height])
                
                dx = random.uniform(-2, 2)
                dy = random.uniform(-2, 2)
                app.asteroids.append({
                    'x': x, 'y': y,
                    'dx': dx, 'dy': dy,
                    'size': 'large'
                })
        
        # Add trail point when thrusting
        if 'up' in app.heldKeys:
            angle = math.radians(app.shipAngle)
            trailX = app.shipX - 15 * math.sin(angle)  # Behind the ship
            trailY = app.shipY + 15 * math.cos(angle)
            app.shipTrail.append({
                'x': trailX,
                'y': trailY,
                'time': app.stepsCount
            })
        
        # Clean up old trail points
        app.shipTrail = [p for p in app.shipTrail 
                        if app.stepsCount - p['time'] < app.trailLifetime]

def resetBall(app):
    app.ballX = app.width // 2
    app.ballY = app.height // 2
    app.ballSpeedX = 5 * (1 if app.ballSpeedX > 0 else -1)
    app.ballSpeedY = 5

def onMouseMove(app, mouseX, mouseY):
    if app.state == GameState.MENU:
        # Check if mouse is over any button
        for i, button in enumerate(app.buttons):
            buttonY = button['y']
            if (app.width//2 - BUTTON_WIDTH//2 <= mouseX <= app.width//2 + BUTTON_WIDTH//2 and
                buttonY <= mouseY <= buttonY + BUTTON_HEIGHT):
                app.hoverIndex = i
                return
        app.hoverIndex = -1

def onMousePress(app, mouseX, mouseY):
    if app.state == GameState.MENU:
        for button in app.buttons:
            buttonY = button['y']
            if (app.width//2 - BUTTON_WIDTH//2 <= mouseX <= app.width//2 + BUTTON_WIDTH//2 and
                buttonY <= mouseY <= buttonY + BUTTON_HEIGHT):
                app.state = button['state']
                return
    
    elif app.state == GameState.PONG:
        # Check if back button was clicked
        if 10 <= mouseX <= 70 and 10 <= mouseY <= 40:
            app.state = GameState.MENU
    
    elif app.state == GameState.BREAKOUT:
        # Check if back button was clicked
        if 10 <= mouseX <= 70 and 10 <= mouseY <= 40:
            app.state = GameState.MENU
            initBreakout(app)  
    
    elif app.state == GameState.SNAKE:
        # Check if back button was clicked
        if 10 <= mouseX <= 70 and 10 <= mouseY <= 40:
            app.state = GameState.MENU
            initSnake(app)  
    
    elif app.state == GameState.PACMAN:
        # Check if back button was clicked
        if (10 <= mouseX <= 70 and 10 <= mouseY <= 40):
            app.state = GameState.MENU

    elif app.state == GameState.ASTEROIDS:
        # Check if back button was clicked
        if (10 <= mouseX <= 70 and 10 <= mouseY <= 40):
            app.state = GameState.MENU

def onKeyHold(app, keys):
    app.heldKeys = set(keys)
    if app.state == GameState.PONG:
        # Left paddle controls (W/S)
        if 'w' in keys and app.paddle1Y > app.paddleHeight//2:
            app.paddle1Y -= 5
        if 's' in keys and app.paddle1Y < app.height - app.paddleHeight//2:
            app.paddle1Y += 5
        
        # Right paddle controls (Up/Down arrows)
        if 'up' in keys and app.paddle2Y > app.paddleHeight//2:
            app.paddle2Y -= 5
        if 'down' in keys and app.paddle2Y < app.height - app.paddleHeight//2:
            app.paddle2Y += 5
    
    elif app.state == GameState.SNAKE and not app.gameOver:
        # Only allow 90-degree turns
        if 'left' in keys and app.direction[0] == 0:
            app.nextDirection = (-1, 0)
        elif 'right' in keys and app.direction[0] == 0:
            app.nextDirection = (1, 0)
        elif 'up' in keys and app.direction[1] == 0:
            app.nextDirection = (0, -1)
        elif 'down' in keys and app.direction[1] == 0:
            app.nextDirection = (0, 1)

    elif app.state == GameState.ASTEROIDS:
        if 'left' in keys:
            app.shipAngle -= app.rotateSpeed
        if 'right' in keys:
            app.shipAngle += app.rotateSpeed
        if 'up' in keys:
            # Add thrust in direction ship is pointing
            angle = math.radians(app.shipAngle)
            app.shipDX += app.thrustPower * math.sin(angle)
            app.shipDY -= app.thrustPower * math.cos(angle)

    elif app.state == GameState.BREAKOUT:
        # Move paddle with arrow keys
        if 'left' in keys:
            app.breakoutPaddleX = max(app.breakoutPaddleWidth//2, 
                                    app.breakoutPaddleX - app.paddleSpeed)
        if 'right' in keys:
            app.breakoutPaddleX = min(app.width - app.breakoutPaddleWidth//2, 
                                    app.breakoutPaddleX + app.paddleSpeed)

def onKeyPress(app, key):
    if app.state == GameState.MENU:
        pass
    elif app.state == GameState.PONG:
        pass
    elif app.state == GameState.BREAKOUT:
        pass
    elif app.state == GameState.SNAKE:
        pass
    elif app.state == GameState.PACMAN:
        if key == 'left':
            app.pacmanDirection = (-1, 0)
        elif key == 'right':
            app.pacmanDirection = (1, 0)
        elif key == 'up':
            app.pacmanDirection = (0, -1)
        elif key == 'down':
            app.pacmanDirection = (0, 1)
        elif key == 'b':
            app.state = GameState.MENU

    elif app.state == GameState.ASTEROIDS:
        if key == 'space':
            # Shoot bullet in direction ship is pointing
            angle = math.radians(app.shipAngle)
            app.bullets.append({
                'x': app.shipX,
                'y': app.shipY,
                'dx': app.bulletSpeed * math.sin(angle),
                'dy': -app.bulletSpeed * math.cos(angle),
                'age': 0
            })
        elif key == 'b':
            app.state = GameState.MENU

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def main():
    runApp(width=800, height=600)

main()
