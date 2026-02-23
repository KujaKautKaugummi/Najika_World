# 🎵 SOUND DESIGN GUIDE - NAJIKA DIGIVICE AUDIO SYSTEM
**Model 1 - Digivice APK**
**Created:** 2025-11-11
**Complete Audio Implementation Guide**

---

## 🎯 AUDIO SYSTEM OVERVIEW

### **Audio Categories:**

```
1. 🎵 MUSIC (Background/BGM)
   - Zone music (7 zones)
   - Menu music
   - Battle music
   - Victory/Defeat music

2. 🔊 SOUND EFFECTS (SFX)
   - UI sounds (clicks, hovers)
   - Character sounds (footsteps, voice)
   - Environmental sounds (wind, water)
   - Combat sounds (attacks, hits)
   - Item sounds (collect, use)

3. 🎤 VOICE (TTS + Recordings)
   - Najika TTS (Megumin voice!)
   - Voice call audio
   - Character reactions

4. 🌍 AMBIENT SOUNDS
   - Birds, insects
   - Water, wind
   - Nature loops
   - Room tone

TOTAL SOUNDS NEEDED: ~100-150 audio files
```

---

## 🎵 CATEGORY 1: BACKGROUND MUSIC (BGM)

### **Music Track List:**

```
TRACK 1: "Welcome Home" (Village Center)
  Genre: Upbeat, Cheerful
  Tempo: 120 BPM
  Instruments: Acoustic guitar, piano, light drums
  Loop: Yes
  Length: 2-3 minutes
  Mood: Safe, cozy, home

TRACK 2: "Forest Wanderer" (Forest Zone)
  Genre: Mysterious, Peaceful
  Tempo: 90 BPM
  Instruments: Flute, strings, harp
  Loop: Yes
  Length: 3-4 minutes
  Mood: Exploration, wonder

TRACK 3: "Lakeside Serenity" (Lake/Fishing)
  Genre: Calm, Relaxing
  Tempo: 70 BPM
  Instruments: Piano, light synth pads
  Loop: Yes
  Length: 4-5 minutes
  Mood: Peaceful, meditative

TRACK 4: "Mountain Climber" (Mountain Zone)
  Genre: Epic, Adventurous
  Tempo: 130 BPM
  Instruments: Orchestral, drums, brass
  Loop: Yes
  Length: 2-3 minutes
  Mood: Challenge, triumph

TRACK 5: "Eden's Dream" (Secret Garden)
  Genre: Dreamy, Magical
  Tempo: 80 BPM
  Instruments: Harp, bells, ethereal vocals
  Loop: Yes
  Length: 3-4 minutes
  Mood: Paradise, bliss

TRACK 6: "Battle Cry" (Battle Arena)
  Genre: Intense, Fast
  Tempo: 160 BPM
  Instruments: Electric guitar, heavy drums, synth
  Loop: Yes
  Length: 2-3 minutes
  Mood: Adrenaline, combat

TRACK 7: "Into the Depths" (Mystery Cave)
  Genre: Tense, Dark
  Tempo: 100 BPM
  Instruments: Low strings, percussion, ambient drones
  Loop: Yes
  Length: 3-4 minutes
  Mood: Suspense, danger

TRACK 8: "Menu Theme" (Main Menu)
  Genre: Inviting, Friendly
  Tempo: 110 BPM
  Instruments: Pop, electronic, upbeat
  Loop: Yes
  Length: 1-2 minutes
  Mood: Welcome, excitement

TRACK 9: "Victory!" (Battle Win)
  Genre: Triumphant
  Tempo: 140 BPM
  Instruments: Brass, drums, celebration sounds
  Loop: No (one-shot)
  Length: 10-15 seconds
  Mood: Success!

TRACK 10: "Defeat..." (Battle Loss)
  Genre: Somber
  Tempo: 60 BPM
  Instruments: Piano, sad strings
  Loop: No (one-shot)
  Length: 8-10 seconds
  Mood: Try again...
```

---

### **Music Implementation in UE5:**

```cpp
// Music Manager Blueprint: BP_MusicManager

VARIABLES:
- CurrentTrack (Sound Wave)
- FadeTime (Float) = 3.0 seconds
- AudioComponent (Audio Component)
- ZoneToMusic (Map<String, Sound Wave>)

FUNCTIONS:

PlayMusicForZone(ZoneName: String):
  1. Get track from ZoneToMusic map
  2. If CurrentTrack == NewTrack → Return (already playing!)
  3. Fade out CurrentTrack (3 seconds)
  4. Fade in NewTrack (3 seconds)
  5. Set CurrentTrack = NewTrack

StopMusic():
  1. Fade out CurrentTrack
  2. Set CurrentTrack = None

SetVolume(Volume: Float):
  1. AudioComponent → Set Volume Multiplier

EVENT GRAPH:

Event BeginPlay:
  → Initialize ZoneToMusic map
     ZoneToMusic["Village"] = BGM_Village
     ZoneToMusic["Forest"] = BGM_Forest
     ... (all zones)
  → Play Menu music

On Zone Change (Trigger):
  → Get new zone name
  → PlayMusicForZone(NewZoneName)
```

---

### **Audio Files Format:**

```
FORMAT: OGG Vorbis (best for mobile!)
SAMPLE RATE: 44100 Hz
BIT RATE: 128-192 kbps (good quality, small size)
CHANNELS: Stereo

WHY OGG?
✅ Smaller file size than WAV
✅ Better quality than MP3 (for same size)
✅ Free/Open source
✅ UE5 supports natively
✅ Loops seamlessly

COMPRESSION:
UE5 Import Settings:
→ Compression Quality: 40-60 (balance size/quality)
→ Sample Rate: 44100 Hz
→ Looping: Enable for BGM!
```

---

## 🔊 CATEGORY 2: SOUND EFFECTS (SFX)

### **UI Sound Effects:**

```
UI_Click.wav
  - Button press
  - Sharp, satisfying "click"
  - Duration: 0.1s
  - Pitch: Medium-High

UI_Hover.wav
  - Mouse/finger hover over button
  - Soft "whoosh" or gentle tone
  - Duration: 0.2s
  - Pitch: Medium

UI_Open.wav
  - Menu/Window opens
  - "Swoosh" up
  - Duration: 0.3s
  - Pitch: Rising

UI_Close.wav
  - Menu/Window closes
  - "Swoosh" down
  - Duration: 0.3s
  - Pitch: Falling

UI_Error.wav
  - Invalid action
  - "Buzz" or "Bonk"
  - Duration: 0.3s
  - Pitch: Low (negative feeling)

UI_Success.wav
  - Action completed
  - Cheerful "ding!" or "chime"
  - Duration: 0.5s
  - Pitch: High (positive!)

UI_Notification.wav
  - New message, alert
  - Gentle "ping"
  - Duration: 0.4s
  - Pitch: Medium-High
```

---

### **Character Sound Effects:**

```
FOOTSTEPS (4 variations for variety!):
Footstep_Grass_01.wav to 04.wav
  - Walking on grass
  - Soft "step" sound
  - Duration: 0.2s each

Footstep_Stone_01.wav to 04.wav
  - Walking on stone/concrete
  - Harder "clack" sound
  - Duration: 0.2s each

Footstep_Wood_01.wav to 04.wav
  - Walking on wooden floor
  - Hollow "thunk"
  - Duration: 0.2s each

IMPLEMENTATION:
→ Add Animation Notify to walk cycle
→ Trigger random footstep variant
→ Play based on surface type (PhysMaterial!)

JUMP/LAND:
Jump_01.wav
  - "Hup!" effort sound
  - Duration: 0.3s

Land_Soft_01.wav
  - Landing on grass
  - Soft "thud"
  - Duration: 0.3s

Land_Hard_01.wav
  - Landing on stone
  - Hard "thump"
  - Duration: 0.4s

NAJIKA VOICE REACTIONS:
Voice_Happy_01.wav to 05.wav
  - "Yay!", "Woo!", giggles
  - Duration: 0.5-1.0s

Voice_Sad_01.wav to 03.wav
  - Sighs, "Aww..."
  - Duration: 0.5-0.8s

Voice_Excited_01.wav to 03.wav
  - "Wow!", "Amazing!"
  - Duration: 0.6-1.0s

Voice_Hurt_01.wav to 03.wav
  - "Ow!", damage grunts
  - Duration: 0.3-0.5s
```

---

### **Combat Sound Effects:**

```
ATTACK SOUNDS:
Attack_Swing_01.wav to 03.wav
  - Sword/weapon swing
  - "Swoosh!" sound
  - Duration: 0.4s

Attack_Hit_01.wav to 03.wav
  - Attack connects with enemy
  - "Thwack!" impact
  - Duration: 0.3s

Attack_Miss_01.wav
  - Attack misses
  - Quieter swoosh
  - Duration: 0.3s

SKILL SOUNDS:
Skill_Fireball_Charge.wav
  - Charging up fireball
  - Building fire sound
  - Duration: 1.0s

Skill_Fireball_Cast.wav
  - Releasing fireball
  - "Whoosh!" + fire
  - Duration: 0.5s

Skill_Lightning_Cast.wav
  - Lightning strike
  - Electric "ZAP!"
  - Duration: 0.6s

Skill_Heal_Cast.wav
  - Healing spell
  - Magical sparkle sound
  - Duration: 1.0s

DAMAGE SOUNDS:
Damage_Taken_01.wav to 03.wav
  - Character takes damage
  - Impact + grunt
  - Duration: 0.5s

Shield_Block_01.wav
  - Damage blocked
  - Metallic "clang!"
  - Duration: 0.4s
```

---

### **Item & Interaction Sounds:**

```
ITEM COLLECTION:
Item_Collect_Food.wav
  - Picked up food
  - Cheerful "bloop!"
  - Duration: 0.3s

Item_Collect_Coin.wav
  - Picked up money
  - Metallic "ching!"
  - Duration: 0.4s

Item_Collect_Rare.wav
  - Picked up rare item
  - Magical "shimmer!"
  - Duration: 0.8s

ITEM USE:
Item_Eat.wav
  - Eating food
  - Chewing, "nom nom"
  - Duration: 1.0s

Item_Drink.wav
  - Drinking
  - Gulping sound
  - Duration: 0.8s

Item_Open_Chest.wav
  - Opening treasure chest
  - Creaking hinges + "click"
  - Duration: 1.2s

INTERACTIONS:
Door_Open.wav
  - Opening door
  - Wooden creak
  - Duration: 0.8s

Door_Close.wav
  - Closing door
  - Wooden thud
  - Duration: 0.6s

Button_Press.wav
  - Physical button/switch
  - Mechanical "click"
  - Duration: 0.2s
```

---

## 🌍 CATEGORY 3: AMBIENT SOUNDS

### **Environmental Ambience:**

```
NATURE SOUNDS (All Looping!):

Amb_Birds_Forest.wav
  - Various bird chirps
  - Peaceful, distant
  - Loop: Yes, 30-60 seconds

Amb_Crickets_Night.wav
  - Cricket sounds
  - Nighttime ambience
  - Loop: Yes, 20-30 seconds

Amb_Wind_Gentle.wav
  - Light wind through trees
  - Soft rustling
  - Loop: Yes, 40-60 seconds

Amb_Wind_Strong.wav
  - Strong mountain wind
  - Howling sound
  - Loop: Yes, 30-50 seconds

Amb_Water_Stream.wav
  - Flowing water (river/stream)
  - Constant babbling
  - Loop: Yes, 30-60 seconds

Amb_Water_Lake.wav
  - Gentle lake waves
  - Lapping against shore
  - Loop: Yes, 40-60 seconds

Amb_Waterfall.wav
  - Waterfall rushing
  - Loud, powerful
  - Loop: Yes, 20-40 seconds

Amb_Cave_Drip.wav
  - Water dripping in cave
  - Echo effect
  - Loop: Yes, 10-20 seconds

Amb_Fire_Crackle.wav
  - Campfire/torch
  - Wood crackling
  - Loop: Yes, 20-30 seconds

IMPLEMENTATION:
→ Place Ambient Sound actors in level
→ Set attenuation (distance fade)
→ Enable looping
→ Adjust volume per zone
```

---

### **Room Tone (Background Noise):**

```
WHY ROOM TONE?
→ Pure silence feels "dead" and unnatural
→ Subtle background noise adds life
→ Makes transitions smoother

RoomTone_Indoors.wav
  - Very quiet room ambience
  - Slight air conditioning hum
  - Volume: Very low (0.1-0.2)
  - Loop: Yes

RoomTone_Outdoors.wav
  - Gentle wind, distant sounds
  - Natural atmosphere
  - Volume: Low (0.2-0.3)
  - Loop: Yes

USAGE:
→ Always playing in background (very quiet!)
→ Different tone for indoors vs outdoors
→ Crossfade when entering/exiting buildings
```

---

## 🎤 CATEGORY 4: VOICE & TTS

### **Najika TTS (Text-to-Speech):**

```
SYSTEM: Coqui TTS XTTS-v2 (Megumin voice clone!)

IMPLEMENTATION:
1. User sends chat message
2. Backend AI generates response text
3. Backend TTS converts text → audio WAV
4. UE5 downloads WAV file
5. UE5 plays audio
6. Lip sync animation matches (ABP_Najika!)

AUDIO SETTINGS:
- Sample Rate: 22050 Hz (TTS default)
- Format: WAV PCM 16-bit
- Mono (single channel)

CACHING:
→ Cache common phrases
   "Hello Mr.K!" (always same audio)
   "I'm hungry!" (frequent)
→ Saves TTS processing time
→ Faster response!
```

---

### **Voice Call Audio Processing:**

```
MICROPHONE INPUT:
→ Capture at 16000 Hz (Whisper STT requirement)
→ Mono audio
→ PCM 16-bit

PROCESSING CHAIN:
1. User speaks → Microphone captures
2. VAD (Voice Activity Detection) filters silence
3. Send audio chunks to backend
4. Whisper STT transcribes
5. AI generates response text
6. TTS generates response audio
7. Play response audio in UE5
8. Lip sync animation

AUDIO QUALITY:
→ Noise reduction (optional - backend!)
→ Echo cancellation (if needed)
→ Volume normalization
```

---

## 🎛️ AUDIO MIXING & MASTER VOLUME

### **Audio Mix Categories:**

```
UE5 Sound Classes:

SoundClass_Master (Everything!)
├── SoundClass_Music (BGM)
│   └── Volume: 0.6 (default)
│
├── SoundClass_SFX (Sound Effects)
│   ├── Volume: 0.8 (default)
│   ├── SoundClass_UI
│   ├── SoundClass_Character
│   ├── SoundClass_Combat
│   └── SoundClass_Item
│
├── SoundClass_Voice (TTS, Dialogue)
│   └── Volume: 1.0 (default)
│
└── SoundClass_Ambient (Environment)
    └── Volume: 0.4 (default)

DUCKING (Auto-volume reduction):
→ When Najika speaks (Voice):
   * Lower Music volume (0.6 → 0.3)
   * Lower Ambient volume (0.4 → 0.2)
→ When voice ends:
   * Fade Music/Ambient back to normal
```

---

### **Settings Menu - Audio Controls:**

```
WBP_SettingsAudio:

SLIDERS:
┌─────────────────────────────────┐
│ 🔊 AUDIO SETTINGS               │
│                                 │
│ Master Volume:  [========] 80%  │
│ Music Volume:   [======  ] 60%  │
│ SFX Volume:     [========] 80%  │
│ Voice Volume:   [==========] 100%│
│ Ambient Volume: [====    ] 40%  │
│                                 │
│ [Apply] [Reset to Default]      │
└─────────────────────────────────┘

IMPLEMENTATION:
OnMasterVolumeChanged(Value: Float):
  → Set SoundClass_Master volume = Value

OnMusicVolumeChanged(Value: Float):
  → Set SoundClass_Music volume = Value

... (same for all categories)

Save settings to EncryptedSharedPreferences!
```

---

## 📱 MOBILE AUDIO OPTIMIZATION

### **Performance Optimization:**

```
LIMITS:
- Max Simultaneous Sounds: 32
- Prioritization: Important sounds play first
- Distance Attenuation: Far sounds don't play

COMPRESSION:
→ Music: OGG Vorbis, Quality 40-60
→ SFX: OGG Vorbis, Quality 60-80
→ Voice/TTS: WAV (uncompressed - clarity!)

FILE SIZES:
→ Music track (3 min): ~3-5 MB (OGG)
→ SFX (0.5s): ~20-50 KB (OGG)
→ Total audio budget: ~100-150 MB

STREAMING:
→ Music: Stream from disk (don't load into RAM!)
→ SFX: Load into RAM (instant playback)
→ Voice: Stream (dynamic, not preloaded)
```

---

### **Android Audio Settings:**

```
Project Settings → Platforms → Android:

Audio:
☑ Use Android Audio Callbacks
☐ Disable Audio Mixer (keep enabled!)
Sample Rate: 48000 Hz (Android standard)
Callback Buffer Size: 1024 (balance latency/performance)

LATENCY:
- Target: <100ms (acceptable for mobile)
- Music latency: OK (not critical)
- SFX latency: Important! (instant feedback)
- Voice latency: Critical! (real-time calls)

TESTING:
→ Test on Xiaomi 11T Pro
→ Check audio doesn't crackle
→ Check no lag between button press & sound
→ Check TTS plays smoothly
```

---

## 🎚️ AUDIO IMPLEMENTATION CHECKLIST

```
SETUP:
☐ Create Sound Classes (Master, Music, SFX, Voice, Ambient)
☐ Create Sound Mix (ducking rules)
☐ Configure attenuation settings

IMPORT AUDIO:
☐ Import all BGM tracks (OGG, looping enabled)
☐ Import all SFX (OGG, various categories)
☐ Import ambient loops (OGG, looping)
☐ Set compression quality appropriately

BLUEPRINTS:
☐ BP_MusicManager (zone music transitions)
☐ BP_AudioManager (SFX playback, volume control)
☐ Update BP_NajikaPlayerController (footstep triggers)
☐ Update UI widgets (button click sounds)

ANIMATION:
☐ Add Animation Notifies for footsteps
☐ Add Animation Notifies for combat sounds
☐ Setup lip sync in ABP_Najika

LEVEL:
☐ Place Ambient Sound actors (birds, wind, water)
☐ Set audio volumes (test balance!)
☐ Test music transitions between zones

TESTING:
☐ Test all UI sounds
☐ Test footsteps on different surfaces
☐ Test combat sounds
☐ Test music loops seamlessly
☐ Test TTS voice playback
☐ Test audio on device (not just editor!)
☐ Test with headphones AND speakers
☐ Check audio levels (nothing too loud/quiet)

POLISH:
☐ Fine-tune volume levels
☐ Add missing sounds
☐ Implement ducking
☐ Create settings menu (volume sliders)
```

---

## 🎵 FREE AUDIO RESOURCES

### **Where to Get Audio:**

```
MUSIC:
- Incompetech (Kevin MacLeod) - Free with attribution!
  https://incompetech.com/music/
- Free Music Archive
  https://freemusicarchive.org
- Purple Planet Music
  https://www.purple-planet.com
- Bensound
  https://www.bensound.com

SFX:
- Freesound.org - Huge library!
  https://freesound.org
- Zapsplat - Free SFX
  https://www.zapsplat.com
- BBC Sound Effects - Public domain!
  https://sound-effects.bbcrewind.co.uk
- Mixkit - Free SFX
  https://mixkit.co/free-sound-effects/

TOOLS:
- Audacity (Free audio editor)
  https://www.audacityteam.org
- LMMS (Free music production)
  https://lmms.io
- FL Studio (Paid, powerful)
  https://www.image-line.com

AI MUSIC GENERATION:
- Suno AI (generate custom music!)
- Udio
- MusicGen (Meta)
```

---

## 🎉 SOUND DESIGN COMPLETE!

**Summary:**
- ✅ BGM: 10 tracks planned
- ✅ SFX: ~100 sound effects categorized
- ✅ Ambient: All environment sounds listed
- ✅ Voice: TTS system planned
- ✅ Mixing: Sound Classes & ducking setup
- ✅ Mobile: Optimized for Android
- ✅ Implementation: Complete checklist

**Next Steps:**
1. Download/Create audio files
2. Import into UE5 (Content/Audio/)
3. Setup Sound Classes
4. Create BP_MusicManager & BP_AudioManager
5. Add sounds to UI/Animations/Combat
6. Test & balance volumes
7. Deploy & enjoy! 🎵

---

**Model 1 - Digivice APK Development**
**Guide:** Complete Sound Design
**Status:** Ready to Implement! ✅

**MAKE NAJIKA SOUND AMAZING! 🎵🚀**
