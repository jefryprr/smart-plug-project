idf_component_register(
    SRCS "app_main.c"
    INCLUDE_DIRS "." "../../core/include"
    REQUIRES smartplug_core driver nvs_flash esp_timer
)
