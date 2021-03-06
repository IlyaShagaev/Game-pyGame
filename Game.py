import pygame
import random
import numpy as np
import pyautogui
import cv2
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,30'

display_width = 800
display_height = 600


plat_width = 100
plat_height = 20
plat_x = display_width // 2
plat_y = display_height // 2.5

centr_plat_x = plat_x + plat_width//2
centr_plat_y = plat_y + plat_height//2
centr_plat = (centr_plat_x, centr_plat_y)


ball_x = display_width // 2
ball_y = display_height // 2
ball_speed_x = 15
ball_speed_y = 15

centr_ball_x = ball_x + 10
centr_ball_y = plat_y + 10
centr_ball = (centr_ball_x, centr_ball_y)

pygame.init()
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Run!')
clock = pygame.time.Clock()

def update(display):
    display.fill((255, 255, 255))
    pygame.draw.rect(display, (255, 0, 0), (plat_x, plat_y, plat_width, plat_height))
    pygame.draw.circle(display, (255, 0, 0), (ball_x, ball_y), 10)
    ball_move()
    pygame.display.update()
    clock.tick(60)

def ball_move():
    global ball_speed_x, ball_speed_y, ball_x, ball_y
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    if ball_y <= 20 or ball_y >= 585:
        ball_speed_y = -ball_speed_y
    if ball_x <= 10 or ball_x >= 785:
        ball_speed_x = -ball_speed_x

def quit_1():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if ball_x <= plat_x + plat_width + 8 and ball_x >= plat_x \
            and ball_y <= plat_y + plat_height + 8 and ball_y >= plat_y - 7:
        quit()

def human():
    global plat_x
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if plat_x >= 0:
            plat_x -= 10
    elif keys[pygame.K_RIGHT]:
        if plat_x <= 700:
            plat_x += 10

def screen():
    hsv_min = np.array((0, 54, 5), np.uint8)
    hsv_max = np.array((187, 255, 253), np.uint8)
    hsv_min1 = np.array((0, 77, 17), np.uint8)
    hsv_max1 = np.array((208, 255, 255), np.uint8)

    image = pyautogui.screenshot(region=(0, 30, 800, 600))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # cv2.imshow('Screenshot', imutils.resize(image, width=600))
    cv2.imwrite('image.jpg', image)

    fn = 'image.jpg'  # имя файла, который будем анализировать
    img = cv2.imread(fn)



    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
    thresh = cv2.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
    contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

    centr_ball = ()
    # перебираем все найденные контуры в цикле
    for cnt in contours0:
        rect = cv2.minAreaRect(cnt)  # пытаемся вписать прямоугольник
        box = cv2.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = np.int0(box)  # округление координат
        area = int(rect[1][0] * rect[1][1])  # вычисление площади

        if area > 1880:
            cv2.drawContours(img, [box], 0, (255, 0, 0), 2)  # рисуем прямоугольник
            centr_plat_x = box[0][0] - (box[0][0] - box[1][0]) // 2
            centr_plat_y = box[0][1] - (box[0][1] - box[2][1]) // 2

        if len(cnt) > 30 and len(cnt) <= 32:
            ellipse = cv2.fitEllipse(cnt)
            centr_ball = ellipse[0]
            cv2.ellipse(img, ellipse, (255, 0, 0), 2)
    cv2.imshow('contours', img)  # вывод обработанного кадра в окно
    cv2.waitKey()
    cv2.destroyAllWindows()
    return centr_plat_x, centr_plat_y, centr_ball

def manipulations(centr_plat_x, centr_plat_y, centr_ball):
    global plat_x
    if abs(centr_plat_x - centr_ball[0]) < 200 and abs(centr_plat_y - centr_ball[1]) < 200:
        if centr_ball[0] > 700 and centr_plat_x > 700:
            plat_x -= 5
        elif centr_ball[0] < 100 and centr_plat_x < 100:
            plat_x += 5
        elif centr_ball[0] - centr_plat_x > -100 and centr_ball[0] - centr_plat_x < 0:
            if plat_x <= 700:
                plat_x += 5
        elif centr_ball[0] - centr_plat_x < 100 and centr_ball[0] - centr_plat_x > 0:
            if plat_x >= 0:
                plat_x -= 5
    elif plat_x < display_width // 2 - 70:
        plat_x += 5
    elif plat_x > display_width // 2:
        plat_x -= 5

def run_game():
    game = True

    while game:
        quit_1()
        human()
        update(display)
        centr_plat_x, centr_plat_y, centr_ball = screen()
        manipulations(centr_plat_x, centr_plat_y, centr_ball)

run_game()


