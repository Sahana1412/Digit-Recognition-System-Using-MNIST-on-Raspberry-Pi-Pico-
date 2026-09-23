#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "pico/stdlib.h"

#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"

#include "model_data.h"


// ============================================================
// Tensor arena
// ============================================================

constexpr int kTensorArenaSize = 120 * 1024;

alignas(16) static uint8_t tensor_arena[kTensorArenaSize];

static tflite::MicroInterpreter* interpreter_ptr = nullptr;


// ============================================================
// Image buffer
// 28 x 28 = 784 INT8 pixels
// ============================================================

static int8_t image[28 * 28];


// ============================================================
// Run inference
// ============================================================

void run_inference()
{
    TfLiteTensor* input = interpreter_ptr->input(0);

    // Copy the complete 28x28 image into the model input
    for (int i = 0; i < 28 * 28; i++) {
        input->data.int8[i] = image[i];
    }

    // Measure inference time
    uint64_t start_time = time_us_64();

    TfLiteStatus status = interpreter_ptr->Invoke();

    uint64_t end_time = time_us_64();

    if (status != kTfLiteOk) {
        printf("ERROR: Inference failed\n");
        printf("READY\n");
        return;
    }

    // Get output tensor
    TfLiteTensor* output = interpreter_ptr->output(0);

    // Find class with highest INT8 output value
    int predicted_digit = 0;

    int8_t highest_value = output->data.int8[0];

    for (int i = 1; i < 10; i++) {

        if (output->data.int8[i] > highest_value) {
            highest_value = output->data.int8[i];
            predicted_digit = i;
        }
    }


    // ========================================================
    // Send result to Python
    // ========================================================

    printf("PREDICTION:%d\n", predicted_digit);

    printf(
        "LATENCY_US:%llu\n",
        (unsigned long long)(end_time - start_time)
    );


    // Send all 10 output values
    printf("OUTPUT:");

    for (int i = 0; i < 10; i++) {

        printf("%d", output->data.int8[i]);

        if (i < 9) {
            printf(",");
        }
    }

    printf("\n");

    printf("READY\n");
}


// ============================================================
// Parse one row of 28 INT8 values
// ============================================================

bool parse_row(char* buffer, int row_number)
{
    int count = 0;

    char* ptr = buffer;

    while (*ptr != '\0' && count < 28) {

        // Skip spaces and tabs
        while (*ptr == ' ' || *ptr == '\t') {
            ptr++;
        }

        // End of string
        if (*ptr == '\0') {
            break;
        }

        int value = 0;
        int sign = 1;

        // Negative number
        if (*ptr == '-') {
            sign = -1;
            ptr++;
        }

        // Must contain a digit
        if (*ptr < '0' || *ptr > '9') {
            return false;
        }

        // Read number
        while (*ptr >= '0' && *ptr <= '9') {

            value = value * 10 + (*ptr - '0');

            ptr++;
        }

        value *= sign;


        // Clamp to INT8 range
        if (value < -128) {
            value = -128;
        }

        if (value > 127) {
            value = 127;
        }


        // Store pixel
        image[row_number * 28 + count] = (int8_t)value;

        count++;
    }


    // Exactly 28 pixels required
    return count == 28;
}


// ============================================================
// Main
// ============================================================

int main()
{
    stdio_init_all();

    // Give USB serial time to initialize
    sleep_ms(2000);


    // ========================================================
    // Startup message
    // ========================================================

    printf("\n");

    printf("=====================================\n");
    printf("   MNIST INT8 - Raspberry Pi Pico\n");
    printf("=====================================\n");


    // ========================================================
    // Load model
    // ========================================================

    const tflite::Model* model =
        tflite::GetModel(g_model);


    if (model->version() != TFLITE_SCHEMA_VERSION) {

        printf("ERROR: Model schema mismatch!\n");

        return 1;
    }


    printf("Model loaded successfully.\n");


    // ========================================================
    // Register required TensorFlow Lite Micro operators
    // ========================================================

    static tflite::MicroMutableOpResolver<10> resolver;

    resolver.AddConv2D();
    resolver.AddMaxPool2D();
    resolver.AddShape();
    resolver.AddStridedSlice();
    resolver.AddPack();
    resolver.AddReshape();
    resolver.AddFullyConnected();
    resolver.AddSoftmax();


    // ========================================================
    // Create interpreter
    // ========================================================

    static tflite::MicroInterpreter interpreter(
        model,
        resolver,
        tensor_arena,
        kTensorArenaSize
    );

    interpreter_ptr = &interpreter;


    // ========================================================
    // Allocate tensors
    // ========================================================

    TfLiteStatus allocate_status =
        interpreter.AllocateTensors();


    if (allocate_status != kTfLiteOk) {

        printf("ERROR: Tensor allocation failed!\n");

        return 1;
    }


    printf("Tensor allocation successful.\n");


    // ========================================================
    // Print input information
    // ========================================================

    TfLiteTensor* input = interpreter.input(0);


    printf("Input type: %d\n", input->type);


    printf("Input dimensions: ");

    for (int i = 0; i < input->dims->size; i++) {

        printf("%d ", input->dims->data[i]);
    }

    printf("\n");


    printf(
        "Input scale: %f\n",
        input->params.scale
    );


    printf(
        "Input zero point: %d\n",
        input->params.zero_point
    );


    // ========================================================
    // Ready
    // ========================================================

    printf("\n");

    printf("READY\n");

    printf("Send PING to synchronize.\n");

    printf("Then send 28 rows of 28 INT8 pixel values.\n");

    printf("Pixel range: -128 to 127\n");

    printf("=====================================\n");


    // ========================================================
    // Serial receive loop
    // ========================================================

    while (true) {

        // Wait until USB serial is connected
        if (!stdio_usb_connected()) {

            sleep_ms(10);

            continue;
        }


        // ----------------------------------------------------
        // Wait for first character
        // ----------------------------------------------------

        int first_char =
            getchar_timeout_us(1000000);


        if (first_char == PICO_ERROR_TIMEOUT) {

            continue;
        }


        // ----------------------------------------------------
        // Receive one complete line
        // ----------------------------------------------------

        char buffer[200];

        int pos = 0;


        buffer[pos++] = (char)first_char;


        while (pos < 199) {

            int c =
                getchar_timeout_us(1000000);


            if (c == PICO_ERROR_TIMEOUT) {

                break;
            }


            if (c == '\n' || c == '\r') {

                break;
            }


            buffer[pos++] = (char)c;
        }


        buffer[pos] = '\0';


        // ----------------------------------------------------
        // PING handshake
        // ----------------------------------------------------

        if (strcmp(buffer, "PING") == 0) {

            printf("READY\n");

            continue;
        }


        // ----------------------------------------------------
        // Check for ROW command
        //
        // Expected:
        //
        // ROW 0 <28 values>
        //
        // ROW 1 <28 values>
        //
        // ...
        //
        // ROW 27 <28 values>
        // ----------------------------------------------------

        if (strncmp(buffer, "ROW ", 4) == 0) {

            char* ptr = buffer + 4;


            // Read row number
            int row_number = 0;


            while (*ptr >= '0' && *ptr <= '9') {

                row_number =
                    row_number * 10 + (*ptr - '0');

                ptr++;
            }


            // Validate row number
            if (row_number < 0 || row_number >= 28) {

                printf("ERROR: Invalid row number\n");

                continue;
            }


            // Skip spaces
            while (*ptr == ' ' || *ptr == '\t') {

                ptr++;
            }


            // Parse 28 pixels
            bool valid =
                parse_row(ptr, row_number);


            if (!valid) {

                printf(
                    "ERROR: Expected 28 pixels for row %d\n",
                    row_number
                );

                continue;
            }


            // Row successfully received
            printf(
                "ACK:%d\n",
                row_number
            );


            // ------------------------------------------------
            // If this is the final row, run inference
            // ------------------------------------------------

            if (row_number == 27) {

                run_inference();
            }


            continue;
        }


        // ----------------------------------------------------
        // Unknown command
        // ----------------------------------------------------

        printf("ERROR: Unknown command\n");
    }


    return 0;
}