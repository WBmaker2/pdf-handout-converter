---
name: PDF Handout Converter
description: Print-shop magazine identity for a local PDF handout converter.
colors:
  paper: "#F7F4EE"
  paper-2: "#EFEAE0"
  ink: "#0E0E0E"
  spot: "#C9352B"
  muted: "#5A5650"
  line: "rgba(14,14,14,0.14)"
typography:
  display:
    fontFamily: "Bodoni Moda, Times New Roman, serif"
    fontSize: "clamp(2.6rem, 6vw, 4.6rem)"
    fontWeight: 600
    lineHeight: 0.95
    letterSpacing: "-0.02em"
  headline:
    fontFamily: "Bodoni Moda, Times New Roman, serif"
    fontSize: "1.5rem"
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Manrope, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Manrope, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.02em"
rounded:
  none: "0px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "48px"
  2xl: "64px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "14px 28px"
  button-primary-hover:
    backgroundColor: "{colors.spot}"
    textColor: "{colors.paper}"
    rounded: "{rounded.none}"
    padding: "14px 28px"
  input-field:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "10px 14px"
  upload-zone:
    backgroundColor: "{colors.paper-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "24px"
---

# Design System: PDF Handout Converter

## Overview

**Creative North Star: "The Print Shop"**

A mid-century magazine identity for a local print tool: black ink on warm coated stock, one vermilion spot color, a serif masthead over a strict two-column grid, drop initials, and heavy rules. The interface refuses the default Gradio card stack and the generic hero-over-features template; every screen reads like a press sheet. Calm, precise, trustworthy.

**Key Characteristics:**
- Warm paper ground (#F7F4EE) with ink (#0E0E0E) text; one spot color (vermilion #C9352B) used sparingly.
- Bodoni Moda serif for display and headlines; Manrope for UI and body.
- Zero radius: all corners are square; rules (1px/3px) carry structure.
- Two-column fold on desktop; single column on mobile.
- Hidden silhouette mark revealed on hover (footer).

## Colors

One spot color on a paper/ink ground.

### Primary
- **Ink** (#0E0E0E): text, rules, primary button ground.

### Accent
- **Vermilion Spot** (#C9352B): primary action hover, drop caps, link emphasis. Used on ≤10% of any screen.

### Neutral
- **Paper** (#F7F4EE): page ground.
- **Paper 2** (#EFEAE0): input and upload-zone ground.
- **Muted** (#5A5650): secondary text, notes, footer.
- **Line** (rgba(14,14,14,0.14)): hairline dividers.

**The One Voice Rule.** The vermilion spot appears on at most one element per viewport; its rarity is the point.

## Typography

**Display Font:** Bodoni Moda (with Times New Roman, serif fallback)
**Body Font:** Manrope (with ui-sans-serif, system-ui fallback)

**Character:** High-contrast serif masthead against a clean grotesque UI; editorial, precise, slightly formal.

### Hierarchy
- **Display** (600, clamp(2.6rem,6vw,4.6rem), 0.95): masthead title.
- **Headline** (600, 1.5rem, 1.1): section titles with drop cap.
- **Body** (400, 1rem, 1.55): lede and notes, max ~65ch.
- **Label** (600, 0.85rem, 0.02em): footer, button text (uppercase).

## Layout

Two-column grid (1:1) on desktop folding to one column under 768px. Container max-width 1200px, centered. Spacing rhythm 8/16/24/48/64px. Masthead padding 48px top. Heavy 3px rule separates masthead from body.

## Elevation & Depth

Flat by default. No shadows. Depth is conveyed by rules, tonal paper steps (paper vs paper-2), and the spot-color hover state. Shadows are not used.

**The Flat-By-Default Rule.** Surfaces are flat at rest; emphasis comes from rules and tonal steps, not shadows.

## Shapes

Square corners throughout (0px radius). Borders are 1px hairlines or 2-3px heavy rules. No rounded rectangles, no pills.

## Components

### Buttons
- **Shape:** square (0px).
- **Primary:** ink ground (#0E0E0E), paper text, 2px ink border, uppercase Manrope 600, padding 14px 28px. Hover: vermilion ground and border, 1px lift.
- **Focus:** 2px vermilion outline, 2px offset.

### Inputs / Fields
- **Style:** paper-2 ground, 1px ink border, square, padding 10px 14px.
- **Focus:** vermilion outline.

### Upload Zone
- **Style:** 2px dashed ink border, paper-2 ground, min-height 140px. Hover: vermilion border, white ground.

### Drop Cap
- **Style:** vermilion, 2.4rem, line-height 0.85, leading section titles.

## Do's and Don'ts

### Do:
- **Do** keep corners square and rules heavy.
- **Do** use vermilion on at most one element per viewport.
- **Do** fold two columns to one on mobile.
- **Do** keep the upload → convert → download flow visible without scrolling.

### Don't:
- **Don't** use rounded corners or pill buttons.
- **Don't** add shadows or glass.
- **Don't** use an eyebrow/kicker above the masthead.
- **Don't** let the convert action leave the first viewport.
