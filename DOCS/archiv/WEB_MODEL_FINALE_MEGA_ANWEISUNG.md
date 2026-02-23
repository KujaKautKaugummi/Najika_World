# 🚀 WEB MODEL - FINALE MEGA-ANWEISUNG
**Datum:** 2025-11-18 (Spät)
**Von:** Claude Code
**An:** Web Model (Sonnet 4)
**Priorität:** ULTRA-HIGH
**Ziel:** ALLES FERTIG MACHEN was möglich ist!

---

## 🎯 MISSION BRIEFING

**ZIEL:**
Du sollst ALLES implementieren was technisch machbar ist, damit Najika World **KOMPLETT SPIELBAR** wird!

**4 HAUPTAUFGABEN:**

1. ✅ **Digivice UI Fix** (1-2h) - Aktiviere was schon fertig ist!
2. ✅ **Triple Triad** (6-8h) - Schnelles Sammelspiel
3. ✅ **DDM Synergy Master** (15-20h) - Wettbewerbs-Modul
4. ✅ **8-Regionen Map** (10-15h) - Lebensraum + Weltmap

**TOTAL:** ~40-50 Stunden Arbeit

---

## 📋 TASK 1: DIGIVICE UI FIX (QUICK WIN!)

### **PROBLEM:**
Code ist DA (747 Zeilen in `game_systems_ui.js`), aber NICHT geladen!

**File:** `digivice/js/ui/game_systems_ui.js`

### **WAS DRIN IST:**
```javascript
// 5 KOMPLETTE UI-SYSTEME:
- RegionBossUI (Territory Control, Boss Challenges)
- OregonEventsUI (Journey, Events, Choices)
- MagicSchoolsUI (9 Schools, Casting, Weaving)
- InstrumentUI (Note Playing, Song Learning)
- WorldInfoUI (Time, Weather, Biomes)
```

### **WAS DU TUN MUSST:**

#### **SCHRITT 1: Script Tag hinzufügen**
**File:** `digivice/index.html`

Füge NACH `<script src="/digivice/js/3d_scene.js"></script>` hinzu:

```html
<script src="/digivice/js/ui/game_systems_ui.js"></script>
```

#### **SCHRITT 2: UI Initialisierung**
**File:** `digivice/index.html` (im `<script>` Block am Ende)

Füge hinzu:

```javascript
// Initialize Game System UIs
window.regionBossUI = new RegionBossUI();
window.oregonUI = new OregonEventsUI();
window.magicUI = new MagicSchoolsUI();
window.instrumentUI = new InstrumentUI();
window.worldUI = new WorldInfoUI();

console.log('✅ All Game System UIs initialized!');
```

#### **SCHRITT 3: Menu Buttons**
**File:** `digivice/index.html` (im Action Bar)

Füge Buttons hinzu:

```html
<button onclick="window.regionBossUI.show()">🏰 Region Boss</button>
<button onclick="window.oregonUI.show()">🛤️ Oregon Trail</button>
<button onclick="window.magicUI.show()">✨ Magic</button>
<button onclick="window.instrumentUI.show()">🎵 Instruments</button>
<button onclick="window.worldUI.show()">🌍 World Info</button>
```

### **FERTIG!**
Nach diesem Fix sind 5 große Features SOFORT spielbar!

---

## 📋 TASK 2: TRIPLE TRIAD (SAMMELSPIEL)

### **🎯 KONZEPT:**

**Triple Triad** = FF8 Kartenspiel, ABER mit **3D Spielsteinen** statt Karten!

**ZWECK:**
- Schnelles, einfaches Spiel (überall spielbar!)
- Sammle Spielsteine (werden zu DDM Würfeln!)
- 100 verschiedene Spielsteine

### **SPIELREGELN:**

#### **Board:**
```
3×3 Grid (9 Felder)

┌───┬───┬───┐
│ 1 │ 2 │ 3 │
├───┼───┼───┤
│ 4 │ 5 │ 6 │
├───┼───┼───┤
│ 7 │ 8 │ 9 │
└───┴───┴───┘
```

#### **Spielsteine:**
Jeder Stein hat **4 Richtungswerte** (1-10):

```javascript
{
  id: 1,
  name: "Fire Imp",
  top: 5,
  right: 3,
  bottom: 7,
  left: 2,
  element: "fire", // fire, water, lightning, nature, shadow, holy
  rarity: "common", // common, rare, epic, legendary
  model_url: "/assets/models/fire_imp.glb" // 3D Model!
}
```

#### **Gameplay:**

1. **Beide Spieler:** 5 Steine aus Sammlung wählen
2. **Turns:** Abwechselnd Stein auf Grid platzieren
3. **Capture:** Wenn dein Stein-Wert > Gegner-Wert an Grenze → Capture!
4. **Win:** Mehr Steine auf Board am Ende = Win!

**BEISPIEL:**
```
Du platzierst Fire Imp (Right: 7) links von Gegner-Stein (Left: 5)
→ 7 > 5 = CAPTURE!
→ Gegner-Stein wird DEIN Stein!
```

#### **3D Präsentation:**
```
- Steine werden als 3D Models angezeigt (wie Yu-Gi-Oh!)
- Schweben über dem Grid
- Angriffs-Animation wenn Capture
- Optional Toggle: An/Aus für Animationen
```

---

### **DATABASE MODELS:**

#### **1. TripleTriadCard (Monster-Steine)**

**File:** `backend/models/triple_triad.py`

```python
from sqlalchemy import Column, Integer, String, Enum
from backend.database import Base

class TripleTriadCard(Base):
    __tablename__ = "triple_triad_cards"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    # Richtungswerte (1-10)
    top_value = Column(Integer, default=5)
    right_value = Column(Integer, default=5)
    bottom_value = Column(Integer, default=5)
    left_value = Column(Integer, default=5)

    # Eigenschaften
    element = Column(Enum('fire', 'water', 'lightning', 'nature', 'shadow', 'holy', name='element_enum'))
    rarity = Column(Enum('common', 'rare', 'epic', 'legendary', name='rarity_enum'))

    # 3D Model
    model_url = Column(String(255))
    description = Column(String(500))

    # Hearthstone-Style Sprüche
    summon_quote = Column(String(200))
    attack_quote = Column(String(200))
    death_quote = Column(String(200))
```

#### **2. PlayerCardCollection (Spieler-Sammlung)**

```python
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class PlayerCardCollection(Base):
    __tablename__ = "player_card_collection"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    card_id = Column(Integer, ForeignKey('triple_triad_cards.id'))

    # Wie viele von dieser Karte?
    quantity = Column(Integer, default=1)

    # Golden Version?
    is_golden = Column(Boolean, default=False)

    # Relationships
    card = relationship("TripleTriadCard")
```

#### **3. TripleTriadMatch (Spiel-History)**

```python
from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from datetime import datetime

class TripleTriadMatch(Base):
    __tablename__ = "triple_triad_matches"

    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey('users.id'))
    player2_id = Column(Integer, ForeignKey('users.id'))  # Oder NULL für NPC

    # Spiel-State
    winner_id = Column(Integer, ForeignKey('users.id'))
    board_state = Column(JSON)  # Final board
    turn_count = Column(Integer)

    # Belohnung
    cards_won = Column(JSON)  # Liste von Card IDs

    created_at = Column(DateTime, default=datetime.utcnow)
```

---

### **API ENDPOINTS:**

**File:** `backend/api/triple_triad.py`

#### **1. GET /api/triple-triad/cards** - Alle verfügbaren Karten

```python
@router.get("/cards")
async def get_all_cards(db: Session = Depends(get_db)):
    """Get all Triple Triad cards"""
    cards = db.query(TripleTriadCard).all()
    return {"cards": cards}
```

#### **2. GET /api/triple-triad/collection** - Spieler-Sammlung

```python
@router.get("/collection")
async def get_player_collection(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get player's card collection"""
    collection = db.query(PlayerCardCollection)\
        .filter(PlayerCardCollection.user_id == user_id)\
        .all()

    # Include card details
    cards_with_details = []
    for item in collection:
        card_dict = item.card.__dict__.copy()
        card_dict['quantity'] = item.quantity
        card_dict['is_golden'] = item.is_golden
        cards_with_details.append(card_dict)

    return {"collection": cards_with_details}
```

#### **3. POST /api/triple-triad/match/start** - Neues Spiel starten

```python
from pydantic import BaseModel
from typing import List

class StartMatchRequest(BaseModel):
    opponent_id: int = None  # NULL = NPC
    selected_cards: List[int]  # 5 Card IDs

@router.post("/match/start")
async def start_match(
    request: StartMatchRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Start new Triple Triad match"""
    # Validate cards
    if len(request.selected_cards) != 5:
        raise HTTPException(400, "Must select exactly 5 cards")

    # Check ownership
    for card_id in request.selected_cards:
        owned = db.query(PlayerCardCollection)\
            .filter(
                PlayerCardCollection.user_id == user_id,
                PlayerCardCollection.card_id == card_id
            ).first()
        if not owned:
            raise HTTPException(400, f"You don't own card {card_id}")

    # Create match
    match = TripleTriadMatch(
        player1_id=user_id,
        player2_id=request.opponent_id,
        board_state={"grid": [None] * 9, "current_turn": "player1"},
        turn_count=0
    )
    db.add(match)
    db.commit()

    return {"match_id": match.id, "board_state": match.board_state}
```

#### **4. POST /api/triple-triad/match/play** - Zug spielen

```python
class PlayCardRequest(BaseModel):
    match_id: int
    card_id: int
    position: int  # 0-8 (Grid position)

@router.post("/match/play")
async def play_card(
    request: PlayCardRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Play a card on the board"""
    match = db.query(TripleTriadMatch)\
        .filter(TripleTriadMatch.id == request.match_id)\
        .first()

    if not match:
        raise HTTPException(404, "Match not found")

    # Validate position
    if request.position < 0 or request.position > 8:
        raise HTTPException(400, "Invalid position")

    board = match.board_state
    if board['grid'][request.position] is not None:
        raise HTTPException(400, "Position already occupied")

    # Get card
    card = db.query(TripleTriadCard)\
        .filter(TripleTriadCard.id == request.card_id)\
        .first()

    # Place card
    board['grid'][request.position] = {
        "card_id": card.id,
        "player": "player1" if match.player1_id == user_id else "player2",
        "top": card.top_value,
        "right": card.right_value,
        "bottom": card.bottom_value,
        "left": card.left_value
    }

    # Check captures (Simplified - implement full logic!)
    captures = check_captures(board, request.position)

    # Update board
    for capture_pos in captures:
        current_player = "player1" if match.player1_id == user_id else "player2"
        board['grid'][capture_pos]['player'] = current_player

    # Switch turn
    board['current_turn'] = "player2" if board['current_turn'] == "player1" else "player1"
    match.turn_count += 1

    # Check if game over (9 cards placed)
    if match.turn_count >= 9:
        winner = calculate_winner(board)
        match.winner_id = winner

        # Award cards
        if winner == user_id:
            reward_cards = award_random_cards(db, user_id, opponent_cards)
            match.cards_won = [c.id for c in reward_cards]

    match.board_state = board
    db.commit()

    return {
        "board_state": board,
        "captures": captures,
        "game_over": match.turn_count >= 9,
        "winner_id": match.winner_id,
        "cards_won": match.cards_won if match.winner_id else None
    }
```

#### **Helper Functions:**

```python
def check_captures(board, position):
    """Check which adjacent cards are captured"""
    captures = []
    grid = board['grid']
    placed_card = grid[position]

    # Check all 4 directions
    adjacents = {
        "top": position - 3 if position >= 3 else None,
        "right": position + 1 if (position + 1) % 3 != 0 else None,
        "bottom": position + 3 if position <= 5 else None,
        "left": position - 1 if position % 3 != 0 else None
    }

    for direction, adj_pos in adjacents.items():
        if adj_pos is None:
            continue

        adj_card = grid[adj_pos]
        if adj_card is None:
            continue

        # Different player?
        if adj_card['player'] == placed_card['player']:
            continue

        # Compare values
        placed_value = placed_card[direction]
        opposite = {"top": "bottom", "right": "left", "bottom": "top", "left": "right"}
        adj_value = adj_card[opposite[direction]]

        if placed_value > adj_value:
            captures.append(adj_pos)

    return captures

def calculate_winner(board):
    """Count cards per player"""
    player1_count = sum(1 for card in board['grid'] if card and card['player'] == 'player1')
    player2_count = sum(1 for card in board['grid'] if card and card['player'] == 'player2')

    return "player1" if player1_count > player2_count else "player2"

def award_random_cards(db, winner_id, opponent_cards):
    """Award random cards from opponent"""
    import random
    # Award 1-3 random cards from opponent's deck
    num_awards = random.randint(1, 3)
    awarded = random.sample(opponent_cards, min(num_awards, len(opponent_cards)))

    for card_id in awarded:
        # Add to winner's collection
        existing = db.query(PlayerCardCollection)\
            .filter(
                PlayerCardCollection.user_id == winner_id,
                PlayerCardCollection.card_id == card_id
            ).first()

        if existing:
            existing.quantity += 1
        else:
            new_card = PlayerCardCollection(
                user_id=winner_id,
                card_id=card_id,
                quantity=1
            )
            db.add(new_card)

    db.commit()
    return awarded
```

---

### **FRONTEND UI:**

**File:** `digivice/js/ui/triple_triad_ui.js`

```javascript
class TripleTriadUI {
    constructor() {
        this.apiBase = '/api/triple-triad';
        this.currentMatch = null;
        this.selectedCards = [];
        this.createUI();
    }

    createUI() {
        this.modal = document.createElement('div');
        this.modal.id = 'triple-triad-modal';
        this.modal.className = 'game-modal hidden';
        this.modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h2>⚔️ Triple Triad</h2>
                    <button class="close-btn" onclick="window.tripleTriadUI.hide()">✕</button>
                </div>

                <div class="modal-body">
                    <!-- Deck Selection -->
                    <div id="tt-deck-selection" class="tt-screen">
                        <h3>Select 5 Cards</h3>
                        <div id="tt-collection" class="tt-card-grid"></div>
                        <button onclick="window.tripleTriadUI.startMatch()">Start Match</button>
                    </div>

                    <!-- Game Board -->
                    <div id="tt-game-board" class="tt-screen hidden">
                        <div class="tt-grid" id="tt-grid">
                            ${Array(9).fill(0).map((_, i) =>
                                `<div class="tt-cell" data-pos="${i}"></div>`
                            ).join('')}
                        </div>

                        <div class="tt-hand" id="tt-hand"></div>

                        <div class="tt-info">
                            <p>Turn: <span id="tt-turn">Player</span></p>
                            <p>Score: <span id="tt-score">0 - 0</span></p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(this.modal);
    }

    async show() {
        this.modal.classList.remove('hidden');
        await this.loadCollection();
    }

    hide() {
        this.modal.classList.add('hidden');
    }

    async loadCollection() {
        const response = await fetch(`${this.apiBase}/collection?user_id=1`);
        const data = await response.json();

        const grid = document.getElementById('tt-collection');
        grid.innerHTML = '';

        data.collection.forEach(card => {
            const cardEl = document.createElement('div');
            cardEl.className = 'tt-card';
            cardEl.dataset.cardId = card.id;
            cardEl.innerHTML = `
                <div class="tt-card-model">
                    <model-viewer src="${card.model_url}"
                                  auto-rotate
                                  camera-controls
                                  style="width:100%;height:150px">
                    </model-viewer>
                </div>
                <div class="tt-card-stats">
                    <span class="top">${card.top_value}</span>
                    <span class="right">${card.right_value}</span>
                    <span class="bottom">${card.bottom_value}</span>
                    <span class="left">${card.left_value}</span>
                </div>
                <p>${card.name}</p>
                <p class="quantity">×${card.quantity}</p>
            `;

            cardEl.onclick = () => this.selectCard(card.id, cardEl);
            grid.appendChild(cardEl);
        });
    }

    selectCard(cardId, element) {
        if (this.selectedCards.includes(cardId)) {
            this.selectedCards = this.selectedCards.filter(id => id !== cardId);
            element.classList.remove('selected');
        } else if (this.selectedCards.length < 5) {
            this.selectedCards.push(cardId);
            element.classList.add('selected');
        }
    }

    async startMatch() {
        if (this.selectedCards.length !== 5) {
            alert('Select exactly 5 cards!');
            return;
        }

        const response = await fetch(`${this.apiBase}/match/start`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                opponent_id: null, // NPC
                selected_cards: this.selectedCards
            })
        });

        const data = await response.json();
        this.currentMatch = data.match_id;
        this.boardState = data.board_state;

        // Switch to game board
        document.getElementById('tt-deck-selection').classList.add('hidden');
        document.getElementById('tt-game-board').classList.remove('hidden');

        this.renderBoard();
        this.renderHand();
    }

    renderBoard() {
        const grid = document.querySelectorAll('.tt-cell');
        this.boardState.grid.forEach((card, i) => {
            if (card) {
                grid[i].innerHTML = `
                    <model-viewer src="/assets/models/${card.card_id}.glb"
                                  auto-rotate
                                  class="card-model ${card.player}">
                    </model-viewer>
                `;
            }
        });

        // Update score
        const p1 = this.boardState.grid.filter(c => c && c.player === 'player1').length;
        const p2 = this.boardState.grid.filter(c => c && c.player === 'player2').length;
        document.getElementById('tt-score').textContent = `${p1} - ${p2}`;
    }

    renderHand() {
        const hand = document.getElementById('tt-hand');
        hand.innerHTML = '';

        this.selectedCards.forEach(cardId => {
            // Render cards in hand (simplified)
            const cardEl = document.createElement('div');
            cardEl.className = 'tt-hand-card';
            cardEl.onclick = () => this.selectCardToPlay(cardId);
            hand.appendChild(cardEl);
        });
    }

    async playCard(cardId, position) {
        const response = await fetch(`${this.apiBase}/match/play`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                match_id: this.currentMatch,
                card_id: cardId,
                position: position
            })
        });

        const data = await response.json();
        this.boardState = data.board_state;
        this.renderBoard();

        if (data.game_over) {
            alert(`Game Over! Winner: ${data.winner_id === 1 ? 'You' : 'Opponent'}`);
            if (data.cards_won) {
                alert(`You won: ${data.cards_won.join(', ')}`);
            }
        }
    }
}
```

---

### **STARTER CARDS (100 Steine):**

**File:** `backend/data/triple_triad_starter_cards.py`

```python
# Erstelle 100 verschiedene Spielsteine
# Beispiel-Daten (du musst 100 erstellen!)

STARTER_CARDS = [
    # Common (60 Karten)
    {"name": "Fire Imp", "top": 5, "right": 3, "bottom": 7, "left": 2, "element": "fire", "rarity": "common"},
    {"name": "Water Sprite", "top": 4, "right": 6, "bottom": 3, "left": 5, "element": "water", "rarity": "common"},
    {"name": "Lightning Wisp", "top": 6, "right": 4, "bottom": 5, "left": 3, "element": "lightning", "rarity": "common"},
    # ... (57 more common)

    # Rare (25 Karten)
    {"name": "Flame Drake", "top": 7, "right": 6, "bottom": 8, "left": 5, "element": "fire", "rarity": "rare"},
    {"name": "Frost Guardian", "top": 6, "right": 7, "bottom": 6, "left": 7, "element": "water", "rarity": "rare"},
    # ... (23 more rare)

    # Epic (12 Karten)
    {"name": "Storm Dragon", "top": 9, "right": 7, "bottom": 8, "left": 8, "element": "lightning", "rarity": "epic"},
    # ... (11 more epic)

    # Legendary (3 Karten)
    {"name": "Ancient Phoenix", "top": 10, "right": 9, "bottom": 10, "left": 9, "element": "fire", "rarity": "legendary"},
    {"name": "Leviathan", "top": 9, "right": 10, "bottom": 9, "left": 10, "element": "water", "rarity": "legendary"},
    {"name": "Bahamut", "top": 10, "right": 10, "bottom": 10, "left": 10, "element": "lightning", "rarity": "legendary"}
]

# Seed Database Funktion
def seed_triple_triad_cards(db: Session):
    for card_data in STARTER_CARDS:
        card = TripleTriadCard(**card_data)
        db.add(card)
    db.commit()
    print(f"✅ Seeded {len(STARTER_CARDS)} Triple Triad cards!")
```

---

## 📋 TASK 3: DDM SYNERGY MASTER (WETTBEWERBS-MODUL)

### **🎯 KONZEPT:**

**DDM Synergy Master** = Yu-Gi-Oh! Dungeon Dice Monsters GBA + MTG Tiefe!

**ZWECK:**
- Komplexes Wettbewerbs-Spiel (nur in Arena/speziellen Räumen!)
- Nutzt Triple Triad Steine als Würfel!
- Path-Building + Tactical Grid Combat

---

### **KERN-MECHANIKEN:**

#### **1. DDM GBA Path-Building:**

```javascript
// Würfel-Pool: 15 Würfel (vor Match wählen)
// Roll Phase: 3 Würfel pro Turn
// Crests sammeln
// 2 Summon Crests = Monster summonen!
// Würfel entfaltet sich = 6 Squares Path auf Grid!
// Monster spawnt auf Path
// Bewege entlang Path zum Gegner
// 30 HP Dice Lord auf 0 = WIN!
```

#### **2. Hybrid 2 (Auto-Mana + Opfer):**

```javascript
// Würfel geben AUTOMATISCH: Crests + Mana
// Beispiel Roll: [Summon Lv2] + [🔥 Fire Mana]
// → Bekommst: 1 Summon Crest + 1🔥 Fire Mana

// Opfer-Mechanik:
// Opfere 1 Crest → +2⚪ generisches Mana
// Flexibilität für Big Spells!
```

#### **3. 2-Crest Synergy (12 Kombos):**

```javascript
// BASIC COMBOS (Cross-Type):
// 1. Summon + Movement = Rush Summon (Monster greift sofort!)
// 2. Summon + Defense = Guardian Summon (+5 HP, Taunt)
// 3. Movement + Attack = Blitz (+3 ATK beim Angriff)
// 4. Movement + Defense = Tactical Retreat (Block 50%)
// 5. Attack + Magic = Power Strike (Attack + Spell gleichzeitig)

// SAME-TYPE COMBOS:
// 6. Summon + Summon = Twin Summon (2 Monster!)
// 7. Movement + Movement = Formation Move (3 Monster bewegen!)
// 8. Attack + Attack = Double Strike (2x angreifen!)
// 9. Defense + Defense = Fortress (Block 100% + Heal 3 HP!)
// 10. Magic + Magic = Spell Cascade (2 Spells gleichzeitig!)

// ADVANCED COMBOS:
// 11. Summon + Attack = Aggressive Summon (Monster greift 2x sofort!)
// 12. Defense + Magic = Arcane Shield (Block 100% + Reflect 3 Damage!)
```

#### **4. Optional Basic Charging:**

```javascript
// Wenn du KEINE Combo nutzt, kannst du warten:
// 1 Crest = Basic Action
// 2 Crests = +1 Bonus
// 3+ Crests = +2 Bonus

// Beispiel:
// 1 Summon = Summon 1-3 Cost Monster
// 2 Summon = Summon 4-6 Cost Monster
// 3 Summon = Summon 7-10 Cost Monster
```

---

### **DATABASE MODELS:**

**File:** `backend/models/ddm_game.py`

```python
from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Enum, Boolean
from datetime import datetime
from backend.database import Base

# 1. DDM Monster (aus Triple Triad Steinen erstellt!)
class DDMMonster(Base):
    __tablename__ = "ddm_monsters"

    id = Column(Integer, primary_key=True)

    # Verbindung zu Triple Triad Card!
    source_card_id = Column(Integer, ForeignKey('triple_triad_cards.id'))

    # Monster Stats
    name = Column(String(100))
    cost = Column(Integer)  # 1-10 Mana Cost
    attack = Column(Integer)  # ATK
    defense = Column(Integer)  # DEF
    health = Column(Integer)  # HP

    # Element (von Triple Triad Karte)
    element = Column(Enum('fire', 'water', 'lightning', 'nature', 'shadow', 'holy'))

    # Abilities/Keywords
    keywords = Column(JSON)  # ["Flying", "Trample", "Lifelink"]
    triggers = Column(JSON)  # [{"type": "etb", "effect": "deal_damage", "value": 3}]

    # 3D Model (von Triple Triad!)
    model_url = Column(String(255))

    # Hearthstone Sprüche
    summon_quote = Column(String(200))
    attack_quote = Column(String(200))
    death_quote = Column(String(200))

# 2. DDM Würfel (Pool von 15 pro Spieler)
class DDMDice(Base):
    __tablename__ = "ddm_dice"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    monster_id = Column(Integer, ForeignKey('ddm_monsters.id'))

    # Würfel-Level (für Dice Mastery später)
    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)

    # Würfel Faces (6 Faces mit Crests)
    faces = Column(JSON)  # [{"crest": "summon_lv2", "mana": "fire"}, ...]

# 3. DDM Match
class DDMMatch(Base):
    __tablename__ = "ddm_matches"

    id = Column(Integer, primary_key=True)

    # Players
    player1_id = Column(Integer, ForeignKey('users.id'))
    player2_id = Column(Integer, ForeignKey('users.id'))

    # Match State
    current_turn = Column(String(10))  # "player1" or "player2"
    turn_count = Column(Integer, default=0)

    # Grid State (Path-Building!)
    grid_state = Column(JSON)  # {"width": 15, "height": 15, "cells": [...]}

    # Player States
    player1_state = Column(JSON)  # {"hp": 30, "crests": {...}, "mana": {...}, "monsters": [...]}
    player2_state = Column(JSON)

    # Winner
    winner_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

# 4. DDM Match History (für Replays)
class DDMMatchAction(Base):
    __tablename__ = "ddm_match_actions"

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('ddm_matches.id'))

    turn_number = Column(Integer)
    player = Column(String(10))  # "player1" or "player2"

    action_type = Column(String(50))  # "roll", "summon", "move", "attack", "spell"
    action_data = Column(JSON)  # Details

    created_at = Column(DateTime, default=datetime.utcnow)
```

---

### **API ENDPOINTS:**

**File:** `backend/api/ddm.py`

#### **1. GET /api/ddm/dice-pool** - Spieler Würfel-Pool

```python
@router.get("/dice-pool")
async def get_dice_pool(user_id: int, db: Session = Depends(get_db)):
    """Get player's DDM dice pool (15 dice max)"""
    dice = db.query(DDMDice)\
        .filter(DDMDice.user_id == user_id)\
        .limit(15)\
        .all()

    dice_with_monsters = []
    for die in dice:
        monster = db.query(DDMMonster)\
            .filter(DDMMonster.id == die.monster_id)\
            .first()

        dice_with_monsters.append({
            "die_id": die.id,
            "monster": monster.__dict__,
            "level": die.level,
            "xp": die.xp,
            "faces": die.faces
        })

    return {"dice_pool": dice_with_monsters}
```

#### **2. POST /api/ddm/create-dice** - Konvertiere Triple Triad Karte zu DDM Würfel

```python
class CreateDiceRequest(BaseModel):
    card_id: int  # Triple Triad Card

@router.post("/create-dice")
async def create_ddm_dice(
    request: CreateDiceRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Convert Triple Triad card to DDM dice"""
    # Check if player owns card
    card_owned = db.query(PlayerCardCollection)\
        .filter(
            PlayerCardCollection.user_id == user_id,
            PlayerCardCollection.card_id == request.card_id
        ).first()

    if not card_owned or card_owned.quantity < 1:
        raise HTTPException(400, "You don't own this card")

    # Get card
    card = db.query(TripleTriadCard)\
        .filter(TripleTriadCard.id == request.card_id)\
        .first()

    # Create DDM Monster from card stats
    monster = DDMMonster(
        source_card_id=card.id,
        name=card.name,
        cost=calculate_cost_from_stats(card),
        attack=card.top_value + card.right_value,  # Simple conversion
        defense=card.bottom_value + card.left_value,
        health=(card.top_value + card.right_value + card.bottom_value + card.left_value) // 2,
        element=card.element,
        keywords=[],  # Add based on stats/element
        triggers=[],
        model_url=card.model_url,
        summon_quote=card.summon_quote,
        attack_quote=card.attack_quote,
        death_quote=card.death_quote
    )
    db.add(monster)
    db.flush()

    # Create Dice with 6 faces
    faces = generate_dice_faces(card.element, monster.cost)

    dice = DDMDice(
        user_id=user_id,
        monster_id=monster.id,
        level=1,
        xp=0,
        faces=faces
    )
    db.add(dice)

    # Consume 1 card
    card_owned.quantity -= 1
    if card_owned.quantity <= 0:
        db.delete(card_owned)

    db.commit()

    return {"dice": dice.__dict__, "monster": monster.__dict__}

def calculate_cost_from_stats(card):
    """Calculate monster cost from card stats"""
    total = card.top_value + card.right_value + card.bottom_value + card.left_value
    return min(10, max(1, total // 4))

def generate_dice_faces(element, cost):
    """Generate 6 dice faces based on element/cost"""
    # Simplified - customize based on element!
    return [
        {"crest": f"summon_lv{cost//3 + 1}", "mana": element},
        {"crest": "movement", "mana": element},
        {"crest": "attack", "mana": element},
        {"crest": "defense", "mana": element},
        {"crest": "movement", "mana": element},
        {"crest": "magic", "mana": element}
    ]
```

#### **3. POST /api/ddm/match/start** - Start DDM Match

```python
class StartDDMMatchRequest(BaseModel):
    opponent_id: int = None  # NULL = NPC
    selected_dice: List[int]  # 15 Dice IDs

@router.post("/match/start")
async def start_ddm_match(
    request: StartDDMMatchRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Start new DDM match"""
    if len(request.selected_dice) != 15:
        raise HTTPException(400, "Must select exactly 15 dice")

    # Validate ownership
    for die_id in request.selected_dice:
        owned = db.query(DDMDice)\
            .filter(
                DDMDice.user_id == user_id,
                DDMDice.id == die_id
            ).first()
        if not owned:
            raise HTTPException(400, f"You don't own die {die_id}")

    # Create match
    match = DDMMatch(
        player1_id=user_id,
        player2_id=request.opponent_id,
        current_turn="player1",
        turn_count=1,
        grid_state={
            "width": 15,
            "height": 15,
            "cells": [[None for _ in range(15)] for _ in range(15)],
            "player1_dice_lord": {"x": 7, "y": 0},  # Bottom center
            "player2_dice_lord": {"x": 7, "y": 14}  # Top center
        },
        player1_state={
            "hp": 30,
            "crests": {},
            "mana": {},
            "monsters_on_board": [],
            "dice_pool": request.selected_dice
        },
        player2_state={
            "hp": 30,
            "crests": {},
            "mana": {},
            "monsters_on_board": [],
            "dice_pool": []  # NPC dice (generate)
        }
    )
    db.add(match)
    db.commit()

    return {
        "match_id": match.id,
        "grid_state": match.grid_state,
        "player1_state": match.player1_state
    }
```

#### **4. POST /api/ddm/match/roll** - Roll Dice

```python
class RollDiceRequest(BaseModel):
    match_id: int

@router.post("/match/roll")
async def roll_dice(
    request: RollDiceRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Roll 3 dice from pool"""
    match = db.query(DDMMatch).filter(DDMMatch.id == request.match_id).first()
    if not match:
        raise HTTPException(404, "Match not found")

    # Get player state
    is_player1 = match.player1_id == user_id
    player_state = match.player1_state if is_player1 else match.player2_state

    # Roll 3 random dice
    import random
    available_dice = player_state['dice_pool']
    rolled_dice_ids = random.sample(available_dice, min(3, len(available_dice)))

    # Get dice and roll faces
    rolls = []
    for die_id in rolled_dice_ids:
        die = db.query(DDMDice).filter(DDMDice.id == die_id).first()
        face = random.choice(die.faces)

        rolls.append({
            "die_id": die_id,
            "face": face
        })

        # Add crest to player
        crest_type = face['crest']
        player_state['crests'][crest_type] = player_state['crests'].get(crest_type, 0) + 1

        # Add mana to player (AUTO-MANA!)
        mana_type = face['mana']
        player_state['mana'][mana_type] = player_state['mana'].get(mana_type, 0) + 1

    # Save state
    if is_player1:
        match.player1_state = player_state
    else:
        match.player2_state = player_state

    db.commit()

    return {
        "rolls": rolls,
        "crests": player_state['crests'],
        "mana": player_state['mana']
    }
```

#### **5. POST /api/ddm/match/summon** - Summon Monster

```python
class SummonRequest(BaseModel):
    match_id: int
    die_id: int
    position: dict  # {"x": 7, "y": 1}
    combo: str = None  # "rush_summon", "guardian_summon", etc.

@router.post("/match/summon")
async def summon_monster(
    request: SummonRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Summon monster using 2 Summon Crests"""
    match = db.query(DDMMatch).filter(DDMMatch.id == request.match_id).first()

    is_player1 = match.player1_id == user_id
    player_state = match.player1_state if is_player1 else match.player2_state

    # Get die and monster
    die = db.query(DDMDice).filter(DDMDice.id == request.die_id).first()
    monster = db.query(DDMMonster).filter(DDMMonster.id == die.monster_id).first()

    # Check crests (need 2 Summon Crests with matching level!)
    summon_level = (monster.cost // 3) + 1
    crest_key = f"summon_lv{summon_level}"

    crests_needed = 1  # Default: 1 Summon Crest

    # Check combo
    if request.combo:
        if request.combo == "rush_summon":
            # Summon + Movement combo
            if player_state['crests'].get(crest_key, 0) < 1:
                raise HTTPException(400, "Not enough Summon Crests")
            if player_state['crests'].get('movement', 0) < 1:
                raise HTTPException(400, "Not enough Movement Crests")

            player_state['crests'][crest_key] -= 1
            player_state['crests']['movement'] -= 1

            # Add Rush keyword!
            monster_data = monster.__dict__.copy()
            if 'Haste' not in monster_data.get('keywords', []):
                monster_data['keywords'] = monster_data.get('keywords', []) + ['Haste']

        elif request.combo == "twin_summon":
            # Summon + Summon combo (2 monsters!)
            # Implement...
            pass

        # ... other combos
    else:
        # Normal summon: need 2 Summon Crests
        if player_state['crests'].get(crest_key, 0) < 2:
            raise HTTPException(400, f"Need 2 {crest_key} crests")
        player_state['crests'][crest_key] -= 2
        monster_data = monster.__dict__.copy()

    # Place monster on grid (PATH-BUILDING!)
    # Würfel entfaltet sich = 6 Squares!
    path_squares = build_path(match.grid_state, request.position, player="player1" if is_player1 else "player2")

    # Add monster to board
    monster_on_board = {
        "monster_id": monster.id,
        "position": request.position,
        "stats": {
            "hp": monster_data['health'],
            "atk": monster_data['attack'],
            "def": monster_data['defense']
        },
        "keywords": monster_data.get('keywords', []),
        "path_squares": path_squares
    }

    player_state['monsters_on_board'].append(monster_on_board)

    # Update grid
    for square in path_squares:
        match.grid_state['cells'][square['y']][square['x']] = {
            "type": "path",
            "player": "player1" if is_player1 else "player2"
        }

    # Place monster on spawn position
    match.grid_state['cells'][request.position['y']][request.position['x']] = {
        "type": "monster",
        "monster_id": monster.id,
        "player": "player1" if is_player1 else "player2"
    }

    # Save
    if is_player1:
        match.player1_state = player_state
    else:
        match.player2_state = player_state

    match.grid_state = match.grid_state  # Trigger update
    db.commit()

    return {
        "monster": monster_on_board,
        "path_squares": path_squares,
        "grid_state": match.grid_state
    }

def build_path(grid_state, spawn_pos, player):
    """Build 6 path squares (DDM GBA style!)"""
    # Simplified - implement full DDM path-building logic!
    path = []
    x, y = spawn_pos['x'], spawn_pos['y']

    # Build forward (toward opponent)
    direction = -1 if player == "player1" else 1

    for i in range(6):
        path.append({"x": x, "y": y + (i * direction)})

    return path
```

#### **6. POST /api/ddm/match/move** - Move Monster

```python
class MoveRequest(BaseModel):
    match_id: int
    monster_id: int
    target_position: dict  # {"x": 7, "y": 3}

@router.post("/match/move")
async def move_monster(
    request: MoveRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Move monster along path"""
    match = db.query(DDMMatch).filter(DDMMatch.id == request.match_id).first()

    is_player1 = match.player1_id == user_id
    player_state = match.player1_state if is_player1 else match.player2_state

    # Find monster
    monster_data = None
    for m in player_state['monsters_on_board']:
        if m['monster_id'] == request.monster_id:
            monster_data = m
            break

    if not monster_data:
        raise HTTPException(404, "Monster not found")

    # Check if target is on path
    if request.target_position not in monster_data['path_squares']:
        raise HTTPException(400, "Target not on path!")

    # Check Movement Crests
    if player_state['crests'].get('movement', 0) < 1:
        raise HTTPException(400, "Not enough Movement Crests")

    # Calculate distance
    dx = abs(request.target_position['x'] - monster_data['position']['x'])
    dy = abs(request.target_position['y'] - monster_data['position']['y'])
    distance = max(dx, dy)

    # 1 Movement Crest = 2 fields
    if distance > 2:
        raise HTTPException(400, "Too far! (1 Movement Crest = 2 fields)")

    # Consume crest
    player_state['crests']['movement'] -= 1

    # Update position
    old_pos = monster_data['position']
    monster_data['position'] = request.target_position

    # Update grid
    match.grid_state['cells'][old_pos['y']][old_pos['x']] = {"type": "path", "player": "player1" if is_player1 else "player2"}
    match.grid_state['cells'][request.target_position['y']][request.target_position['x']] = {
        "type": "monster",
        "monster_id": request.monster_id,
        "player": "player1" if is_player1 else "player2"
    }

    # Save
    if is_player1:
        match.player1_state = player_state
    else:
        match.player2_state = player_state

    match.grid_state = match.grid_state
    db.commit()

    return {
        "monster": monster_data,
        "grid_state": match.grid_state
    }
```

#### **7. POST /api/ddm/match/attack** - Attack

```python
class AttackRequest(BaseModel):
    match_id: int
    attacker_id: int
    target_id: int = None  # NULL = Dice Lord

@router.post("/match/attack")
async def attack(
    request: AttackRequest,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Attack enemy monster or Dice Lord"""
    match = db.query(DDMMatch).filter(DDMMatch.id == request.match_id).first()

    is_player1 = match.player1_id == user_id
    player_state = match.player1_state if is_player1 else match.player2_state
    opponent_state = match.player2_state if is_player1 else match.player1_state

    # Get attacker
    attacker = None
    for m in player_state['monsters_on_board']:
        if m['monster_id'] == request.attacker_id:
            attacker = m
            break

    if not attacker:
        raise HTTPException(404, "Attacker not found")

    # Check Attack Crest
    if player_state['crests'].get('attack', 0) < 1:
        raise HTTPException(400, "Not enough Attack Crests")

    player_state['crests']['attack'] -= 1

    # Attack Dice Lord?
    if request.target_id is None:
        # Check if adjacent to Dice Lord
        dice_lord_pos = match.grid_state['player2_dice_lord' if is_player1 else 'player1_dice_lord']

        if not is_adjacent(attacker['position'], dice_lord_pos):
            raise HTTPException(400, "Not adjacent to Dice Lord!")

        # Deal damage
        damage = attacker['stats']['atk']
        opponent_state['hp'] -= damage

        # Check win
        if opponent_state['hp'] <= 0:
            match.winner_id = user_id
            match.finished_at = datetime.utcnow()

        result = {
            "target": "dice_lord",
            "damage": damage,
            "opponent_hp": opponent_state['hp'],
            "game_over": opponent_state['hp'] <= 0
        }
    else:
        # Attack monster
        target = None
        for m in opponent_state['monsters_on_board']:
            if m['monster_id'] == request.target_id:
                target = m
                break

        if not target:
            raise HTTPException(404, "Target not found")

        # Check adjacent
        if not is_adjacent(attacker['position'], target['position']):
            raise HTTPException(400, "Not adjacent!")

        # Combat
        damage_to_target = max(0, attacker['stats']['atk'] - target['stats']['def'])
        damage_to_attacker = max(0, target['stats']['atk'] - attacker['stats']['def'])

        target['stats']['hp'] -= damage_to_target
        attacker['stats']['hp'] -= damage_to_attacker

        # Remove dead monsters
        if target['stats']['hp'] <= 0:
            opponent_state['monsters_on_board'].remove(target)
            # Clear grid
            match.grid_state['cells'][target['position']['y']][target['position']['x']] = {"type": "path"}

        if attacker['stats']['hp'] <= 0:
            player_state['monsters_on_board'].remove(attacker)
            match.grid_state['cells'][attacker['position']['y']][attacker['position']['x']] = {"type": "path"}

        result = {
            "target": "monster",
            "damage_to_target": damage_to_target,
            "damage_to_attacker": damage_to_attacker,
            "target_died": target['stats']['hp'] <= 0 if target else False,
            "attacker_died": attacker['stats']['hp'] <= 0 if attacker else False
        }

    # Save
    if is_player1:
        match.player1_state = player_state
        match.player2_state = opponent_state
    else:
        match.player1_state = opponent_state
        match.player2_state = player_state

    match.grid_state = match.grid_state
    db.commit()

    return result

def is_adjacent(pos1, pos2):
    """Check if two positions are adjacent"""
    dx = abs(pos1['x'] - pos2['x'])
    dy = abs(pos1['y'] - pos2['y'])
    return (dx <= 1 and dy <= 1) and not (dx == 0 and dy == 0)
```

---

### **FRONTEND UI:**

**File:** `digivice/js/ui/ddm_ui.js`

```javascript
class DDMGameUI {
    constructor() {
        this.apiBase = '/api/ddm';
        this.currentMatch = null;
        this.selectedDice = [];
        this.createUI();
    }

    createUI() {
        this.modal = document.createElement('div');
        this.modal.id = 'ddm-modal';
        this.modal.className = 'game-modal hidden';
        this.modal.innerHTML = `
            <div class="modal-content ddm-fullscreen">
                <div class="modal-header">
                    <h2>🎲 Dungeon Dice Monsters</h2>
                    <button class="close-btn" onclick="window.ddmUI.hide()">✕</button>
                </div>

                <div class="modal-body ddm-layout">
                    <!-- Dice Selection Screen -->
                    <div id="ddm-dice-selection" class="ddm-screen">
                        <h3>Select 15 Dice</h3>
                        <div id="ddm-dice-pool" class="ddm-dice-grid"></div>
                        <button onclick="window.ddmUI.startMatch()">Start Match</button>
                    </div>

                    <!-- Game Board -->
                    <div id="ddm-game-screen" class="ddm-screen hidden">
                        <!-- Top: Opponent State -->
                        <div class="ddm-player-state opponent">
                            <div class="player-hp">
                                <span>Opponent HP:</span>
                                <span id="opponent-hp">30</span>
                            </div>
                            <div class="player-resources">
                                Crests: <span id="opponent-crests">-</span>
                            </div>
                        </div>

                        <!-- Middle: Grid (15×15) -->
                        <div class="ddm-grid-container">
                            <canvas id="ddm-grid-canvas" width="750" height="750"></canvas>
                        </div>

                        <!-- Bottom: Player State -->
                        <div class="ddm-player-state player">
                            <div class="player-hp">
                                <span>Your HP:</span>
                                <span id="player-hp">30</span>
                            </div>
                            <div class="player-resources">
                                <div>Crests: <span id="player-crests"></span></div>
                                <div>Mana: <span id="player-mana"></span></div>
                            </div>
                            <div class="player-actions">
                                <button onclick="window.ddmUI.rollDice()">🎲 Roll Dice</button>
                                <button onclick="window.ddmUI.showSummonMenu()">⚔️ Summon</button>
                                <button onclick="window.ddmUI.endTurn()">✓ End Turn</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(this.modal);

        this.canvas = null;
        this.ctx = null;
    }

    async show() {
        this.modal.classList.remove('hidden');
        await this.loadDicePool();
    }

    hide() {
        this.modal.classList.add('hidden');
    }

    async loadDicePool() {
        const response = await fetch(`${this.apiBase}/dice-pool?user_id=1`);
        const data = await response.json();

        const grid = document.getElementById('ddm-dice-pool');
        grid.innerHTML = '';

        data.dice_pool.forEach(die => {
            const dieEl = document.createElement('div');
            dieEl.className = 'ddm-die';
            dieEl.dataset.dieId = die.die_id;
            dieEl.innerHTML = `
                <div class="die-model">
                    <model-viewer src="${die.monster.model_url}"
                                  auto-rotate
                                  camera-controls
                                  style="width:100%;height:100px">
                    </model-viewer>
                </div>
                <p>${die.monster.name}</p>
                <p class="die-stats">
                    Cost: ${die.monster.cost} |
                    ${die.monster.attack}/${die.monster.defense}/${die.monster.health}
                </p>
                <p class="die-level">Level ${die.level}</p>
            `;

            dieEl.onclick = () => this.selectDie(die.die_id, dieEl);
            grid.appendChild(dieEl);
        });
    }

    selectDie(dieId, element) {
        if (this.selectedDice.includes(dieId)) {
            this.selectedDice = this.selectedDice.filter(id => id !== dieId);
            element.classList.remove('selected');
        } else if (this.selectedDice.length < 15) {
            this.selectedDice.push(dieId);
            element.classList.add('selected');
        }
    }

    async startMatch() {
        if (this.selectedDice.length !== 15) {
            alert('Select exactly 15 dice!');
            return;
        }

        const response = await fetch(`${this.apiBase}/match/start`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                opponent_id: null,
                selected_dice: this.selectedDice
            })
        });

        const data = await response.json();
        this.currentMatch = data.match_id;
        this.gridState = data.grid_state;
        this.playerState = data.player1_state;

        // Switch to game screen
        document.getElementById('ddm-dice-selection').classList.add('hidden');
        document.getElementById('ddm-game-screen').classList.remove('hidden');

        this.canvas = document.getElementById('ddm-grid-canvas');
        this.ctx = this.canvas.getContext('2d');

        this.renderGrid();
        this.renderPlayerState();
    }

    renderGrid() {
        const cellSize = 50;  // 750 / 15 = 50px per cell

        // Clear canvas
        this.ctx.clearRect(0, 0, 750, 750);

        // Draw grid
        this.ctx.strokeStyle = '#333';
        for (let x = 0; x <= 15; x++) {
            this.ctx.beginPath();
            this.ctx.moveTo(x * cellSize, 0);
            this.ctx.lineTo(x * cellSize, 750);
            this.ctx.stroke();
        }
        for (let y = 0; y <= 15; y++) {
            this.ctx.beginPath();
            this.ctx.moveTo(0, y * cellSize);
            this.ctx.lineTo(750, y * cellSize);
            this.ctx.stroke();
        }

        // Draw cells (paths, monsters)
        for (let y = 0; y < 15; y++) {
            for (let x = 0; x < 15; x++) {
                const cell = this.gridState.cells[y][x];
                if (cell) {
                    if (cell.type === 'path') {
                        this.ctx.fillStyle = cell.player === 'player1' ? 'rgba(0,100,255,0.3)' : 'rgba(255,0,0,0.3)';
                        this.ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
                    } else if (cell.type === 'monster') {
                        this.ctx.fillStyle = cell.player === 'player1' ? 'blue' : 'red';
                        this.ctx.fillRect(x * cellSize + 5, y * cellSize + 5, cellSize - 10, cellSize - 10);
                        // TODO: Render 3D model here (use Three.js overlay!)
                    }
                }
            }
        }

        // Draw Dice Lords
        const p1Lord = this.gridState.player1_dice_lord;
        const p2Lord = this.gridState.player2_dice_lord;

        this.ctx.fillStyle = 'gold';
        this.ctx.fillRect(p1Lord.x * cellSize + 10, p1Lord.y * cellSize + 10, cellSize - 20, cellSize - 20);
        this.ctx.fillRect(p2Lord.x * cellSize + 10, p2Lord.y * cellSize + 10, cellSize - 20, cellSize - 20);
    }

    renderPlayerState() {
        // Update HP
        document.getElementById('player-hp').textContent = this.playerState.hp;

        // Update Crests
        const crestText = Object.entries(this.playerState.crests)
            .map(([type, count]) => `${type}: ${count}`)
            .join(', ');
        document.getElementById('player-crests').textContent = crestText || 'None';

        // Update Mana
        const manaText = Object.entries(this.playerState.mana)
            .map(([type, count]) => `${type}: ${count}`)
            .join(', ');
        document.getElementById('player-mana').textContent = manaText || 'None';
    }

    async rollDice() {
        const response = await fetch(`${this.apiBase}/match/roll`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({match_id: this.currentMatch})
        });

        const data = await response.json();

        // Show roll results
        alert(`Rolled: ${JSON.stringify(data.rolls)}`);

        // Update state
        this.playerState.crests = data.crests;
        this.playerState.mana = data.mana;
        this.renderPlayerState();
    }

    showSummonMenu() {
        // TODO: Implement summon UI with combo selection
        alert('Summon menu - implement me!');
    }
}
```

---

## 📋 TASK 4: 8-REGIONEN MAP + LEBENSRAUM

### **🎯 KONZEPT:**

**9600×9600 Grid Welt mit:**
- ⛰️ **Götterfels** (Zentrum: Schwarze Mühle - 12 Räume)
- 🏜️ **8 Regionen** rund um den Berg
- 🌍 **Living Quarters** für Najika

---

### **WAS NOCH FEHLT:**

#### **1. Schwarze Mühle - 12 Räume System:**

**BEREITS VORHANDEN (Digivice):**
- ✅ 12 Räume definiert (Wohnzimmer, Schlafzimmer, Küche, etc.)
- ✅ KayKit 3D Models
- ✅ Room Switching Logic

**WAS FEHLT:**
- ❌ **Persistence** - Räume/Objekte speichern!
- ❌ **Housing System** - Möbel platzieren
- ❌ **Farming** - Pflanzen anbauen
- ❌ **Fishing** - Zelda OoT Style

#### **2. 8-Regionen World Map:**

**DESIGN VORHANDEN:**
- ✅ 8 Regionen definiert (Layout, Biomes, Features)
- ✅ 9600×9600 Grid
- ✅ Zentrum: Götterfels

**WAS FEHLT:**
- ❌ **3D World Generation** - Terrain, Biomes
- ❌ **Region Boundaries** - Übergänge
- ❌ **Fast Travel System** - Teleport zwischen Regionen
- ❌ **Weather System** - Pro Region
- ❌ **Day/Night Cycle**

---

### **PRIORITÄT: LEBENSRAUM PERSISTENCE**

#### **DATABASE MODELS:**

**File:** `backend/models/housing.py`

```python
from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, Boolean
from backend.database import Base

class PlayerHouse(Base):
    __tablename__ = "player_houses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Location
    region = Column(String(50))  # "schwarze_muehle", "heisse_duenen", etc.
    house_type = Column(String(50))  # "mühle_room", "desert_house", etc.

    # House State
    furniture = Column(JSON)  # [{"type": "bed", "position": {"x": 5, "y": 3}, "rotation": 0}, ...]
    decorations = Column(JSON)

    # Upgrades
    level = Column(Integer, default=1)
    max_furniture = Column(Integer, default=20)

class FarmPlot(Base):
    __tablename__ = "farm_plots"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    house_id = Column(Integer, ForeignKey('player_houses.id'))

    # Position
    position_x = Column(Float)
    position_y = Column(Float)

    # Crop
    crop_type = Column(String(50))  # "wheat", "carrot", "fire_flower"
    planted_at = Column(DateTime)
    growth_stage = Column(Integer, default=0)  # 0-4
    ready_to_harvest = Column(Boolean, default=False)

class FishingSpot(Base):
    __tablename__ = "fishing_spots"

    id = Column(Integer, primary_key=True)
    region = Column(String(50))

    # Position
    position_x = Column(Float)
    position_y = Column(Float)

    # Fish available
    fish_pool = Column(JSON)  # ["carp", "salmon", "lava_fish"]
    rarity_weights = Column(JSON)  # {"common": 0.7, "rare": 0.25, "legendary": 0.05}
```

---

### **API ENDPOINTS:**

**File:** `backend/api/housing.py`

```python
@router.get("/house")
async def get_player_house(user_id: int, db: Session = Depends(get_db)):
    """Get player's house in Schwarze Mühle"""
    house = db.query(PlayerHouse)\
        .filter(
            PlayerHouse.user_id == user_id,
            PlayerHouse.region == "schwarze_muehle"
        ).first()

    if not house:
        # Create default house
        house = PlayerHouse(
            user_id=user_id,
            region="schwarze_muehle",
            house_type="mühle_room",
            furniture=[],
            decorations=[],
            level=1,
            max_furniture=20
        )
        db.add(house)
        db.commit()

    return {"house": house.__dict__}

@router.post("/house/furniture/place")
async def place_furniture(
    user_id: int,
    furniture_type: str,
    position: dict,
    rotation: int = 0,
    db: Session = Depends(get_db)
):
    """Place furniture in house"""
    house = db.query(PlayerHouse)\
        .filter(
            PlayerHouse.user_id == user_id,
            PlayerHouse.region == "schwarze_muehle"
        ).first()

    if len(house.furniture) >= house.max_furniture:
        raise HTTPException(400, "House is full!")

    house.furniture.append({
        "type": furniture_type,
        "position": position,
        "rotation": rotation
    })

    db.commit()
    return {"furniture": house.furniture}
```

**File:** `backend/api/farming.py`

```python
@router.post("/farm/plant")
async def plant_crop(
    user_id: int,
    house_id: int,
    crop_type: str,
    position: dict,
    db: Session = Depends(get_db)
):
    """Plant crop on farm plot"""
    plot = FarmPlot(
        user_id=user_id,
        house_id=house_id,
        position_x=position['x'],
        position_y=position['y'],
        crop_type=crop_type,
        planted_at=datetime.utcnow(),
        growth_stage=0,
        ready_to_harvest=False
    )
    db.add(plot)
    db.commit()

    return {"plot": plot.__dict__}

@router.post("/farm/harvest")
async def harvest_crop(
    user_id: int,
    plot_id: int,
    db: Session = Depends(get_db)
):
    """Harvest crop"""
    plot = db.query(FarmPlot)\
        .filter(
            FarmPlot.id == plot_id,
            FarmPlot.user_id == user_id
        ).first()

    if not plot:
        raise HTTPException(404, "Plot not found")

    if not plot.ready_to_harvest:
        raise HTTPException(400, "Crop not ready!")

    # Give items (add to inventory)
    # ...

    # Remove plot
    db.delete(plot)
    db.commit()

    return {"success": True, "crop": plot.crop_type}
```

**File:** `backend/api/fishing.py`

```python
@router.post("/fishing/cast")
async def cast_fishing_rod(
    user_id: int,
    spot_id: int,
    db: Session = Depends(get_db)
):
    """Cast fishing rod (Zelda OoT style!)"""
    spot = db.query(FishingSpot).filter(FishingSpot.id == spot_id).first()

    if not spot:
        raise HTTPException(404, "Fishing spot not found")

    # Roll for fish
    import random
    rarity = random.choices(
        ['common', 'rare', 'legendary'],
        weights=[
            spot.rarity_weights['common'],
            spot.rarity_weights['rare'],
            spot.rarity_weights['legendary']
        ]
    )[0]

    # Select fish of that rarity
    available = [f for f in spot.fish_pool if get_fish_rarity(f) == rarity]
    fish = random.choice(available)

    return {
        "success": True,
        "fish": fish,
        "rarity": rarity,
        "message": "You caught a fish!"
    }

def get_fish_rarity(fish_name):
    # Simple lookup - expand this!
    rarities = {
        "carp": "common",
        "salmon": "rare",
        "lava_fish": "legendary"
    }
    return rarities.get(fish_name, "common")
```

---

### **WORLD MAP - BASIC IMPLEMENTATION:**

**File:** `backend/api/world.py`

```python
@router.get("/map")
async def get_world_map():
    """Get 8-region world map layout"""
    return {
        "size": {"width": 9600, "height": 9600},
        "center": {"x": 4800, "y": 4800},
        "regions": [
            {
                "id": 1,
                "name": "Heiße Dünen",
                "position": {"x": 6000, "y": 6000, "width": 3600, "height": 3600},
                "slime_color": "dusty_gold",
                "biome": "desert"
            },
            {
                "id": 2,
                "name": "Samtmoos-Tiefwald",
                "position": {"x": 3000, "y": 0, "width": 3000, "height": 2400},
                "slime_color": "moss_green",
                "biome": "forest"
            },
            # ... (6 more regions)
        ],
        "center_mountain": {
            "name": "Götterfels",
            "position": {"x": 3300, "y": 3300, "width": 3000, "height": 3000},
            "peak": "schwarze_muehle"
        }
    }

@router.post("/travel")
async def fast_travel(
    user_id: int,
    target_region: str,
    db: Session = Depends(get_db)
):
    """Fast travel to region"""
    # Update player position
    # ...

    return {
        "success": True,
        "region": target_region,
        "position": {"x": 4800, "y": 4800}  # Spawn point
    }
```

---

## 🎯 ZUSAMMENFASSUNG FÜR WEB MODEL

**AUFGABEN-LISTE:**

### ✅ **TASK 1: Digivice UI Fix (1-2h)**
1. Add script tag to index.html
2. Initialize UIs
3. Add menu buttons
4. Test!

### ✅ **TASK 2: Triple Triad (6-8h)**
1. Database Models (3 tables)
2. API Endpoints (5 endpoints)
3. Frontend UI (grid + 3D models)
4. Seed 100 starter cards
5. Test gameplay!

### ✅ **TASK 3: DDM Synergy Master (15-20h)**
1. Database Models (4 tables)
2. API Endpoints (8+ endpoints)
3. Frontend UI (grid + canvas + 3D)
4. Implement 12 Synergy Combos
5. Path-Building Logic
6. Combat System
7. Test full match!

### ✅ **TASK 4: Housing/Farming/Fishing (10-15h)**
1. Database Models (3 tables)
2. API Endpoints (housing, farming, fishing)
3. Frontend integration
4. World Map API (basic)
5. Test in Schwarze Mühle!

---

## 📝 **WICHTIGE HINWEISE:**

### **MIGRATIONS:**
Nach Models-Erstellung:
```bash
cd backend
alembic revision --autogenerate -m "add triple triad and ddm models"
alembic upgrade head
```

### **SEED DATA:**
Erstelle Seed-Script für 100 Starter Cards!

### **FRONTEND:**
- Nutze `model-viewer` für 3D Models (wie in Slime UI!)
- Canvas für DDM Grid
- Mobile-optimiert!

### **TESTING:**
Teste ALLES lokal bevor commit!

---

## 🚀 **LOS GEHT'S!**

**Web Model, du hast jetzt ALLES was du brauchst!**

**VIEL ERFOLG!** 🔥

---

**Erstellt:** 2025-11-18 (Spät)
**Von:** Claude Code
**Für:** Web Model (Sonnet 4)
**Priorität:** MAXIMUM
