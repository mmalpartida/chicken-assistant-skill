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

## Project Status - OVOS Compatible!

**Migrated to OVOS!** This skill has been updated for OVOS (Open Voice OS), the spiritual successor to Mycroft AI. While originally built for Mycroft (which ceased operations in 2023), the skill is now fully compatible with OVOS and actively maintained.

### Platform Support
- ✅ **OVOS** (Open Voice OS) - Primary platform, fully supported
- ✅ **Home Assistant** - Full integration available!
- ✅ **Neon AI** - Should work with minimal changes
- 🔄 **OVOS + Home Assistant** - Can run both together!

### Recent Updates (2025)
**OVOS Migration:**
- Restructured as proper Python package with setup.py
- Added OVOS plugin entry point registration
- Created version tracking system
- Added comprehensive requirements.txt

**Home Assistant Integration:**
- Complete voice control setup with custom sentences
- Dashboard UI for manual control
- Automations for time/sensor triggers
- Python control script for easy HA integration
- Comprehensive setup documentation

**Bug Fixes:**
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

### Prerequisites
- OVOS installation (see https://openvoiceos.org/ for setup)
- Raspberry Pi with Python 3.7+
- Pololu Maestro servo controller connected to `/dev/ttyAMA0`
- Serial permissions configured (user in `dialout` group)

### Install from Source (Development)

1. Clone this repository:
```bash
git clone https://github.com/mmalpartida/chicken-assistant-skill.git
cd chicken-assistant-skill
```

2. Install in development mode:
```bash
pip install -e .
```

3. Restart OVOS:
```bash
systemctl --user restart ovos
```

### Install from PyPI (Future)
```bash
pip install ovos-skill-chicken-assistant
```

### Verify Installation
Check that OVOS recognizes the skill:
```bash
ovos-skill list | grep chicken
```

### Configuration

#### Serial Port Permissions
Make sure your user has access to the serial port:
```bash
sudo usermod -a -G dialout $USER
# Log out and back in for changes to take effect
```

#### Test Serial Connection
You can test the servo controller independently:
```bash
cd chicken-assistant-skill
python test.py
```

### Troubleshooting

**Skill not loading?**
- Check OVOS logs: `journalctl --user -u ovos -f`
- Verify plugin entry point: `pip show ovos-skill-chicken-assistant`

**Serial port errors?**
- Verify device exists: `ls -l /dev/ttyAMA0`
- Check permissions: `groups` (should include `dialout`)
- Test with `test.py` script first

**Audio not playing?**
- Check OVOS audio service is running
- Verify speaker configuration in OVOS settings

---

## Home Assistant Integration

Want to control your chicken through Home Assistant? We've got you covered!

### Features
- 🎤 **Voice Control** - Custom sentences for HA Assist
- 📱 **Dashboard** - Beautiful UI controls via mobile app or web
- 🤖 **Automations** - Time, motion, or event-based triggers
- 🔊 **TTS Integration** - Works with Piper, OpenAI, or any HA TTS
- 🏠 **Smart Home** - Integrate with lights, sensors, and more

### Quick Start

1. **Copy files to Home Assistant:**
```bash
# In your Home Assistant config directory
cp -r chicken-assistant-skill/homeassistant/* /config/
```

2. **Follow the setup guide:**
See [HOME_ASSISTANT_SETUP.md](HOME_ASSISTANT_SETUP.md) for complete instructions.

3. **Say "Where is Moana?"** and watch the magic happen!

### Running OVOS + Home Assistant Together

Want the best of both worlds? Check out [OVOS_HA_INTEGRATION.md](OVOS_HA_INTEGRATION.md) for:
- Architecture options
- Communication methods
- Coordination strategies
- Complete integration examples

---

## Documentation

- **[OVOS_MIGRATION_PLAN.md](OVOS_MIGRATION_PLAN.md)** - OVOS migration details
- **[HOME_ASSISTANT_SETUP.md](HOME_ASSISTANT_SETUP.md)** - Complete HA setup guide
- **[OVOS_HA_INTEGRATION.md](OVOS_HA_INTEGRATION.md)** - Run both platforms together

---

## Credits
Mitchell Malpartida

## Category
**Entertainment**
Daily

## Tags
#Heihei #chicken #Moana #robotics #voice-assistant

