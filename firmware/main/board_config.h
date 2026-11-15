#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

/*
 * PROVISIONAL board profile for Espressif ESP32-S3-DevKitC-1 N16R8.
 * Revision is NOT verified. Do not treat these GPIO numbers as final until
 * the physical board is photographed and its revision is confirmed.
 *
 * Avoid: GPIO0/3/45/46 (strapping), GPIO19/20 (native USB),
 * GPIO26-37 (flash/PSRAM on N16R8), GPIO43/44 (UART0 console).
 */

#define BOARD_PROFILE "esp32s3_devkitc1_v1.1_provisional"
#define BOARD_REVISION_VERIFIED 0

#define PIN_RELAY_CTRL 4
#define PIN_RELAY_FEEDBACK 11
#define PIN_BUTTON 5
#define PIN_I2C_SDA 8
#define PIN_I2C_SCL 9
#define PIN_OLED_RESET 6
#define PIN_RGB_DATA 10
#define PIN_PZEM_TX 17
#define PIN_PZEM_RX 18
#define PIN_RTC_INT 7

/* No temperature sensor is installed in REV_B. Thermal protection is hardware
 * only (fuse + one-shot thermal cutoff). Do not define a temperature GPIO. */

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
