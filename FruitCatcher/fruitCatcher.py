import pygame
from sys import exit
from random import randint,choice
import time

pygame.init()
screen = pygame.display.set_mode((1200,600))
pygame.display.set_caption("FruitCatcher")
clock = pygame.time.Clock()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 300)
bomb_exploded = pygame.image.load("objects/bomb_exploded.png").convert_alpha()
game_active = False
start_bg = pygame.image.load("start_bg.jpg").convert_alpha()
flag = False
score = 0
collision = False
bg_music = pygame.mixer.Sound("music/bg_music.mp3")
apple_pickup = pygame.mixer.Sound("music/apple_sound.mp3")
bomb_sound = pygame.mixer.Sound("music/bomb_sound.mp3")
bg_music.set_volume(0.15)
bg_music.play(-1)


bg_surface = pygame.image.load("background.png").convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        farmer_right_1 = pygame.image.load("player/farmer_right_1.png").convert_alpha()
        farmer_right_2 = pygame.image.load("player/farmer_right_2.png").convert_alpha()
        farmer_right_3 = pygame.image.load("player/farmer_right_3.png").convert_alpha()

        self.farmer_stand = pygame.image.load("player/farmer_stand.png").convert_alpha()

        farmer_left_1 = pygame.image.load("player/farmer_left_1.png").convert_alpha()
        farmer_left_2 = pygame.image.load("player/farmer_left_2.png").convert_alpha()
        farmer_left_3 = pygame.image.load("player/farmer_left_3.png").convert_alpha()

        self.farmer_right_frames = [farmer_right_1,farmer_right_2,farmer_right_3]
        self.farmer_left_frames = [farmer_left_1,farmer_left_2,farmer_left_3]
        self.farmer_animation_index = 0.9
        self.image = self.farmer_stand
        self.rect = self.image.get_rect(midbottom=(100,535),height=100,width=50)
    def player_movement_animation(self):
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_d]):
            self.farmer_animation_index += 0.1
            if(self.farmer_animation_index > len(self.farmer_right_frames)):self.farmer_animation_index = 0
            self.image = self.farmer_right_frames[int(self.farmer_animation_index)]
            self.rect.right += 5

        elif(keys[pygame.K_a]):
            self.farmer_animation_index += 0.1
            if(self.farmer_animation_index > len(self.farmer_left_frames)):self.farmer_animation_index = 0
            self.image = self.farmer_left_frames[int(self.farmer_animation_index)]
            self.rect.left -= 5

        else:
            self.image = self.farmer_stand

    def player_check_boundaries(self):
        if(self.rect.right > 1200):
            self.rect.right = 1200

        elif(self.rect.left < 0):
            self.rect.left = 0


    def player_to_origin(self):
        if(collision):
            self.rect.left = 100


    def update(self):
        self.player_movement_animation()
        self.player_check_boundaries()
        self.player_to_origin()

def collision_sprites():
    global game_active,flag
    spare = False
    i = pygame.sprite.spritecollide(player.sprite, objects, False)
    if(i):
        if(i[0].type == "bomb"):
            i[0].image = bomb_exploded
            bomb_sound.play()
            screen.blit(i[0].image, i[0].rect)
            time.sleep(0.7)
            spare = True
            if(spare):
                flag = True
                collision = True
                game_active = False
                objects.empty()


    
def score_calculation():
    global score
    j = pygame.sprite.spritecollide(player.sprite, objects, True)
    if(j):
        if(j[0].type == "apple"):
            apple_pickup.play()
            score += 1



                


class Font:
    def __init__(self):
        self.font1 = pygame.font.Font("AlegreyaSans-Black.ttf", 90)
        self.font2 = pygame.font.Font("AlegreyaSans-Black.ttf", 50)
        self.font3 = pygame.font.Font("AlegreyaSans-Black.ttf", 30)

    def start_screen(self):
        self.start_screen_text = self.font1.render("FRUIT CATCHER BY  TheReign", True, "#F1FF03")
        self.start_screen_text_rect = self.start_screen_text.get_rect(center=(600,80))
        start_screen_rect = pygame.draw.rect(screen, "red", self.start_screen_text_rect)
        screen.blit(self.start_screen_text, self.start_screen_text_rect)


    def game_start_button(self):
        self.start_game_button = self.font2.render("PRESS ENTER TO START THE GAME", True, "yellow")
        self.start_game_button_rect = self.start_game_button.get_rect(center=(600,500))
        start_game_border = pygame.draw.rect(screen, "green", self.start_game_button_rect)
        screen.blit(self.start_game_button, self.start_game_button_rect)

    def score_display(self):
        score_text = self.font3.render(f"SCORE:{score}", True,"red")
        score_text_rect = score_text.get_rect(center=(900,580))
        score_display_frame = pygame.draw.rect(screen,"green", score_text_rect)
        screen.blit(score_text, score_text_rect)

    def game_end_screen(self):
        self.game_end_screen_text = self.font2.render(f"YOUR SCORE IS: {score}", True, "red")
        self.game_end_screen_text_rect = self.game_end_screen_text.get_rect(center=(600,100))
        end_screen_border = pygame.draw.rect(screen, "green", self.game_end_screen_text_rect)

        self.start_game_button = self.font2.render("PRESS ENTER TO CONTINUE", True, "yellow")
        self.start_game_button_rect = self.start_game_button.get_rect(center=(600,500))
        start_game_border = pygame.draw.rect(screen, "green", self.start_game_button_rect)

        screen.blit(self.game_end_screen_text, self.game_end_screen_text_rect)
        screen.blit(self.start_game_button, self.start_game_button_rect)






font = Font()


class object(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        self.apple = pygame.image.load("objects/apple.png").convert_alpha()
        self.bomb_normal = pygame.image.load("objects/bomb.png").convert_alpha()
        self.gravity = 5
        if(type == "apple"):
            self.image = self.apple
            self.type = "apple"

        else:
            self.image = self.bomb_normal
            self.type = "bomb"

        self.rect = self.image.get_rect(topleft=(randint(0,1200),randint(-100,100)),height=10,width=20)


    def apply_gravity_objects(self):
        self.rect.top += self.gravity

    def object_remove(self):
        if(self.rect.bottom > 520):
            self.kill()


                
                

    def update(self):
        self.apply_gravity_objects()
        self.object_remove()

player = pygame.sprite.GroupSingle()
player.add(Player())

objects = pygame.sprite.Group()


while True:
    pygame.mixer.unpause()
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.quit()
            exit()

        if game_active:
            if(event.type == obstacle_timer):
                objects.add(object(choice(["apple","bomb"])))

        else:
            if(event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                game_active = True
                score = 0


    if game_active:
        screen.blit(bg_surface, (0,0))
        font.score_display()
        player.draw(screen)
        player.update()
        objects.draw(screen)
        objects.update()
        collision_sprites()
        score_calculation()

    else:
        pygame.mixer.pause()
        screen.blit(start_bg, (0,0))
        if(score == 0 and flag == False):
            font.start_screen()
            font.game_start_button()

        else:
            if(score == 0 and flag == True):
                font.game_end_screen()
            else:
                font.game_end_screen()
        

    
    pygame.display.update()
    clock.tick(60)
