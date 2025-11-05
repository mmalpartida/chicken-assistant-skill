# <img src="https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg" card_color="#22A7F0" width="50" height="50" style="vertical-align:bottom"/> Chicken Assistant
Companion skill to the heihei voice assistant robot project

## About
This is an upgrade to the HeiHei Chicken project to add a servo controller, Raspberry Pi, and Mycroft voice control.
Mainly a proof of concept and a way to teach myself about working with voice skills and servo controllers.

The servo controller used is the Pololu Maestro 6 channel for around $20 USD
https://www.pololu.com/product/1350

For reference the maestro class and more info can be found at:
https://github.com/FRC4564/Maestro

See the project at: https://makeprojects.com/project/chicken-robot-voice-assistant

## Project Status - Legacy/Historical

**Note:** This project was built for the Mycroft AI platform, which ceased operations in 2023. While the code has been preserved and bugs fixed, it is primarily maintained as a historical reference and learning resource.

For those interested in continuing voice assistant development, consider these alternatives:
- **OVOS** (Open Voice OS) - Community-driven Mycroft successor
- **Neon AI** - Another Mycroft-compatible platform
- **Home Assistant** with voice integration
- Modern alternatives like Rhasspy or other open-source voice platforms

### Recent Bug Fixes (2025)
- Fixed missing parentheses on `servo.close()` calls
- Corrected `random.choice()` usage with dictionary in main handler
- Fixed typo in test.py (setAccel → setTarget)
- Corrected intent file typos ("where you" → "were you")

## Hardware Requirements
- Raspberry Pi (2 or 3)
- Pololu Maestro 6-channel servo controller
- Servo motors for chicken animatronics
- Speakers for audio playback

## Examples
* "Where is Moana?"
* "Were you in Moana?"
* "Didn't I see you in the movie Moana?"

The chicken responds with audio clips and servo movements!

## Installation

This skill requires:
1. A Mycroft installation (or compatible fork like OVOS)
2. Serial connection to Pololu Maestro on `/dev/ttyAMA0`
3. Audio files included in the repo
4. pyserial library for serial communication

## Credits
Mitchell Malpartida

## Category
**Entertainment**
Daily

## Tags
#Heihei #chicken #Moana #robotics #voice-assistant

