import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jose's Aim Trainer")

TARGET_INCREASE = 400  # Time in milliseconds target spawn rate
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30  # Padding for target to not spawn on the edge

BACKGROUND_COLOR = (121, 170, 62)
LIVES = 5
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont('comicsans', 22)


class Target:
    MAX_SIZE = 32
    GROWTH_RATE = 0.2
    COLOR = (242, 189, 0)
    COLOR2 = (255, 255, 255)
    # Target attributes

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
    # Target positioning and start size

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
        # Updates if target is growing or shrinking

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(
            win, self.COLOR2, (self.x, self.y), self.size * 0.75)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.55)
        pygame.draw.circle(
            win, self.COLOR2, (self.x, self.y), self.size * 0.35)
        # Drawing the target multiple times to create the ring shape

    def collide(self, x, y):  # Collision detection with mouse click using distance to a point formula
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size


def draw(win, targets):
    win.fill(BACKGROUND_COLOR)

    for target in targets:
        target.draw(win)


def format_time(secs):
    millisec = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    # 02d formats the number to have 2 digits and start with 0 if it's less than 10
    return f"{minutes:02d}:{seconds:02d}.{millisec}"


def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, (31, 30, 29), (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, (255, 255, 255))

    speed = round(target_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(
        f"Speed: {speed} clicks/s", 1, (255, 255, 255))

    hits_label = LABEL_FONT.render(
        f"Hits: {target_pressed}", 1, (255, 255, 255))

    lives_label = LABEL_FONT.render(
        f"Lives: {LIVES - misses}", 1, (255, 255, 255))
    # blit displays another surface on top of the current surface
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (180, 5))
    win.blit(hits_label, (420, 5))
    win.blit(lives_label, (610, 5))


def end_score(win, elapsed_time, target_pressed, clicks):
    win.fill(BACKGROUND_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, (255, 255, 255))

    speed = round(target_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(
        f"Speed: {speed} clicks/s", 1, (255, 255, 255))

    hits_label = LABEL_FONT.render(
        f"Hits: {target_pressed}", 1, (255, 255, 255))

    accuracy = round(target_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(
        f"Accuracy: {accuracy}%", 1, (255, 255, 255))

    win.blit(time_label, (middle_screen(time_label), 100))
    win.blit(speed_label, (middle_screen(speed_label), 200))
    win.blit(hits_label, (middle_screen(hits_label), 300))
    win.blit(accuracy_label, (middle_screen(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

    def middle_screen(surface):
        return WIDTH / 2 - surface.get_width() / 2


def main():
    run = True
    targets = []  # custom event to spawn targets
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    # Trigger event every TARGET_INCREASE milliseconds
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREASE)

    while run:
        clock.tick(60)  # 60 FPS
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                # ensures target does not spawn on the edge
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                # removes target from list when it reaches 0
                misses += 1

            # * unpacks the tuple into individual arguments
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            end_score(WIN, elapsed_time, target_pressed, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
