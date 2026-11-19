#ifndef STATUS_RGB_H
#define STATUS_RGB_H

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    STATUS_RGB_BOOT = 0,
    STATUS_RGB_WIFI_CONNECTING,
    STATUS_RGB_TIME_INVALID,
    STATUS_RGB_NORMAL,
    STATUS_RGB_FAULT
} status_rgb_pattern_t;

void status_rgb_init(void);
void status_rgb_set(status_rgb_pattern_t pattern);

#ifdef __cplusplus
}
#endif

#endif /* STATUS_RGB_H */
