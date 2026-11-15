#include "smartplug_core.h"

#include <math.h>
#include <stdio.h>
#include <string.h>

static const char *const REASON_MALFORMED = "command_id/device_id tidak valid";
static const char *const REASON_WRONG_DEVICE = "perintah untuk perangkat lain";
static const char *const REASON_REPLAY = "command_id sudah pernah diproses";
static const char *const REASON_STALE_SEQ = "sequence tidak lebih baru";
static const char *const REASON_EXPIRED = "perintah kedaluwarsa";
static const char *const REASON_FUTURE = "issued_at di masa depan";
static const char *const REASON_INVALID_TTL = "TTL tidak valid";
static const char *const REASON_LOCKOUT = "lockout aktif";
static const char *const REASON_FAULT = "fault aktif";
static const char *const REASON_MODE = "mode memblokir ON";
static const char *const REASON_METER = "metering tidak valid";
static const char *const REASON_TEMP = "sensor suhu tidak valid";
static const char *const REASON_CLOCK = "jam tidak valid untuk ON otomatis";
static const char *const REASON_OFF_OK = "perintah OFF diizinkan";
static const char *const REASON_ON_OK = "semua interlock yang tersedia lolos";
static const char *const REASON_ALREADY_OFF = "output sudah commanded OFF";
static const char *const REASON_ALREADY_ON = "output sudah commanded ON";

void sp_copy_string(char *dst, size_t dst_size, const char *src) {
    if (dst == NULL || dst_size == 0) {
        return;
    }
    if (src == NULL) {
        dst[0] = '\0';
        return;
    }
    size_t length = strlen(src);
    if (length >= dst_size) {
        length = dst_size - 1;
    }
    memcpy(dst, src, length);
    dst[length] = '\0';
}

void sp_state_init(sp_state_t *state, const char *device_id, int64_t now_ms) {
    if (state == NULL) {
        return;
    }
    memset(state, 0, sizeof(*state));
    sp_copy_string(state->device_id, sizeof(state->device_id), device_id);
    state->mode = SP_MODE_BOOT_SAFE;
    state->commanded_output = SP_OUTPUT_OFF;
    state->observed_output_valid = false;
    state->observed_output = SP_OUTPUT_OFF;
    state->lockout = false;
    state->fault_code[0] = '\0';
    state->clock_valid = false;
    state->meter_valid = false;
    state->temperature_valid = false;
    state->last_command_sequence = 0;
    state->last_command_id[0] = '\0';
    state->state_version = 0;
    state->last_transition_ms = now_ms;
}

int sp_command_priority(sp_source_t source) {
    switch (source) {
        case SP_SRC_EMERGENCY:
            return 900;
        case SP_SRC_PHYSICAL_BUTTON:
            return 600;
        case SP_SRC_LOCAL_API:
            return 550;
        case SP_SRC_CLOUD_API:
            return 500;
        case SP_SRC_SCHEDULE:
            return 400;
        case SP_SRC_AUTOMATION:
            return 300;
        default:
            return 0;
    }
}

bool sp_is_automatic_source(sp_source_t source) {
    return source == SP_SRC_SCHEDULE || source == SP_SRC_AUTOMATION;
}

static sp_output_t resolve_requested(const sp_state_t *state, sp_request_t requested) {
    if (requested == SP_REQ_TOGGLE) {
        return state->commanded_output == SP_OUTPUT_ON ? SP_OUTPUT_OFF : SP_OUTPUT_ON;
    }
    return requested == SP_REQ_ON ? SP_OUTPUT_ON : SP_OUTPUT_OFF;
}

static void reject(sp_decision_t *decision, const sp_state_t *state, sp_source_t source,
                   const char *code, const char *reason) {
    decision->accepted = false;
    decision->resulting_command = state->commanded_output;
    decision->reason_code = code;
    decision->reason = reason;
    decision->priority = sp_command_priority(source);
    decision->requires_observed_confirmation = false;
    decision->state_changed = false;
}

void sp_decide_command(const sp_state_t *state,
                       const sp_command_t *command,
                       int64_t now_ms,
                       int64_t max_clock_skew_ms,
                       sp_decision_t *decision) {
    if (state == NULL || command == NULL || decision == NULL) {
        return;
    }
    memset(decision, 0, sizeof(*decision));
    decision->resulting_command = state->commanded_output;
    decision->priority = sp_command_priority(command->source);

    if (command->command_id[0] == '\0' || command->device_id[0] == '\0') {
        reject(decision, state, command->source, "MALFORMED_COMMAND", REASON_MALFORMED);
        return;
    }
    if (strncmp(command->device_id, state->device_id, SP_DEVICE_ID_MAX) != 0) {
        reject(decision, state, command->source, "WRONG_DEVICE", REASON_WRONG_DEVICE);
        return;
    }
    if (state->last_command_id[0] != '\0' &&
        strncmp(command->command_id, state->last_command_id, SP_COMMAND_ID_MAX) == 0) {
        reject(decision, state, command->source, "REPLAY_DETECTED", REASON_REPLAY);
        return;
    }
    if (command->sequence <= state->last_command_sequence) {
        reject(decision, state, command->source, "STALE_SEQUENCE", REASON_STALE_SEQ);
        return;
    }
    if (command->expires_at_ms <= now_ms) {
        reject(decision, state, command->source, "COMMAND_EXPIRED", REASON_EXPIRED);
        return;
    }
    if (command->issued_at_ms > now_ms + max_clock_skew_ms) {
        reject(decision, state, command->source, "COMMAND_FROM_FUTURE", REASON_FUTURE);
        return;
    }
    if (command->expires_at_ms <= command->issued_at_ms) {
        reject(decision, state, command->source, "INVALID_TTL", REASON_INVALID_TTL);
        return;
    }

    sp_output_t requested = resolve_requested(state, command->requested_output);

    if (requested == SP_OUTPUT_OFF) {
        if (state->commanded_output == SP_OUTPUT_OFF) {
            decision->accepted = true;
            decision->resulting_command = SP_OUTPUT_OFF;
            decision->reason_code = "ALREADY_OFF";
            decision->reason = REASON_ALREADY_OFF;
            decision->requires_observed_confirmation = false;
            decision->state_changed = false;
            return;
        }
        decision->accepted = true;
        decision->resulting_command = SP_OUTPUT_OFF;
        decision->reason_code = "OFF_ACCEPTED";
        decision->reason = REASON_OFF_OK;
        decision->requires_observed_confirmation = true;
        decision->state_changed = true;
        return;
    }

    if (state->lockout || state->mode == SP_MODE_FAULT_LOCKOUT) {
        reject(decision, state, command->source, "LOCKOUT_ACTIVE", REASON_LOCKOUT);
        return;
    }
    if (state->fault_code[0] != '\0') {
        reject(decision, state, command->source, "HARD_FAULT_ACTIVE", REASON_FAULT);
        return;
    }
    if (state->mode == SP_MODE_BOOT_SAFE || state->mode == SP_MODE_PROVISIONING ||
        state->mode == SP_MODE_UPDATING) {
        reject(decision, state, command->source, "MODE_BLOCKS_ON", REASON_MODE);
        return;
    }
    if (!state->meter_valid) {
        reject(decision, state, command->source, "METER_INVALID", REASON_METER);
        return;
    }
    if (!state->temperature_valid) {
        reject(decision, state, command->source, "TEMPERATURE_INVALID", REASON_TEMP);
        return;
    }
    if (state->mode == SP_MODE_DEGRADED) {
        reject(decision, state, command->source, "DEGRADED_MODE_BLOCKS_ON", REASON_MODE);
        return;
    }
    if (sp_is_automatic_source(command->source) && !state->clock_valid) {
        reject(decision, state, command->source, "CLOCK_INVALID", REASON_CLOCK);
        return;
    }
    if (state->mode != SP_MODE_READY_OFF && state->mode != SP_MODE_READY_ON &&
        state->mode != SP_MODE_WARNING) {
        reject(decision, state, command->source, "MODE_BLOCKS_ON", REASON_MODE);
        return;
    }
    if (state->commanded_output == SP_OUTPUT_ON) {
        decision->accepted = true;
        decision->resulting_command = SP_OUTPUT_ON;
        decision->reason_code = "ALREADY_ON";
        decision->reason = REASON_ALREADY_ON;
        decision->requires_observed_confirmation =
            !(state->observed_output_valid && state->observed_output == SP_OUTPUT_ON);
        decision->state_changed = false;
        return;
    }

    decision->accepted = true;
    decision->resulting_command = SP_OUTPUT_ON;
    decision->reason_code = "ON_ACCEPTED";
    decision->reason = REASON_ON_OK;
    decision->requires_observed_confirmation = true;
    decision->state_changed = true;
}

void sp_apply_decision(sp_state_t *state,
                       const sp_command_t *command,
                       const sp_decision_t *decision,
                       int64_t now_ms) {
    if (state == NULL || command == NULL || decision == NULL || !decision->accepted) {
        return;
    }
    sp_copy_string(state->last_command_id, sizeof(state->last_command_id), command->command_id);
    state->last_command_sequence = command->sequence;
    if (decision->state_changed && decision->resulting_command != state->commanded_output) {
        state->commanded_output = decision->resulting_command;
        state->state_version += 1;
        state->last_transition_ms = now_ms;
        state->mode = decision->resulting_command == SP_OUTPUT_ON ? SP_MODE_READY_ON : SP_MODE_READY_OFF;
    }
}

static bool finite_float(float value) {
    return isfinite((double)value) ? true : false;
}

static void apply_warning(uint32_t *warnings, uint32_t warning) {
    *warnings |= warning;
}

bool sp_validate_measurement(const sp_measurement_t *measurement,
                             const sp_measurement_limits_t *limits,
                             sp_validation_t *validation) {
    if (measurement == NULL || limits == NULL || validation == NULL) {
        return false;
    }
    memset(validation, 0, sizeof(*validation));
    validation->quality = SP_QUALITY_INVALID;

    if (measurement->sampled_at_ms <= 0) {
        validation->issues |= SP_ISSUE_INVALID_TIMESTAMP;
    }
    if (measurement->quality == SP_QUALITY_INVALID) {
        validation->issues |= SP_ISSUE_METER_INVALID;
    }
    if (measurement->quality == SP_QUALITY_STALE) {
        apply_warning(&validation->warnings, SP_WARN_STALE);
    }

    if (!finite_float(measurement->voltage_v)) {
        validation->issues |= SP_ISSUE_MISSING_VOLTAGE;
    } else if (measurement->voltage_v < limits->voltage_min_v ||
               measurement->voltage_v > limits->voltage_max_v) {
        validation->issues |= SP_ISSUE_VOLTAGE_RANGE;
    } else if (measurement->voltage_v > 253.0f) {
        apply_warning(&validation->warnings, SP_WARN_OVERVOLTAGE);
    } else if (measurement->voltage_v > 0.0f && measurement->voltage_v < 207.0f) {
        apply_warning(&validation->warnings, SP_WARN_UNDERVOLTAGE);
    }

    if (!finite_float(measurement->current_a)) {
        validation->issues |= SP_ISSUE_MISSING_CURRENT;
    } else if (measurement->current_a < 0.0f || measurement->current_a > limits->current_max_a) {
        validation->issues |= SP_ISSUE_CURRENT_RANGE;
    } else if (measurement->current_a > 10.5f) {
        apply_warning(&validation->warnings, SP_WARN_OVERCURRENT);
    }

    if (!finite_float(measurement->active_power_w)) {
        validation->issues |= SP_ISSUE_MISSING_POWER;
    } else if (measurement->active_power_w < 0.0f ||
               measurement->active_power_w > limits->active_power_max_w) {
        validation->issues |= SP_ISSUE_POWER_RANGE;
    } else if (measurement->active_power_w > 2300.0f) {
        apply_warning(&validation->warnings, SP_WARN_HIGH_POWER);
    }

    if (!finite_float(measurement->energy_kwh_total)) {
        validation->issues |= SP_ISSUE_MISSING_ENERGY;
    } else if (measurement->energy_kwh_total < 0.0f) {
        validation->issues |= SP_ISSUE_ENERGY_NEGATIVE;
    }

    if (measurement->power_factor_valid) {
        if (!finite_float(measurement->power_factor) || measurement->power_factor < 0.0f ||
            measurement->power_factor > 1.0f) {
            validation->issues |= SP_ISSUE_PF_RANGE;
        }
    }
    if (measurement->frequency_valid) {
        if (!finite_float(measurement->frequency_hz) ||
            measurement->frequency_hz < limits->frequency_min_hz ||
            measurement->frequency_hz > limits->frequency_max_hz) {
            validation->issues |= SP_ISSUE_FREQUENCY_RANGE;
        }
    }

    validation->valid = validation->issues == 0u;
    validation->quality = validation->valid ? SP_QUALITY_VALID : SP_QUALITY_INVALID;
    return validation->valid;
}

bool sp_energy_delta(const sp_energy_reading_t *previous,
                     const sp_energy_reading_t *current,
                     double max_delta_kwh,
                     int64_t max_gap_ms,
                     sp_energy_delta_t *delta) {
    if (previous == NULL || current == NULL || delta == NULL) {
        return false;
    }
    memset(delta, 0, sizeof(*delta));

    if (previous->quality != SP_QUALITY_VALID || current->quality != SP_QUALITY_VALID) {
        delta->gap = true;
        delta->reason_code = "INVALID_METER_QUALITY";
        return false;
    }
    if (current->sequence <= previous->sequence) {
        delta->gap = true;
        delta->reason_code = "NON_MONOTONIC_SEQUENCE";
        return false;
    }
    if (current->sampled_at_ms < previous->sampled_at_ms) {
        delta->gap = true;
        delta->reason_code = "NON_MONOTONIC_TIME";
        return false;
    }
    if (current->sampled_at_ms - previous->sampled_at_ms > max_gap_ms) {
        delta->gap = true;
        delta->reason_code = "TELEMETRY_GAP_TOO_LARGE";
        return false;
    }
    if (!isfinite(previous->energy_kwh_total) || !isfinite(current->energy_kwh_total) ||
        previous->energy_kwh_total < 0.0 || current->energy_kwh_total < 0.0) {
        delta->gap = true;
        delta->reason_code = "INVALID_ENERGY_VALUE";
        return false;
    }
    if (current->energy_kwh_total < previous->energy_kwh_total) {
        delta->gap = true;
        delta->reset_detected = true;
        delta->reason_code = "COUNTER_RESET_OR_ROLLOVER";
        return false;
    }
    double difference = current->energy_kwh_total - previous->energy_kwh_total;
    if (difference > max_delta_kwh) {
        delta->gap = true;
        delta->reason_code = "IMPLAUSIBLE_DELTA";
        return false;
    }
    delta->delta_kwh = difference;
    delta->gap = false;
    delta->reason_code = "OK";
    return true;
}

bool sp_schedule_due(const sp_weekly_schedule_t *schedule,
                     int weekday,
                     int hour,
                     int minute,
                     int32_t last_run_date,
                     int32_t today_date,
                     sp_schedule_result_t *result) {
    if (schedule == NULL || result == NULL) {
        return false;
    }
    memset(result, 0, sizeof(*result));
    if (!schedule->enabled) {
        result->reason_code = "SCHEDULE_DISABLED";
        return false;
    }
    if (weekday < 0 || weekday > 6 || hour < 0 || hour > 23 || minute < 0 || minute > 59) {
        result->reason_code = "INVALID_TIME";
        return false;
    }
    if ((schedule->days_mask & (uint8_t)(1u << weekday)) == 0u) {
        result->reason_code = "WRONG_WEEKDAY";
        return false;
    }
    if (schedule->duration_minutes == 0u) {
        result->reason_code = "INVALID_DURATION";
        return false;
    }
    if (last_run_date == today_date) {
        result->reason_code = "ALREADY_RAN_TODAY";
        return false;
    }
    int start_minutes = (int)schedule->start_hour * 60 + (int)schedule->start_minute;
    int now_minutes = hour * 60 + minute;
    int end_minutes = start_minutes + (int)schedule->duration_minutes;
    if (now_minutes < start_minutes || now_minutes >= end_minutes) {
        result->reason_code = "OUTSIDE_WINDOW";
        return false;
    }
    result->due = true;
    result->action = schedule->action;
    result->reason_code = "DUE";
    return true;
}

uint16_t sp_crc16_modbus(const uint8_t *data, size_t length) {
    uint16_t crc = 0xFFFFu;
    if (data == NULL) {
        return crc;
    }
    for (size_t index = 0; index < length; ++index) {
        crc ^= (uint16_t)data[index];
        for (int bit = 0; bit < 8; ++bit) {
            if ((crc & 1u) != 0u) {
                crc = (uint16_t)((crc >> 1) ^ 0xA001u);
            } else {
                crc = (uint16_t)(crc >> 1);
            }
        }
    }
    return crc;
}

static void format_float(char *buffer, size_t size, float value, int precision) {
    if (!finite_float(value)) {
        sp_copy_string(buffer, size, "null");
        return;
    }
    (void)snprintf(buffer, size, "%.*f", precision, (double)value);
}

int sp_format_telemetry(const sp_measurement_t *measurement,
                        const sp_state_t *state,
                        char *buffer,
                        size_t buffer_size) {
    if (measurement == NULL || state == NULL || buffer == NULL || buffer_size == 0) {
        return -1;
    }
    char voltage[24];
    char current[24];
    char power[24];
    char energy[24];
    char pf[24];
    char frequency[24];
    format_float(voltage, sizeof(voltage), measurement->voltage_v, 2);
    format_float(current, sizeof(current), measurement->current_a, 3);
    format_float(power, sizeof(power), measurement->active_power_w, 2);
    format_float(energy, sizeof(energy), measurement->energy_kwh_total, 4);
    if (measurement->power_factor_valid) {
        format_float(pf, sizeof(pf), measurement->power_factor, 3);
    } else {
        sp_copy_string(pf, sizeof(pf), "null");
    }
    if (measurement->frequency_valid) {
        format_float(frequency, sizeof(frequency), measurement->frequency_hz, 2);
    } else {
        sp_copy_string(frequency, sizeof(frequency), "null");
    }

    char fault[SP_FAULT_CODE_MAX + 8];
    if (state->fault_code[0] == '\0') {
        sp_copy_string(fault, sizeof(fault), "null");
    } else {
        (void)snprintf(fault, sizeof(fault), "\"%s\"", state->fault_code);
    }

    int written = snprintf(
        buffer,
        buffer_size,
        "{\"schema_version\":1,\"device_id\":\"%s\",\"sampled_at_ms\":%lld,"
        "\"quality\":\"%s\",\"measurements\":{\"voltage_v\":%s,\"current_a\":%s,"
        "\"active_power_w\":%s,\"energy_kwh_total\":%s,\"power_factor\":%s,"
        "\"frequency_hz\":%s},\"state\":{\"mode\":\"%s\",\"commanded_output\":\"%s\","
        "\"observed_output\":%s,\"fault\":%s,\"lockout\":%s,\"state_version\":%u,"
        "\"clock_valid\":%s,\"meter_valid\":%s,\"temperature_valid\":%s}}",
        state->device_id,
        (long long)measurement->sampled_at_ms,
        measurement->quality == SP_QUALITY_VALID ? "VALID" :
            (measurement->quality == SP_QUALITY_STALE ? "STALE" : "INVALID"),
        voltage,
        current,
        power,
        energy,
        pf,
        frequency,
        sp_mode_name(state->mode),
        sp_output_name(state->commanded_output),
        state->observed_output_valid ? (state->observed_output == SP_OUTPUT_ON ? "\"ON\"" : "\"OFF\"") : "null",
        fault,
        state->lockout ? "true" : "false",
        state->state_version,
        state->clock_valid ? "true" : "false",
        state->meter_valid ? "true" : "false",
        state->temperature_valid ? "true" : "false");
    return written;
}

const char *sp_mode_name(sp_mode_t mode) {
    switch (mode) {
        case SP_MODE_BOOT_SAFE: return "BOOT_SAFE";
        case SP_MODE_PROVISIONING: return "PROVISIONING";
        case SP_MODE_READY_OFF: return "READY_OFF";
        case SP_MODE_READY_ON: return "READY_ON";
        case SP_MODE_WARNING: return "WARNING";
        case SP_MODE_FAULT_LOCKOUT: return "FAULT_LOCKOUT";
        case SP_MODE_UPDATING: return "UPDATING";
        case SP_MODE_DEGRADED: return "DEGRADED";
        default: return "UNKNOWN";
    }
}

const char *sp_output_name(sp_output_t output) {
    return output == SP_OUTPUT_ON ? "ON" : "OFF";
}

const char *sp_source_name(sp_source_t source) {
    switch (source) {
        case SP_SRC_PHYSICAL_BUTTON: return "physical_button";
        case SP_SRC_LOCAL_API: return "local_api";
        case SP_SRC_CLOUD_API: return "cloud_api";
        case SP_SRC_SCHEDULE: return "schedule";
        case SP_SRC_AUTOMATION: return "automation";
        case SP_SRC_EMERGENCY: return "emergency";
        default: return "unknown";
    }
}
