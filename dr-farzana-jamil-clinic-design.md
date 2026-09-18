# Dr. Farzana Jamil Clinic — Design & Architecture Specification

## Overview
An independent static website demonstration concept for Dr. Farzana Jamil Clinic, providing female gynecology and women's health consultations at City Hospital, Pakpattan, Punjab, Pakistan.

## Brand Identity & Color Tokens
* **Brand Blue:** `#012E75` (Deep Blue primary branding)
* **Brand Blue Light:** `#0B4DA2` (Royal Blue interactive links, focus, and icons)
* **Brand Red:** `#ED060F` (Medical Red accents, badges, and cross motif)
* **Accessible Red:** `#B50918` (High contrast accessible red text)
* **Canvas / Background:** `#F7FAFF` (Clean cool tint canvas)
* **Blue Tint Panel:** `#EAF1FB` (Soft container backgrounds)
* **Surface:** `#FFFFFF` (Card and header surfaces)
* **Border:** `#D7E0ED` (Subtle boundary borders)
* **Text Ink:** `#1B2430` / `#111111` (High legibility typography)

## Typography
* **Display Font Family:** `"Century Gothic", "Avenir Next", Arial, Helvetica, sans-serif`
* **Body Font Family:** `"Inter", "Segoe UI", Arial, Helvetica, sans-serif`
* No editorial serif fonts (Bodoni, Didot, Georgia, Times New Roman) are permitted.

## Map & Privacy Architecture
* **Consent Storage Key:** `farzana_clinic_map_consent_v1`
* **Values:** `granted` or `declined`
* **Click-to-Load Interaction:** The Google Maps iframe uses `data-src` by default and contains no initial `src` attribute. It is blocked until explicit user consent via the privacy bar or placeholder button.
* **Direct Navigation:** Unconditional "Get Directions" link to Google Maps remains available without embedding scripts or requiring consent.
