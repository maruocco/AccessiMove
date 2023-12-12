import subprocess


def run_splash_screen():
    subprocess.call(["python", "boot_up.py"])


def run_eye_track():
    subprocess.call(["python", "eye_track.py"])



if __name__ == "__main__":
    run_splash_screen()
    #run_eye_track()

