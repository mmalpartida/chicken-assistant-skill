# Home Assistant Integration Guide

Complete guide for integrating the HeiHei Chicken Assistant with Home Assistant.

---

## Overview

This integration allows you to control your chicken robot through:
- 🎤 **Voice commands** via Home Assistant Assist
- 📱 **Dashboard controls** via the HA mobile app or web interface
- 🤖 **Automations** triggered by time, sensors, or other events
- 🔊 **TTS responses** with custom voice synthesis

---

## Prerequisites

### Hardware
- Raspberry Pi with Home Assistant installed
- Pololu Maestro servo controller connected to `/dev/ttyAMA0`
- Servos connected and configured in Maestro Control Center
- Speakers for audio playback

### Software
- Home Assistant OS or Supervised (2024.11+)
- Python 3.9+ available in Home Assistant
- Audio player installed (`mpg123` or `ffplay`)
- Voice assistant configured (Piper TTS + Whisper recommended)

---

## Installation

### Step 1: Clone Repository

SSH into your Home Assistant machine:

```bash
# Navigate to config directory
cd /config

# Clone the repository
git clone https://github.com/mmalpartida/chicken-assistant-skill.git
```

### Step 2: Install Python Dependencies

```bash
# Install the chicken assistant package
cd /config/chicken-assistant-skill
pip install -e .
```

### Step 3: Install Audio Player

You need an audio player to play the chicken sounds:

```bash
# Option 1: mpg123 (recommended)
apk add mpg123

# Option 2: ffmpeg (if mpg123 not available)
apk add ffmpeg
```

### Step 4: Configure Serial Permissions

Make sure Home Assistant can access the serial port:

```bash
# Add homeassistant user to dialout group
usermod -a -G dialout homeassistant

# Verify device exists
ls -l /dev/ttyAMA0
```

### Step 5: Test the Script

Before integrating with HA, test the control script:

```bash
cd /config/chicken-assistant-skill/homeassistant/scripts
python3 chicken_control.py respond
```

You should hear audio and see servo movement!

---

## Home Assistant Configuration

### Step 1: Add Custom Sentences

Copy the custom sentences file:

```bash
mkdir -p /config/custom_sentences/en
cp /config/chicken-assistant-skill/homeassistant/custom_sentences/en/chicken_assistant.yaml \
   /config/custom_sentences/en/
```

### Step 2: Update Configuration

Add the following to your `/config/configuration.yaml`:

```yaml
# Include the chicken assistant configuration
shell_command: !include_dir_merge_named chicken-assistant-skill/homeassistant/shell_commands/
script: !include_dir_merge_named chicken-assistant-skill/homeassistant/scripts/
intent_script: !include chicken-assistant-skill/homeassistant/configuration.yaml

# Or manually add the sections from homeassistant/configuration.yaml
```

**Manual configuration option:** Open `homeassistant/configuration.yaml` and copy the sections to your main `configuration.yaml`.

### Step 3: Add Input Helpers

Via Home Assistant UI:

1. Go to **Settings** → **Devices & Services** → **Helpers**
2. Click **+ CREATE HELPER**
3. Create these helpers:

**Toggle:**
- Name: `Chicken Assistant Enabled`
- Entity ID: `input_boolean.chicken_enabled`
- Icon: `mdi:bird`

**Dropdown:**
- Name: `Chicken Response Type`
- Entity ID: `input_select.chicken_response_type`
- Options:
  - Full Response (Sound + Movement)
  - Movement Only
  - Sound Only
- Icon: `mdi:gesture-tap`

### Step 4: Add Automations

**Option A - Via UI:**
1. Go to **Settings** → **Automations & Scenes**
2. Click **+ CREATE AUTOMATION**
3. Use the examples from `homeassistant/automations/example_automations.yaml`

**Option B - Via YAML:**
```bash
# Add to your automations.yaml
cat /config/chicken-assistant-skill/homeassistant/automations/example_automations.yaml >> /config/automations.yaml
```

### Step 5: Add Dashboard

1. Go to **Settings** → **Dashboards**
2. Click **+ ADD DASHBOARD**
3. Name it "Chicken Assistant"
4. Switch to **YAML mode** (three dots menu)
5. Paste contents of `homeassistant/dashboards/chicken_dashboard.yaml`

### Step 6: Restart Home Assistant

```bash
# Restart to apply all changes
ha core restart
```

---

## Voice Assistant Setup

For voice control to work, you need to configure Home Assistant's voice assistant (Assist).

### Quick Setup (2025)

1. Go to **Settings** → **Voice assistants**
2. Click **+ ADD ASSISTANT**
3. Configure:
   - **Name:** Chicken Assistant
   - **Language:** English
   - **Conversation Agent:** Home Assistant
   - **Speech-to-Text:** Whisper (or cloud service)
   - **Text-to-Speech:** Piper (local) or OpenAI TTS
   - **Wake word:** (optional) Configure if using satellite

### Recommended TTS: Piper

For local, fast TTS:

1. Go to **Settings** → **Devices & Services** → **+ ADD INTEGRATION**
2. Search for "Piper"
3. Install and select a voice (en_US recommended)

### Testing Voice Commands

1. Open Home Assistant on mobile or web
2. Tap the **microphone icon**
3. Say: *"Where is Moana?"*
4. The chicken should respond!

---

## Usage

### Voice Commands

Say any of these phrases:

**Moana Questions:**
- "Where is Moana?"
- "Were you in Moana?"
- "Are you in Moana?"
- "Didn't I see you in the movie Moana?"

**Greetings:**
- "How are you, chicken?"
- "Hey chicken!"
- "Tell me about yourself"

**Sounds:**
- "Make a chicken sound"
- "Bawk bawk"
- "Do the chicken"

### Manual Control

Use the dashboard buttons:
- **Full Response** - Sound + servo movement
- **Move Only** - Just servos
- **Sound Only** - Just audio

### Automation Examples

**Morning greeting:**
```yaml
- alias: "Chicken Morning Greeting"
  trigger:
    - platform: time
      at: "08:00:00"
  action:
    - service: script.chicken_assistant_respond
```

**Motion activated:**
```yaml
- alias: "Chicken Motion Response"
  trigger:
    - platform: state
      entity_id: binary_sensor.motion_sensor
      to: "on"
  action:
    - service: script.chicken_assistant_respond
```

---

## Troubleshooting

### Voice Commands Not Working

**Check conversation integration:**
```bash
# View logs
ha core logs | grep conversation
```

**Verify custom sentences loaded:**
1. Developer Tools → States
2. Search for your intents
3. Should see `ChickenMoana`, etc.

**Test intent manually:**
1. Developer Tools → Actions
2. Service: `conversation.process`
3. Data: `{"text": "where is moana"}`

### Script Errors

**Check script output:**
```bash
# Run manually to see errors
cd /config/chicken-assistant-skill/homeassistant/scripts
python3 chicken_control.py respond
```

**Common issues:**
- **Serial port errors:** Check permissions and device path
- **Audio not playing:** Install `mpg123` or `ffplay`
- **Import errors:** Reinstall package with `pip install -e .`

### Servo Not Moving

**Check serial connection:**
```bash
ls -l /dev/ttyAMA0
# Should show: crw-rw---- 1 root dialout ...

# Test with basic script
cd /config/chicken-assistant-skill
python3 test.py
```

**Maestro configuration:**
- Ensure scripts are loaded in Maestro Control Center
- Subroutines 0 and 1 must be defined
- USB Dual Port mode configured

### Audio Not Playing

**Check audio system:**
```bash
# Test with a simple file
mpg123 /config/chicken-assistant-skill/chicken_assistant_skill/chicken_response_01.mp3

# Or with ffplay
ffplay -nodisp -autoexit /config/chicken-assistant-skill/chicken_assistant_skill/chicken_response_01.mp3
```

**Configure default audio output:**
```bash
# Check available outputs
aplay -l

# Set default in /etc/asound.conf or ~/.asoundrc
```

---

## Advanced Configuration

### Custom Audio Files

Replace or add audio files in:
```
/config/chicken-assistant-skill/chicken_assistant_skill/*.mp3
```

Update `chicken_control.py` AUDIO_FILES list if adding new files.

### Custom Servo Sequences

Modify the Maestro scripts in Maestro Control Center:
1. Connect Maestro via USB
2. Open Maestro Control Center
3. Edit Script tab
4. Modify subroutines 0 and 1
5. Apply settings

### Integration with Other Services

**Example: Notify when chicken responds**
```yaml
automation:
  - alias: "Chicken Response Notification"
    trigger:
      - platform: event
        event_type: call_service
        event_data:
          service: script.chicken_assistant_respond
    action:
      - service: notify.mobile_app_phone
        data:
          message: "The chicken responded!"
```

---

## Integration with OVOS

Want to run both OVOS and Home Assistant together? See `OVOS_HA_INTEGRATION.md` for details on:
- Running OVOS skill alongside HA
- Sharing audio resources
- Coordinating responses
- Unified voice control

---

## Resources

- **Home Assistant Voice Control:** https://www.home-assistant.io/voice_control/
- **Piper TTS:** https://github.com/rhasspy/piper
- **Pololu Maestro:** https://www.pololu.com/product/1350
- **Project Page:** https://makeprojects.com/project/chicken-robot-voice-assistant

---

## Support

Having issues? Check:
1. Home Assistant logs: `Settings → System → Logs`
2. Test script manually to isolate issues
3. Verify serial permissions and hardware connections
4. Check Home Assistant community forums

---

## Next Steps

- ✅ Configure custom voice with Piper or OpenAI TTS
- ✅ Create more automations based on your needs
- ✅ Add motion sensors or other triggers
- ✅ Integrate with OVOS for dual-platform control
- ✅ Customize responses and audio files

Have fun with your chicken assistant! 🐔
