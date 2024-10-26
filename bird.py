import pygame as pg


class Bird(pg.sprite.Sprite):
    def __init__(self, scaleFactor):
        super(Bird, self).__init__()
        self.img_list = [
            pg.transform.scale_by(
                pg.image.load("assets/birdup.png").convert_alpha(), scaleFactor
            ),
            pg.transform.scale_by(
                pg.image.load("assets/birddown.png").convert_alpha(), scaleFactor
            ),
        ]
        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.rect = self.image.get_rect(center=(100, 100))
        self.y_velocity = 0
        self.gravity = 10
        self.flappySpeed = 200
        self.image_counter = 0
        self.update_on = False

    def update(self, dt):
        if self.update_on:
            self.playAnimation()
            self.applyGravity(dt)

            if self.rect.y <= 0 and self.flappySpeed == 200:
                self.rect.y = 0
                self.flappySpeed = 0
                self.y_velocity = 0
            elif self.rect.y > 0 and self.flappySpeed == 0:
                self.flappySpeed = 200

    def applyGravity(self, dt):
        self.y_velocity += self.gravity * dt
        self.rect.y += self.y_velocity

    def flap(self, dt):
        self.y_velocity -= self.flappySpeed * dt

    def playAnimation(self):
        if self.image_counter == 5:
            self.image = self.img_list[self.image_index]
            if self.image_index == 0:
                self.image_index = 1
            else:
                self.image_index = 0
            self.image_counter = 0
        self.image_counter += 1

    def reset(self):
        self.rect.center = (100, 100)
        self.y_velocity = 0
