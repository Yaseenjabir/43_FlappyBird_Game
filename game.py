import pygame as pg
import sys, time
from bird import Bird
from pipe import Pipe

pg.init()
pg.mixer.init()


class Game:
    def __init__(self):
        self.width = 600
        self.height = 700
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))

        self.clock = pg.time.Clock()
        self.move_speed = 200

        self.bird = Bird(self.scale_factor)
        self.isEnteredPress = False

        self.pipes = []
        self.pipe_generate_counter = 99

        self.check_monitoring = False

        self.score = 0
        self.font = pg.font.Font("assets/font.ttf", 24)
        self.score_text = self.font.render("Score : 0", True, (255, 0, 0))
        self.score_rect = self.score_text.get_rect(center=(300, 10))

        self.restart_text = self.font.render("Restart", True, (255, 0, 0))
        self.restart_rect = self.restart_text.get_rect(center=(300, 650))

        self.is_game_started = True

        self.flap_sound = pg.mixer.Sound("assets/sfx/flap.wav")
        self.score_sound = pg.mixer.Sound("assets/sfx/score.mp3")
        self.background_music = pg.mixer.Sound("assets/sfx/background.mp3")

        self.move_speed_counter = 0
        self.setupGroundandBG()

        self.gameLoop()

    def gameLoop(self):
        self.background_music.play(loops=-1)
        last_time = time.time()
        while True:
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time
            self.move_speed_counter += 1
            print(self.move_speed)
            if self.move_speed_counter == 300:
                self.move_speed += 20
                self.move_speed_counter = 0

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN and self.is_game_started:
                    if event.key == pg.K_RETURN:

                        self.isEnteredPress = True
                        self.bird.update_on = True

                    if event.key == pg.K_SPACE and self.isEnteredPress:
                        self.bird.flap(dt)
                        self.flap_sound.play()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.restart_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()

            self.updateEverthing(dt)
            self.checkCollision()
            self.checkScore()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def restartGame(self):
        self.score = 0
        self.score_text = self.font.render("Score : 0", True, (255, 0, 0))
        self.isEnteredPress = False
        self.is_game_started = True
        self.bird.reset()
        self.pipes.clear()
        self.pipe_generate_counter = 99
        self.move_speed = 200

    def checkScore(self):
        if len(self.pipes) > 0:

            if (
                self.bird.rect.left > self.pipes[0].rect_down.left
                and self.bird.rect.right < self.pipes[0].rect_down.right
                and not self.check_monitoring
            ):

                self.check_monitoring = True
            if (
                self.bird.rect.left > self.pipes[0].rect_down.right
                and self.check_monitoring
            ):

                self.check_monitoring = False
                self.score += 1
                self.score_sound.play()
                self.score_text = self.font.render(
                    f"Score : {self.score}", True, (255, 0, 0)
                )

    def checkCollision(self):
        if len(self.pipes):
            if self.bird.rect.bottom > 500:
                self.bird.update_on = False
                self.isEnteredPress = False
                self.is_game_started = False

            if self.bird.rect.colliderect(
                self.pipes[0].rect_down
            ) or self.bird.rect.colliderect(self.pipes[0].rect_up):
                self.is_game_started = False
                self.isEnteredPress = False

    def updateEverthing(self, dt):
        if self.isEnteredPress:
            # Moving the ground
            self.ground1_rect.x -= int(self.move_speed * dt)
            self.ground2_rect.x -= int(self.move_speed * dt)

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            #  Generating pipes
            if self.pipe_generate_counter > 130:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0
            self.pipe_generate_counter += 1

            # moving the pipes
            for pipe in self.pipes:
                pipe.update(dt)

            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)

            # moving the bird
        self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_image, (0, -300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)
        self.win.blit(self.score_text, self.score_rect)
        if not self.is_game_started:
            self.win.blit(self.restart_text, self.restart_rect)

    def setupGroundandBG(self):
        self.bg_image = pg.transform.scale_by(
            pg.image.load("assets/bg.png").convert(), self.scale_factor
        )
        self.ground1_img = pg.transform.scale_by(
            pg.image.load("assets/ground.png").convert(), self.scale_factor
        )
        self.ground2_img = pg.transform.scale_by(
            pg.image.load("assets/ground.png").convert(), self.scale_factor
        )

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 500
        self.ground2_rect.y = 500


game = Game()
