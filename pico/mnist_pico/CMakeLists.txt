cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

set(PICO_BOARD pico CACHE STRING "Board type")

include(pico_sdk_import.cmake)

project(mnist_pico C CXX ASM)

pico_sdk_init()

# Disable CMSIS-NN because we are using the
# standard TensorFlow Lite Micro reference kernels.
set(TFLM_OPTIMIZED_KERNELS OFF CACHE BOOL "" FORCE)

# TensorFlow Lite Micro
set(TFLMICRO_DIR
    ${CMAKE_CURRENT_LIST_DIR}/../../pico-tflmicro
)

add_subdirectory(
    ${TFLMICRO_DIR}
    ${CMAKE_BINARY_DIR}/tflmicro
)

# MNIST Pico firmware
add_executable(mnist_pico
    main.cpp
    model_data.cc
)

target_include_directories(mnist_pico PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(mnist_pico
    pico_stdlib
    pico-tflmicro
)

pico_enable_stdio_usb(mnist_pico 1)
pico_enable_stdio_uart(mnist_pico 0)
add_custom_command(
    TARGET mnist_pico POST_BUILD
    COMMAND ${CMAKE_OBJCOPY}
            -O binary
            $<TARGET_FILE:mnist_pico>
            ${CMAKE_CURRENT_BINARY_DIR}/mnist_pico.bin
    COMMAND ${CMAKE_COMMAND}
            -E echo "ELF and BIN generated"
)
# We only need the ELF for Wokwi.
# Do not generate extra outputs that invoke picotool.