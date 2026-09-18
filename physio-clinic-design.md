# Physio Clinic — Design & Architecture Specification

## Overview
An independent static website demonstration concept for Physio Clinic and Dr. Talib Hussain, providing physiotherapy, rehabilitation and pain-care information at Al Fareed Garden, Pakpattan, Punjab, Pakistan.

## Brand Identity & Color Tokens (Original Logo Brand System)
* **Primary Blue:** `#045ED1` (`--brand-blue`, `--color-primary`) — Core clinic branding, primary buttons, accents
* **Primary Green:** `#71C030` (`--brand-green`, `--color-accent`) — Rehabilitation vitality accent, hover rings, step indicators, active states
* **Deep Navy Blue:** `#12304F` (`--brand-blue-deep`, `--color-primary-deep`) — High-contrast display headings, marquee bar, footer headers
* **Dark Blue:** `#034CB0` (`--brand-blue-dark`) — Hover button states and active links
* **Supporting Neutral Grey:** `#6F7478` (`--brand-grey`, `--color-muted`) — Subtitles, captions, supporting copy
* **Soft Blue Tint:** `#EBF3FD` (`--brand-blue-soft`, `--color-tint-soft`) — Confidence section background, trust strip, card subtle fills
* **Soft Green Accent:** `#E3F5D4` (`--brand-green-soft`, `--color-accent-light`) — Soft accents, badge backgrounds
* **Clean Cool Canvas:** `#F5F8FA` (`--color-canvas`) — Main background canvas
* **Crisp Surface:** `#FFFFFF` (`--color-surface`) — Component cards, modal dialogs, header surface
* **High Contrast Body Text:** `#1A2530` (`--color-text`) — Crisp legibility body copy
* **Subtle Border:** `#DCE5EC` (`--color-border`) — Component and section borders

## Typography
* **Headings:** `"Montserrat", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` (600, 700)
* **Body / Interface:** `"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` (400, 500, 600)

## Information Architecture & Content
1. **Hero:** "Move better. Manage pain. Return to everyday life." — Primary actions to Official Facebook Page and Google Maps Directions.
2. **Focus Areas (6 Cards):**
   - Back and Neck Pain
   - Joint and Musculoskeletal Pain
   - Sports and Activity-Related Injuries
   - Post-Injury Rehabilitation
   - Neurological Rehabilitation
   - Heel and Foot Pain
3. **Practitioner Overview:** "Meet Dr. Talib Hussain" with clear disclaimers regarding verification.
4. **Clinic Experience:** "Care Built Around Movement" — Clear information before visiting.
5. **Visit Steps:** 3 practical steps (Understand Your Concern, Contact the Clinic, Confirm Before Travelling).
6. **Patient Confidence:** 4 cards (Individual Assessment, Movement-Focused Care, Rehabilitation Guidance, Convenient Pakpattan Location).
7. **Location & Directions:** Al Fareed Garden, Pakpattan, Punjab with privacy-friendly Google Map.
8. **Administrative FAQ:** 8 clear answers covering location, practitioner, treatments, appointments, emergency guidance, and demo scope.
9. **Bukhari AI Pitch:** Presentation of conversion readiness for Dr. Talib Hussain.

## Map & Privacy Architecture
* **Consent Storage Key:** `physio_clinic_map_consent_v1`
* **Values:** `granted` or `declined`
* **Click-to-Load Interaction:** The Google Maps iframe uses `data-src` by default and contains no initial `src` attribute. It is blocked until explicit user consent via the privacy bar or placeholder button.
* **Direct Navigation:** Unconditional "Get Directions" link to Google Maps remains available without embedding scripts or requiring consent.
