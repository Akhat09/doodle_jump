add_library('minim')
import random, os
path = os.getcwd()
player = Minim(this)

WIDTH = 320
HEIGHT = 480
DOODLER = False
BOOSTED = False
NUM_BOOSTERS = 0

class Doodler():
    
    def __init__(self, x, y, r, g, img_name, img_w, img_h):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.vx = 0
        self.vy = 0
        self.img_w = img_w
        self.img_h = img_h
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.dir = RIGHT
        self.alive = True
        
        # all of the images of the doodler
        self.img_right = loadImage(path + "/images/" + img_name + "_right.png")
        self.img_left = loadImage(path + "/images/" + img_name + "_left.png")
        self.img_up = loadImage(path + "/images/" + img_name + "_up.png")
        self.spray = loadImage(path + "/images/spray.png")
        self.doodle_jetpack_right = loadImage(path + "/images/" + img_name + "_jetpack_right.png")
        self.doodle_jetpack_left = loadImage(path + "/images/" + img_name + "_jetpack_left.png")
        self.doodle_hat_right = loadImage(path + "/images/" + img_name + "_hat_right.png")
        self.doodle_hat_left = loadImage(path + "/images/" + img_name + "_hat_left.png")
        
        # doolder spray variables
        self.spray_y = 0
        self.spray_flag = 0
        self.spray_coor_x = 0
        self.spray_coor_y = 0
        self.spray_r = 20
        
        
        self.sound_jump = player.loadFile(path + "/sounds/jump.wav")
        self.sound_spray = player.loadFile(path + "/sounds/spray.mp3")
       
                         
    def display(self):
        self.update()
        
        # if the jetpack or hat activated then display them with doodler
        for b in game.boosters:
            if b.boost == True and b.type_boost == "jetpack":
                if self.dir == LEFT:
                    image(self.doodle_jetpack_left, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w * 2, self.img_h * 2)
                else:
                    image(self.doodle_jetpack_right, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w * 2, self.img_h * 2)
                break
            elif b.boost == True and b.type_boost == "hat":
                if self.dir == LEFT:
                    image(self.doodle_hat_left, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w * 1.5, self.img_h * 1.5)
                else:
                    image(self.doodle_hat_right, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w * 1.5, self.img_h * 1.5)
                break
        # display usual doodler
        else:    
            if self.dir == RIGHT:
                image(self.img_right, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h)
            elif self.dir == LEFT:
                image(self.img_left, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h)
            elif self.dir == UP:
                image(self.img_up, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h)
                self.dir = RIGHT
            if self.spray_flag == 1:
                image(self.spray, self.spray_coor_x, self.spray_coor_y + self.spray_y, self.spray_r, self.spray_r)
            
            
    def update(self):
        self.gravity()
        
        # moving doodler to left or right based on the key
        if self.key_handler[LEFT] == True:
            self.vx = -5
            self.dir = LEFT
        elif self.key_handler[RIGHT] == True:
            self.vx = 5
            self.dir = RIGHT
        # shouting the spray
        elif self.key_handler[UP] == True:
            self.spray_coor_y = self.y - self.img_h
            self.spray_coor_x = self.x - 10
            self.spray_flag = 1
            self.dir = UP
            self.vx = 0
            self.sound_spray.play()
            self.sound_spray.rewind()
        else:
            self.vx = 0
        
        if self.spray_flag == 1:
            self.spray_y -= 10
        
        # checking if spray out of the boarder
        if abs(self.spray_coor_y) % HEIGHT + self.spray_y <= 0:
            self.spray_flag = 0
            self.spray_y = 0
        
        self.x += self.vx
        self.y += self.vy
        
        # teleporting from side to side
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        
        for h in game.hazards:
            
            # checking if doodler jumped on the monster
            if self.distance(h) <= self.r + h.r:
                if self.vy > 0 and self.y + self.r <= h.y and self.x + self.r >= h.x - h.r and self.x - self.r <= h.x + h.r and h.c != "hole":
                    h.sound_jump_on_monster.play()
                    game.hazards.remove(h)
                    self.vy = -10
                else:
                    # checking if it's hole then die, and play sound
                    if h.c == "hole":
                        h.sound_hole_die.play()
                        game.not_ufo_or_hole = False
                    # if it's ufo dies, and play sound
                    elif h.c == "ufo":
                        h.sound_ufo_die.play()
                        game.not_ufo_or_hole = False
                    self.alive = False
            
            # checking if spray hit the monster
            if self.hit(h) <= self.spray_r + h.r:
                h.hit += 1
                # if it's green monster than 2 hits are needed
                if (h.c != "green" and h.c != "hole") or (h.c == "green" and h.hit == 2):
                    game.hazards.remove(h)
                self.spray_flag = 0
                self.spray_y = 0
        
        # y_shift of the game
        if self.y < game.h//2:
            game.y_shift = game.h//2 - self.y
            self.y = game.h//2
            
            for p in game.platforms:
                p.y += game.y_shift
                game.score += game.y_shift
                
            for h in game.hazards:
                h.y += game.y_shift
            
            for b in game.boosters:
                b.y += game.y_shift
        
        # if doodler fell then die
        if self.y + self.r > HEIGHT:
            self.alive = False
    
    def gravity(self):
        # if not with the booster
        if BOOSTED == False:
            # jumping up
            if self.y + self.r >= self.g:
                self.vy = -10
                self.sound_jump.rewind()
                self.sound_jump.play()
            else:
                self.vy += 0.3
            
            for p in game.platforms[::-1]:
                # checking if doodler on the platform and change it to the ground, self.r//3 needed to cut the nose of the doodler and not count it
                if self.y + self.r <= p.y and self.x + self.r//3 >= p.x and self.x - self.r <= p.x + p.w and self.dir == RIGHT:
                    if p.c == "brown":
                        p.brown = True
                    else:
                        self.g = p.y
                        break
                elif self.y + self.r <= p.y and self.x + self.r >= p.x and self.x - self.r//3 <= p.x + p.w and self.dir == LEFT:
                    if p.c == "brown":
                        p.brown = True
                    else:
                        self.g = p.y
                        break
                else:
                    self.g = game.g
    
    # counting the distance between doodler and target
    def distance(self, target):
        return ((self.x - target.x)**2 + (self.y - target.y)**2) ** 0.5
    
    # checking if doodler hit anything with a spray
    def hit(self, target):
        return ((self.spray_coor_x - target.x)**2 + (self.spray_coor_y + self.spray_y - target.y)**2) ** 0.5
    
    # checking if doodler object touched the target, mainly platform
    def touched(self, object, target):
        return True if object.y + object.r >= target.y and object.y + object.r <= target.y + target.h and object.x + object.r >= target.x and object.x - object.r <= target.x + target.w else False

class Platform:
    
    def __init__(self, x, y, w, h, c, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
        self.img = loadImage(path + "/images/" + img)
        self.vx = 2
        self.vy = 2
        self.count = 20
        self.tmp_y = 0
        self.tmp_x = 0
        
        # special image array for brown platform
        self.brown = False
        if self.c == "brown":
            self.img_brown = []
            for i in range(2, 7):
                self.img_brown.append(loadImage(path + "/images/brown/brown_" + str(i) + ".png"))
        
        self.sound_brown = player.loadFile(path + "/sounds/brown_break.mp3")
        self.sound_white = player.loadFile(path + "/sounds/white.mp3")

    def display(self):
        self.update()
        self.blue_move()
        self.darkblue_move()
        self.white()
        
        # if image is brown then displaying all frames, else display the image
        if self.brown == False:
            image(self.img, self.x, self.y, self.w, self.h)
        else:
            image(self.img, self.x, self.y, self.w, self.h)
            for i in range(5):
                image(self.img_brown[i], self.x, self.y, self.w, self.h)
        self.brown_break()

    def update(self):
        # removing left begind platforms
        if self.y > HEIGHT:
            game.platforms.remove(self)
        
        # last level of platforms
        if game.score / 10 > 10000:
            while len(game.platforms) <= 7:
                # randoming y position but making it possible to jump
                self.tmp_y = game.platforms[-1].y - random.randint(100, 150)
                if self.tmp_y > 70:
                    self.tmp_y = game.platforms[-1].y - random.randint(50, 70)
                self.tmp_x = random.randint(0, WIDTH - self.w)
                # counting the number of white platforms 
                count = 0
                for p in game.platforms:
                    if p.c == "white":
                        count += 1
                # if their number is less than 2 then add them and call the monster method
                if count < 2:
                    game.platforms.append(Platform(self.tmp_x, self.tmp_y, 100, 20, "white", "white.png"))
                    self.monster()
                # based on random add either darkblue or green platform and call the booster method
                elif random.randint(0,10) > 7:
                    if random.choice([0, 1]) == 0:
                        game.platforms.append(Platform(self.tmp_x, self.tmp_y, 100, 20, "darkblue", "darkblue.png"))
                    else:
                        game.platforms.append(Platform(self.tmp_x, self.tmp_y, 100, 20, "green", "green.png")) 
                        self.booster()  
                else:
                    game.platforms.append(Platform(self.tmp_x, self.tmp_y, 100, 20, "blue", "blue.png"))
        # second level of platforms
        elif game.score / 10 > 5000:
            if len(game.platforms) <= 10:
                # randoming y position but making it possible to jump
                self.tmp_y = game.platforms[-1].y - random.randint(20, 100)
                if self.tmp_y > 70:
                    self.tmp_y = game.platforms[-1].y - random.randint(40, 70)
                self.tmp_x = random.randint(0, WIDTH - self.w)
                # counting the number of brown and blue platforms 
                count = 0
                for p in game.platforms:
                    if p.c == "brown" or p.c == "blue":
                        count += 1
                # if their number is less than 2 then add them and call the monster method  
                if count < 2:
                    if random.choice([0, 1]) == 0:
                        game.platforms.append(Platform(random.randint(0, WIDTH - self.w), self.tmp_y, 100, 20, "brown", "brown/brown_1.png"))
                    game.platforms.append(Platform(self.tmp_x, self.tmp_y - random.randint(20, 50), 100, 20, "blue", "blue.png"))
                    self.monster()
                else:
                    game.platforms.append(Platform(self.tmp_x, self.tmp_y, 100, 20, "green", "green.png"))
                    self.booster()
        # first level of platforms
        else:
            if len(game.platforms) <= 12:
                # randoming y position but making it possible to jump
                self.tmp_y = game.platforms[-1].y - random.randint(30, 60)
                if self.tmp_y > 70:
                    self.tmp_y = game.platforms[-1].y - random.randint(20, 70)
                self.tmp_x = random.randint(0, WIDTH - self.w)
                # based on random either add brown or green platforms and call booster method
                if random.randint(0, 10) > 9:
                    game.platforms.append(Platform(self.tmp_x, self.tmp_y, 100, 20, "brown", "brown/brown_1.png"))
                    game.platforms.append(Platform(random.randint(0, WIDTH - self.w), self.tmp_y - random.randint(20, 50), 100, 20, "green", "green.png"))
                else:
                    game.platforms.append(Platform(self.tmp_x, self.tmp_y, 100, 20, "green", "green.png"))
                    self.booster()
    
    
    # based on randomness choose a booster and call the Boosters class
    def booster(self):
        x = random.randint(1, 4)
        if len(game.boosters) == 0:
            if x == 1:
                game.boosters.append(Boosters(self.tmp_x + random.randint(0,self.w - 20), self.tmp_y - 15, 20, "jetpack_" + str(doodle) + ".png", 40, 40, "jetpack"))
            elif x == 2:
                game.boosters.append(Boosters(self.tmp_x + random.randint(0,self.w - 20), self.tmp_y - 15, 20, "hat_" + str(doodle) + ".png", 40, 40, "hat"))
            elif x == 3:
                game.boosters.append(Boosters(self.tmp_x + random.randint(0,self.w - 20), self.tmp_y - 5, 10, "spring_" + str(doodle) + ".png", 20, 20, "spring"))
            else:
                game.boosters.append(Boosters(self.tmp_x + random.randint(0,self.w - 20), self.tmp_y - 15, 20, "trampoline_" + str(doodle) + ".png", 40, 40, "trampoline"))
    
    
    # based on randomness choose a monster and call the Hazards class
    def monster(self):
        x = random.randint(1, 5)
        if len(game.hazards) == 0:
            if x == 1:
                game.hazards.append(Hazards(self.tmp_x, self.tmp_y - random.randint(30, 50), 50, "hole", "hole.png", 100, 100))
            elif x == 2:
                game.hazards.append(Hazards(self.tmp_x, self.tmp_y - random.randint(30, 50), 30, "blue", "monster1.png", 70, 70))
            elif x == 3:
                game.hazards.append(Hazards(self.tmp_x, self.tmp_y - random.randint(30, 50), 30, "red", "monster7.png", 70, 70))
            elif x == 4:
                game.hazards.append(Hazards(self.tmp_x, self.tmp_y - random.randint(30, 50), 30, "green", "monster2.png", 70, 70))
            else:
                game.hazards.append(Hazards(self.tmp_x, self.tmp_y - random.randint(30, 50), 30, "ufo", "ufo.png", 70, 70))
    
    
    # moving blue platform from left to right
    def blue_move(self):
        if self.c == "blue":
            if self.x + self.w >= WIDTH - 5:
                self.vx = -2
            elif self.x <= 5:
                self.vx = 2
            self.x += self.vx
   
    
    # moving darkblue platform up and down
    def darkblue_move(self):
        if self.c == "darkblue":
            if self.count > 0:
                self.vy = -2
                self.count -= 1
            elif self.count == 0 and self.vy == -2:
                self.count = -20
            elif self.count == 0 and self.vy == 2:
                self.count = 20
            elif self.count < 0:
                self.vy = 2
                self.count += 1
            self.y += self.vy
    
    
    # removing white platform if doodler jumped on it
    def white(self):
        for p in game.platforms[::-1]:
            if p.c == 'white' and game.doodler.touched(game.doodler, p) and game.doodler.vy > 0:
                self.sound_white.rewind()
                self.sound_white.play()
                game.platforms.remove(p)
                break
    
    
    # removing brown platform if it's touched
    def brown_break(self):
        for p in game.platforms[::-1]:
            if p.c == 'brown' and game.doodler.touched(game.doodler, p) and game.doodler.vy > 0:
                self.sound_brown.rewind()
                self.sound_brown.play()
                game.platforms.remove(p)
                break
            
class Hazards():
    
    def __init__(self, x, y, r, c, img_name, img_w, img_h):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        self.vx = 2
        self.vy = 2
        self.sign = 1
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        self.hit = 0
        self.tmp_x = self.x
        self.tmp_y = self.y
        if self.c == "hole":
            self.sound_hole_die = player.loadFile(path + "/sounds/hole.mp3")
        else:
            self.sound_ufo_die = player.loadFile(path + "/sounds/ufo_die.mp3")
            self.sound_jump_on_monster = player.loadFile(path + "/sounds/jump_on_monster.mp3")
        
    def display(self):
        self.update()
        self.monster_blue()
        self.monster_red()
        image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h)
    
    
    
    def update(self):
        # removing monsters left behind
        for h in game.hazards:
            if h.y > HEIGHT:
                game.hazards.remove(h)
     
     
    # blue monster that moves from left to right
    def monster_blue(self):
        if self.c == "blue":
            if self.x + self.r >= WIDTH - 5:
                self.vx = -2
            elif self.x - self.r <= 5:
                self.vx = 2
            if self.sign < 0:
                self.sign = 1
            else:
                self.sign = -1
            
            if self.x > 280:
                self.vy = -2
            elif self.x > 240:
                self.vy = 2
            elif self.x > 200:
                self.vy = -2
            elif self.x > 160:
                self.vy = 2
            elif self.x > 120:
                self.vy = -2
            elif self.x > 80:
                self.vy = 2
            elif self.x > 40:
                self.vy = -2
            elif self.x >= 0:
                self.vy = 1
            
                    
            self.y += self.vy 
            self.x += self.vx
    
    
    # monster that moves from left to right but short distance
    def monster_red(self):
        if self.c == "red":
            if self.x + self.r >= self.tmp_x + 40:
                self.vx = -2
            elif self.x - self.r <= self.tmp_x - 40:
                self.vx = 2
            
            self.x += self.vx

class Boosters():
    
    def __init__(self, x, y, r, img_name, img_w, img_h, type_boost):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/images/" + img_name)
        self.img_w = img_w
        self.img_h = img_h
        self.boost = False
        self.time = 0
        self.type_boost = type_boost
        if self.type_boost == "jetpack":
            self.sound_jetpack = player.loadFile(path + "/sounds/jetpack1.mp3")
        if self.type_boost == "spring":
            self.sound_spring = player.loadFile(path + "/sounds/spring.mp3")
        if self.type_boost == "hat":
            self.sound_hat = player.loadFile(path + "/sounds/hat.mp3")
        if self.type_boost == "trampoline":
            self.sound_trampoline = player.loadFile(path + "/sounds/trampoline.mp3")
    
    def display(self):
        #removing boosters if they are left below and wasn't used
        if self.y > HEIGHT and self.boost == False:
            game.boosters.remove(self)
        
        self.boosted()
        if self.boost == False:
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h)

    
    def boosted(self):
        # checking if doodler touched the booster
        if self.distance(game.doodler) <= self.r + game.doodler.r:
            # checking if the doodler fall down on the booster or touched it while going up
            if (game.doodler.y + game.doodler.r <= self.y) or self.type_boost == "jetpack" or self.type_boost == "hat":
                self.boost = True
                global BOOSTED
                BOOSTED = True
        # calling the booster method type based on the booster
        if self.boost == True:
            # changing the doodler's velocity to 0
            if self.time == 0:
                game.doodler.vy = 0
            if self.type_boost == "jetpack":
                self.jetpack()
            elif self.type_boost == "spring":
                self.spring()
            elif self.type_boost == "hat":
                self.hat()
            elif self.type_boost == "trampoline":
                self.trampoline()
    
    # changing doodler's velocity with some numbers, playing sound and then removing the booster from the list
    def jetpack(self):
        if self.time < 100:
            self.time += 1
            game.doodler.vy -= 0.3
            self.sound_jetpack.play()
        else:
            self.time = 0
            self.boost = False
            global BOOSTED
            BOOSTED = False
            self.sound_jetpack.pause()
            game.boosters.remove(self)
    
    
    # same as above but for spring            
    def spring(self):
        if self.time < 50: 
            self.time += 1
            game.doodler.vy -= 0.4
            self.sound_spring.play()
        else:
            self.time = 0
            self.boost = False
            global BOOSTED
            BOOSTED = False
            self.sound_spring.pause()
            game.boosters.remove(self)
    
    
    # same as above but for hat
    def hat(self):
        if self.time < 100: 
            self.time += 1
            game.doodler.vy -= 0.2
            self.sound_hat.play()
        else:
            self.time = 0
            self.boost = False
            global BOOSTED
            BOOSTED = False
            self.sound_hat.pause()
            game.boosters.remove(self)
                    
                    
    # same as above but for trampoline
    def trampoline(self):
        if self.time < 50: 
            self.time += 1
            game.doodler.vy -= 0.3
            self.sound_trampoline.play()
        else:
            self.time = 0
            self.boost = False
            global BOOSTED
            BOOSTED = False
            self.sound_trampoline.pause()
            game.boosters.remove(self)
    
    # method for finding distance between doodler and target
    def distance(self, target):
        return ((self.x - target.x)**2 + (self.y - target.y)**2) ** 0.5

class Game():
    
    def __init__(self, w, h, g):
        self.w = w
        self.h = h
        self.g = g
        self.y_shift = 0
        self.score = 0
        self.not_ufo_or_hole = True
        self.sound_monster = player.loadFile(path + "/sounds/monster.mp3")
        self.sound_ufo = player.loadFile(path + "/sounds/ufo.mp3")
        self.sound_game_over = player.loadFile(path + "/sounds/game_over.mp3")
        
        self.doodler = Doodler(160, 450, 35, self.g, "doodle_" + str(doodle), 70, 70)
        
        self.platforms = []
        self.platforms.append(Platform(160, 400, 100, 20, "green", "green.png"))  
        self.hazards = []
        self.number_boosters = 0
        self.boosters = []
    
        self.backgrounds = loadImage(path + "/images/background.png")
        self.topbar = loadImage(path + "/images/topbar.png")
        self.lost = loadImage(path + "/images/lost_2.jpg")
        self.poggers = loadImage(path + "/images/poggers.png")

        
    def display(self):
        
        if self.doodler.alive == False:
            # checking if doodler was killed by ufo or hole or not
            if self.not_ufo_or_hole == True:
                self.sound_game_over.play()
            image(self.lost, 0, 0, WIDTH, HEIGHT)
            image(self.poggers, 100, 305, 120, 150)
            textAlign(CENTER, CENTER)
            textSize(15)
            fill(255, 0, 0)
            text("Retry: [CLICK ANYWHERE]", width/2, 9.5*height/10)
            return
        
        image(self.backgrounds, 0, 0, self.w, self.h)
        image(self.topbar, 0, 0, self.w, 70)
        
        for p in self.platforms:
            p.display()
            
        for h in self.hazards:
            h.display()
            # checking if hazards is ufo or hole and playing related music
            if h.c == "ufo":
                self.sound_ufo.play()
            elif h.c != "ufo" and h.c != "hole":
                self.sound_monster.play()
        # pausing the music if no more hazards
        if len(self.hazards) == 0:
            self.sound_monster.pause()
            self.sound_ufo.pause()
        
        for b in self.boosters:
            b.display()
            
        self.doodler.display()
        
        # displaying score
        fill(0, 0, 0)
        textSize(20)
        textAlign(LEFT)
        text("Score: "+ str(int(self.score/10)), 10, 28)


doodle = 0
I = 0
V = 1

game = Game(WIDTH, HEIGHT, HEIGHT)

# doodlers
doodler_1 = loadImage(path + "/images/doodle_1_right.png")
doodler_2 = loadImage(path + "/images/doodle_2_right.png")
doodler_3 = loadImage(path + "/images/doodle_3_right.png")

back = loadImage(path + "/images/back.jpg")
choose = player.loadFile(path + "/sounds/Choose_your_character.mp3")

# button coordinates
button_1 = [130, 100, 100, 100]
button_2 = [10, 170, 100, 100]
button_3 = [205, 210, 100, 100]

def setup():
    size(WIDTH, HEIGHT)
    
def draw():
    background(255)
    # first screen where player chooses his doodler
    if DOODLER == False:
        if choose.isPlaying() == False:
            choose.rewind()
            choose.play()
        global I, V
        i = I
        image(back, 0, 0, WIDTH, HEIGHT)
        image(doodler_1, 130 + i, 100, 100, 100)
        image(doodler_2, 10 + i, 170, 100, 100)
        image(doodler_3, 205 + i, 210, 100, 100)
        if I > 10:
            V = -1
        elif I < -10:
            V = 1
        I += V
    # if doodler chosen thenn start the game
    if DOODLER == True:
        choose.pause()
        game.display()
    
# letting player use arrows and WASD
def keyPressed():
    if keyCode == LEFT or key == "a" or key == "A":
        game.doodler.key_handler[LEFT] = True
    elif keyCode == RIGHT or key == "d" or key == "D":
        game.doodler.key_handler[RIGHT] = True
    elif keyCode == UP or key == "w" or key == "W":
        game.doodler.key_handler[UP] = True

def keyReleased():
    if keyCode == LEFT or key == "a" or key == "A":
        game.doodler.key_handler[LEFT] = False
    elif keyCode == RIGHT or key == "d" or key == "D":
        game.doodler.key_handler[RIGHT] = False
    elif keyCode == UP or key == "w" or key == "W":
        game.doodler.key_handler[UP] = False
    
def mouseClicked():
    global DOODLER, doodle, game
    # tracking users mouse pressed coordinates in order to choose the skin for the doodler
    if DOODLER == False:
        if mouseX <= button_1[0] + button_1[1] and mouseX >= button_1[0] and mouseY <= button_1[1] + button_1[3] and mouseY >= button_1[1]:
            DOODLER = True
            doodle = 1
        elif mouseX <= button_2[0] + button_2[1] and mouseX >= button_2[0] and mouseY <= button_2[1] + button_3[3] and mouseY >= button_2[1]:
            DOODLER = True
            doodle = 2
        elif mouseX <= button_3[0] + button_3[1] and mouseX >= button_3[0] and mouseY <= button_3[1] + button_3[3] and mouseY >= button_3[1]:
            DOODLER = True
            doodle = 3
        # starting the game
        if DOODLER == True:
            game = Game(WIDTH, HEIGHT, HEIGHT)
    else:
        # restarting the game
        if game.doodler.alive == False:
            game = Game(WIDTH, HEIGHT, HEIGHT)
