# 🎨 Asset Acquisition Guide - Complete Walkthrough

**Purpose:** Get all necessary 3D models, animations, audio, and UI assets for Najika Digivice

---

## 📋 Table of Contents

1. [Najika 3D Character Model](#1-najika-3d-character-model)
2. [Animations (40+ needed)](#2-animations)
3. [Audio Assets](#3-audio-assets)
4. [UI Assets](#4-ui-assets)
5. [Environment Assets](#5-environment-assets)
6. [Import into UE5](#6-import-into-ue5)

---

## 1️⃣ Najika 3D Character Model

### Option A: Mixamo (FREE + Easy) ⭐ RECOMMENDED

**Perfect for prototyping and indie games!**

#### Step 1: Choose Base Character

1. Go to: https://www.mixamo.com
2. Sign in with Adobe account (free)
3. Browse Characters → Female
4. Look for anime-style characters:
   - **"Amy"** - cute, anime-ish
   - **"Kaya"** - young female
   - **"Aj"** - athletic girl

5. Click character → Customize (change colors if you want)

#### Step 2: Download Character

1. Click **"Download"** button
2. Format: **FBX Binary (.fbx)**
3. Pose: **T-Pose**
4. Include: **✅ Skin** (check this!)
5. Frames/second: **30**
6. Download → Save to: `C:\Najika_World\Assets\Characters\Najika\Najika_Base.fbx`

**Size:** ~5-15 MB

---

### Option B: Ready Player Me (Customizable Avatars)

**Good for unique character creation!**

1. Go to: https://readyplayer.me/
2. Create custom avatar:
   - Upload face photo (optional)
   - Choose body type
   - Customize hair, clothes, accessories
3. Export as GLB/FBX
4. **Convert GLB to FBX** (if needed): https://products.aspose.app/3d/conversion/glb-to-fbx

**Pros:**
- ✅ Highly customizable
- ✅ Anime/realistic styles available
- ✅ FREE

**Cons:**
- ❌ More "metaverse" style (less anime)

---

### Option C: VRoid Studio (ANIME STYLE) ⭐ BEST FOR ANIME

**If you want true anime character like Najika!**

#### Download VRoid Studio

1. Go to: https://vroid.com/en/studio
2. Download (Windows 64-bit)
3. Install VRoid Studio

#### Create Najika

1. Open VRoid Studio
2. **New Project** → Female
3. Customize:
   - **Hair:** Pink/Purple (Najika style)
   - **Eyes:** Big, anime-style, vibrant color
   - **Face:** Anime proportions
   - **Body:** Slim, mobile-game optimized
   - **Outfit:** Cute dress or school uniform

4. **Paint textures** (optional, but makes her unique)
5. **Export:**
   - File → Export → VRM
   - Save as: `Najika.vrm`

#### Convert VRM to FBX for UE5

**Use UniVRM Converter:**

1. Download: https://github.com/vrm-c/UniVRM/releases
2. Or use online: https://www.vrmtofbx.com/ (easier!)
3. Upload `Najika.vrm`
4. Download FBX
5. Save to: `C:\Najika_World\Assets\Characters\Najika\`

**Pros:**
- ✅ TRUE anime style
- ✅ Fully customizable
- ✅ FREE
- ✅ Hair physics support

**Cons:**
- ❌ Requires VRM → FBX conversion
- ❌ May need rigging adjustments for UE5

---

### Option D: Purchase from Asset Store

**If you have budget ($20-100):**

**Unreal Marketplace:**
- Search: "Anime Character"
- Filter: Mobile-optimized
- Price: $20-80
- **Examples:**
  - "Stylized Character Kit" (~$50)
  - "Anime Girl Pack" (~$30)

**Unity Asset Store (then convert):**
- More anime characters available
- Export as FBX from Unity
- Import to UE5

---

### Option E: Commission Custom Character

**Professional quality, but expensive:**

**Where to find artists:**
- **Fiverr:** $100-500 (search "3D anime character")
- **ArtStation:** $500-2000 (professional)
- **Sketchfab Artists:** $200-800

**Timeline:** 2-4 weeks

**What to provide:**
- Concept art / reference images
- Character sheet (front, side, back views)
- Color palette
- Technical specs (polycount, UE5 compatible)

---

## 2️⃣ Animations (40+ needed)

### Option A: Mixamo Animations (FREE) ⭐ EASIEST

**Best for beginners!**

#### Step 1: Upload Your Character to Mixamo

1. Go to: https://www.mixamo.com
2. Click **"Upload Character"**
3. Upload your Najika FBX (from Step 1)
4. Mixamo auto-rigs it (2-5 minutes)

**Success:** Character appears rigged and ready!

#### Step 2: Download Animations

**For each animation needed:**

1. Browse Animations library
2. Search for animation (e.g., "idle", "walk", "run")
3. Click animation → Preview on your character
4. Click **"Download"**

**Download Settings:**
- Format: **FBX Binary**
- Skin: **❌ Without Skin** (we already have character mesh)
- Frames/second: **30**
- **Important:** ✅ **In Place** (for locomotion) or **✅ Atexit** (for root motion)

#### Recommended Animations List:

**Locomotion (9):**
- Idle
- Walking
- Walking Backward
- Strafe Left
- Strafe Right
- Running
- Jump (or Jump Start)
- Jump Loop (In Air)
- Jump Land

**Combat (9):**
- Punch (or variants: Punch 1, 2, 3)
- Kick
- Cast Spell (search "magic" or "casting")
- Block
- Hit Reaction Front
- Hit Reaction Back
- Death (or Fall)

**Interaction (6):**
- Pick Up Item
- Use Item
- Sitting Down
- Sitting Idle
- Standing Up
- Talking (or Waving)

**Emotes (5):**
- Wave
- Dance (many variants!)
- Cheer
- Crying
- Laugh

**Download all to:** `C:\Najika_World\Assets\Characters\Najika\Animations\`

**Total downloads:** ~30-40 animations (5-10 minutes)

---

### Option B: Asset Store Animation Packs

**If Mixamo doesn't have what you need:**

**Unreal Marketplace:**
- "Animation Starter Pack" (FREE!)
- "Advanced Locomotion System" (~$40)

**Unity Asset Store (convert to FBX):**
- "Mecanim Animation Pack" (~$20)

---

## 3️⃣ Audio Assets

### Music Tracks (6 needed)

#### Option A: Free Royalty-Free Music

**Incompetech (by Kevin MacLeod):**
1. Go to: https://incompetech.com/music/royalty-free/
2. Browse by mood:
   - **Menu Theme:** "Carefree" or "Wallpaper"
   - **Gameplay:** "Cipher" or "Pixel Peeker Polka"
   - **Combat:** "Volatile Reaction" or "Cipher"
   - **Boss Battle:** "Mechanolith" or "Black Vortex"
   - **Victory:** "Jaunty Gumption"
   - **Game Over:** "Sorrow"

3. Download MP3 → Convert to OGG (for UE5)

**Attribution:** Must credit "Kevin MacLeod (incompetech.com)" in game

---

#### Option B: Epidemic Sound ($15/month)

1. Go to: https://www.epidemicsound.com/
2. Subscribe: $15/month (personal)
3. Download unlimited royalty-free music
4. Better quality than free options

---

### Sound Effects (50+ needed)

#### Free Sources:

**Freesound.org:**
1. Go to: https://freesound.org
2. Create free account
3. Search for:
   - UI Sounds: "button click", "ui beep", "menu open"
   - Combat: "punch hit", "sword swing", "magic spell"
   - Environment: "footstep grass", "door open", "chest open"

4. Download as WAV (best quality)

**ZapSplat:**
1. Go to: https://www.zapsplat.com/
2. Free account (attribution required)
3. Download SFX packs

**OpenGameArt:**
1. Go to: https://opengameart.org/art-search-advanced?keys=&field_art_type_tid=13
2. Filter: Sound Effects
3. License: CC0 (public domain)

---

### Voice Acting (Optional)

#### Option A: ElevenLabs TTS (AI Voice)

1. Go to: https://elevenlabs.io/
2. Sign up (free tier: 10K chars/month)
3. Choose/create voice:
   - Browse Voice Library → Anime/Young Female
   - Or clone voice from sample

4. Generate Najika's lines:
   - "Hello! I'm Najika!"
   - "Let's train together!"
   - "I'm hungry..."
   - (etc., 20-50 lines)

5. Download as MP3

**Cost:** Free tier OK for testing, $5/month for full game

---

#### Option B: Voice Actor (Professional)

**Where to find:**
- **Fiverr:** $20-100 per script
- **Voices.com:** $100-500 (professional)
- **CastingCall.Club:** FREE (community voice actors)

**What you need:**
- Script (20-50 lines)
- Voice direction ("Energetic anime girl, age 16-18")
- Character description

**Timeline:** 1-2 weeks

---

## 4️⃣ UI Assets (Icons, Buttons, Panels)

### Icons (100+ needed)

#### Option A: Flaticon (FREE + Paid)

1. Go to: https://www.flaticon.com
2. Search for:
   - Game icons
   - RPG icons
   - Mobile game icons

3. Create collection:
   - Health potion icon
   - Mana potion icon
   - Sword icon
   - Shield icon
   - Settings icon
   - Chat icon
   - Inventory icon
   - (50-100 more)

4. Download:
   - Format: PNG
   - Size: 256x256 or 512x512
   - Free: Attribution required
   - Premium: $10/month, no attribution

**Save to:** `C:\Najika_World\Assets\UI\Icons\`

---

#### Option B: Icons8 (FREE + Paid)

1. Go to: https://icons8.com/icons
2. Style: "Cute Color" or "Fluffy"
3. Download icons
4. Free: Attribution, PNG only
5. Paid: $20/month, SVG + PNG

---

#### Option C: Game-Icons.net (FREE, Open Source)

1. Go to: https://game-icons.net/
2. Search game-related icons
3. Download SVG (scalable)
4. Convert to PNG if needed
5. License: CC-BY 3.0 (attribution)

---

### Buttons & UI Elements

#### Create Custom Buttons (Figma - FREE)

1. Go to: https://www.figma.com
2. Sign up (free account)
3. New Design File
4. Use Button template:
   - Rectangle: 512x128
   - Rounded corners: 20px
   - Fill: Gradient (pink → purple)
   - Text: "Button"
   - Export as PNG (4 states: Normal, Hover, Pressed, Disabled)

**Or use pre-made:**
- Search Figma Community: "Game UI Kit"
- Duplicate free kit
- Customize colors
- Export

---

#### Asset Store UI Packs

**Unreal Marketplace:**
- "UI Essentials Kit" (FREE)
- "Sci-Fi UI Pack" (~$20)

---

## 5️⃣ Environment Assets (Optional - Can use placeholders)

### Quick Setup: UE5 Built-in Assets

**UE5 includes:**
- ✅ Starter Content (landscapes, props)
- ✅ City Sample (free, high-quality city)
- ✅ Procedural Foliage (trees, grass)

**How to enable:**
1. Open UE5 project
2. Edit → Project Settings → Engine → Starter Content
3. Enable: ✅ Show Starter Content

**No download needed!**

---

### Free Asset Packs

**Megascans (Quixel Bridge - FREE for UE5):**
1. Download: Quixel Bridge app
2. Sign in with Epic Games account
3. Browse assets:
   - Landscapes
   - Props
   - Vegetation
4. Download directly to UE5 project

**Cost:** FREE (unlimited for UE5 projects)

---

## 6️⃣ Import into UE5

### Folder Structure

**Create in UE5 Content Browser:**

```
Content/
├── Characters/
│   └── Najika/
│       ├── Meshes/
│       │   └── SK_Najika.fbx
│       ├── Textures/
│       │   ├── T_Najika_BaseColor.png
│       │   ├── T_Najika_Normal.png
│       │   └── T_Najika_Roughness.png
│       └── Animations/
│           ├── Idle.fbx
│           ├── Walk.fbx
│           └── (40+ more)
├── Audio/
│   ├── Music/
│   │   ├── BGM_Menu.ogg
│   │   ├── BGM_Gameplay.ogg
│   │   └── (6 tracks)
│   └── SFX/
│       ├── UI/
│       ├── Combat/
│       └── Environment/
└── UI/
    ├── Icons/
    ├── Buttons/
    └── Panels/
```

---

### Import Character Model

1. **Drag & Drop** `Najika_Base.fbx` into Content Browser → Characters/Najika/Meshes/
2. Import Options:
   - Skeletal Mesh: ✅
   - Import Animations: ❌ (we'll import separately)
   - Materials: ✅ Create Materials
   - Normal Import Method: Import Normals
3. Click **Import All**

**Result:**
- `SK_Najika` (Skeletal Mesh)
- `SK_Najika_Skeleton` (Skeleton asset)
- Materials (M_Najika_Body, etc.)

---

### Import Animations

1. **Select all** animation FBX files
2. **Drag & Drop** into Content Browser → Characters/Najika/Animations/
3. Import Options:
   - Skeleton: **Select SK_Najika_Skeleton** (important!)
   - Import Meshes: ❌
   - Import Animations: ✅
4. Click **Import All**

**Result:** 40+ Animation assets

---

### Import Audio

**Music:**
1. Drag `.ogg` files → Content/Audio/Music/
2. Auto-imports as Sound Wave assets

**SFX:**
1. Drag `.wav` files → Content/Audio/SFX/
2. Organize in subfolders (UI/, Combat/, etc.)

---

### Import UI Assets

**Icons:**
1. Drag PNG files → Content/UI/Icons/
2. Import as Texture
3. Compression: **UserInterface2D (RGBA)**

**Buttons:**
1. Create Material:
   - Right-click → Material → User Interface
   - Name: M_Button
   - Add Texture Sample node
   - Connect to Final Color

---

## ✅ Asset Acquisition Checklist

### Character
- [ ] Najika 3D Model downloaded
- [ ] Imported to UE5 as Skeletal Mesh
- [ ] Textures working (not pink)
- [ ] Skeleton created

### Animations
- [ ] 9 Locomotion animations
- [ ] 9 Combat animations
- [ ] 6 Interaction animations
- [ ] 5 Emote animations (optional)
- [ ] All animations imported with correct skeleton

### Audio
- [ ] 6 Music tracks (OGG format)
- [ ] 20+ UI sound effects
- [ ] 20+ Combat sound effects
- [ ] 10+ Environment sounds
- [ ] (Optional) Voice lines

### UI
- [ ] 50+ Icons (256x256 PNG)
- [ ] Button images (Normal, Hover, Pressed, Disabled)
- [ ] Panel backgrounds
- [ ] Font (readable on mobile)

### Environment (Optional)
- [ ] Starter Content enabled
- [ ] Or Quixel Megascans downloaded

---

## 💰 Cost Breakdown

### Budget Option (FREE!)
- Character: Mixamo (FREE)
- Animations: Mixamo (FREE)
- Music: Incompetech (FREE)
- SFX: Freesound (FREE)
- UI: Flaticon Free (with attribution)
- **Total: $0**

### Standard Option (~$50)
- Character: VRoid Studio (FREE)
- Animations: Mixamo (FREE)
- Music: Epidemic Sound (1 month, $15)
- SFX: ZapSplat Premium ($20/year)
- UI: Flaticon Premium (1 month, $10)
- Voice: ElevenLabs (1 month, $5)
- **Total: ~$50**

### Premium Option (~$500)
- Character: Commission ($200-400)
- Animations: Asset Store Pack ($50)
- Music: Custom Composer ($100-200)
- Voice Actor: Professional ($50-100)
- UI: Custom Design ($50-100)
- **Total: ~$450-850**

---

## 📝 Next Steps

1. ✅ Choose character option (Mixamo/VRoid/Commission)
2. ✅ Download character model
3. ✅ Download 40+ animations from Mixamo
4. ✅ Gather audio assets (music + SFX)
5. ✅ Download/create UI assets
6. ✅ Import all to UE5
7. ✅ Verify assets work (no errors)
8. ✅ Proceed to Blueprint creation!

**Recommended Timeline:**
- Day 1: Character + Animations (2-4 hours)
- Day 2: Audio gathering (2-3 hours)
- Day 3: UI assets (1-2 hours)
- Day 4: Import & verify all assets (2-3 hours)

**Ready to start?** 🚀
