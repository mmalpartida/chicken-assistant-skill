# OVOS + Home Assistant Integration Guide

How to run both OVOS and Home Assistant together for the ultimate chicken control experience!

---

## Why Use Both?

### OVOS Strengths
- ✅ Better conversational AI
- ✅ Skill-based architecture (familiar if you came from Mycroft)
- ✅ Dedicated voice assistant platform
- ✅ Wake word detection
- ✅ Plugin ecosystem

### Home Assistant Strengths
- ✅ Powerful automation engine
- ✅ Beautiful dashboards and mobile app
- ✅ Integration with 1000+ smart home devices
- ✅ Location-based triggers
- ✅ Advanced scheduling

### Together = Best of Both Worlds
- 🎤 OVOS handles voice conversations
- 🏠 Home Assistant handles automations and dashboards
- 🐔 Chicken can be controlled from either platform
- 📱 Mobile control + voice control

---

## Architecture Options

### Option 1: OVOS Primary, HA Secondary (Recommended)

```
User says "Where is Moana?"
    ↓
OVOS Skill catches intent
    ↓
Controls servos directly
    ↓
(Optional) Notifies Home Assistant
    ↓
HA logs the event / triggers additional automations
```

**Best for:** Voice-first experience, minimal complexity

### Option 2: HA Primary, OVOS for Voice Only

```
User says "Where is Moana?"
    ↓
OVOS forwards to Home Assistant
    ↓
HA runs automation
    ↓
HA controls servos via script
    ↓
Returns response to OVOS for TTS
```

**Best for:** Complex automations, integration with other devices

### Option 3: Dual Control (Most Flexible)

```
OVOS Skill ←→ Servo Controller ←→ HA Scripts
               ↑
         Both can control independently
```

**Best for:** Maximum flexibility, redundancy

---

## Setup: Option 1 - OVOS Primary

This is the easiest setup.

### Prerequisites
- OVOS skill installed and working (see `OVOS_MIGRATION_PLAN.md`)
- Home Assistant installed on same Raspberry Pi

### Step 1: Install Both

```bash
# OVOS skill (already done)
cd /home/pi/chicken-assistant-skill
pip install -e .

# Home Assistant (if not installed)
# Follow: https://www.home-assistant.io/installation/
```

### Step 2: Configure Serial Port Sharing

Only one process can access the serial port at a time. Choose:

**A) Time-based control:**
- OVOS active during daytime
- HA active during evening
- Use systemd timers to switch

**B) OVOS-only serial:**
- OVOS skill controls servos
- HA controls other stuff
- No conflicts!

**C) Home Assistant REST API (recommended):**
- OVOS calls HA API to trigger servo actions
- HA actually controls servos
- Single point of control

### Step 3: OVOS Calls Home Assistant

Modify the OVOS skill to call HA:

```python
# In chicken_assistant_skill/__init__.py
import requests

def handle_assistant_chicken(self, message):
    # Instead of directly controlling servos...
    # Call Home Assistant
    ha_url = "http://localhost:8123/api/services/script/chicken_assistant_respond"
    headers = {
        "Authorization": "Bearer YOUR_LONG_LIVED_TOKEN",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ha_url, headers=headers, json={})
        self.speak_dialog('assistant.chicken')
    except Exception as e:
        self.log.error(f"Error calling Home Assistant: {e}")
        # Fallback to direct control
        self.direct_servo_control()
```

### Step 4: Get Home Assistant Long-Lived Token

1. Open Home Assistant
2. Click your profile (bottom left)
3. Scroll to **Long-Lived Access Tokens**
4. **CREATE TOKEN**
5. Copy the token
6. Add to OVOS skill configuration

---

## Setup: Option 2 - HA Primary

Make Home Assistant the central controller.

### Step 1: Install OVOS Home Assistant Integration

Check if OVOS has an official HA integration:

```bash
# In Home Assistant
# Settings → Devices & Services → + ADD INTEGRATION
# Search for "OVOS" or "OpenVoiceOS"
```

If not available, use webhooks:

### Step 2: Create Webhook in Home Assistant

```yaml
# configuration.yaml
automation:
  - alias: "OVOS Webhook - Chicken"
    trigger:
      - platform: webhook
        webhook_id: chicken_respond
    action:
      - service: script.chicken_assistant_respond
```

### Step 3: Configure OVOS to Call Webhook

```python
# In OVOS skill
import requests

def handle_assistant_chicken(self, message):
    webhook_url = "http://localhost:8123/api/webhook/chicken_respond"

    try:
        requests.post(webhook_url)
        self.speak_dialog('assistant.chicken')
    except Exception as e:
        self.log.error(f"Webhook error: {e}")
```

---

## Setup: Option 3 - Dual Control

Both platforms can independently control the chicken.

### Requirements
- Prevent simultaneous serial access
- Coordinate responses
- Shared audio files

### Implementation

**Use a lock file:**

```python
# chicken_control_lock.py
import fcntl
import time

class ServoLock:
    def __init__(self, lockfile='/tmp/chicken_servo.lock'):
        self.lockfile = lockfile

    def __enter__(self):
        self.lock = open(self.lockfile, 'w')
        fcntl.flock(self.lock, fcntl.LOCK_EX)
        return self

    def __exit__(self, *args):
        fcntl.flock(self.lock, fcntl.LOCK_UN)
        self.lock.close()

# Usage in both OVOS and HA:
with ServoLock():
    servo = maestro.Controller('/dev/ttyAMA0')
    # ... control servos ...
    servo.close()
```

**Add to both:**
- OVOS skill `__init__.py`
- HA control script `chicken_control.py`

---

## Coordination Examples

### Example 1: OVOS Voice, HA Automation

**OVOS handles:**
- "Where is Moana?" → Direct response

**Home Assistant handles:**
- Time-based: Morning greeting at 8am
- Motion-based: Respond when you enter room
- Dashboard: Manual button controls

### Example 2: Unified Logging

Track all chicken activations in one place:

```yaml
# Home Assistant automation
automation:
  - alias: "Log All Chicken Activity"
    trigger:
      # When HA triggers chicken
      - platform: event
        event_type: call_service
        event_data:
          service: script.chicken_assistant_respond

      # When OVOS triggers chicken (via webhook/API)
      - platform: webhook
        webhook_id: ovos_chicken_triggered

    action:
      - service: logbook.log
        data:
          name: "Chicken Assistant"
          message: "Chicken responded via {{ trigger.platform }}"
```

### Example 3: Shared Audio Resources

Both platforms use the same audio files:

```bash
# Symlink from OVOS to HA
ln -s /home/pi/chicken-assistant-skill/chicken_assistant_skill/*.mp3 \
      /config/www/chicken_sounds/
```

---

## Voice Control Comparison

| Feature | OVOS | Home Assistant |
|---------|------|----------------|
| Wake word | ✅ Built-in | ✅ Via satellites |
| Custom intents | ✅ Padatious/Adapt | ✅ Custom sentences |
| Conversational | ✅ Excellent | ⚠️ Basic |
| Multi-turn dialog | ✅ Yes | ❌ No |
| Easy setup | ⚠️ Moderate | ✅ Very easy (2025) |
| TTS quality | ✅ Piper/Coqui | ✅ Piper/Cloud |
| Offline capable | ✅ Fully | ✅ With Piper+Whisper |

**Recommendation:** Use OVOS for conversational AI, HA for everything else!

---

## Communication Methods

### Method 1: REST API

**OVOS → Home Assistant:**
```python
import requests

def call_ha_service(service, entity_id=None):
    url = f"http://localhost:8123/api/services/{service}"
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    data = {"entity_id": entity_id} if entity_id else {}
    requests.post(url, headers=headers, json=data)
```

**Home Assistant → OVOS:**
```yaml
shell_command:
  trigger_ovos_skill: "ovos-cli send-message 'where is moana'"
```

### Method 2: MQTT (Advanced)

Both publish to shared MQTT broker:

```yaml
# Home Assistant
mqtt:
  publish:
    topic: "chicken/trigger"
    payload: "respond"

# OVOS
# Subscribe to topic and respond
```

### Method 3: Webhooks

Simple HTTP callbacks (shown earlier).

---

## Best Practices

### 1. Single Source of Truth
Choose one platform to own the hardware:
- **OVOS owns serial** → HA calls OVOS when needed
- **HA owns serial** → OVOS calls HA when needed

### 2. Graceful Degradation
If one platform fails, the other should still work:

```python
try:
    # Try Home Assistant first
    call_home_assistant()
except:
    # Fallback to direct control
    direct_servo_control()
```

### 3. Avoid Conflicts
Use locks or scheduling to prevent simultaneous access.

### 4. Share Resources
Audio files, configuration, and logs should be accessible to both.

---

## Troubleshooting

### Both Platforms Responding

**Problem:** Say "where is moana" and both OVOS and HA respond

**Solution:**
- Disable conversation in one platform
- Use different wake words
- Configure HA to only respond to specific phrases

### Serial Port Busy

**Problem:** `Serial port already in use`

**Solution:**
- Implement locking mechanism (shown above)
- Check with `lsof /dev/ttyAMA0` to see who has it open
- Ensure only one platform controls hardware

### Voice Commands Not Working

**Check both platforms:**
```bash
# OVOS logs
journalctl --user -u ovos -f

# Home Assistant logs
ha core logs -f
```

---

## Example: Complete Integration

Here's a real-world setup:

**OVOS Configuration:**
- Handles all voice interactions
- Calls HA REST API for servo control
- Provides conversational responses

**Home Assistant Configuration:**
- Controls servos via shell_command
- Provides dashboard for manual control
- Automations for time/sensor triggers
- Logs all activity

**Coordination:**
- HA owns the serial port
- OVOS calls HA API when voice triggered
- HA can also trigger independently
- Shared audio files via symlink
- Unified logging in HA

---

## Next Steps

1. ✅ Choose your architecture (Option 1 recommended)
2. ✅ Install both platforms
3. ✅ Configure communication (REST API recommended)
4. ✅ Test voice control from both
5. ✅ Set up automations in HA
6. ✅ Configure OVOS skill to call HA
7. ✅ Implement locking if needed

---

## Resources

- **OVOS Documentation:** https://openvoiceos.org/
- **Home Assistant Voice:** https://www.home-assistant.io/voice_control/
- **REST API:** https://developers.home-assistant.io/docs/api/rest/
- **Webhooks:** https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger

---

Happy integrating! 🐔🏠🎤
