#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

/*
 * CORE-only board profile: Espressif ESP32-S3-DevKitC-1 N16R8 v1.0.
 *
 * The board revision is USER-CONFIRMED (2026-11-19), not measured by this
 * repository. If the physical unit is a clone/compatible board, record the
 * Q08=B deviation and do not claim it is an official Espressif board.
 *
 * Onboard RGB:
 *   v1.0 = GPIO48
 *   v1.1 = GPIO38
 * This project uses the v1.0 board, so PIN_STATUS_RGB is 48. Do not use the
 * v1.1 default.
 *
 * Avoid: GPIO0/3/45/46 (strapping), GPIO19/20 (native USB),
 * GPIO26-37 (flash/PSRAM on N16R8), GPIO43/44 (UART0 console).
 */

#define BOARD_PROFILE "esp32s3_devkitc1_v1.0"
#define BOARD_DEVKITC1_REV 10
#define BOARD_REVISION_VERIFIED 1
#define BOARD_REVISION_SOURCE "user-confirmed"

/* CORE-only external interface. No OLED, RTC, or external RGB. */
#define PIN_RELAY_CTRL 4
#define PIN_RELAY_FEEDBACK 11
#define PIN_BUTTON 5
#define PIN_PZEM_TX 17
#define PIN_PZEM_RX 18

/* Onboard WS2812 of the DevKitC-1 v1.0. Not a carrier net. */
#define PIN_STATUS_RGB 48

/* Time service: UTC internally, Asia/Jakarta for display. */
#define TIME_MAX_AGE_SECONDS (12 * 3600)
#define TIME_SNTP_RESYNC_SECONDS (6 * 3600)
#define TIME_DEFAULT_TIMEZONE "Asia/Jakarta"
#define TIME_SNTP_SERVER_1 "pool.ntp.org"
#define TIME_SNTP_SERVER_2 "time.google.com"

/* No temperature sensor is installed. Thermal protection is hardware only
 * (fuse + one-shot thermal cutoff). Do not define a temperature GPIO. */

/*
 * Relay module: common 2-channel 5 V optocoupler module, OFF-BOARD.
 * Assumed ACTIVE-LOW inputs: the carrier MOSFET pulls IN1/IN2 low to turn ON.
 * The MOSFET gate is driven by PIN_RELAY_CTRL with an external 100k pulldown,
 * so the module is OFF at reset/boot. Verify the actual module before use.
 */
#define RELAY_MODULE_CHANNELS 2
#define RELAY_MODULE_ACTIVE_LOW 1
#define RELAY_MODULE_OFFBOARD 1

#define RELAY_ACTIVE_LEVEL 1
#define RELAY_SAFE_LEVEL 0
#define BUTTON_ACTIVE_LEVEL 0

#endif /* BOARD_CONFIG_H */
