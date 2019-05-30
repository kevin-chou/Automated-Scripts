import os
import pyautogui as pg
from PIL import Image
import pytesseract
import time


battle_start_btn_pos = (949, 734)
battle_screen_text_pos = (893, 728, 128, 34)

skip_btn_pos = (889, 772)
skip_screen_text_pos = (835, 756, 110, 35)

victory_btn1_pos = (1054, 657)
victory_btn2_pos = battle_start_btn_pos
victory_screen_text_pos = (764, 410, 381, 100)

defeat_btn_pos = (965, 645)
defeat_screen_text_pos = (859, 430, 169, 47)

levelup_battleon_btn = (949, 773)
levelup_screen_text_pos = (839, 572, 233, 41)

first_move_cd_pos = (1075, 511, 30, 31)
move_cd_red_colour = (104, 44, 54)
move_cd_offset = 43

first_atk_pos = (889, 514)
offset_atk_btn = 43


# the order in which the program should instruct mech to attack
# upon reaching end the program will attempt to cycle back to beginning of move order if cooldowns allow it
# otherwise program selects first available attack in player's menu
# if no attacks available due to lack of EP, broken parts, cd then program skips turn

# 0 refers to first attack
# 5 refers to last attack
# 6 refers to skip button [4, 5, 1, 0, 2]
preferred_move_order = [4, 5, 1, 0, 2]
curr_move_idx = 0

NUM_BATTLES = 2

def replace_pixel_colour(image, width, height, colour_to_replace, replacement_colour):

    for x_pos in range(0, width):
        for y_pos in range(0, height):
            if image.getpixel((x_pos, y_pos)) == colour_to_replace:
                image.putpixel((x_pos, y_pos), replacement_colour)

    return image


def find_next_move():
    idx = curr_move_idx
    num_moves_checked = 0

    # check if list is not empty
    if preferred_move_order:
        while num_moves_checked != len(preferred_move_order) - 1:
            print("Using preferred moves")
            print(idx)
            pg.screenshot("screenshots/cd.png", region=(first_move_cd_pos[0],
                                                        first_move_cd_pos[1] + preferred_move_order[idx] * move_cd_offset,
                                                        first_move_cd_pos[2], first_move_cd_pos[3]))

            if is_move_available("screenshots/cd.png", first_move_cd_pos[2], first_move_cd_pos[3], move_cd_red_colour):
                print("using: " + str(preferred_move_order[idx]))
                return preferred_move_order[idx]

            num_moves_checked += 1
            idx = (idx + 1) % len(preferred_move_order)

    print("could not find preferred move")

    # made a full rotation of preferred move list
    # select the first available move that is not on cooldown
    for x in range(0, 6):
        pg.screenshot("screenshots/cd.png", region=(first_move_cd_pos[0],
                                                    first_move_cd_pos[1] + x * move_cd_offset,
                                                    first_move_cd_pos[2], first_move_cd_pos[3]))

        if is_move_available("screenshots/cd.png", first_move_cd_pos[2], first_move_cd_pos[3], move_cd_red_colour):
            return x

    # if no moves are available then skip the turn
    return 6


def is_move_available(img, width, height, colour_to_check):
    cd_image = Image.open(img)

    for x_pos in range(0, width):
        for y_pos in range(0, height):
            if cd_image.getpixel((x_pos, y_pos)) == colour_to_check:
                return False

    return True


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

    # Create directory to store screenshots for processing if it does not exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    for battles in range(0, NUM_BATTLES):

        # PHASE 1
        # Take a screenshot and look for "BATTLE" button
        pg.screenshot("screenshots/battle_btn.png", region=battle_screen_text_pos)
        image = Image.open("screenshots/battle_btn.png")

        while "Battle" not in pytesseract.image_to_string(image, lang='eng', config='--psm 8'):
            print("searching for battle button...")
            time.sleep(1)
            pg.screenshot("screenshots/battle_btn.png", region=battle_screen_text_pos)
            image = Image.open("screenshots/battle_btn.png")

        # Move mouse to click the button
        pg.click(battle_start_btn_pos[0], battle_start_btn_pos[1])

        # Give time for fight to load
        time.sleep(2)

        # PHASE 2
        # 3 possibilities: player is still fighting, player has won, player has been defeated
        pg.screenshot("screenshots/skip_btn.png", region=skip_screen_text_pos)
        image = Image.open("screenshots/skip_btn.png")

        pg.screenshot("screenshots/victory.png", region=victory_screen_text_pos)
        image2 = Image.open("screenshots/victory.png")

        pg.screenshot("screenshots/defeat.png", region=defeat_screen_text_pos)
        image3 = Image.open("screenshots/defeat.png")

        while True:
            print("searching for skip, victory or defeat...")
            if "Skip" in pytesseract.image_to_string(image, lang='eng', config='--psm 7'):
                # Use a move or skip turn
                pg.click(first_atk_pos[0], first_atk_pos[1] + offset_atk_btn * find_next_move())
                pg.moveTo(100, 100)
            elif "Victory!" in pytesseract.image_to_string(image2, lang='eng', config='--psm 7'):
                # player has won, so click through menus to return back to home screen
                pg.click(victory_btn1_pos[0], victory_btn1_pos[1])

                """ [Need further testing]
                # need to click one extra menu if player has leveled up
                pg.screenshot("screenshots/levelup.png", region=levelup_screen_text_pos)
                image = Image.open("screenshots/levelup.png")
                if "LEVEL UP!" in pytesseract.image_to_string(image, lang='eng', config='--psm 7'):
                    time.sleep(1)
                    pg.click(levelup_battleon_btn[0], levelup_battleon_btn[1])
                """

                pg.click(victory_btn2_pos[0], victory_btn2_pos[1])
                break
            elif "Defeat" in pytesseract.image_to_string(image3, lang='eng', config='--psm 8'):
                time.sleep(1)
                # player has lost, so click through menu to return back to home screen
                pg.click(defeat_btn_pos[0], defeat_btn_pos[1])
                time.sleep(1)
                break

            time.sleep(0.3)
            pg.screenshot("screenshots/skip_btn.png", region=skip_screen_text_pos)
            image = Image.open("screenshots/skip_btn.png")

            pg.screenshot("screenshots/victory.png", region=victory_screen_text_pos)
            image2 = Image.open("screenshots/victory.png")

            pg.screenshot("screenshots/defeat.png", region=defeat_screen_text_pos)
            image3 = Image.open("screenshots/defeat.png")

            print(pytesseract.image_to_string(image2, lang='eng', config='--psm 7'))
