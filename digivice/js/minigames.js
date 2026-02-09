// MINIGAMES MODULE v2
(function() {
    let currentGame = null;
    let score = 0;
    let gameInterval = null;
    let cleanupFn = null;
    let frameHandle = null;
    const timeouts = new Set();
    let currentGameLabel = '';
    function scheduleTimeout(handler, delay) {
        const id = setTimeout(() => {
            timeouts.delete(id);
            handler();
        }, delay);
        timeouts.add(id);
        return id;
    }
    function cancelTimeout(id) {
        if (timeouts.has(id)) {
            clearTimeout(id);
            timeouts.delete(id);
        }
    }
    function clamp(value, min, max) {
        return Math.min(max, Math.max(min, value));
    }
    function clearTimers() {
        if (gameInterval) {
            clearInterval(gameInterval);
            gameInterval = null;
        }
        if (frameHandle) {
            cancelAnimationFrame(frameHandle);
            frameHandle = null;
        }
        timeouts.forEach(id => clearTimeout(id));
        timeouts.clear();
    }
    function setCleanup(fn) {
        cleanupFn = fn;
    }
    function createOverlay() {
        if (document.getElementById('minigameOverlay')) return;
        const overlay = document.createElement('div');
        overlay.id = 'minigameOverlay';
        overlay.className = 'minigame-overlay';
        overlay.innerHTML = `
            <div class="minigame-container">
                <div class="minigame-header">
                    <h2 id="minigameTitle">Minigame</h2>
                    <div class="minigame-score">Score: <span id="minigameScore">0</span></div>
                    <button class="minigame-close" onclick="MiniGames.close()">×</button>
                </div>
                <div class="minigame-content" id="minigameContent"></div>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    function updateScore(points = 0, reset = false) {
        if (reset) {
            score = 0;
        } else {
            score += points;
        }
        const scoreEl = document.getElementById('minigameScore');
        if (scoreEl) {
            scoreEl.textContent = Math.max(0, Math.round(score));
        }
    }
    function open(gameName) {
        createOverlay();
        const overlay = document.getElementById('minigameOverlay');
        const content = document.getElementById('minigameContent');
        const title = document.getElementById('minigameTitle');
        clearTimers();
        if (cleanupFn) {
            cleanupFn();
            cleanupFn = null;
        }
        score = 0;
        updateScore(0, true);
        setCleanup(null);
        overlay.classList.add('active');
        currentGame = gameName;
        currentGameLabel = 'Minigame';
        switch (gameName) {
            case 'rhythm':
                title.textContent = '🎵 Rhythmus-Spiel';
                currentGameLabel = title.textContent;
                startRhythmGame(content);
                break;
            case 'garden':
                title.textContent = '🌿 Garten-Spiel';
                currentGameLabel = title.textContent;
                startGardenGame(content);
                break;
            case 'reflex':
                title.textContent = '⚡ Reflex-Spiel';
                currentGameLabel = title.textContent;
                startReflexGame(content);
                break;
            case 'broom':
                title.textContent = '🧹 Besen-Lieferung';
                currentGameLabel = title.textContent;
                startBroomGame(content);
                break;
            case 'craft':
                title.textContent = '🛠️ Crafting-Workshop';
                currentGameLabel = title.textContent;
                startCraftingGame(content);
                break;
            case 'training':
                title.textContent = '🥋 Trainings-Dojō';
                currentGameLabel = title.textContent;
                startTrainingGame(content);
                break;
            case 'cooking':
                title.textContent = '🍳 Najikas Hexenküche';
                currentGameLabel = title.textContent;
                startCookingGame(content);
                break;
            case 'tripletriad':
            case 'triple_triad':
            case 'triad':
                title.textContent = '🃏 Triple Triad';
                currentGameLabel = title.textContent;
                startTripleTriadGame(content);
                break;
            case 'dice':
            case 'wuerfel':
            case 'gambling':
                title.textContent = '🎲 Dungeon Dice';
                currentGameLabel = title.textContent;
                startDiceGame(content);
                break;
            default:
                title.textContent = '🎮 Minigame';
                currentGameLabel = title.textContent;
                content.innerHTML = '<div class="minigame-placeholder">Kein Minigame verfügbar.</div>';
        }
    }
    function close(showResult = true) {
        clearTimers();
        if (cleanupFn) {
            cleanupFn();
            cleanupFn = null;
        }
        const overlay = document.getElementById('minigameOverlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
        if (showResult && currentGame && score > 0) {
            const finalScore = Math.max(0, Math.round(score));
            scheduleTimeout(() => {
                if (typeof notify === 'function') {
                    notify(`🎮 ${currentGameLabel} beendet! Score: ${finalScore}`, 'success');
                }
            }, 200);
        }
        currentGame = null;
    }
    /* === RHYTHM GAME === */
    function startRhythmGame(content) {
        content.innerHTML = `
            <div class="rhythm-game">
                <div class="rhythm-track" id="rhythmTrack">
                    <div class="rhythm-hitzone"></div>
                </div>
                <div class="rhythm-keys">
                    <div class="rhythm-key" data-key="a">A</div>
                    <div class="rhythm-key" data-key="s">S</div>
                    <div class="rhythm-key" data-key="d">D</div>
                </div>
            </div>
        `;
        const keys = ['a', 's', 'd'];
        const track = document.getElementById('rhythmTrack');
        gameInterval = setInterval(() => {
            const randomKey = keys[Math.floor(Math.random() * keys.length)];
            const note = document.createElement('div');
            note.className = 'rhythm-note';
            note.textContent = randomKey.toUpperCase();
            note.dataset.key = randomKey;
            note.style.left = (Math.random() * 60 + 20) + '%';
            note.style.animationDuration = '3.2s';
            track.appendChild(note);
            scheduleTimeout(() => note.remove(), 3200);
        }, 1500);
        const handleKeyPress = (e) => {
            const key = e.key.toLowerCase();
            if (!keys.includes(key)) return;
            const keyEl = document.querySelector(`.rhythm-key[data-key="${key}"]`);
            if (keyEl) {
                keyEl.classList.add('pressed');
                scheduleTimeout(() => keyEl.classList.remove('pressed'), 120);
            }
            const notes = Array.from(document.querySelectorAll('.rhythm-note'));
            const hitzoneRect = document.querySelector('.rhythm-hitzone').getBoundingClientRect();
            let hit = false;
            notes.forEach(note => {
                if (note.dataset.key !== key) return;
                const rect = note.getBoundingClientRect();
                if (rect.bottom >= hitzoneRect.top && rect.top <= hitzoneRect.bottom) {
                    updateScore(10);
                    note.remove();
                    hit = true;
                }
            });
            if (!hit) {
                updateScore(-5);
            }
        };
        document.addEventListener('keydown', handleKeyPress);
        setCleanup(() => document.removeEventListener('keydown', handleKeyPress));
    }
    /* === GARDEN GAME === */
    function startGardenGame(content) {
        content.innerHTML = '<div class="garden-game" id="gardenGrid"></div>';
        const grid = document.getElementById('gardenGrid');
        const tiles = [];
        for (let i = 0; i < 16; i++) {
            const tile = document.createElement('div');
            tile.className = 'garden-tile';
            grid.appendChild(tile);
            tiles.push(tile);
        }
        function spawnWeed() {
            const emptyTiles = tiles.filter(t => !t.classList.contains('weed') && !t.classList.contains('flower'));
            if (!emptyTiles.length) return;
            const tile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
            tile.classList.add('weed');
            tile.textContent = '🌱';
            scheduleTimeout(() => {
                if (tile.classList.contains('weed')) {
                    tile.classList.remove('weed');
                    tile.textContent = '';
                }
            }, 2800);
        }
        tiles.forEach(tile => {
            tile.onclick = () => {
                if (tile.classList.contains('weed')) {
                    tile.classList.remove('weed');
                    tile.classList.add('flower');
                    tile.textContent = '🌸';
                    updateScore(5);
                    scheduleTimeout(() => {
                        tile.classList.remove('flower');
                        tile.textContent = '';
                    }, 900);
                }
            };
        });
        gameInterval = setInterval(spawnWeed, 1400);
        spawnWeed();
        setCleanup(() => tiles.forEach(tile => (tile.onclick = null)));
    }
    /* === REFLEX GAME === */
    function startReflexGame(content) {
        let round = 0;
        let waiting = false;
        let startTime = 0;
        content.innerHTML = `
            <div class="reflex-game">
                <div class="reflex-target" id="reflexTarget">Warte...</div>
                <div class="reflex-instruction">Klicke, sobald der Kreis ROT wird!</div>
            </div>
        `;
        const target = document.getElementById('reflexTarget');
        function startRound() {
            if (round >= 5) {
                target.textContent = 'Fertig!';
                scheduleTimeout(() => close(), 1200);
                return;
            }
            round++;
            waiting = false;
            target.textContent = 'Warte...';
            target.classList.remove('ready');
            const delay = 900 + Math.random() * 2000;
            scheduleTimeout(() => {
                target.textContent = 'JETZT!';
                target.classList.add('ready');
                waiting = true;
                startTime = Date.now();
            }, delay);
        }
        target.onclick = () => {
            if (waiting) {
                const reaction = Date.now() - startTime;
                const points = Math.max(1, Math.floor(120 - reaction / 8));
                updateScore(points);
                target.textContent = `${reaction} ms!`;
                target.classList.remove('ready');
                waiting = false;
                scheduleTimeout(startRound, 800);
            } else {
                target.textContent = 'Zu früh!';
                scheduleTimeout(startRound, 900);
            }
        };
        setCleanup(() => (target.onclick = null));
        startRound();
    }
    /* === BROOM DELIVERY GAME === */
    function startBroomGame(content) {
        content.innerHTML = `
            <div class="broom-game">
                <canvas id="broomCanvas" width="720" height="400"></canvas>
                <div class="broom-hud">
                    <span>🧹 Leben: <span id="broomLives">3</span></span>
                    <span>📦 Lieferungen: <span id="broomDeliveries">0</span></span>
                    <span>⏳ <span id="broomTimer">60</span>s</span>
                    <p>Steuerung: W / S oder Pfeile ↑ ↓ · SPACE liefert Hexenpost</p>
                </div>
            </div>
        `;
        const canvas = document.getElementById('broomCanvas');
        const ctx = canvas.getContext('2d');
        const livesEl = document.getElementById('broomLives');
        const deliveriesEl = document.getElementById('broomDeliveries');
        const timerEl = document.getElementById('broomTimer');
        const player = { x: 90, y: canvas.height / 2, width: 42, height: 22 };
        const packages = [];
        const houses = [];
        const keys = new Set();
        let lives = 3;
        let deliveries = 0;
        let timer = 60;
        let lastThrow = 0;
        let running = true;
        function spawnHouse() {
            const doorY = 110 + Math.random() * (canvas.height - 180);
            houses.push({
                x: canvas.width + Math.random() * 220 + 200,
                y: doorY,
                width: 70,
                height: 120
            });
        }
        while (houses.length < 4) {
            spawnHouse();
        }
        function updateHud() {
            livesEl.textContent = Math.max(0, lives);
            deliveriesEl.textContent = deliveries;
            timerEl.textContent = Math.max(0, timer);
        }
        function throwPackage() {
            const now = performance.now();
            if (now - lastThrow < 400) return;
            lastThrow = now;
            packages.push({
                x: player.x + 28,
                y: player.y,
                vx: 6.2,
                vy: 0
            });
        }
        function drawBackground() {
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#05021d');
            gradient.addColorStop(1, '#0f3057');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = 'rgba(255,255,255,0.5)';
            for (let i = 0; i < 60; i++) {
                const x = (i * 73 + performance.now() * 0.02) % canvas.width;
                const y = (i * 53) % canvas.height;
                ctx.fillRect(x, y, 2, 2);
            }
        }
        function drawPlayer() {
            ctx.save();
            ctx.translate(player.x, player.y);
            ctx.fillStyle = '#452b7c';
            ctx.beginPath();
            ctx.ellipse(0, 0, 24, 16, 0, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#ffcf40';
            ctx.fillRect(12, -4, 26, 8);
            ctx.fillStyle = '#c08457';
            ctx.fillRect(28, -8, 18, 16);
            ctx.restore();
        }
        function drawHouse(house) {
            ctx.save();
            ctx.translate(house.x, house.y);
            ctx.fillStyle = '#2f2a4a';
            ctx.fillRect(-house.width / 2, -house.height / 2, house.width, house.height);
            ctx.fillStyle = '#1b5e20';
            ctx.fillRect(-house.width / 2, house.height / 2 - 50, house.width, 50);
            ctx.fillStyle = '#ffea00';
            ctx.fillRect(-15, 10, 30, 40);
            ctx.restore();
        }
        function gameLoop() {
            if (!running) return;
            frameHandle = requestAnimationFrame(gameLoop);
            drawBackground();
            if (keys.has('ArrowUp') || keys.has('KeyW')) player.y -= 4;
            if (keys.has('ArrowDown') || keys.has('KeyS')) player.y += 4;
            player.y = clamp(player.y, 50, canvas.height - 50);
            drawPlayer();
            const speed = 3.2 + deliveries * 0.04;
            houses.forEach(house => {
                house.x -= speed;
                drawHouse(house);
                if (house.x < -120) {
                    lives -= 1;
                    house.x = canvas.width + Math.random() * 220 + 200;
                    house.y = 110 + Math.random() * (canvas.height - 180);
                }
            });
            for (let i = packages.length - 1; i >= 0; i--) {
                const pkg = packages[i];
                pkg.x += pkg.vx;
                pkg.y += pkg.vy;
                ctx.fillStyle = '#ff7043';
                ctx.fillRect(pkg.x - 6, pkg.y - 6, 12, 12);
                if (pkg.x > canvas.width + 40) {
                    packages.splice(i, 1);
                    continue;
                }
                houses.forEach(house => {
                    const doorY = house.y + house.height / 2 - 20;
                    if (
                        pkg.x > house.x - house.width / 2 &&
                        pkg.x < house.x + house.width / 2 &&
                        Math.abs(pkg.y - doorY) < 30
                    ) {
                        deliveries += 1;
                        updateScore(15);
                        packages.splice(i, 1);
                        house.x = canvas.width + Math.random() * 220 + 220;
                        house.y = 110 + Math.random() * (canvas.height - 180);
                    }
                });
            }
            if (lives <= 0) {
                running = false;
                triggerExplosion(content);
            }
            updateHud();
        }
        function triggerExplosion(contentContainer) {
            clearTimers();
            const splash = document.createElement('div');
            splash.className = 'broom-explosion';
            splash.innerHTML = `
                <h3>💥 EXPLOSION!</h3>
                <p>Najika rastet aus und jagt die Welt mit einer Explosion in die Luft!</p>
            `;
            contentContainer.appendChild(splash);
            scheduleTimeout(() => close(), 2500);
        }
        function tickTimer() {
            timer -= 1;
            updateHud();
            if (timer <= 0) {
                running = false;
                const banner = document.createElement('div');
                banner.className = 'broom-success';
                banner.innerHTML = '<h3>✨ Alle Lieferungen geschafft!</h3><p>Najika ist zufrieden.</p>';
                content.appendChild(banner);
                scheduleTimeout(() => close(), 1500);
            }
        }
        const keyDown = (e) => {
            if (['ArrowUp', 'ArrowDown', 'KeyW', 'KeyS'].includes(e.code)) {
                keys.add(e.code);
                e.preventDefault();
            }
            if (e.code === 'Space' || e.code === 'Enter') {
                throwPackage();
                e.preventDefault();
            }
        };
        const keyUp = (e) => {
            if (['ArrowUp', 'ArrowDown', 'KeyW', 'KeyS'].includes(e.code)) {
                keys.delete(e.code);
                e.preventDefault();
            }
        };
        window.addEventListener('keydown', keyDown);
        window.addEventListener('keyup', keyUp);
        setCleanup(() => {
            window.removeEventListener('keydown', keyDown);
            window.removeEventListener('keyup', keyUp);
        });
        frameHandle = requestAnimationFrame(gameLoop);
        gameInterval = setInterval(tickTimer, 1000);
        updateHud();
    }
    /* === CRAFTING GAME === */
    function startCraftingGame(content) {
        content.innerHTML = `
            <div class="craft-game">
                <div class="craft-recipe">
                    <h3>Rezept</h3>
                    <div class="craft-recipe-steps" id="craftRecipe"></div>
                </div>
                <div class="craft-buttons" id="craftButtons"></div>
                <div class="craft-status">
                    <span>⏳ <span id="craftTimer">60</span>s</span>
                    <span id="craftHint">Klicke die Zutaten in der richtigen Reihenfolge!</span>
                </div>
            </div>
        `;
        const ingredients = [
            { icon: '🔥', name: 'Flamme' },
            { icon: '💧', name: 'Essenz' },
            { icon: '🍃', name: 'Blatt' },
            { icon: '⚙️', name: 'Mechanismus' },
            { icon: '💎', name: 'Kristall' },
            { icon: '🌙', name: 'Mondlicht' }
        ];
        const recipeEl = document.getElementById('craftRecipe');
        const buttonsEl = document.getElementById('craftButtons');
        const timerEl = document.getElementById('craftTimer');
        const hintEl = document.getElementById('craftHint');
        let timer = 60;
        let stepIndex = 0;
        let currentRecipe = [];
        const buttons = ingredients.map(item => {
            const btn = document.createElement('button');
            btn.className = 'craft-button';
            btn.innerHTML = `${item.icon}<span>${item.name}</span>`;
            btn.dataset.name = item.name;
            buttonsEl.appendChild(btn);
            return btn;
        });
        function renderRecipe() {
            recipeEl.innerHTML = '';
            currentRecipe.forEach((item, index) => {
                const span = document.createElement('span');
                span.className = 'craft-step';
                span.textContent = item.icon;
                if (index === stepIndex) {
                    span.classList.add('active');
                }
                recipeEl.appendChild(span);
            });
        }
        function newRecipe() {
            const length = Math.min(3 + Math.floor(score / 60), 6);
            currentRecipe = Array.from({ length }, () => ingredients[Math.floor(Math.random() * ingredients.length)]);
            stepIndex = 0;
            renderRecipe();
            hintEl.textContent = 'Rezept zusammenstellen!';
        }
        function completeStep(name) {
            const expected = currentRecipe[stepIndex];
            if (expected && expected.name === name) {
                stepIndex += 1;
                updateScore(5);
                if (stepIndex >= currentRecipe.length) {
                    updateScore(20);
                    hintEl.textContent = 'Perfekt! Neues Rezept...';
                    newRecipe();
                } else {
                    renderRecipe();
                }
            } else {
                updateScore(-8);
                hintEl.textContent = 'Falsche Zutat!';
            }
            renderRecipe();
        }
        buttons.forEach(btn => {
            btn.onclick = () => completeStep(btn.dataset.name);
        });
        setCleanup(() => buttons.forEach(btn => (btn.onclick = null)));
        newRecipe();
        gameInterval = setInterval(() => {
            timer -= 1;
            timerEl.textContent = Math.max(0, timer);
            if (timer <= 0) {
                hintEl.textContent = 'Zeit vorbei!';
                scheduleTimeout(() => close(), 1000);
            }
        }, 1000);
    }
    /* === TRAINING GAME === */
    function startTrainingGame(content) {
        content.innerHTML = `
            <div class="training-game">
                <div class="training-arena" id="trainingArena"></div>
                <div class="training-status">
                    <span>🎯 Treffer: <span id="trainingHits">0</span></span>
                    <span>❤️ <span id="trainingLives">5</span></span>
                </div>
            </div>
        `;
        const arena = document.getElementById('trainingArena');
        const hitsEl = document.getElementById('trainingHits');
        const livesEl = document.getElementById('trainingLives');
        let hits = 0;
        let lives = 5;
        function updateHud() {
            hitsEl.textContent = hits;
            livesEl.textContent = Math.max(0, lives);
        }
        function spawnTarget() {
            if (!arena.isConnected) return;
            const target = document.createElement('div');
            target.className = 'training-target';
            const arenaRect = arena.getBoundingClientRect();
            const size = 60;
            target.style.left = Math.random() * (arenaRect.width - size) + 'px';
            target.style.top = Math.random() * (arenaRect.height - size) + 'px';
            arena.appendChild(target);
            const timeoutId = scheduleTimeout(() => {
                if (target.isConnected) {
                    arena.removeChild(target);
                    lives -= 1;
                    updateHud();
                    if (lives <= 0) {
                        arena.innerHTML = '<div class="training-message">Najika ist erschöpft!</div>';
                        scheduleTimeout(() => close(), 1200);
                    }
                }
            }, 1400);
            target.onclick = () => {
                hits += 1;
                updateScore(12);
                updateHud();
                target.classList.add('hit');
                cancelTimeout(timeoutId);
                scheduleTimeout(() => target.remove(), 120);
            };
        }
        gameInterval = setInterval(spawnTarget, 900);
        spawnTarget();
        updateHud();
        setCleanup(() => arena.innerHTML = '');
    }
    /* === COOKING GAME (Fruit Ninja Style) === */
    function startCookingGame(content) {
        content.innerHTML = `
            <div class="cooking-game-ninja">
                <div class="cooking-recipe-display" id="recipeDisplay">
                    <h4>Rezept: <span id="recipeName">Hexentrank</span></h4>
                    <div class="recipe-ingredients" id="recipeIngredients"></div>
                </div>
                <canvas id="cookingCanvas" width="700" height="500"></canvas>
                <div class="cooking-hud">
                    <span>❤️ <span id="cookingLives">3</span></span>
                    <span>🎯 Combo: <span id="cookingCombo">0</span></span>
                    <span>📋 Zutaten: <span id="cookingProgress">0/5</span></span>
                </div>
            </div>
        `;

        const canvas = document.getElementById('cookingCanvas');
        const ctx = canvas.getContext('2d');
        const livesEl = document.getElementById('cookingLives');
        const comboEl = document.getElementById('cookingCombo');
        const progressEl = document.getElementById('cookingProgress');
        const recipeNameEl = document.getElementById('recipeName');
        const recipeIngredientsEl = document.getElementById('recipeIngredients');

        // Rezepte mit verschiedenen Zutaten
        const recipes = [
            { name: 'Hexentrank', ingredients: ['🍄', '🧄', '🌿', '🦎', '🕷️'], icon: '🧪' },
            { name: 'Suppenzauber', ingredients: ['🥕', '🥔', '🧅', '🍅', '🌶️'], icon: '🍲' },
            { name: 'Fruchtbombe', ingredients: ['🍎', '🍊', '🍋', '🍇', '🍓'], icon: '🍹' },
            { name: 'Giftgebräu', ingredients: ['🦴', '☠️', '🕸️', '🐛', '🪲'], icon: '⚗️' }
        ];

        let currentRecipe = recipes[Math.floor(Math.random() * recipes.length)];
        let items = [];
        let lives = 3;
        let combo = 0;
        let collected = [];
        let slicePaths = [];
        let isSlicing = false;
        let sliceStart = null;

        recipeNameEl.textContent = currentRecipe.name + ' ' + currentRecipe.icon;
        renderRecipeDisplay();

        function renderRecipeDisplay() {
            recipeIngredientsEl.innerHTML = '';
            currentRecipe.ingredients.forEach((ing, i) => {
                const span = document.createElement('span');
                span.className = 'recipe-ingredient';
                span.textContent = ing;
                if (collected.includes(ing)) {
                    span.classList.add('collected');
                }
                recipeIngredientsEl.appendChild(span);
            });
        }

        function spawnItem() {
            // 70% Chance für Rezept-Zutat, 30% für "falsche" Zutat
            const isRecipeItem = Math.random() > 0.3;
            const ingredient = isRecipeItem
                ? currentRecipe.ingredients[Math.floor(Math.random() * currentRecipe.ingredients.length)]
                : ['💀', '🔥', '❌', '💣'][Math.floor(Math.random() * 4)];

            const x = Math.random() * (canvas.width - 100) + 50;
            const vy = -(8 + Math.random() * 4);
            const vx = (Math.random() - 0.5) * 6;

            items.push({
                x,
                y: canvas.height - 50,
                vx,
                vy,
                gravity: 0.35,
                icon: ingredient,
                isRecipe: isRecipeItem && currentRecipe.ingredients.includes(ingredient),
                isWrong: !isRecipeItem,
                rotation: 0,
                rotationSpeed: (Math.random() - 0.5) * 0.2,
                size: 50
            });
        }

        function drawItem(item) {
            ctx.save();
            ctx.translate(item.x, item.y);
            ctx.rotate(item.rotation);
            ctx.font = `${item.size}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(item.icon, 0, 0);
            ctx.restore();
        }

        function drawSlicePaths() {
            slicePaths.forEach((path, idx) => {
                ctx.strokeStyle = `rgba(255, 100, 100, ${1 - idx / slicePaths.length})`;
                ctx.lineWidth = 4;
                ctx.lineCap = 'round';
                ctx.beginPath();
                path.points.forEach((pt, i) => {
                    if (i === 0) ctx.moveTo(pt.x, pt.y);
                    else ctx.lineTo(pt.x, pt.y);
                });
                ctx.stroke();
            });
        }

        function checkSlice(sliceX, sliceY) {
            for (let i = items.length - 1; i >= 0; i--) {
                const item = items[i];
                const dx = item.x - sliceX;
                const dy = item.y - sliceY;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < item.size / 2 + 20) {
                    // Treffer!
                    items.splice(i, 1);

                    if (item.isWrong) {
                        // Falsche Zutat geschnitten → Verliere Leben
                        lives -= 1;
                        combo = 0;
                        updateHud();
                        createParticles(item.x, item.y, '💥');
                        if (lives <= 0) {
                            endGame('💀 Najika hat sich vergiftet!');
                            return;
                        }
                    } else if (item.isRecipe) {
                        // Richtige Zutat!
                        if (!collected.includes(item.icon)) {
                            collected.push(item.icon);
                            renderRecipeDisplay();
                        }
                        combo += 1;
                        updateScore(10 + combo * 3);
                        updateHud();
                        createParticles(item.x, item.y, '✨');

                        // Rezept komplett?
                        if (collected.length >= currentRecipe.ingredients.length) {
                            finishRecipe();
                        }
                    }
                }
            }
        }

        function createParticles(x, y, icon) {
            for (let i = 0; i < 6; i++) {
                const angle = (i / 6) * Math.PI * 2;
                const speed = 3 + Math.random() * 2;
                items.push({
                    x,
                    y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed - 2,
                    gravity: 0.2,
                    icon,
                    size: 20,
                    rotation: 0,
                    rotationSpeed: 0.1,
                    isParticle: true
                });
            }
        }

        function finishRecipe() {
            updateScore(50);
            combo = 0;
            collected = [];
            currentRecipe = recipes[Math.floor(Math.random() * recipes.length)];
            recipeNameEl.textContent = currentRecipe.name + ' ' + currentRecipe.icon;
            renderRecipeDisplay();
            updateHud();
        }

        function endGame(message) {
            clearTimers();
            ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#fff';
            ctx.font = '36px Arial';
            ctx.textAlign = 'center';
            ctx.fillText(message, canvas.width / 2, canvas.height / 2);
            scheduleTimeout(() => close(), 2000);
        }

        function updateHud() {
            livesEl.textContent = Math.max(0, lives);
            comboEl.textContent = combo;
            progressEl.textContent = `${collected.length}/${currentRecipe.ingredients.length}`;
        }

        function gameLoop() {
            if (!canvas.isConnected) return;
            frameHandle = requestAnimationFrame(gameLoop);

            // Clear
            const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
            gradient.addColorStop(0, '#1a0808');
            gradient.addColorStop(1, '#0f1722');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Update items
            for (let i = items.length - 1; i >= 0; i--) {
                const item = items[i];
                item.vy += item.gravity;
                item.x += item.vx;
                item.y += item.vy;
                item.rotation += item.rotationSpeed;

                // Entferne Items die unten raus fallen
                if (item.y > canvas.height + 60) {
                    items.splice(i, 1);
                    if (!item.isParticle && item.isRecipe) {
                        lives -= 1;
                        combo = 0;
                        updateHud();
                        if (lives <= 0) {
                            endGame('😵 Alle Zutaten verpasst!');
                            return;
                        }
                    }
                    continue;
                }

                drawItem(item);
            }

            // Draw slice paths
            drawSlicePaths();

            // Fade out old slices
            slicePaths = slicePaths.filter(path => path.age++ < 15);
        }

        // Mouse/Touch Controls
        const getPos = (e) => {
            const rect = canvas.getBoundingClientRect();
            const clientX = e.clientX || (e.touches && e.touches[0]?.clientX);
            const clientY = e.clientY || (e.touches && e.touches[0]?.clientY);
            return {
                x: (clientX - rect.left) * (canvas.width / rect.width),
                y: (clientY - rect.top) * (canvas.height / rect.height)
            };
        };

        const onStart = (e) => {
            isSlicing = true;
            const pos = getPos(e);
            sliceStart = pos;
            slicePaths.push({ points: [pos], age: 0 });
        };

        const onMove = (e) => {
            if (!isSlicing) return;
            const pos = getPos(e);
            if (slicePaths.length > 0) {
                slicePaths[slicePaths.length - 1].points.push(pos);
            }
            checkSlice(pos.x, pos.y);
        };

        const onEnd = () => {
            isSlicing = false;
            sliceStart = null;
        };

        canvas.addEventListener('mousedown', onStart);
        canvas.addEventListener('mousemove', onMove);
        canvas.addEventListener('mouseup', onEnd);
        canvas.addEventListener('touchstart', onStart);
        canvas.addEventListener('touchmove', onMove);
        canvas.addEventListener('touchend', onEnd);

        setCleanup(() => {
            canvas.removeEventListener('mousedown', onStart);
            canvas.removeEventListener('mousemove', onMove);
            canvas.removeEventListener('mouseup', onEnd);
            canvas.removeEventListener('touchstart', onStart);
            canvas.removeEventListener('touchmove', onMove);
            canvas.removeEventListener('touchend', onEnd);
        });

        frameHandle = requestAnimationFrame(gameLoop);
        gameInterval = setInterval(spawnItem, 900);
        updateHud();
    }

    /* === TRIPLE TRIAD (FF8 Style Kartenspiel) === */
    function startTripleTriadGame(content) {
        // Najika-Karten mit Werten (oben, rechts, unten, links)
        const CARDS = [
            { name: 'Najika', values: [8, 5, 6, 7], emoji: '🧙‍♀️', color: '#ff69b4' },
            { name: 'Kuja', values: [7, 7, 7, 7], emoji: '⚔️', color: '#4169e1' },
            { name: 'Slime', values: [2, 3, 2, 1], emoji: '🟢', color: '#32cd32' },
            { name: 'Goblin', values: [3, 2, 4, 3], emoji: '👺', color: '#8b4513' },
            { name: 'Skeleton', values: [4, 3, 3, 5], emoji: '💀', color: '#dcdcdc' },
            { name: 'Wolf', values: [5, 4, 3, 4], emoji: '🐺', color: '#696969' },
            { name: 'Dragon', values: [9, 6, 7, 8], emoji: '🐉', color: '#ff4500' },
            { name: 'Phoenix', values: [6, 8, 5, 6], emoji: '🔥', color: '#ff8c00' },
            { name: 'Golem', values: [4, 5, 7, 6], emoji: '🗿', color: '#a0522d' },
            { name: 'Spirit', values: [5, 6, 4, 5], emoji: '👻', color: '#9370db' },
            { name: 'Megumin', values: [9, 9, 1, 1], emoji: '💥', color: '#ff0000' },
            { name: 'Harley', values: [6, 6, 6, 6], emoji: '🃏', color: '#ff1493' }
        ];

        let playerHand = [];
        let aiHand = [];
        let board = Array(9).fill(null); // 3x3 Board
        let playerTurn = true;
        let selectedCard = null;
        let playerScore = 5;
        let aiScore = 5;

        // Zufällige Karten für beide Spieler
        function dealCards() {
            const shuffled = [...CARDS].sort(() => Math.random() - 0.5);
            playerHand = shuffled.slice(0, 5).map(c => ({...c, owner: 'player'}));
            aiHand = shuffled.slice(5, 10).map(c => ({...c, owner: 'ai'}));
        }

        function renderGame() {
            content.innerHTML = `
                <div class="triad-game">
                    <div class="triad-score">
                        <span class="player-score">Du: <strong>${playerScore}</strong></span>
                        <span class="ai-score">Najika: <strong>${aiScore}</strong></span>
                    </div>
                    <div class="triad-main">
                        <div class="triad-hand player-hand" id="playerHand"></div>
                        <div class="triad-board" id="triadBoard"></div>
                        <div class="triad-hand ai-hand" id="aiHand"></div>
                    </div>
                    <div class="triad-status" id="triadStatus">${playerTurn ? '🎯 Dein Zug! Wähle eine Karte.' : '⏳ Najika denkt nach...'}</div>
                </div>
            `;

            // Render Player Hand
            const playerHandEl = document.getElementById('playerHand');
            playerHand.forEach((card, i) => {
                const cardEl = createCardElement(card, i, 'player');
                if (selectedCard === i) cardEl.classList.add('selected');
                cardEl.onclick = () => selectCard(i);
                playerHandEl.appendChild(cardEl);
            });

            // Render AI Hand (verdeckt)
            const aiHandEl = document.getElementById('aiHand');
            aiHand.forEach((card, i) => {
                const cardEl = document.createElement('div');
                cardEl.className = 'triad-card back';
                cardEl.innerHTML = '🃏';
                aiHandEl.appendChild(cardEl);
            });

            // Render Board
            const boardEl = document.getElementById('triadBoard');
            for (let i = 0; i < 9; i++) {
                const cell = document.createElement('div');
                cell.className = 'triad-cell';
                if (board[i]) {
                    const cardEl = createCardElement(board[i], i, board[i].owner, true);
                    cell.appendChild(cardEl);
                } else if (playerTurn && selectedCard !== null) {
                    cell.classList.add('playable');
                    cell.onclick = () => playCard(i);
                }
                boardEl.appendChild(cell);
            }
        }

        function createCardElement(card, index, owner, onBoard = false) {
            const el = document.createElement('div');
            el.className = `triad-card ${owner}`;
            el.style.borderColor = card.color;
            if (onBoard) el.style.background = owner === 'player' ? 'rgba(65,105,225,0.3)' : 'rgba(255,105,180,0.3)';
            el.innerHTML = `
                <div class="card-top">${card.values[0]}</div>
                <div class="card-middle">
                    <span class="card-left">${card.values[3]}</span>
                    <span class="card-emoji">${card.emoji}</span>
                    <span class="card-right">${card.values[1]}</span>
                </div>
                <div class="card-bottom">${card.values[2]}</div>
                <div class="card-name">${card.name}</div>
            `;
            return el;
        }

        function selectCard(index) {
            if (!playerTurn) return;
            selectedCard = selectedCard === index ? null : index;
            renderGame();
        }

        function playCard(cellIndex) {
            if (!playerTurn || selectedCard === null || board[cellIndex]) return;

            const card = playerHand.splice(selectedCard, 1)[0];
            board[cellIndex] = card;
            selectedCard = null;

            // Capture Logik
            captureCards(cellIndex, card);
            updateScores();

            playerTurn = false;
            renderGame();

            // Check Game End
            if (checkGameEnd()) return;

            // AI Turn
            scheduleTimeout(() => {
                aiTurn();
            }, 1000);
        }

        function captureCards(cellIndex, card) {
            const neighbors = [
                { dir: 0, offset: -3, oppDir: 2 }, // oben
                { dir: 1, offset: 1, oppDir: 3 },  // rechts
                { dir: 2, offset: 3, oppDir: 0 },  // unten
                { dir: 3, offset: -1, oppDir: 1 }  // links
            ];

            const row = Math.floor(cellIndex / 3);
            const col = cellIndex % 3;

            neighbors.forEach(n => {
                const targetIdx = cellIndex + n.offset;
                const targetRow = Math.floor(targetIdx / 3);
                const targetCol = targetIdx % 3;

                // Boundary Check
                if (n.offset === 1 && col === 2) return;
                if (n.offset === -1 && col === 0) return;
                if (targetIdx < 0 || targetIdx > 8) return;

                const target = board[targetIdx];
                if (target && target.owner !== card.owner) {
                    if (card.values[n.dir] > target.values[n.oppDir]) {
                        target.owner = card.owner;
                    }
                }
            });
        }

        function updateScores() {
            playerScore = board.filter(c => c && c.owner === 'player').length + playerHand.length;
            aiScore = board.filter(c => c && c.owner === 'ai').length + aiHand.length;
        }

        function aiTurn() {
            if (aiHand.length === 0) return;

            // Einfache AI: Finde beste Position
            let bestMove = null;
            let bestScore = -1;

            aiHand.forEach((card, cardIdx) => {
                for (let cellIdx = 0; cellIdx < 9; cellIdx++) {
                    if (board[cellIdx]) continue;

                    let score = 0;
                    const neighbors = [
                        { dir: 0, offset: -3, oppDir: 2 },
                        { dir: 1, offset: 1, oppDir: 3 },
                        { dir: 2, offset: 3, oppDir: 0 },
                        { dir: 3, offset: -1, oppDir: 1 }
                    ];

                    neighbors.forEach(n => {
                        const targetIdx = cellIdx + n.offset;
                        if (targetIdx < 0 || targetIdx > 8) return;
                        const col = cellIdx % 3;
                        if (n.offset === 1 && col === 2) return;
                        if (n.offset === -1 && col === 0) return;

                        const target = board[targetIdx];
                        if (target && target.owner === 'player') {
                            if (card.values[n.dir] > target.values[n.oppDir]) {
                                score += 10;
                            }
                        }
                    });

                    score += Math.random() * 2;

                    if (score > bestScore) {
                        bestScore = score;
                        bestMove = { cardIdx, cellIdx };
                    }
                }
            });

            if (bestMove) {
                const card = aiHand.splice(bestMove.cardIdx, 1)[0];
                board[bestMove.cellIdx] = card;
                captureCards(bestMove.cellIdx, card);
                updateScores();
            }

            playerTurn = true;
            renderGame();
            checkGameEnd();
        }

        function checkGameEnd() {
            if (board.filter(c => c).length === 9) {
                const status = document.getElementById('triadStatus');
                if (playerScore > aiScore) {
                    status.innerHTML = '🎉 GEWONNEN! Du hast Najika geschlagen!';
                    updateScore(100);
                } else if (playerScore < aiScore) {
                    status.innerHTML = '😈 VERLOREN! Najika lacht: "Besser trainieren, Puddin\'!"';
                    updateScore(20);
                } else {
                    status.innerHTML = '🤝 UNENTSCHIEDEN!';
                    updateScore(50);
                }
                scheduleTimeout(() => close(), 3000);
                return true;
            }
            return false;
        }

        // Styles hinzufügen
        if (!document.getElementById('triad-styles')) {
            const style = document.createElement('style');
            style.id = 'triad-styles';
            style.textContent = `
                .triad-game { display: flex; flex-direction: column; align-items: center; gap: 15px; padding: 10px; }
                .triad-score { display: flex; gap: 40px; font-size: 18px; }
                .player-score { color: #4169e1; }
                .ai-score { color: #ff69b4; }
                .triad-main { display: flex; gap: 20px; align-items: center; }
                .triad-hand { display: flex; flex-direction: column; gap: 8px; }
                .triad-board { display: grid; grid-template-columns: repeat(3, 90px); gap: 5px; background: #2a2a2a; padding: 10px; border-radius: 8px; }
                .triad-cell { width: 90px; height: 110px; background: #1a1a1a; border: 2px solid #444; border-radius: 5px; display: flex; align-items: center; justify-content: center; }
                .triad-cell.playable { cursor: pointer; border-color: #4CAF50; background: rgba(76,175,80,0.2); }
                .triad-cell.playable:hover { background: rgba(76,175,80,0.4); }
                .triad-card { width: 80px; height: 100px; background: #333; border: 3px solid #666; border-radius: 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer; transition: transform 0.2s; font-size: 14px; }
                .triad-card:hover { transform: scale(1.05); }
                .triad-card.selected { transform: scale(1.1); box-shadow: 0 0 15px gold; }
                .triad-card.back { background: linear-gradient(135deg, #4a0e4e, #1a1a2e); font-size: 30px; }
                .triad-card.player { background: rgba(65,105,225,0.2); }
                .triad-card.ai { background: rgba(255,105,180,0.2); }
                .card-top, .card-bottom { font-weight: bold; }
                .card-middle { display: flex; align-items: center; gap: 5px; }
                .card-emoji { font-size: 24px; }
                .card-left, .card-right { font-weight: bold; }
                .card-name { font-size: 10px; color: #aaa; margin-top: 2px; }
                .triad-status { font-size: 16px; color: #fff; padding: 10px; background: rgba(0,0,0,0.5); border-radius: 5px; }
            `;
            document.head.appendChild(style);
        }

        dealCards();
        renderGame();
    }

    /* === DUNGEON DICE (Gambling Minigame) === */
    function startDiceGame(content) {
        let playerGold = 100;
        let betAmount = 10;
        let playerDice = [0, 0];
        let npcDice = [0, 0];
        let gamePhase = 'betting'; // 'betting', 'rolling', 'result'
        let streak = 0;

        function renderGame() {
            content.innerHTML = `
                <div class="dice-game">
                    <div class="dice-gold">💰 Dein Gold: <strong>${playerGold}</strong></div>
                    <div class="dice-streak">${streak > 0 ? `🔥 Streak: ${streak}` : ''}</div>

                    <div class="dice-arena">
                        <div class="dice-player">
                            <h4>Du</h4>
                            <div class="dice-container">
                                <div class="die" id="playerDie1">${playerDice[0] || '?'}</div>
                                <div class="die" id="playerDie2">${playerDice[1] || '?'}</div>
                            </div>
                            <div class="dice-total">${playerDice[0] && playerDice[1] ? playerDice[0] + playerDice[1] : '-'}</div>
                        </div>

                        <div class="dice-vs">VS</div>

                        <div class="dice-npc">
                            <h4>🧙‍♀️ Najika</h4>
                            <div class="dice-container">
                                <div class="die npc" id="npcDie1">${gamePhase === 'result' ? npcDice[0] : '?'}</div>
                                <div class="die npc" id="npcDie2">${gamePhase === 'result' ? npcDice[1] : '?'}</div>
                            </div>
                            <div class="dice-total">${gamePhase === 'result' ? npcDice[0] + npcDice[1] : '-'}</div>
                        </div>
                    </div>

                    ${gamePhase === 'betting' ? `
                        <div class="dice-betting">
                            <label>Einsatz:</label>
                            <div class="bet-controls">
                                <button onclick="window.diceAdjustBet(-10)">-10</button>
                                <span class="bet-amount">${betAmount}</span>
                                <button onclick="window.diceAdjustBet(10)">+10</button>
                            </div>
                            <button class="roll-btn" onclick="window.diceRoll()">🎲 WÜRFELN!</button>
                        </div>
                    ` : gamePhase === 'rolling' ? `
                        <div class="dice-rolling">
                            <div class="rolling-text">🎲 Würfel rollen... 🎲</div>
                        </div>
                    ` : `
                        <div class="dice-result">
                            <div class="result-text" id="diceResult"></div>
                            <button class="roll-btn" onclick="window.diceNextRound()">Nächste Runde</button>
                        </div>
                    `}

                    <div class="dice-status" id="diceStatus">${getStatusText()}</div>
                </div>
            `;

            if (gamePhase === 'result') {
                showResult();
            }
        }

        function getStatusText() {
            if (playerGold <= 0) return '💀 Pleite! Najika lacht...';
            if (gamePhase === 'betting') return 'Setze deinen Einsatz!';
            if (gamePhase === 'rolling') return '...';
            return '';
        }

        function adjustBet(amount) {
            betAmount = Math.max(10, Math.min(playerGold, betAmount + amount));
            renderGame();
        }

        function roll() {
            if (betAmount > playerGold) {
                alert('Nicht genug Gold!');
                return;
            }

            gamePhase = 'rolling';
            renderGame();

            // Würfel-Animation
            let rollCount = 0;
            const rollInterval = setInterval(() => {
                playerDice = [Math.ceil(Math.random() * 6), Math.ceil(Math.random() * 6)];
                const d1 = document.getElementById('playerDie1');
                const d2 = document.getElementById('playerDie2');
                if (d1) d1.textContent = playerDice[0];
                if (d2) d2.textContent = playerDice[1];

                rollCount++;
                if (rollCount >= 15) {
                    clearInterval(rollInterval);
                    // Finale Werte
                    playerDice = [Math.ceil(Math.random() * 6), Math.ceil(Math.random() * 6)];
                    npcDice = [Math.ceil(Math.random() * 6), Math.ceil(Math.random() * 6)];
                    gamePhase = 'result';
                    renderGame();
                }
            }, 100);
        }

        function showResult() {
            const playerTotal = playerDice[0] + playerDice[1];
            const npcTotal = npcDice[0] + npcDice[1];
            const resultEl = document.getElementById('diceResult');

            if (playerTotal > npcTotal) {
                const winnings = betAmount * (streak >= 3 ? 3 : streak >= 1 ? 2 : 1.5);
                playerGold += Math.floor(winnings);
                streak++;
                updateScore(Math.floor(winnings));
                if (resultEl) resultEl.innerHTML = `🎉 GEWONNEN! +${Math.floor(winnings)} Gold`;
            } else if (playerTotal < npcTotal) {
                playerGold -= betAmount;
                streak = 0;
                if (resultEl) resultEl.innerHTML = `😈 VERLOREN! -${betAmount} Gold<br>Najika: "Pech gehabt, Puddin'~"`;
            } else {
                if (resultEl) resultEl.innerHTML = '🤝 UNENTSCHIEDEN! Einsatz zurück.';
            }

            if (playerGold <= 0) {
                scheduleTimeout(() => {
                    alert('💀 Du bist pleite!\nNajika: "Tja, vielleicht beim nächsten Mal~"');
                    close();
                }, 1500);
            }
        }

        function nextRound() {
            if (playerGold <= 0) {
                close();
                return;
            }
            playerDice = [0, 0];
            npcDice = [0, 0];
            gamePhase = 'betting';
            betAmount = Math.min(betAmount, playerGold);
            renderGame();
        }

        // Global functions for onclick
        window.diceAdjustBet = adjustBet;
        window.diceRoll = roll;
        window.diceNextRound = nextRound;

        // Styles
        if (!document.getElementById('dice-styles')) {
            const style = document.createElement('style');
            style.id = 'dice-styles';
            style.textContent = `
                .dice-game { display: flex; flex-direction: column; align-items: center; gap: 15px; padding: 15px; }
                .dice-gold { font-size: 20px; color: #FFD700; }
                .dice-streak { color: #ff6b35; font-size: 16px; height: 20px; }
                .dice-arena { display: flex; align-items: center; gap: 30px; margin: 20px 0; }
                .dice-player, .dice-npc { text-align: center; }
                .dice-player h4 { color: #4169e1; }
                .dice-npc h4 { color: #ff69b4; }
                .dice-container { display: flex; gap: 10px; margin: 10px 0; }
                .die { width: 60px; height: 60px; background: #fff; color: #333; font-size: 32px; font-weight: bold; display: flex; align-items: center; justify-content: center; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); }
                .die.npc { background: #ffb6c1; }
                .dice-total { font-size: 24px; font-weight: bold; }
                .dice-vs { font-size: 28px; color: #fff; font-weight: bold; }
                .dice-betting { display: flex; flex-direction: column; align-items: center; gap: 15px; }
                .bet-controls { display: flex; align-items: center; gap: 15px; }
                .bet-controls button { padding: 8px 15px; font-size: 16px; cursor: pointer; background: #444; color: #fff; border: none; border-radius: 5px; }
                .bet-controls button:hover { background: #666; }
                .bet-amount { font-size: 24px; color: #FFD700; min-width: 60px; text-align: center; }
                .roll-btn { padding: 15px 40px; font-size: 20px; background: linear-gradient(135deg, #ff6b35, #ff9500); color: #fff; border: none; border-radius: 10px; cursor: pointer; font-weight: bold; }
                .roll-btn:hover { transform: scale(1.05); }
                .dice-rolling { font-size: 24px; animation: pulse 0.5s infinite; }
                @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
                .dice-result { text-align: center; }
                .result-text { font-size: 20px; margin-bottom: 15px; }
                .dice-status { color: #aaa; font-size: 14px; }
            `;
            document.head.appendChild(style);
        }

        renderGame();

        setCleanup(() => {
            delete window.diceAdjustBet;
            delete window.diceRoll;
            delete window.diceNextRound;
        });
    }

    window.MiniGames = {
        open,
        close: () => close(true)
    };
    console.log('✅ Minigames module loaded');
})();
