import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOT_COOLDOWN
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = pygame.Vector2(0, -1).rotate(self.rotation + 90) * self.radius / 1.2
        a = self.position + forward * self.radius * 1.3
        b = self.position - forward * self.radius * 0.8 - right
        c = self.position - forward * self.radius * 0.8 + right
        return [a, b, c]

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Decrease the cooldown timer
        if self.cooldown > 0:
            self.cooldown -= dt
        
        # Arrow keys (primary controls)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rotation -= PLAYER_TURN_SPEED * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rotation += PLAYER_TURN_SPEED * dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move(dt, 1) 
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move(dt, -1)  
        if keys[pygame.K_SPACE]:
            self.shoot()
    
    def move(self, dt, direction):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt * direction

    def shoot(self):
        # Prevent shooting if cooldown is active
        if self.cooldown > 0:
            return
            
        # Create a new shot at the position of the player
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        
        # Set the cooldown timer
        self.cooldown = PLAYER_SHOT_COOLDOWN