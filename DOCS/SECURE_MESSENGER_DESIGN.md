# 🔐 NAJIKA SECURE MESSENGER - Design & Spezifikation

**Erstellt:** 2025-11-07
**Zweck:** Hochsicherer, privater Messenger integriert in Najika Digivice
**Sicherheits-Level:** Military-Grade E2E Encryption
**Inspiration:** Signal + Snapchat + Telegram

---

## 🎯 VISION

Ein **ultra-sicherer Messenger**, der sich nahtlos in die Najika-App integriert und höchste Privatsphäre garantiert.

### Kern-Features
- ✅ **Ende-zu-Ende-Verschlüsselung** (E2E) - Niemand außer dir kann Messages lesen
- ✅ **Perfect Forward Secrecy** - Alte Messages bleiben sicher, selbst wenn Schlüssel kompromittiert
- ✅ **Self-Destructing Messages** - Snapchat-Style Auto-Delete
- ✅ **Verschlüsselte Voice/Video-Calls** - Sichere Telefonie
- ✅ **Zero-Knowledge-Server** - Server kann Messages nicht lesen
- ✅ **Deniable Authentication** - Kryptografisch beweisbar, wer etwas schrieb
- ✅ **Metadata-Protection** - Verschleiert, wer mit wem kommuniziert

---

## 🏗️ ARCHITEKTUR

```
┌─────────────────────────────────────────────────────────┐
│              NAJIKA SECURE MESSENGER                    │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  UI Layer                                         │ │
│  │  ├─ Chat List                                     │ │
│  │  ├─ Chat Screen (E2E-verschlüsselt)               │ │
│  │  ├─ Contact Management                            │ │
│  │  ├─ Settings                                      │ │
│  │  └─ Safety Number Verification                    │ │
│  └───────────────────────────────────────────────────┘ │
│                        ⬇                                │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Crypto Layer (Signal Protocol)                  │ │
│  │  ├─ X3DH (Extended Triple Diffie-Hellman)        │ │
│  │  ├─ Double Ratchet Algorithm                     │ │
│  │  ├─ Key Derivation (HKDF)                        │ │
│  │  └─ AES-256-GCM Encryption                       │ │
│  └───────────────────────────────────────────────────┘ │
│                        ⬇                                │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Network Layer                                    │ │
│  │  ├─ WebSocket (Real-time)                        │ │
│  │  ├─ REST API (Fallback)                          │ │
│  │  ├─ Tor Support (optional)                       │ │
│  │  └─ Sealed Sender (Metadata-Protection)          │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                        ⬇
┌─────────────────────────────────────────────────────────┐
│              NAJIKA MESSENGER SERVER                    │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Zero-Knowledge Server                            │ │
│  │  • Speichert nur verschlüsselte Messages          │ │
│  │  • Kann Inhalte NICHT lesen                       │ │
│  │  • Minimale Metadaten                             │ │
│  │  • Automatische Löschung                          │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 KRYPTOGRAFIE-STACK

### 1. Signal Protocol (Double Ratchet)

**Warum Signal Protocol?**
- Von Kryptografie-Experten entwickelt und auditiert
- Genutzt von WhatsApp, Signal, Facebook Messenger
- Bietet Perfect Forward Secrecy und Future Secrecy
- Open Source und peer-reviewed

#### X3DH (Extended Triple Diffie-Hellman)

**Initial Key Exchange:**
```dart
// lib/services/crypto/x3dh.dart

import 'package:cryptography/cryptography.dart';

class X3DHKeyExchange {
  // Identitäts-Schlüssel (langfristig)
  late SimpleKeyPair identityKey;

  // Signed PreKey (mittelfristig, rotiert monatlich)
  late SimpleKeyPair signedPreKey;

  // One-Time PreKeys (einmalig, für jede neue Konversation)
  List<SimpleKeyPair> oneTimePreKeys = [];

  Future<void> generateKeys() async {
    final algorithm = X25519();

    // Identitäts-Schlüssel generieren
    identityKey = await algorithm.newKeyPair();

    // Signed PreKey generieren
    signedPreKey = await algorithm.newKeyPair();

    // 100 One-Time PreKeys generieren
    for (var i = 0; i < 100; i++) {
      oneTimePreKeys.add(await algorithm.newKeyPair());
    }
  }

  Future<KeyBundle> getKeyBundle() async {
    return KeyBundle(
      identityKey: await identityKey.extractPublicKey(),
      signedPreKey: await signedPreKey.extractPublicKey(),
      oneTimePreKey: await oneTimePreKeys.first.extractPublicKey(),
    );
  }

  Future<SharedSecret> performKeyAgreement(
    KeyBundle recipientBundle,
  ) async {
    final algorithm = X25519();

    // DH1 = Identity × SignedPreKey
    final dh1 = await algorithm.sharedSecretKey(
      keyPair: identityKey,
      remotePublicKey: recipientBundle.signedPreKey,
    );

    // DH2 = Ephemeral × Identity
    final ephemeralKey = await algorithm.newKeyPair();
    final dh2 = await algorithm.sharedSecretKey(
      keyPair: ephemeralKey,
      remotePublicKey: recipientBundle.identityKey,
    );

    // DH3 = Ephemeral × SignedPreKey
    final dh3 = await algorithm.sharedSecretKey(
      keyPair: ephemeralKey,
      remotePublicKey: recipientBundle.signedPreKey,
    );

    // DH4 = Ephemeral × OneTimePreKey (falls vorhanden)
    final dh4 = recipientBundle.oneTimePreKey != null
        ? await algorithm.sharedSecretKey(
            keyPair: ephemeralKey,
            remotePublicKey: recipientBundle.oneTimePreKey!,
          )
        : null;

    // Kombiniere alle DH-Secrets zu Master-Secret
    final sharedSecret = await _deriveSharedSecret([
      await dh1.extractBytes(),
      await dh2.extractBytes(),
      await dh3.extractBytes(),
      if (dh4 != null) await dh4.extractBytes(),
    ]);

    return sharedSecret;
  }

  Future<SharedSecret> _deriveSharedSecret(List<List<int>> dhSecrets) async {
    // HKDF (HMAC-based Key Derivation Function)
    final algorithm = Hkdf(
      hmac: Hmac(Sha256()),
      outputLength: 32,
    );

    final combined = dhSecrets.expand((x) => x).toList();

    return await algorithm.deriveKey(
      secretKey: SecretKey(combined),
      nonce: Nonce(List.filled(32, 0)),
    );
  }
}
```

#### Double Ratchet Algorithm

**Nachschlüssel-Aktualisierung:**
```dart
// lib/services/crypto/double_ratchet.dart

class DoubleRatchet {
  late ChainKey sendingChain;
  late ChainKey receivingChain;
  late SimpleKeyPair dhRatchetKey;

  int sendingMessageNumber = 0;
  int receivingMessageNumber = 0;

  // Initialisierung mit Shared Secret aus X3DH
  Future<void> initialize(SharedSecret sharedSecret) async {
    final rootKey = await _deriveRootKey(sharedSecret);

    sendingChain = await _deriveChainKey(rootKey, 'sending');
    receivingChain = await _deriveChainKey(rootKey, 'receiving');

    dhRatchetKey = await X25519().newKeyPair();
  }

  // Nachricht verschlüsseln
  Future<EncryptedMessage> encrypt(String plaintext) async {
    // 1. Message Key ableiten
    final messageKey = await _deriveMessageKey(sendingChain);

    // 2. AES-256-GCM Verschlüsselung
    final algorithm = AesGcm.with256bits();

    final secretKey = SecretKey(await messageKey.extractBytes());
    final nonce = algorithm.newNonce();

    final encrypted = await algorithm.encrypt(
      utf8.encode(plaintext),
      secretKey: secretKey,
      nonce: nonce,
    );

    // 3. Chain Key aktualisieren (Forward Secrecy!)
    sendingChain = await _ratchetChainKey(sendingChain);
    sendingMessageNumber++;

    return EncryptedMessage(
      ciphertext: encrypted.cipherText,
      mac: encrypted.mac.bytes,
      nonce: nonce.bytes,
      messageNumber: sendingMessageNumber,
      dhPublicKey: await dhRatchetKey.extractPublicKey(),
    );
  }

  // Nachricht entschlüsseln
  Future<String> decrypt(EncryptedMessage message) async {
    // 1. DH Ratchet Step (falls nötig)
    if (message.dhPublicKey != null) {
      await _performDHRatchetStep(message.dhPublicKey!);
    }

    // 2. Message Key ableiten
    final messageKey = await _deriveMessageKey(receivingChain);

    // 3. AES-256-GCM Entschlüsselung
    final algorithm = AesGcm.with256bits();

    final secretKey = SecretKey(await messageKey.extractBytes());

    final decrypted = await algorithm.decrypt(
      SecretBox(
        message.ciphertext,
        nonce: Nonce(message.nonce),
        mac: Mac(message.mac),
      ),
      secretKey: secretKey,
    );

    // 4. Chain Key aktualisieren
    receivingChain = await _ratchetChainKey(receivingChain);
    receivingMessageNumber++;

    return utf8.decode(decrypted);
  }

  Future<void> _performDHRatchetStep(PublicKey recipientDHKey) async {
    // Neues DH-Schlüsselpaar generieren
    final newDHKey = await X25519().newKeyPair();

    // Neues Shared Secret berechnen
    final newSharedSecret = await X25519().sharedSecretKey(
      keyPair: newDHKey,
      remotePublicKey: recipientDHKey,
    );

    // Root Key und Chain Keys ableiten
    final newRootKey = await _deriveRootKey(newSharedSecret);
    sendingChain = await _deriveChainKey(newRootKey, 'sending');
    receivingChain = await _deriveChainKey(newRootKey, 'receiving');

    dhRatchetKey = newDHKey;
  }
}
```

---

## 💬 MESSAGE-TYPEN

### 1. Text-Nachrichten

```dart
class TextMessage {
  String id;
  String chatId;
  String senderId;
  String recipientId;
  String content;              // E2E-verschlüsselt
  DateTime timestamp;
  bool isRead;
  bool isDelivered;
  MessageLifetime lifetime;    // Snapchat-Style

  // Self-Destruct Settings
  Duration? autoDeleteAfter;   // z.B. 24h, 7d, never
  bool deleteAfterRead;        // true für Snapchat-Mode
  DateTime? readAt;
}

enum MessageLifetime {
  NORMAL,      // Bleibt permanent
  SNAPCHAT,    // Löscht nach Lesen (10s Countdown)
  TIMED_1H,    // Löscht nach 1 Stunde
  TIMED_24H,   // Löscht nach 24 Stunden
  TIMED_7D,    // Löscht nach 7 Tagen
}
```

### 2. Sprachnachrichten

```dart
class VoiceMessage extends TextMessage {
  String audioUrl;             // E2E-verschlüsselt
  int durationSeconds;
  List<double> waveform;       // Für Visualisierung

  // Verschlüsselung
  List<int> encryptedAudio;
  List<int> audioKey;          // Verschlüsselt mit Message Key
}
```

### 3. Medien (Bilder/Videos)

```dart
class MediaMessage extends TextMessage {
  String mediaUrl;             // E2E-verschlüsselt
  MediaType type;              // IMAGE, VIDEO, GIF
  String? thumbnailUrl;        // E2E-verschlüsselt
  int? width;
  int? height;

  // Verschlüsselung
  List<int> encryptedMedia;
  List<int> mediaKey;
}
```

### 4. Verschwindende Nachrichten (Snapchat-Style)

```dart
class DisappearingMessage extends TextMessage {
  bool isOpened = false;
  DateTime? openedAt;
  int countdownSeconds = 10;   // Countdown nach Öffnen

  Timer? _destructTimer;

  void open() {
    isOpened = true;
    openedAt = DateTime.now();

    // Starte Countdown
    _destructTimer = Timer(Duration(seconds: countdownSeconds), () {
      _selfDestruct();
    });
  }

  Future<void> _selfDestruct() async {
    // 1. Lokal löschen
    await deleteLocal();

    // 2. Server benachrichtigen (löscht auch dort)
    await notifyServerToDelete();

    // 3. Screenshot-Erkennung (Android/iOS)
    // (Benachrichtigt Sender wenn Empfänger Screenshot macht)
  }
}
```

---

## 🔒 SICHERHEITS-FEATURES

### 1. Perfect Forward Secrecy

**Was ist das?**
Wenn ein Schlüssel kompromittiert wird, bleiben **alle vorherigen Nachrichten** sicher.

**Wie?**
- Jede Nachricht nutzt einen **einmaligen** Message Key
- Message Keys werden aus Chain Keys abgeleitet
- Chain Keys werden nach jeder Nachricht **gelöscht** (Ratcheting)

**Beispiel:**
```
Message 1: Key A → [verschlüsselt] → Key A wird GELÖSCHT
Message 2: Key B → [verschlüsselt] → Key B wird GELÖSCHT
Message 3: Key C → [verschlüsselt] → Key C wird GELÖSCHT

Angreifer stiehlt Key C → Kann NUR Message 3 lesen, 1 & 2 bleiben sicher!
```

### 2. Safety Numbers (Fingerprint-Verifikation)

```dart
// lib/services/crypto/safety_numbers.dart

class SafetyNumber {
  static String generate(PublicKey yourIdentityKey, PublicKey theirIdentityKey) {
    // SHA-256 Hash über beide Identity Keys
    final combined = [
      ...await yourIdentityKey.extractBytes(),
      ...await theirIdentityKey.extractBytes(),
    ];

    final hash = Sha256().hashSync(combined);

    // In lesbare Zahlenfolge umwandeln
    final safetyNumber = _formatAsDigits(hash);

    return safetyNumber; // z.B. "12345 67890 12345 67890 12345 67890"
  }

  static String _formatAsDigits(List<int> hash) {
    final digits = hash.map((byte) => byte % 10).toList();

    // Gruppiere in 6er-Blöcke
    final groups = <String>[];
    for (var i = 0; i < digits.length; i += 6) {
      groups.add(digits.sublist(i, min(i + 6, digits.length)).join());
    }

    return groups.join(' ');
  }
}
```

**UI für Verifikation:**
```dart
Widget buildSafetyNumberScreen(Contact contact) {
  final mySafetyNumber = SafetyNumber.generate(
    myIdentityKey,
    contact.identityKey,
  );

  return Scaffold(
    appBar: AppBar(title: Text('Sicherheitsnummer')),
    body: Column(
      children: [
        Text('Deine Sicherheitsnummer mit ${contact.name}:'),
        SizedBox(height: 20),

        // Große, lesbare Anzeige
        Text(
          mySafetyNumber,
          style: TextStyle(
            fontSize: 24,
            fontFamily: 'monospace',
            letterSpacing: 2,
          ),
        ),

        SizedBox(height: 20),

        // QR-Code zum Scannen
        QrImage(data: mySafetyNumber, size: 200),

        SizedBox(height: 20),

        Text('Vergleiche diese Nummer mit ${contact.name} persönlich oder per Videocall.'),

        ElevatedButton(
          onPressed: () => _markAsVerified(contact),
          child: Text('Als verifiziert markieren'),
        ),
      ],
    ),
  );
}
```

### 3. Sealed Sender (Metadata-Protection)

**Problem:**
Auch bei E2E-Verschlüsselung kann der Server sehen **wer mit wem** kommuniziert.

**Lösung: Sealed Sender**
```dart
class SealedSender {
  // Verschickt Nachrichten OHNE Absender-Info an Server
  Future<void> sendSealedMessage(
    EncryptedMessage message,
    String recipientId,
  ) async {
    // 1. Message doppelt verschlüsseln
    final innerEncrypted = await _encryptWithRecipientKey(message);

    // 2. Äußere Schicht mit Server-Key verschlüsseln
    final sealedMessage = await _sealWithServerKey(innerEncrypted);

    // 3. An Server senden (Server sieht NUR Empfänger)
    await _apiClient.sendSealedMessage(
      recipientId: recipientId,
      sealedPayload: sealedMessage,
      // KEIN senderId!
    );
  }

  // Server kann Message weiterleiten, aber nicht:
  // - Wer der Absender ist
  // - Was der Inhalt ist
  // - Wann sie verschickt wurde
}
```

### 4. Deniable Authentication

**Was ist das?**
Du kannst **beweisen**, dass eine Nachricht von Person X kam (für dich selbst), aber **nicht öffentlich** beweisen (vor Gericht z.B.).

**Warum wichtig?**
Schützt vor Erpressung durch geleakte Screenshots.

**Technisch:**
```dart
// Signal Protocol nutzt bereits Deniable Authentication via:
// - HMAC statt Signaturen
// - Symmetrische Authentifizierung
```

### 5. Screenshot-Erkennung

**Android:**
```dart
// lib/services/security/screenshot_detection.dart

class ScreenshotDetection {
  StreamSubscription? _subscription;

  void enable(Function onScreenshot) {
    _subscription = ScreenshotCallback.onScreenshotTaken.listen((file) {
      print('Screenshot detected: $file');
      onScreenshot();
    });
  }

  void disable() {
    _subscription?.cancel();
  }
}

// In Chat Screen:
void _onScreenshotDetected() {
  // 1. Benachrichtige Sender
  _notifySenderOfScreenshot();

  // 2. Zeige lokale Warnung
  showDialog(
    context: context,
    builder: (_) => AlertDialog(
      title: Text('Screenshot erkannt'),
      content: Text('Der Absender wurde benachrichtigt.'),
    ),
  );
}
```

---

## 🗄️ LOKALE DATEN-SPEICHERUNG

### Verschlüsselte Datenbank

```dart
// lib/services/storage/encrypted_database.dart

import 'package:sqflite_sqlcipher/sqflite.dart';

class EncryptedDatabase {
  late Database _db;

  Future<void> initialize(String password) async {
    final dbPath = await getDatabasesPath();

    _db = await openDatabase(
      '$dbPath/najika_messenger.db',
      version: 1,
      password: password, // SQLCipher-Verschlüsselung
      onCreate: (db, version) async {
        // Chats Tabelle
        await db.execute('''
          CREATE TABLE chats (
            id TEXT PRIMARY KEY,
            participant_id TEXT NOT NULL,
            participant_name TEXT,
            last_message TEXT,
            last_message_time INTEGER,
            unread_count INTEGER DEFAULT 0,
            identity_key BLOB,
            safety_number TEXT
          )
        ''');

        // Messages Tabelle
        await db.execute('''
          CREATE TABLE messages (
            id TEXT PRIMARY KEY,
            chat_id TEXT NOT NULL,
            sender_id TEXT,
            recipient_id TEXT,
            encrypted_content BLOB NOT NULL,
            message_key BLOB NOT NULL,
            timestamp INTEGER NOT NULL,
            is_read INTEGER DEFAULT 0,
            is_delivered INTEGER DEFAULT 0,
            lifetime INTEGER,
            delete_after INTEGER,
            opened_at INTEGER,
            FOREIGN KEY (chat_id) REFERENCES chats (id)
          )
        ''');

        // Keys Tabelle
        await db.execute('''
          CREATE TABLE crypto_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_type TEXT NOT NULL,
            key_data BLOB NOT NULL,
            created_at INTEGER NOT NULL
          )
        ''');
      },
    );
  }

  Future<void> saveMessage(EncryptedMessage message) async {
    await _db.insert('messages', {
      'id': message.id,
      'chat_id': message.chatId,
      'encrypted_content': message.ciphertext,
      'message_key': message.messageKey,
      'timestamp': message.timestamp.millisecondsSinceEpoch,
      'lifetime': message.lifetime?.index,
    });
  }

  Future<List<EncryptedMessage>> getMessages(String chatId) async {
    final results = await _db.query(
      'messages',
      where: 'chat_id = ?',
      whereArgs: [chatId],
      orderBy: 'timestamp ASC',
    );

    return results.map((row) => EncryptedMessage.fromDb(row)).toList();
  }
}
```

---

## 📡 SERVER-ARCHITEKTUR

### Zero-Knowledge Messenger Server

```python
# najika_messenger_server.py

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Datenbank (speichert nur verschlüsselte Daten!)
def init_db():
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()

    # Messages Queue (temporäre Speicherung)
    c.execute('''
        CREATE TABLE IF NOT EXISTS message_queue (
            id TEXT PRIMARY KEY,
            recipient_id TEXT NOT NULL,
            encrypted_payload BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_sealed INTEGER DEFAULT 0
        )
    ''')

    # PreKeys (für X3DH)
    c.execute('''
        CREATE TABLE IF NOT EXISTS prekeys (
            user_id TEXT NOT NULL,
            key_type TEXT NOT NULL,
            public_key BLOB NOT NULL,
            key_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, key_type, key_id)
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/api/messenger/send', methods=['POST'])
def send_message():
    """
    Server empfängt verschlüsselte Message.
    Server kann Inhalt NICHT lesen!
    """
    data = request.json

    recipient_id = data['recipient_id']
    encrypted_payload = data['encrypted_payload']  # Bereits E2E-verschlüsselt!
    is_sealed = data.get('is_sealed', False)

    # Speichere in Queue (für offline Empfänger)
    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()

    message_id = str(uuid.uuid4())

    c.execute('''
        INSERT INTO message_queue
        (id, recipient_id, encrypted_payload, is_sealed, expires_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        message_id,
        recipient_id,
        encrypted_payload,
        is_sealed,
        datetime.now() + timedelta(days=30)  # Auto-Delete nach 30 Tagen
    ))

    conn.commit()
    conn.close()

    # Sende via WebSocket wenn Empfänger online
    socketio.emit('new_message', {
        'message_id': message_id,
        'encrypted_payload': encrypted_payload,
    }, room=recipient_id)

    return jsonify({'status': 'sent', 'message_id': message_id})

@app.route('/api/messenger/fetch', methods=['GET'])
def fetch_messages():
    """
    Empfänger holt wartende Messages ab.
    """
    user_id = request.args.get('user_id')

    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()

    c.execute('''
        SELECT id, encrypted_payload, created_at
        FROM message_queue
        WHERE recipient_id = ?
        ORDER BY created_at ASC
    ''', (user_id,))

    messages = c.fetchall()

    # Lösche abgeholte Messages
    c.execute('DELETE FROM message_queue WHERE recipient_id = ?', (user_id,))
    conn.commit()
    conn.close()

    return jsonify({
        'messages': [
            {
                'id': msg[0],
                'encrypted_payload': msg[1],
                'timestamp': msg[2],
            }
            for msg in messages
        ]
    })

@app.route('/api/messenger/prekeys/upload', methods=['POST'])
def upload_prekeys():
    """
    User uploaded PreKeys für X3DH.
    """
    data = request.json
    user_id = data['user_id']

    identity_key = data['identity_key']
    signed_prekey = data['signed_prekey']
    onetime_prekeys = data['onetime_prekeys']

    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()

    # Identity Key speichern
    c.execute('''
        INSERT OR REPLACE INTO prekeys
        (user_id, key_type, public_key, key_id)
        VALUES (?, ?, ?, ?)
    ''', (user_id, 'identity', identity_key, 0))

    # Signed PreKey speichern
    c.execute('''
        INSERT OR REPLACE INTO prekeys
        (user_id, key_type, public_key, key_id)
        VALUES (?, ?, ?, ?)
    ''', (user_id, 'signed_prekey', signed_prekey, 0))

    # One-Time PreKeys speichern
    for i, otk in enumerate(onetime_prekeys):
        c.execute('''
            INSERT OR REPLACE INTO prekeys
            (user_id, key_type, public_key, key_id)
            VALUES (?, ?, ?, ?)
        ''', (user_id, 'onetime_prekey', otk, i))

    conn.commit()
    conn.close()

    return jsonify({'status': 'uploaded'})

@app.route('/api/messenger/prekeys/fetch', methods=['GET'])
def fetch_prekeys():
    """
    Holt PreKeys eines Users (für Initial Key Exchange).
    """
    target_user_id = request.args.get('user_id')

    conn = sqlite3.connect('messenger.db')
    c = conn.cursor()

    # Identity Key
    c.execute('''
        SELECT public_key FROM prekeys
        WHERE user_id = ? AND key_type = 'identity'
    ''', (target_user_id,))
    identity_key = c.fetchone()[0]

    # Signed PreKey
    c.execute('''
        SELECT public_key FROM prekeys
        WHERE user_id = ? AND key_type = 'signed_prekey'
    ''', (target_user_id,))
    signed_prekey = c.fetchone()[0]

    # One-Time PreKey (nimm ersten verfügbaren, lösche dann)
    c.execute('''
        SELECT key_id, public_key FROM prekeys
        WHERE user_id = ? AND key_type = 'onetime_prekey'
        LIMIT 1
    ''', (target_user_id,))
    otk_result = c.fetchone()

    onetime_prekey = None
    if otk_result:
        otk_id, onetime_prekey = otk_result
        # Lösche genutzten One-Time PreKey
        c.execute('''
            DELETE FROM prekeys
            WHERE user_id = ? AND key_type = 'onetime_prekey' AND key_id = ?
        ''', (target_user_id, otk_id))
        conn.commit()

    conn.close()

    return jsonify({
        'identity_key': identity_key,
        'signed_prekey': signed_prekey,
        'onetime_prekey': onetime_prekey,
    })

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=8001)
```

---

## 🎨 UI/UX DESIGN

### Chat List Screen

```
┌─────────────────────────┐
│ 🔒 Secure Messenger     │
├─────────────────────────┤
│ [🔍 Suche...]           │
├─────────────────────────┤
│ Alice                   │
│ ✓✓ Alles klar!    10:23 │ ← Zugestellt & Gelesen
│ ─────────────────────── │
│ Bob                  🔐 │
│ ✓ Bis später!     09:15 │ ← Verifiziert (Safety Number)
│ ─────────────────────── │
│ Charlie              💣 │
│ 👁 Foto gesendet   gestern │ ← Selbstzerstörend
│ ─────────────────────── │
│ Group: Team         (3) │
│ Dave: Meeting?     08:00 │
└─────────────────────────┘
```

### Chat Screen

```
┌─────────────────────────┐
│ [←] Alice          [⋮]  │ ← Header mit Safety Number
│ 🔐 Verifiziert          │
├─────────────────────────┤
│                         │
│ [Alice]    10:20        │
│ Hey! Wie gehts?         │
│                         │
│        10:21  [Du] ✓✓   │
│      Gut danke!         │
│                         │
│ [Alice]    10:22   👁   │
│ [FOTO - Selbstzerstörend]│ ← Click zum Öffnen
│ Countdown: 10s          │
│                         │
│        10:23  [Du] 🔊   │
│      [VOICE 0:15]       │
│      ▁▃▅▇▅▃▁            │ ← Waveform
│                         │
├─────────────────────────┤
│ 🔐 E2E-verschlüsselt    │ ← Indikator
│ [📷][🎤] Type...  [🚀]   │
│                         │
│ ⏱ Selbstzerstörend: OFF │ ← Toggle
└─────────────────────────┘
```

### Safety Number Verification

```
┌─────────────────────────┐
│ [←] Sicherheitsnummer   │
├─────────────────────────┤
│ Deine Nummer mit Alice: │
│                         │
│  12345 67890 12345      │
│  67890 12345 67890      │
│  12345 67890 12345      │
│                         │
│ ┌─────────────────────┐ │
│ │                     │ │
│ │    [QR-CODE]        │ │ ← Zum Scannen
│ │                     │ │
│ └─────────────────────┘ │
│                         │
│ Vergleiche diese Nummer │
│ persönlich oder per     │
│ Videocall mit Alice.    │
│                         │
│ Status: ⚠ Nicht verifiziert│
│                         │
│ [Als verifiziert markieren]│
└─────────────────────────┘
```

---

## 🔔 BENACHRICHTIGUNGEN

### Push Notifications (Verschlüsselt!)

**Problem:**
Standard-Push-Notifications gehen durch Google/Apple Server → nicht E2E.

**Lösung:**
```dart
// lib/services/notifications/secure_push.dart

class SecurePushNotifications {
  Future<void> sendEncryptedPush(String recipientId, String message) async {
    // 1. Verschlüssele Notification-Payload
    final encryptedPayload = await _encryptNotification(message);

    // 2. Sende via Firebase Cloud Messaging
    await _fcm.send(
      recipientId: recipientId,
      data: {
        'encrypted_payload': encryptedPayload,
        'type': 'secure_message',
      },
      // KEINE plaintext Message!
    );
  }

  // Empfänger-Seite
  void onNotificationReceived(Map<String, dynamic> data) async {
    final encryptedPayload = data['encrypted_payload'];

    // Entschlüssele lokal
    final decryptedMessage = await _decryptNotification(encryptedPayload);

    // Zeige Notification
    _showLocalNotification(
      title: 'Neue Nachricht',
      body: decryptedMessage,
    );
  }
}
```

---

## 🚀 IMPLEMENTIERUNGSPLAN

### Phase 1: Krypto-Grundlage (2 Wochen)
```
✅ Signal Protocol implementieren
  ├─ X3DH Key Exchange
  ├─ Double Ratchet
  └─ AES-256-GCM Encryption

✅ Key Management
  ├─ Identity Keys
  ├─ Signed PreKeys
  └─ One-Time PreKeys

✅ Safety Numbers
```

### Phase 2: Basis-Messenger (2 Wochen)
```
✅ Chat-Liste
✅ Chat-Screen
✅ Text-Nachrichten senden/empfangen
✅ E2E-Verschlüsselung aktiv
✅ Lokale verschlüsselte Datenbank
```

### Phase 3: Medien & Features (2 Wochen)
```
✅ Sprachnachrichten
✅ Bilder/Videos
✅ Selbstzerstörende Nachrichten
✅ Read Receipts
✅ Typing Indicators
```

### Phase 4: Server & Sync (1 Woche)
```
✅ Zero-Knowledge Server
✅ Message Queue
✅ PreKey Server
✅ WebSocket Real-time
```

### Phase 5: Erweiterte Sicherheit (1 Woche)
```
✅ Sealed Sender
✅ Screenshot-Erkennung
✅ Verschlüsselte Push-Notifications
✅ Safety Number Verification UI
```

### Phase 6: Polish & Testing (1 Woche)
```
✅ UI/UX Feinschliff
✅ Security Audit
✅ Penetration Testing
✅ Performance-Optimierung
```

---

## 📊 VERGLEICH MIT ANDEREN MESSENGERN

```
┌──────────────────┬─────────┬──────────┬──────────┬────────────┐
│                  │ Najika  │ Signal   │ WhatsApp │ Telegram   │
├──────────────────┼─────────┼──────────┼──────────┼────────────┤
│ E2E-Encryption   │ ✅ Ja   │ ✅ Ja    │ ✅ Ja    │ ⚠ Optional │
│ Open Source      │ ✅ Ja   │ ✅ Ja    │ ❌ Nein  │ ⚠ Teilw.   │
│ Metadata-Schutz  │ ✅ Ja   │ ✅ Ja    │ ❌ Nein  │ ❌ Nein    │
│ Snapchat-Mode    │ ✅ Ja   │ ✅ Ja    │ ✅ Ja    │ ✅ Ja      │
│ Self-Hosted      │ ✅ Ja   │ ❌ Nein  │ ❌ Nein  │ ❌ Nein    │
│ Tor-Support      │ ✅ Ja   │ ✅ Ja    │ ❌ Nein  │ ⚠ Optional │
│ Phone Number     │ ❌ Nein │ ✅ Ja    │ ✅ Ja    │ ✅ Ja      │
│ Zero-Knowledge   │ ✅ Ja   │ ✅ Ja    │ ❌ Nein  │ ❌ Nein    │
└──────────────────┴─────────┴──────────┴──────────┴────────────┘
```

---

## ✅ ZUSAMMENFASSUNG

### Was macht Najika Messenger besonders?

1. **Military-Grade Security**
   - Signal Protocol (bewährt!)
   - Perfect Forward Secrecy
   - Zero-Knowledge Server

2. **Snapchat-Style Features**
   - Selbstzerstörende Nachrichten
   - Screenshot-Erkennung
   - Countdown-Timer

3. **Maximale Privatsphäre**
   - Sealed Sender (Metadata-Schutz)
   - Tor-Integration
   - Keine Telefonnummer erforderlich

4. **Nahtlose Integration**
   - Teil der Najika Digivice App
   - Gemeinsame Verschlüsselung
   - Einheitliches Design

---

**Dokumentiert von:** Claude Code
**Datum:** 2025-11-07
**Version:** 1.0
**Status:** Design Complete - Ready for Implementation 🔐
