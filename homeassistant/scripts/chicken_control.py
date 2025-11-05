#!/usr/bin/env python3
"""
Chicken Assistant Control Script for Home Assistant

This script controls the HeiHei chicken animatronic via the Pololu Maestro
servo controller. It can be called from Home Assistant using shell_command.

Usage:
    python3 chicken_control.py [action]

Actions:
    respond - Play random chicken sound and move servos (default)
    move - Just move servos without sound
    sound - Just play random sound without moving

Examples:
    python3 chicken_control.py respond
    python3 chicken_control.py move
"""

import sys
import time
import random
from pathlib import Path

# Add the chicken_assistant_skill package to path
script_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(script_dir))

from chicken_assistant_skill import maestro


# Configuration
SERIAL_PORT = '/dev/ttyAMA0'
AUDIO_DIR = script_dir / 'chicken_assistant_skill'
AUDIO_FILES = [
    'chicken_response_01.mp3',
    'chicken_response_02.mp3',
    'heihei-bawk.mp3'
]


def play_audio():
    """Play a random chicken audio file"""
    audio_file = AUDIO_DIR / random.choice(AUDIO_FILES)

    # Use mpg123 or similar audio player
    # Home Assistant should have audio configured
    import subprocess
    try:
        subprocess.run(['mpg123', '-q', str(audio_file)], check=False)
    except FileNotFoundError:
        # Try alternative players
        try:
            subprocess.run(['ffplay', '-nodisp', '-autoexit', str(audio_file)],
                         check=False, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print(f"Warning: No audio player found. Would play: {audio_file}")


def move_servos():
    """Control the servos to animate the chicken"""
    try:
        servo = maestro.Controller(SERIAL_PORT)

        # Run first script subroutine
        servo.runScriptSub(0)
        time.sleep(2)

        # Run second script subroutine
        servo.runScriptSub(1)

        # Close connection
        servo.close()

        print("Servos moved successfully")
        return True

    except Exception as e:
        print(f"Error controlling servos: {e}", file=sys.stderr)
        return False


def chicken_respond():
    """Full chicken response - sound and movement"""
    print("Chicken responding...")

    # Start servo movement
    success = move_servos()

    # Play audio
    play_audio()

    return success


def main():
    """Main entry point"""
    action = sys.argv[1] if len(sys.argv) > 1 else 'respond'

    if action == 'respond':
        return chicken_respond()
    elif action == 'move':
        return move_servos()
    elif action == 'sound':
        play_audio()
        return True
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        print(__doc__)
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
