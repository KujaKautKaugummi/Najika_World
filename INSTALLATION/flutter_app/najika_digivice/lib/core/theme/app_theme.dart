import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// App Theme
///
/// Gothic Lolita dark theme with:
/// - Deep blacks and purples
/// - Elegant typography
/// - Smooth animations
class AppTheme {
  // Color palette
  static const Color primaryColor = Color(0xFF9C27B0);  // Deep Purple
  static const Color secondaryColor = Color(0xFFE91E63);  // Pink
  static const Color backgroundColor = Color(0xFF0A0A0A);  // Almost Black
  static const Color surfaceColor = Color(0xFF1A1A1A);  // Dark Grey
  static const Color errorColor = Color(0xFFCF6679);  // Red

  static const Color textPrimaryColor = Color(0xFFFFFFFF);  // White
  static const Color textSecondaryColor = Color(0xFFB0B0B0);  // Grey

  static const Color accentGold = Color(0xFFFFD700);  // Gold accent
  static const Color accentSilver = Color(0xFFC0C0C0);  // Silver accent

  /// Dark theme
  static ThemeData get darkTheme {
    return ThemeData(
      brightness: Brightness.dark,
      primaryColor: primaryColor,
      scaffoldBackgroundColor: backgroundColor,

      // Color scheme
      colorScheme: const ColorScheme.dark(
        primary: primaryColor,
        secondary: secondaryColor,
        surface: surfaceColor,
        background: backgroundColor,
        error: errorColor,
      ),

      // App bar theme
      appBarTheme: AppBarTheme(
        backgroundColor: surfaceColor,
        elevation: 0,
        centerTitle: true,
        titleTextStyle: GoogleFonts.cinzel(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: textPrimaryColor,
        ),
        iconTheme: const IconThemeData(color: textPrimaryColor),
      ),

      // Text theme
      textTheme: TextTheme(
        displayLarge: GoogleFonts.cinzel(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: textPrimaryColor,
        ),
        displayMedium: GoogleFonts.cinzel(
          fontSize: 24,
          fontWeight: FontWeight.bold,
          color: textPrimaryColor,
        ),
        bodyLarge: GoogleFonts.lato(
          fontSize: 16,
          color: textPrimaryColor,
        ),
        bodyMedium: GoogleFonts.lato(
          fontSize: 14,
          color: textSecondaryColor,
        ),
      ),

      // Card theme
      cardTheme: CardTheme(
        color: surfaceColor,
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),

      // Button themes
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: textPrimaryColor,
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),

      // Input decoration
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surfaceColor,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: BorderSide.none,
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8),
          borderSide: const BorderSide(color: primaryColor, width: 2),
        ),
      ),

      // Icon theme
      iconTheme: const IconThemeData(
        color: textPrimaryColor,
        size: 24,
      ),
    );
  }
}
