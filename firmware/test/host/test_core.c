#include "smartplug_core.h"

#include <math.h>
#include <stdio.h>
#include <string.h>

static int checks = 0;
static int failures = 0;

#define CHECK(condition) do { \
    checks++; \
    if (!(condition)) { \
        failures++; \
        printf("FAIL %s:%d: %s\n", __FILE__, __LINE__, #condition); \
    } \
} while (0)

static const int64_t NOW = 1000000;

static sp_state_t ready_state(void) {
    sp_state_t state;
    sp_state_init(&state, "dev-test-001", NOW);
    state.mode = SP_MODE_READY_OFF;
    state.meter_valid = true;
    state.temperature_valid = true;
    state.temperature_required = true;
    state.clock_valid = true;
    return state;
}

static sp_command_t command(const char *id, sp_request_t request, uint32_t sequence) {
    sp_command_t cmd;
    memset(&cmd, 0, sizeof(cmd));
    sp_copy_string(cmd.command_id, sizeof(cmd.command_id), id);
    sp_copy_string(cmd.device_id, sizeof(cmd.device_id), "dev-test-001");
    cmd.requested_output = request;
    cmd.source = SP_SRC_LOCAL_API;
    cmd.issued_at_ms = NOW - 1000;
    cmd.expires_at_ms = NOW + 30000;
    cmd.sequence = sequence;
    return cmd;
}

static void test_decisions(void) {
    sp_state_t state = ready_state();
    sp_command_t cmd = command("cmd-1", SP_REQ_ON, 1);
    sp_decision_t decision;
    sp_decide_command(&state, &cmd, NOW, 30000, &decision);
    CHECK(decision.accepted);
    CHECK(decision.resulting_command == SP_OUTPUT_ON);
    CHECK(strcmp(decision.reason_code, "ON_ACCEPTED") == 0);
    CHECK(decision.state_changed);
    CHECK(decision.requires_observed_confirmation);

    state = ready_state();
    state.lockout = true;
    state.mode = SP_MODE_FAULT_LOCKOUT;
    sp_copy_string(state.fault_code, sizeof(state.fault_code), "OVERTEMP");
    sp_decide_command(&state, &cmd, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "LOCKOUT_ACTIVE") == 0);

    state = ready_state();
    state.lockout = true;
    state.mode = SP_MODE_FAULT_LOCKOUT;
    state.commanded_output = SP_OUTPUT_ON;
    sp_command_t off = command("cmd-off", SP_REQ_OFF, 2);
    sp_decide_command(&state, &off, NOW, 30000, &decision);
    CHECK(decision.accepted);
    CHECK(decision.resulting_command == SP_OUTPUT_OFF);
    CHECK(strcmp(decision.reason_code, "OFF_ACCEPTED") == 0);

    state = ready_state();
    state.commanded_output = SP_OUTPUT_ON;
    sp_command_t toggle = command("cmd-toggle", SP_REQ_TOGGLE, 3);
    sp_decide_command(&state, &toggle, NOW, 30000, &decision);
    CHECK(decision.accepted);
    CHECK(decision.resulting_command == SP_OUTPUT_OFF);

    state = ready_state();
    state.last_command_id[0] = '\0';
    sp_copy_string(state.last_command_id, sizeof(state.last_command_id), "cmd-1");
    state.last_command_sequence = 1;
    sp_decide_command(&state, &cmd, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "REPLAY_DETECTED") == 0);

    state = ready_state();
    state.last_command_sequence = 5;
    sp_command_t stale = command("cmd-stale", SP_REQ_ON, 5);
    sp_decide_command(&state, &stale, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "STALE_SEQUENCE") == 0);

    state = ready_state();
    sp_command_t wrong = command("cmd-wrong", SP_REQ_ON, 2);
    sp_copy_string(wrong.device_id, sizeof(wrong.device_id), "dev-other");
    sp_decide_command(&state, &wrong, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "WRONG_DEVICE") == 0);

    state = ready_state();
    sp_command_t expired = command("cmd-expired", SP_REQ_ON, 2);
    expired.issued_at_ms = NOW - 60000;
    expired.expires_at_ms = NOW - 1000;
    sp_decide_command(&state, &expired, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "COMMAND_EXPIRED") == 0);

    state = ready_state();
    sp_command_t future = command("cmd-future", SP_REQ_ON, 2);
    future.issued_at_ms = NOW + 60000;
    future.expires_at_ms = NOW + 90000;
    sp_decide_command(&state, &future, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "COMMAND_FROM_FUTURE") == 0);

    state = ready_state();
    state.clock_valid = false;
    sp_command_t schedule = command("cmd-schedule", SP_REQ_ON, 2);
    schedule.source = SP_SRC_SCHEDULE;
    sp_decide_command(&state, &schedule, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "CLOCK_INVALID") == 0);

    state = ready_state();
    state.clock_valid = false;
    sp_command_t button = command("cmd-button", SP_REQ_ON, 3);
    button.source = SP_SRC_PHYSICAL_BUTTON;
    sp_decide_command(&state, &button, NOW, 30000, &decision);
    CHECK(decision.accepted);

    state = ready_state();
    state.mode = SP_MODE_DEGRADED;
    sp_decide_command(&state, &cmd, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "DEGRADED_MODE_BLOCKS_ON") == 0);

    state = ready_state();
    state.meter_valid = false;
    sp_decide_command(&state, &cmd, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "METER_INVALID") == 0);

    state = ready_state();
    state.temperature_valid = false;
    sp_decide_command(&state, &cmd, NOW, 30000, &decision);
    CHECK(!decision.accepted);
    CHECK(strcmp(decision.reason_code, "TEMPERATURE_INVALID") == 0);

    /* REV_B has no temperature sensor: hardware TCO/fuse only. ON is allowed
     * when temperature monitoring is explicitly not required. */
    state = ready_state();
    state.temperature_required = false;
    state.temperature_valid = false;
    sp_decide_command(&state, &cmd, NOW, 30000, &decision);
    CHECK(decision.accepted);

    state = ready_state();
    sp_decide_command(&state, &cmd, NOW, 30000, &decision);
    sp_apply_decision(&state, &cmd, &decision, NOW);
    CHECK(state.commanded_output == SP_OUTPUT_ON);
    CHECK(state.state_version == 1);
    CHECK(strcmp(state.last_command_id, "cmd-1") == 0);
    CHECK(state.last_command_sequence == 1);
}

static void test_measurement(void) {
    sp_measurement_t measurement;
    memset(&measurement, 0, sizeof(measurement));
    measurement.voltage_v = 230.1f;
    measurement.current_a = 0.45f;
    measurement.active_power_w = 92.7f;
    measurement.energy_kwh_total = 15.214f;
    measurement.power_factor = 0.90f;
    measurement.power_factor_valid = true;
    measurement.frequency_hz = 50.0f;
    measurement.frequency_valid = true;
    measurement.sampled_at_ms = NOW;
    measurement.quality = SP_QUALITY_VALID;

    sp_measurement_limits_t limits = {0.0f, 300.0f, 16.0f, 4000.0f, 45.0f, 65.0f};
    sp_validation_t validation;
    CHECK(sp_validate_measurement(&measurement, &limits, &validation));
    CHECK(validation.valid);
    CHECK(validation.issues == 0u);

    measurement.voltage_v = NAN;
    measurement.current_a = NAN;
    CHECK(!sp_validate_measurement(&measurement, &limits, &validation));
    CHECK((validation.issues & SP_ISSUE_MISSING_VOLTAGE) != 0u);
    CHECK((validation.issues & SP_ISSUE_MISSING_CURRENT) != 0u);

    measurement.voltage_v = 260.0f;
    measurement.current_a = 1.0f;
    measurement.active_power_w = 260.0f;
    CHECK(sp_validate_measurement(&measurement, &limits, &validation));
    CHECK((validation.warnings & SP_WARN_OVERVOLTAGE) != 0u);

    measurement.voltage_v = 230.0f;
    measurement.current_a = 40.0f;
    CHECK(!sp_validate_measurement(&measurement, &limits, &validation));
    CHECK((validation.issues & SP_ISSUE_CURRENT_RANGE) != 0u);
}

static void test_energy(void) {
    sp_energy_reading_t previous = {10.0, 1000, 1, SP_QUALITY_VALID};
    sp_energy_reading_t current = {10.5, 2000, 2, SP_QUALITY_VALID};
    sp_energy_delta_t delta;
    CHECK(sp_energy_delta(&previous, &current, 20.0, 60000, &delta));
    CHECK(fabs(delta.delta_kwh - 0.5) < 1e-9);
    CHECK(!delta.gap);

    current.energy_kwh_total = 0.2;
    CHECK(!sp_energy_delta(&previous, &current, 20.0, 60000, &delta));
    CHECK(delta.gap);
    CHECK(delta.reset_detected);
    CHECK(strcmp(delta.reason_code, "COUNTER_RESET_OR_ROLLOVER") == 0);

    current.energy_kwh_total = 10.6;
    current.sequence = 1;
    CHECK(!sp_energy_delta(&previous, &current, 20.0, 60000, &delta));
    CHECK(strcmp(delta.reason_code, "NON_MONOTONIC_SEQUENCE") == 0);

    current.sequence = 2;
    current.sampled_at_ms = 1000 + 120000;
    CHECK(!sp_energy_delta(&previous, &current, 20.0, 60000, &delta));
    CHECK(strcmp(delta.reason_code, "TELEMETRY_GAP_TOO_LARGE") == 0);
}

static void test_schedule(void) {
    sp_weekly_schedule_t schedule;
    memset(&schedule, 0, sizeof(schedule));
    schedule.days_mask = 1u << 0;
    schedule.start_hour = 12;
    schedule.start_minute = 0;
    schedule.duration_minutes = 30;
    schedule.action = SP_OUTPUT_ON;
    schedule.enabled = true;
    sp_schedule_result_t result;
    CHECK(sp_schedule_due(&schedule, 0, 12, 10, -1, 100, &result));
    CHECK(result.due);
    CHECK(result.action == SP_OUTPUT_ON);
    CHECK(strcmp(result.reason_code, "DUE") == 0);

    CHECK(!sp_schedule_due(&schedule, 0, 12, 10, 100, 100, &result));
    CHECK(strcmp(result.reason_code, "ALREADY_RAN_TODAY") == 0);

    CHECK(!sp_schedule_due(&schedule, 1, 12, 10, -1, 100, &result));
    CHECK(strcmp(result.reason_code, "WRONG_WEEKDAY") == 0);

    schedule.enabled = false;
    CHECK(!sp_schedule_due(&schedule, 0, 12, 10, -1, 100, &result));
    CHECK(strcmp(result.reason_code, "SCHEDULE_DISABLED") == 0);
}

static void test_crc_and_json(void) {
    const uint8_t data[] = "123456789";
    CHECK(sp_crc16_modbus(data, 9) == 0x4B37u);

    sp_state_t state = ready_state();
    state.mode = SP_MODE_READY_ON;
    state.commanded_output = SP_OUTPUT_ON;
    state.observed_output_valid = false;
    state.state_version = 7;
    sp_measurement_t measurement;
    memset(&measurement, 0, sizeof(measurement));
    measurement.voltage_v = 230.1f;
    measurement.current_a = 0.45f;
    measurement.active_power_w = 92.7f;
    measurement.energy_kwh_total = 15.214f;
    measurement.power_factor = 0.9f;
    measurement.power_factor_valid = true;
    measurement.frequency_hz = 50.0f;
    measurement.frequency_valid = true;
    measurement.sampled_at_ms = NOW;
    measurement.quality = SP_QUALITY_VALID;

    char buffer[1024];
    int written = sp_format_telemetry(&measurement, &state, buffer, sizeof(buffer));
    CHECK(written > 0);
    CHECK(strstr(buffer, "nan") == NULL);
    CHECK(strstr(buffer, "inf") == NULL);
    CHECK(strstr(buffer, "\"voltage_v\":230.10") != NULL);
    CHECK(strstr(buffer, "\"commanded_output\":\"ON\"") != NULL);
    CHECK(strstr(buffer, "\"observed_output\":null") != NULL);

    measurement.voltage_v = NAN;
    sp_format_telemetry(&measurement, &state, buffer, sizeof(buffer));
    CHECK(strstr(buffer, "\"voltage_v\":null") != NULL);
}

int main(void) {
    test_decisions();
    test_measurement();
    test_energy();
    test_schedule();
    test_crc_and_json();
    printf("%d checks, %d failures\n", checks, failures);
    return failures == 0 ? 0 : 1;
}
