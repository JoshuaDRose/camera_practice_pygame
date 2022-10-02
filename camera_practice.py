import pygame, sys
from random import randint

class Tree(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,group):
		super().__init__(group)
		self.image = pygame.image.load('graphics/player.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        
        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        # box setup
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        # ground
        self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft=(0,0))
    
        # camera speed
        self.keyboard_speed = 5

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left'] 
        self.offset.y = self.camera_rect.top - self.camera_borders['top'] 

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_a]:
        #     self.offset.x -= self.keyboard_speed
        # if keys[pygame.K_d]:
        #     self.offset.x += self.keyboard_speed
        # if keys[pygame.K_w]:
        #     self.offset.y -= self.keyboard_speed
        # if keys[pygame.K_s]:
        #     self.offset.y += self.keyboard_speed

        # keyboard control + box camera
        if keys[pygame.K_a]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]:
            self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left'] 
        self.offset.y = self.camera_rect.top - self.camera_borders['top'] 

    def keyboard_control2(self, target):
        # 이게 더 나은거 아냐! (이건 box camera를 keyboard_control에 붙여서 구현!)
        keys = pygame.key.get_pressed()

        # keyboard control + box camera
        if keys[pygame.K_a]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]:
            self.camera_rect.y += self.keyboard_speed

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left'] 
        self.offset.y = self.camera_rect.top - self.camera_borders['top'] 

    def custom_draw(self, player):
        # key camera
        self.keyboard_control()

        # box camera
        self.box_target_camera(player)

        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        # pygame.draw.rect(self.display_surface, 'yellow', self.camera_rect, 5)

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

# setup 
camera_group = CameraGroup()
player = Player((640,360),camera_group)

for i in range(20):
	random_x = randint(1000,2000)
	random_y = randint(1000,2000)
	Tree((random_x,random_y),camera_group)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill('#71ddee')

	camera_group.update()
	camera_group.custom_draw(player)

	pygame.display.update()
	clock.tick(60)
