/**
 * JAVA BASICS - Training Data für Najika
 * Grundlegende Java-Konzepte und Syntax
 */

// ============================================
// KLASSEN & OBJEKTE
// ============================================

public class JavaBasics {

    // ============================================
    // VARIABLEN & DATENTYPEN
    // ============================================

    // Primitive Typen
    int number = 42;
    double pi = 3.14159;
    boolean isActive = true;
    char letter = 'A';

    // Strings
    String name = "Najika";
    String greeting = "Hallo, ich bin " + name + "!";

    // Arrays
    String[] explosionTargets = {"Dämon", "Drache", "Boss", "Burg"};
    int[] damageValues = {100, 250, 500, 1000};

    // ============================================
    // METHODEN
    // ============================================

    /**
     * Begrüßt einen User
     */
    public String greetUser(String username) {
        return "EXPLOSION!!! Willkommen " + username + "! ✨";
    }

    /**
     * Berechnet Schadenswert
     */
    public int calculateDamage(int baseDamage, double multiplier) {
        return (int)(baseDamage * multiplier);
    }

    /**
     * Berechnet Schadenswert mit default multiplier
     */
    public int calculateDamage(int baseDamage) {
        return calculateDamage(baseDamage, 1.5);
    }

    // ============================================
    // STATIC METHODEN
    // ============================================

    public static void main(String[] args) {
        JavaBasics basics = new JavaBasics();
        System.out.println(basics.greetUser("Kuja"));
        System.out.println("Schaden: " + basics.calculateDamage(100));
    }
}

// ============================================
// CHARAKTER-KLASSE (OOP)
// ============================================

class Character {
    // Private Felder
    private String name;
    private int hp;
    private int attack;

    // Konstruktor
    public Character(String name, int hp, int attack) {
        this.name = name;
        this.hp = hp;
        this.attack = attack;
    }

    // Getter & Setter
    public String getName() {
        return name;
    }

    public int getHp() {
        return hp;
    }

    public void setHp(int hp) {
        this.hp = Math.max(0, hp); // HP nicht unter 0
    }

    public int getAttack() {
        return attack;
    }

    // Methoden
    public void takeDamage(int damage) {
        this.hp -= damage;
        if (this.hp < 0) {
            this.hp = 0;
        }
    }

    public boolean isAlive() {
        return this.hp > 0;
    }

    public String attackEnemy(Character enemy) {
        int damage = this.attack;
        enemy.takeDamage(damage);
        return this.name + " greift " + enemy.getName() + " für " + damage + " Schaden an!";
    }

    @Override
    public String toString() {
        return name + " (HP: " + hp + ", ATK: " + attack + ")";
    }
}

// ============================================
// VERERBUNG (INHERITANCE)
// ============================================

class Megumin extends Character {
    private int mana;

    public Megumin() {
        super("Megumin", 100, 50);
        this.mana = 100;
    }

    public int getMana() {
        return mana;
    }

    public void setMana(int mana) {
        this.mana = mana;
    }

    public String castExplosion(Character target) {
        if (this.mana < 100) {
            return "Nicht genug Mana für EXPLOSION!";
        }

        this.mana = 0;
        int damage = 999;
        target.takeDamage(damage);
        return "✨ EXPLOSION!!! " + target.getName() + " nimmt " + damage + " Schaden!";
    }

    @Override
    public String toString() {
        return super.toString() + " (Mana: " + mana + ")";
    }
}

// ============================================
// INTERFACES
// ============================================

interface Attackable {
    void takeDamage(int damage);
    boolean isAlive();
}

interface Castable {
    String castSpell(Character target);
    int getManaCost();
}

// ============================================
// ABSTRACT CLASSES
// ============================================

abstract class Spell {
    protected String name;
    protected int manaCost;
    protected int baseDamage;

    public Spell(String name, int manaCost, int baseDamage) {
        this.name = name;
        this.manaCost = manaCost;
        this.baseDamage = baseDamage;
    }

    public abstract String cast(Character caster, Character target);

    public int getManaCost() {
        return manaCost;
    }
}

class ExplosionSpell extends Spell {
    public ExplosionSpell() {
        super("EXPLOSION", 100, 999);
    }

    @Override
    public String cast(Character caster, Character target) {
        target.takeDamage(baseDamage);
        return "✨ " + caster.getName() + " wirkt EXPLOSION auf " + target.getName() + "!";
    }
}

// ============================================
// GENERICS
// ============================================

class Container<T> {
    private T value;

    public Container(T value) {
        this.value = value;
    }

    public T getValue() {
        return value;
    }

    public void setValue(T value) {
        this.value = value;
    }
}

// ============================================
// COLLECTIONS (LISTS, MAPS, SETS)
// ============================================

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

class CollectionsExample {
    public static void demonstrateCollections() {
        // ArrayList
        List<String> names = new ArrayList<>();
        names.add("Megumin");
        names.add("Kazuma");
        names.add("Aqua");
        names.add("Darkness");

        // HashMap
        Map<String, Integer> levels = new HashMap<>();
        levels.put("Megumin", 50);
        levels.put("Kazuma", 35);

        // HashSet
        Set<String> skills = new HashSet<>();
        skills.add("EXPLOSION");
        skills.add("Fireball");
        skills.add("EXPLOSION"); // Duplikat wird ignoriert

        // Iteration
        for (String name : names) {
            System.out.println(name);
        }

        // Lambda & Streams (Java 8+)
        names.stream()
             .filter(n -> n.startsWith("M"))
             .forEach(System.out::println);
    }
}

// ============================================
// ERROR HANDLING (EXCEPTIONS)
// ============================================

class FileHandler {
    public String readFile(String filePath) throws IOException {
        try {
            // File lesen
            return new String(Files.readAllBytes(Paths.get(filePath)));
        } catch (IOException e) {
            System.err.println("FEHLER beim Lesen: " + e.getMessage());
            throw e;
        }
    }

    public void writeFile(String filePath, String content) {
        try {
            Files.write(Paths.get(filePath), content.getBytes());
            System.out.println("Datei gespeichert: " + filePath);
        } catch (IOException e) {
            System.err.println("FEHLER beim Schreiben: " + e.getMessage());
        }
    }
}

// ============================================
// ENUMS
// ============================================

enum CharacterClass {
    ARCH_WIZARD("Arch Wizard", 50),
    CRUSADER("Crusader", 100),
    PRIEST("Priest", 80),
    ADVENTURER("Adventurer", 60);

    private final String displayName;
    private final int baseHp;

    CharacterClass(String displayName, int baseHp) {
        this.displayName = displayName;
        this.baseHp = baseHp;
    }

    public String getDisplayName() {
        return displayName;
    }

    public int getBaseHp() {
        return baseHp;
    }
}

// ============================================
// THREADS & CONCURRENCY
// ============================================

class AsyncTask implements Runnable {
    private String name;

    public AsyncTask(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        System.out.println("Task " + name + " startet...");
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Task " + name + " fertig!");
    }
}

// ============================================
// WICHTIGE TIPPS
// ============================================

/**
 * JAVA BEST PRACTICES:
 *
 * 1. Verwende sprechende Variablennamen (camelCase)
 * 2. Schreibe JavaDoc-Kommentare für Klassen/Methoden
 * 3. Nutze private Felder + public Getter/Setter
 * 4. Verwende Interfaces für Abstraktion
 * 5. Error-Handling mit try/catch/finally
 * 6. Nutze try-with-resources für Auto-Closeable
 * 7. Vermeide null - nutze Optional<T> (Java 8+)
 * 8. Immutable Objects wenn möglich (final Felder)
 * 9. Nutze StringBuilder statt + für String-Konkatenation
 * 10. Schreibe Unit-Tests (JUnit)
 */

// ============================================
// MODERNE JAVA FEATURES (Java 8+)
// ============================================

import java.util.Optional;
import java.util.stream.Collectors;

class ModernJava {
    // Lambda Expressions
    public void demonstrateLambda() {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

        // Lambda
        numbers.forEach(n -> System.out.println(n));

        // Method Reference
        numbers.forEach(System.out::println);

        // Stream API
        List<Integer> doubled = numbers.stream()
                                       .map(n -> n * 2)
                                       .collect(Collectors.toList());

        int sum = numbers.stream()
                        .filter(n -> n % 2 == 0)
                        .mapToInt(Integer::intValue)
                        .sum();
    }

    // Optional (null-safe)
    public Optional<Character> findCharacterByName(String name) {
        if (name == null || name.isEmpty()) {
            return Optional.empty();
        }

        // Suche Charakter...
        Character found = new Character(name, 100, 50);
        return Optional.of(found);
    }

    public void useOptional() {
        Optional<Character> character = findCharacterByName("Megumin");

        // Alte Art (mit null-check)
        // if (character != null) { ... }

        // Neue Art (mit Optional)
        character.ifPresent(c -> System.out.println(c.getName()));

        String name = character.map(Character::getName)
                              .orElse("Unknown");
    }
}
