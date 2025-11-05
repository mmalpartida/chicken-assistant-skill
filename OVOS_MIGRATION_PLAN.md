# OVOS Migration Plan - Chicken Assistant Skill

## Overview
This document outlines the migration path from Mycroft to OVOS (Open Voice OS) for the HeiHei Chicken Assistant skill.

---

## Phase 1: OVOS Compatibility (Current Phase)

### Goals
- Make skill installable as a Python package
- Maintain backward compatibility with existing functionality
- Minimal code changes to core skill logic

### What Needs to Change

#### 1. Add setup.py (REQUIRED for OVOS)
**Status:** To be created

OVOS skills must be installable Python packages. We need to add a `setup.py` file with:
- Package metadata (name, version, author)
- Plugin entry point registration
- Automatic resource file discovery (locale, intents, dialogs)
- Dependencies (pyserial for servo control)

**Entry point format:**
```python
entry_points={'ovos.plugin.skill': 'chicken-assistant.mmalpartida=chicken_assistant_skill:ChickenAssistant'}
```

#### 2. Package Structure Rename (RECOMMENDED)
**Status:** To be done

Current: Files in root directory
Recommended: Files in `chicken_assistant_skill/` package directory

```
chicken-assistant-skill/
├── chicken_assistant_skill/          # New package directory
│   ├── __init__.py                   # Move from root
│   ├── maestro.py                    # Move from root
│   ├── maestro_uart.py               # Move from root
│   ├── locale/                       # Move from root
│   │   └── en-us/
│   │       ├── assistant.chicken.intent
│   │       └── assistant.chicken.dialog
│   ├── chicken_response_01.mp3       # Move from root
│   ├── chicken_response_02.mp3       # Move from root
│   └── heihei-bawk.mp3               # Move from root
├── setup.py                          # NEW - Package setup
├── requirements.txt                  # NEW - Python dependencies
├── version.py                        # NEW - Version tracking
├── README.md                         # Update for OVOS
├── test.py                           # Keep for manual testing
└── test2.py                          # Keep for manual testing
```

#### 3. Update Dependencies
**Status:** To be created

Create `requirements.txt`:
```
ovos-core >= 0.0.8
pyserial >= 3.5
```

Create `version.py`:
```python
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_BUILD = 0
VERSION_ALPHA = 0
```

#### 4. Code Changes to __init__.py (MINIMAL)
**Status:** Already fixed bugs, minor updates needed

Changes needed:
- Import path updates (if we rename to package structure)
- Everything else stays the same! OVOS is Mycroft-compatible

Current imports work fine:
```python
from mycroft import MycroftSkill, intent_handler
from mycroft.skills.audioservice import AudioService
from mycroft.audio import wait_while_speaking
```

OVOS supports these Mycroft imports natively!

#### 5. Manifest.yml (OPTIONAL for OVOS)
**Status:** Currently just a template, can keep or remove

OVOS prefers setup.py over manifest.yml, but both work. We can:
- **Option A:** Remove manifest.yml (use setup.py only)
- **Option B:** Keep for backward compatibility

**Recommendation:** Remove it to follow OVOS best practices

---

## Phase 2: Testing & Validation

### Testing Checklist
- [ ] Install skill via pip in development mode
- [ ] OVOS can discover and load the skill
- [ ] Intent recognition works ("Where is Moana?")
- [ ] Audio playback functions
- [ ] Servo control via Pololu Maestro works
- [ ] Error handling for missing serial device

### Test Environment
- Raspberry Pi 3 or 4
- OVOS installation (latest stable)
- Pololu Maestro connected to /dev/ttyAMA0

---

## Phase 3: Custom Voice Integration

### Voice Preservation Options

#### Option A: Piper TTS (Recommended - Local & Free)
- **Pros:** Runs locally, fast, privacy-focused
- **Cons:** Need to train model with voice samples
- **Requirements:** 2-5 minutes of clean audio recordings

#### Option B: Coqui XTTS (Quick Voice Cloning)
- **Pros:** Only needs 6-30 seconds of audio, high quality
- **Cons:** More resource intensive
- **Requirements:** Short clean voice sample

#### Option C: OpenAI Voice Cloning (Premium)
- **Pros:** Best quality, minimal audio needed (~15 seconds)
- **Cons:** Paid service, cloud-based (privacy concerns)
- **Requirements:** OpenAI API key, subscription

### Voice Recording Requirements
For any option, record yourself:
1. In a quiet environment
2. Speaking clearly and naturally
3. Various phrases (greetings, questions, responses)
4. 30 seconds minimum, 5 minutes ideal

**Sample phrases to record:**
- "Hello, how can I help you?"
- "Bawk bawk bawk" (for the chicken!)
- "I was in Moana with my friend Moana"
- Various emotional tones

---

## Phase 4: Home Assistant Integration (Future)

### Integration Approach
Once working on OVOS, we can add Home Assistant integration:

#### Option A: OVOS → Home Assistant Commands
OVOS skill sends commands to Home Assistant when triggered

#### Option B: Home Assistant → OVOS Skill
Home Assistant automations call OVOS skill

#### Option C: Standalone HA Automation
Rewrite as pure Home Assistant automation (future consideration)

### Benefits of Adding Home Assistant
- Web dashboard for chicken control
- More complex automation triggers
- Integration with other smart devices
- Mobile app control

---

## Migration Steps - Execution Order

### Step 1: Create OVOS Package Structure
1. Create `chicken_assistant_skill/` directory
2. Move files into package
3. Create `setup.py`
4. Create `requirements.txt`
5. Create `version.py`

### Step 2: Update Imports (if needed)
1. Test imports still work
2. Update paths for audio files
3. Update paths for locale files

### Step 3: Install and Test
1. Install in development mode: `pip install -e .`
2. Test OVOS can find the skill
3. Test skill functionality

### Step 4: Voice Configuration
1. Record voice samples
2. Train/configure TTS model
3. Configure OVOS to use custom voice

### Step 5: Documentation
1. Update README with OVOS installation instructions
2. Document voice configuration
3. Add troubleshooting guide

---

## Compatibility Notes

### What Will Stay the Same
✅ Core skill logic (intent handlers, audio playback, servo control)
✅ Mycroft imports (OVOS supports them natively)
✅ Intent/dialog file format
✅ Audio files
✅ Serial communication with Pololu Maestro

### What Will Change
⚠️ Installation method (pip install instead of MSM)
⚠️ Package structure (proper Python package)
⚠️ Skill discovery (via plugin entry points)

### What's Better in OVOS
🎉 Active development and community
🎉 Better performance
🎉 Modern TTS options
🎉 Docker support
🎉 More plugin ecosystem

---

## Timeline Estimate

- **Phase 1 (Package Setup):** 1-2 hours
- **Phase 2 (Testing):** 1-2 hours (assuming hardware available)
- **Phase 3 (Voice Cloning):** 2-4 hours (depending on method)
- **Phase 4 (Home Assistant):** Future/Optional

**Total for OVOS Migration:** ~4-8 hours

---

## Success Criteria

Migration is complete when:
1. ✅ Skill installs via `pip install`
2. ✅ OVOS discovers and loads skill automatically
3. ✅ "Where is Moana?" triggers chicken response
4. ✅ Audio plays correctly
5. ✅ Servos move as expected
6. ✅ Custom voice works (optional but recommended)

---

## Resources

### OVOS Documentation
- Main site: https://openvoiceos.org/
- GitHub: https://github.com/OpenVoiceOS
- Community: https://community.openconversational.ai/

### Tools
- ovos-skill-projen: Tool for retrofitting Mycroft skills
- OVOS Technical Manual: https://openvoiceos.github.io/ovos-technical-manual/

### Hardware
- Pololu Maestro: https://www.pololu.com/product/1350
- Raspberry Pi setup guides

---

## Next Steps

**Ready to start?** The next action is:
1. Create the package structure
2. Write setup.py
3. Test installation
4. Deploy to OVOS instance

**Questions before proceeding?**
- Do you have OVOS installed already, or do we need installation instructions?
- Do you have the hardware handy for testing?
- Should we start with the package structure now?
