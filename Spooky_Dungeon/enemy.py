import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, images):
        super().__init__()
        self.images = images
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.direction = 1  # 1 = right, -1 = left
        self.animation_speed = 0.1
        self.animation_timer = 0

    def update(self, dt):
        # Move enemy
        self.rect.x += self.speed * self.direction
        
        # Reverse direction when hitting the screen edges
        if self.rect.left <= 0 or self.rect.right >= 800:
            self.direction *= -1
        
        # Animate enemy
        self.animate(dt)

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)



# Load your enemy sprite frames like this:
enemy_images = [pygame.image.load('sprite1.png'), pygame.image.load('sprite2.png')]
enemy = Enemy(100, 300, enemy_images)

# In your game loop:
enemy.update(dt)
enemy.draw(screen)
