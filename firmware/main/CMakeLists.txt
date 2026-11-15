idf_component_register(
    SRCS "app_main.c"
    INCLUDE_DIRS "."
    REQUIRES smartplug_core esp_driver_gpio nvs_flash esp_timer
)
