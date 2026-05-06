# EDES 301 Project 02 — PocketBeagle TFT PCB

## Project Overview

This project is a two-sided PCB design for a PocketBeagle-based interface board. The board includes an Adafruit 2.8" TFT display, two push buttons, two potentiometers, three LEDs with current-limiting resistors, and a USB connector.

The PCB was designed in KiCad and prepared for manufacturing quote review through MacroFab.

## Board Description

The board is designed as a 5 in × 4 in two-sided PCB.

### Front Side Components

The front side contains the user-interface components:

- Adafruit 2.8" TFT display
- Two push buttons
- Two potentiometers
- Three LEDs
- LED current-limiting resistors

### Back Side Components

The back side contains the main controller and USB connector:

- PocketBeagle
- USB Type-A connector

## Major Electrical Connections

### TFT Display

The Adafruit TFT footprint includes many additional pads for features such as SD card, touchscreen, and interface configuration. This project only uses the SPI display interface.

The routed TFT pins are:

- `GND` → Ground
- `3-5V` → +5 V
- `CLK` → PocketBeagle SPI clock
- `MOSI` → PocketBeagle SPI MOSI
- `MISO` → PocketBeagle SPI MISO
- `CS` → TFT chip select GPIO
- `D/C` → TFT data/command GPIO
- `RST` → TFT reset GPIO

Unused TFT-related pads may include:

- `Card Detect`
- `Card CS`
- `M0`
- `M1`
- `M2`
- `M3`
- `X+`
- `X-`
- `Y+`
- `Y-`
- `3.3V out`
- other unused breakout-board pads

These pads are intentionally left unconnected because the project does not use SD card, touchscreen, or alternate interface features.

### Potentiometers

Each potentiometer is connected as a voltage divider:

- One side to `GND`
- One side to `+1V8`
- Wiper to a PocketBeagle analog input

### Push Buttons

Each push button is connected between a PocketBeagle GPIO input and ground.

### LEDs

Each LED is connected through a current-limiting resistor to a PocketBeagle GPIO pin and ground.

### USB Connector

The USB connector is used for power and/or board access depending on the final configuration.

Basic connections include:

- `VBUS` → +5 V
- `GND` → Ground
- Shield → Ground, if connected in final layout

## PCB Design Rules

The design follows the class PCB design-rule target where possible:

- Signal trace width: 10 mil typical
- Signal clearance: 5–10 mil
- Power trace width: approximately 15 mil where space allows
- Via size: 24 mil
- Via drill: 12 mil

In dense areas near the TFT and PocketBeagle headers, 5 mil routing/clearance may be used where necessary to complete routing.

## Known Warnings / Final PCB Notes

The final PCB design may contain warnings related to unused pads on the Adafruit TFT footprint.

These warnings are expected because the Adafruit TFT breakout footprint includes additional physical pads for optional features that are not used in this design, including SD card, touchscreen, and configuration pins.

The required TFT display pins are routed. The unused TFT pads are intentionally left unconnected.

Warnings that were reviewed and considered acceptable:

- Unused TFT breakout-board pads with no assigned schematic connection
- Optional TFT feature pins not used in this project
- Silkscreen or labeling warnings that do not affect electrical operation, if present

Errors that should not be ignored:

- Copper clearance violations
- Short circuits
- Unconnected required nets
- Missing board outline
- Incorrect footprint-to-symbol pin matching for required signals

## Library Components Created or Imported

Custom or imported library components used in this project include:

- PocketBeagle symbol/footprint
- Adafruit 2.8" TFT breakout footprint
- Custom simplified Adafruit TFT schematic symbol
- Potentiometer symbol/footprint, if modified or imported
- USB_A symbol/footprint, if imported

Standard KiCad components such as resistors, LEDs, and push buttons were used where appropriate.

## Manufacturing Files

The generated manufacturing package includes:

- Gerber files
- Drill files
- PCB layout files
- Schematic PDF
- Bill of Materials
- PCB screenshots
- MacroFab quote documentation

Gerber layers include:

- Front copper
- Back copper
- Front solder mask
- Back solder mask
- Front silkscreen
- Back silkscreen
- Edge cuts
- Drill files

## MacroFab Quote

A MacroFab quote was generated for the completed PCB design. The quote shows a volume discount, where the per-unit cost decreases as the order quantity increases.

Quoted quantities include low-volume prototype and larger production quantities.

## Documentation Screenshots

The project documentation includes screenshots of:

- Full schematic
- Front PCB layout
- Back PCB layout
- 3D PCB view, if available
- Design Rule Check result
- MacroFab price break / quote page

## Final Notes

## Final Notes

The final PCB still has a few KiCad warnings. The remaining warnings are mostly from small leftover routing features and silkscreen details.

One warning is for an unconnected track end on `Net-(U1-GPIO27)`. Another warning is for a via on `Net-(U1-GPIO20)` that is not fully connected on both layers. These are likely from leftover or partial routing segments during layout cleanup. If this board were revised again, I would remove or reconnect those small segments.

There are also silkscreen clipping warnings from the TFT footprint near the board edge. These warnings affect the printed outline/text only and should not change the electrical function of the board.

The Adafruit TFT footprint also includes extra pads for features such as the SD card, touchscreen, and configuration pins. This Etch-a-Sketch design only uses the display SPI pins, so the unused TFT pads are intentionally left unconnected.
