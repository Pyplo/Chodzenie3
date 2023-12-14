import pydirectinput as pdi
import pyautogui as pg
import time
import random
import sys
import signal
import keyboard
import threading

f10_pressed = False


def listen_for_f10():
    global f10_pressed
    while True:
        if keyboard.is_pressed('f10'):
            f10_pressed = True
            break


def signal_handler(signal, frame):
    stop_recording()
    sys.exit(0)


def start_recording():
    pg.hotkey('shift', 'f11')
    print("Recording started...")


def stop_recording():
    print('Stopping CapFrame...')
    pg.hotkey('shift', 'f11')
    time.sleep(2)


def walk(direction, duration):
    pg.keyDown(direction)
    time.sleep(duration)
    pg.keyUp(direction)


def get_input(prompt, options):
    print(prompt)
    for key, value in options.items():
        print(f"{value}: {key}")
    while True:
        choice = input("Selection: ").lower()
        if choice in options:
            return choice
        else:
            print("Invalid Option")


def run_presentmon():
    choice = get_input("Should the script start and stop presentmon?", {"y": "Yes", "n": "No"})
    if choice == 'y':
        return True
    elif choice == 'n':
        return False


def choose_press_duration():
    choice = get_input("How long should each key press last?", {"a": "1 second", "b": "2 seconds", "c": "5 seconds"})
    return {"a": 1, "b": 2, "c": 5}.get(choice, 1)


def get_total_duration():
    total_duration = input("Enter in seconds the total duration for the script to run (Default: 900s): ")
    if total_duration.isdigit():
        return int(total_duration)
    elif total_duration == "":
        return 900
    elif total_duration.isascii():
        print("Invalid")
        get_total_duration()



def choose_movement_pattern():
    choice = get_input("Choose a movement pattern",
                       {"a": "Random", "b": "Circle (WSDA)", "c": "Zigzag (WDSA)", "d": "Custom"}).lower()

    if choice == 'd':
        return get_custom_pattern()

    patterns = {
        "a": None,
        "b": ['w', 'a', 's', 'd'],
        "c": ['w', 'd', 's', 'a']
    }
    return patterns.get(choice, ['w', 'a', 's', 'd'])


def get_custom_pattern():
    a = input("Enter your custom Pattern (e.g 'space', 'a', 'shift'): ")
    a = "".join(a.lower().split()).split(',')
    return a


def simulate_movement(press_duration, total_duration, start_presentmon, movement_pattern):
    f10_listener_thread = threading.Thread(target=listen_for_f10)
    f10_listener_thread.start()
    print("Press ENTER to start walking...")
    keyboard.wait('enter')

    if start_presentmon:
        start_recording()

    directions = movement_pattern if movement_pattern else ['w', 'a', 's', 'd']
    start_time = time.time()
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        current_time = time.time()
        if total_duration > 0 and current_time - start_time > total_duration:
            break
        if f10_pressed:
            print("F10 pressed. Aborting")
            break
        if not movement_pattern:
            random.shuffle(directions)
        for direction in directions:
            walk(direction, press_duration)
            current_time = time.time()

    if start_presentmon:
        stop_recording()
    print("Simulation finished.")


if __name__ == '__main__':
    start_presentmon = run_presentmon()
    press_duration = choose_press_duration()
    if start_presentmon:
        total_duration = get_total_duration()
    else:
        total_duration = 0
    movement_pattern = choose_movement_pattern()
    simulate_movement(press_duration, total_duration, start_presentmon, movement_pattern)