import os
import pyautogui as pg
from PIL import Image
import pytesseract
import time


battle_start_btn_pos = (949, 734)
victory_btn1_pos = (1054, 657)
victory_btn2_pos = battle_start_btn_pos
defeat_btn_pos = (965, 645)

first_atk_pos = (889, 514)
offset_atk_btn = 43

# the order in which the program should instruct mech to attack
# upon reaching end the program will attempt to cycle back to beginning of move order if cooldowns allow it
# otherwise program selects first available attack in player's menu
# if no attacks available due to lack of EP, broken parts, cd then program skips turn

# 0 refers to first attack
# 5 refers to last attack
# 6 refers to skip button
preferred_move_order = [4, 5, 1, 0, 2]


def replace_pixel_colour(image, width, height, colour_to_replace, replacement_colour):

    for x_pos in range(0, width):
        for y_pos in range(0, height):
            if image.getpixel((x_pos, y_pos)) == colour_to_replace:
                image.putpixel((x_pos, y_pos), replacement_colour)

    return image


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

    # Create directory to store screenshots for processing if it does not exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # PHASE 1
    # Take a screenshot and look for "BATTLE" button
    pg.screenshot("screenshots/battle_btn.png", region=(893, 728, 128, 34))
    image = Image.open("screenshots/battle_btn.png")

    while "Battle" not in pytesseract.image_to_string(image, lang='eng', config='--psm 8'):
        print("searching for battle button...")
        time.sleep(2)
        pg.screenshot("screenshots/battle_btn.png", region=(893, 728, 128, 34))
        image = Image.open("screenshots/battle_btn.png")

    # Move mouse to click the button
    pg.click(battle_start_btn_pos[0], battle_start_btn_pos[1])

    # Give time for fight to load
    time.sleep(2)

    # PHASE 2
    # 3 possibilities: player is still fighting, player has won, player has been defeated
    pg.screenshot("screenshots/skip_btn.png", region=(835, 756, 110, 35))
    image = Image.open("screenshots/skip_btn.png")

    pg.screenshot("screenshots/victory.png", region=(764, 410, 381, 100))
    image2 = Image.open("screenshots/victory.png")

    pg.screenshot("screenshots/defeat.png", region=(859, 430, 169, 47))
    image3 = Image.open("screenshots/defeat.png")

    while True:
        print("searching for skip, victory or defeat...")
        if "Skip" in pytesseract.image_to_string(image, lang='eng', config='--psm 7'):
            pass
        elif "Victory!" in pytesseract.image_to_string(image2, lang='eng', config='--psm 7'):
            time.sleep(1)
            # player has won, so click through menus to return back to home screen
            pg.click(victory_btn1_pos[0], victory_btn1_pos[1])
            time.sleep(1)
            pg.click(victory_btn2_pos[0], victory_btn2_pos[1])
            break
        elif "Defeat" in pytesseract.image_to_string(image3, lang='eng', config='--psm 8'):
            time.sleep(1)
            # player has lost, so click through menu to return back to home screen
            pg.click(defeat_btn_pos[0], defeat_btn_pos[1])
            time.sleep(1)
            break

        time.sleep(2)
        pg.screenshot("screenshots/skip_btn.png", region=(835, 756, 110, 35))
        image = Image.open("screenshots/skip_btn.png")

        pg.screenshot("screenshots/victory.png", region=(764, 410, 381, 100))
        image2 = Image.open("screenshots/victory.png")

        pg.screenshot("screenshots/defeat.png", region=(859, 430, 169, 47))
        image3 = Image.open("screenshots/defeat.png")

        print(pytesseract.image_to_string(image2, lang='eng', config='--psm 7'))

"""
    time.sleep(2)
    pg.screenshot("screenshots/skip1.png", region=(827, 756, 190, 35))
    num_y = 511
    for x in range(0, 6):
        pg.screenshot("screenshots/test" + str(x) + ".png", region=(1075, num_y, 30, 31))
        num_y += 41
        time.sleep(1)

    while True:
        print(pg.position())

    im = Image.open("screenshots/battle.png")
    #im = im.convert('1', dither=Image.NONE)
    im.show()
    print(pytesseract.image_to_string(im, lang='eng', config='--psm 8'))
"""