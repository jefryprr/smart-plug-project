#ifndef SMARTPLUG_CORE_H
#define SMARTPLUG_CORE_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define SP_DEVICE_ID_MAX 32
#define SP_COMMAND_ID_MAX 40
#define SP_FAULT_CODE_MAX 24
#define SP_REASON_MAX 96

typedef enum {
    SP_OUTPUT_OFF = 0,
    SP_OUTPUT_ON = 1
} sp_output_t;

typedef enum {
    SP_MODE_BOOT_SAFE = 0,
    SP_MODE_PROVISIONING,
    SP_MODE_READY_OFF,
    SP_MODE_READY_ON,
    SP_MODE_WARNING,
    SP_MODE_FAULT_LOCKOUT,
    SP_MODE_UPDATING,
    SP_MODE_DEGRADED
} sp_mode_t;

typedef enum {
    SP_SRC_PHYSICAL_BUTTON = 0,
    SP_SRC_LOCAL_API,
    SP_SRC_CLOUD_API,
    SP_SRC_SCHEDULE,
    SP_SRC_AUTOMATION,
    SP_SRC_EMERGENCY
} sp_source_t;

typedef enum {
    SP_REQ_ON = 0,
    SP_REQ_OFF,
    SP_REQ_TOGGLE
} sp_request_t;

typedef enum {
    SP_QUALITY_VALID = 0,
    SP_QUALITY_STALE,
    SP_QUALITY_INVALID
} sp_quality_t;

typedef enum {
    SP_TIME_SOURCE_NONE = 0,
    SP_TIME_SOURCE_SNTP,
    SP_TIME_SOURCE_API,
    SP_TIME_SOURCE_MQTT,
    SP_TIME_SOURCE_MANUAL
} sp_time_source_t;

#define SP_TIME_MAX_AGE_MS (12LL * 60LL * 60LL * 1000LL)
#define SP_TIME_TIMEZONE_MAX 32

typedef struct {
    bool valid;
    sp_time_source_t source;
    int64_t last_sync_ms;
    int64_t last_known_utc_ms;
    char timezone[SP_TIME_TIMEZONE_MAX];
} sp_time_status_t;

typedef struct {
    char device_id[SP_DEVICE_ID_MAX];
    sp_mode_t mode;
    sp_output_t commanded_output;
    bool observed_output_valid;
    sp_output_t observed_output;
    bool lockout;
    char fault_code[SP_FAULT_CODE_MAX];
    bool clock_valid; /* derived from time.valid; kept for compatibility */
    sp_time_status_t time;
    bool meter_valid;
    bool temperature_valid;
    bool temperature_required;
    uint32_t last_command_sequence;
    char last_command_id[SP_COMMAND_ID_MAX];
    uint32_t state_version;
    int64_t last_transition_ms;
} sp_state_t;

typedef struct {
    char command_id[SP_COMMAND_ID_MAX];
    char device_id[SP_DEVICE_ID_MAX];
    sp_request_t requested_output;
    sp_source_t source;
    int64_t issued_at_ms;
    int64_t expires_at_ms;
    uint32_t sequence;
} sp_command_t;

typedef struct {
    bool accepted;
    sp_output_t resulting_command;
    const char *reason_code;
    const char *reason;
    int priority;
    bool requires_observed_confirmation;
    bool state_changed;
} sp_decision_t;

typedef struct {
    float voltage_v;
    float current_a;
    float active_power_w;
    float energy_kwh_total;
    float power_factor;
    float frequency_hz;
    bool power_factor_valid;
    bool frequency_valid;
    int64_t sampled_at_ms;
    sp_quality_t quality;
} sp_measurement_t;

typedef struct {
    float voltage_min_v;
    float voltage_max_v;
    float current_max_a;
    float active_power_max_w;
    float frequency_min_hz;
    float frequency_max_hz;
} sp_measurement_limits_t;

typedef struct {
    bool valid;
    sp_quality_t quality;
    uint32_t issues;
    uint32_t warnings;
} sp_validation_t;

#define SP_ISSUE_INVALID_TIMESTAMP (1u << 0)
#define SP_ISSUE_METER_INVALID (1u << 1)
#define SP_ISSUE_MISSING_VOLTAGE (1u << 2)
#define SP_ISSUE_MISSING_CURRENT (1u << 3)
#define SP_ISSUE_MISSING_POWER (1u << 4)
#define SP_ISSUE_MISSING_ENERGY (1u << 5)
#define SP_ISSUE_VOLTAGE_RANGE (1u << 6)
#define SP_ISSUE_CURRENT_RANGE (1u << 7)
#define SP_ISSUE_POWER_RANGE (1u << 8)
#define SP_ISSUE_ENERGY_NEGATIVE (1u << 9)
#define SP_ISSUE_PF_RANGE (1u << 10)
#define SP_ISSUE_FREQUENCY_RANGE (1u << 11)

#define SP_WARN_OVERVOLTAGE (1u << 0)
#define SP_WARN_UNDERVOLTAGE (1u << 1)
#define SP_WARN_OVERCURRENT (1u << 2)
#define SP_WARN_HIGH_POWER (1u << 3)
#define SP_WARN_STALE (1u << 4)

typedef struct {
    double energy_kwh_total;
    int64_t sampled_at_ms;
    uint32_t sequence;
    sp_quality_t quality;
} sp_energy_reading_t;

typedef struct {
    double delta_kwh;
    bool gap;
    bool reset_detected;
    const char *reason_code;
} sp_energy_delta_t;

typedef struct {
    uint8_t days_mask; /* bit 0 = Sunday ... bit 6 = Saturday */
    uint8_t start_hour;
    uint8_t start_minute;
    uint16_t duration_minutes;
    sp_output_t action;
    bool enabled;
} sp_weekly_schedule_t;

typedef struct {
    bool due;
    sp_output_t action;
    const char *reason_code;
} sp_schedule_result_t;

void sp_state_init(sp_state_t *state, const char *device_id, int64_t now_ms);
void sp_copy_string(char *dst, size_t dst_size, const char *src);
int sp_command_priority(sp_source_t source);
bool sp_is_automatic_source(sp_source_t source);

void sp_decide_command(const sp_state_t *state,
                       const sp_command_t *command,
                       int64_t now_ms,
                       int64_t max_clock_skew_ms,
                       sp_decision_t *decision);

void sp_apply_decision(sp_state_t *state,
                       const sp_command_t *command,
                       const sp_decision_t *decision,
                       int64_t now_ms);

bool sp_validate_measurement(const sp_measurement_t *measurement,
                             const sp_measurement_limits_t *limits,
                             sp_validation_t *validation);

bool sp_energy_delta(const sp_energy_reading_t *previous,
                     const sp_energy_reading_t *current,
                     double max_delta_kwh,
                     int64_t max_gap_ms,
                     sp_energy_delta_t *delta);

bool sp_schedule_due(const sp_weekly_schedule_t *schedule,
                     int weekday,
                     int hour,
                     int minute,
                     int32_t last_run_date,
                     int32_t today_date,
                     bool time_valid,
                     sp_schedule_result_t *result);

void sp_time_set(sp_state_t *state, sp_time_source_t source, int64_t utc_ms,
                 int64_t now_ms, const char *timezone);
void sp_time_invalidate(sp_state_t *state, int64_t now_ms);
bool sp_time_is_valid_for_schedule(const sp_state_t *state, int64_t now_ms);
const char *sp_time_source_name(sp_time_source_t source);

uint16_t sp_crc16_modbus(const uint8_t *data, size_t length);

/* Format a compact telemetry JSON object. Non-finite values become null.
 * Returns the number of bytes that would have been written (snprintf style). */
int sp_format_telemetry(const sp_measurement_t *measurement,
                        const sp_state_t *state,
                        char *buffer,
                        size_t buffer_size);

const char *sp_mode_name(sp_mode_t mode);
const char *sp_output_name(sp_output_t output);
const char *sp_source_name(sp_source_t source);

#ifdef __cplusplus
}
#endif

#endif /* SMARTPLUG_CORE_H */
