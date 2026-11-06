# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary users are instructors and teachers preparing printed handouts from presentation slides; they work in education settings and need A4 portrait output from landscape slide decks.

## Product Purpose

Convert landscape presentation PDFs into A4 portrait handout PDFs (2, 6 or 8 slides per page), preserving vector quality, with optional borders and original page numbers. Success means a fast, local, lossless conversion that instructors can run without internet access.

## Positioning

Unlike rasterizing or screenshot-based converters, this tool places source pages vectorially via PyMuPDF show_pdf_page, so text and graphics stay sharp; it also handles multiple files in one run and exports individual files or a ZIP.

## Operating Context

Runs locally via a Gradio web UI (http://127.0.0.1:7860) or as a Python library/CLI; no network dependency for conversion. Users upload one or more PDFs, choose layout (2, 6 or 8 per page), toggle borders and page numbers, and download results.

## Capabilities and Constraints

- n_per_page: 2, 6 or 8
- margin_mm, gutter_mm configurable in code
- border and show_numbers toggles
- Handles empty PDFs, single slide, encrypted PDFs, portrait input, large documents
- Must run offline/local (no external services at conversion time)
- Gradio-based UI (Python)

## Brand Commitments

None stated; no brand assets or visual identity commitments.

## Evidence on Hand

No testimonials, case studies, or usage metrics available; product claims rest on implementation (PyMuPDF vector placement).

## Product Principles

- Preserve source fidelity: never rasterize slides.
- Keep the workflow short: upload → choose → convert → download.
- Work offline and locally.
- Support batch processing without added friction.

## Accessibility & Inclusion

No product-specific accessibility standard established; standard web accessibility expected for the Gradio UI.
