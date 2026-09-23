# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()

set(sdkVersion 2.3.1)
set(toolchainVersion "")
set(picotoolVersion 2.3.1)

set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()

# ====================================================================================
set(PICO_BOARD pico CACHE STRING "Board type")

cmake_minimum_required(VERSION 3.12)

# Pull in PICO SDK (must be before project)
include(pico_sdk_import.cmake)

project(pico-tflmicro C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_library(pico-tflmicro STATIC)
file(GLOB_RECURSE CMSIS_NN_SOURCES
    ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis_nn/Source/*.c
)

target_sources(pico-tflmicro PRIVATE
    ${CMSIS_NN_SOURCES}
)
target_include_directories(pico-tflmicro
  PUBLIC
  ${CMAKE_CURRENT_LIST_DIR}/src/
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/ruy
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/gemmlowp
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/kissfft
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/flatbuffers
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis/CMSIS/Core/Include
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/flatbuffers/include
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis_nn/Include
)

target_compile_definitions(
  pico-tflmicro
  PUBLIC
  COMPILE_DEFINITIONS TF_LITE_DISABLE_X86_NEON=1
  COMPILE_DEFINITIONS TF_LITE_STATIC_MEMORY=1
  COMPILE_DEFINITIONS TF_LITE_USE_CTIME=1
  COMPILE_DEFINITIONS CMSIS_NN=1
  COMPILE_DEFINITIONS ARDUINO=1
  COMPILE_DEFINITIONS TFLITE_USE_CTIME=1
)

set_target_properties(
  pico-tflmicro
  PROPERTIES
  COMPILE_FLAGS -Os
  COMPILE_FLAGS -fno-rtti
  COMPILE_FLAGS -fno-exceptions
  COMPILE_FLAGS -fno-threadsafe-statics
  COMPILE_FLAGS -nostdlib
)

target_link_libraries(
  pico-tflmicro
  pico_stdlib
  pico_multicore
)

target_sources(pico-tflmicro
  PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/delay.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/delay_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/energy.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/energy_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/fft_auto_scale_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/fft_auto_scale_kernel.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/fft_auto_scale_kernel.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/fft_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank_log.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank_log_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank_spectral_subtraction.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank_spectral_subtraction_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank_square_root.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank_square_root.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/filter_bank_square_root_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/framer.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/framer_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/irfft.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/irfft.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/overlap_add.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/overlap_add_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/pcan.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/pcan_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/rfft.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/rfft.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/stacker.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/stacker_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/window.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/micro/kernels/window_flexbuffers_generated_data.h

  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/circular_buffer.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/circular_buffer.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/complex.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/energy.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/energy.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/fft_auto_scale.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/fft_auto_scale.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/filter_bank.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/filter_bank.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/filter_bank_log.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/filter_bank_log.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/filter_bank_spectral_subtraction.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/filter_bank_spectral_subtraction.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/filter_bank_square_root.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/filter_bank_square_root.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/irfft.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/irfft_float.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/irfft_int16.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/irfft_int32.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/kiss_fft_wrappers/kiss_fft_common.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/kiss_fft_wrappers/kiss_fft_float.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/kiss_fft_wrappers/kiss_fft_float.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/kiss_fft_wrappers/kiss_fft_int16.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/kiss_fft_wrappers/kiss_fft_int16.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/kiss_fft_wrappers/kiss_fft_int32.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/kiss_fft_wrappers/kiss_fft_int32.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/log.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/log.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/max_abs.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/max_abs.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/msb.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/msb_32.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/msb_64.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/overlap_add.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/overlap_add.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/pcan_argc_fixed.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/pcan_argc_fixed.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/rfft.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/rfft_float.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/rfft_int16.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/rfft_int32.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/square_root.h
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/square_root_32.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/square_root_64.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/window.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/signal/src/window.h

  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/compiler/mlir/lite/core/api/error_reporter.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/compiler/mlir/lite/core/api/error_reporter.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/compiler/mlir/lite/core/c/builtin_op_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/compiler/mlir/lite/core/c/tflite_types.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/compiler/mlir/lite/kernels/internal/compatibility_macros.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/compiler/mlir/lite/schema/schema_generated.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/compiler/mlir/lite/schema/schema_utils.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/compiler/mlir/lite/schema/schema_utils.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/builtin_op_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/builtin_ops.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/c/builtin_op_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/c/c_api_types.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/c/common.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/context_util.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/api/error_reporter.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/api/flatbuffer_conversions.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/api/flatbuffer_conversions.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/api/tensor_utils.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/api/tensor_utils.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/c/builtin_op_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/c/c_api_types.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/c/common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/c/common.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/core/macros.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/common.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/compatibility.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/cppmath.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/max.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/min.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/optimized/neon_check.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/portable_tensor.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/portable_tensor_utils.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/portable_tensor_utils.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/quantization_util.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/quantization_util.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/add.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/add_n.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/arg_min_max.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/batch_matmul.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/batch_to_space_nd.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/binary_function.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/broadcast_args.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/broadcast_to.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/ceil.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/comparisons.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/comparisons.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/concatenation.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/conv.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/cumsum.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/depth_to_space.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/depthwiseconv_float.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/depthwiseconv_uint8.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/dequantize.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/div.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/elu.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/exp.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/fill.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/floor.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/floor_div.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/floor_mod.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/fully_connected.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/hard_swish.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/add.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/conv.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/depthwise_conv.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/fully_connected.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/l2normalization.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/logistic.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/fully_connected.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/logistic.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/mean.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/mul.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/pooling.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/tanh.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/integer_ops/transpose_conv.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/l2normalization.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/leaky_relu.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/log_softmax.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/logistic.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/lstm_cell.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/maximum_minimum.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/mul.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/neg.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/pad.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/pooling.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/portable_tensor_utils.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/portable_tensor_utils.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/portable_tensor_utils_impl.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/prelu.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/process_broadcast_shapes.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/quantize.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/reduce.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/requantize.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/resize_bilinear.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/resize_nearest_neighbor.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/round.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/select.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/slice.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/softmax.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/space_to_batch_nd.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/space_to_depth.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/strided_slice.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/sub.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/tanh.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/transpose.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/reference/transpose_conv.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/runtime_shape.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/runtime_shape.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/strided_slice_logic.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/tensor_ctypes.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/tensor_ctypes.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/tensor_utils.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/internal/types.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/kernel_util.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/kernel_util.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/op_macros.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/kernels/padding.h

  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/ibuffer_allocator.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/non_persistent_arena_buffer_allocator.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/persistent_arena_buffer_allocator.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/recording_single_arena_buffer_allocator.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/arena_allocator/single_arena_buffer_allocator.h

  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/benchmarks/micro_benchmark.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/compatibility.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/compression.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/debug_log.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/debug_log.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/fake_micro_context.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/fake_micro_context.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/flatbuffer_utils.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/flatbuffer_utils.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/tflite_bridge/flatbuffer_conversions_bridge.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/tflite_bridge/micro_error_reporter.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/hexdump.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/hexdump.h

  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/activation_utils.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/activations.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/activations.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/activations_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/add.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/add_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/add_n.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/arg_min_max.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/assign_variable.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/batch_matmul.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/batch_to_space_nd.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/broadcast_args.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/broadcast_to.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/call_once.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cast.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/ceil.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/circular_buffer.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/circular_buffer.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/circular_buffer_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/circular_buffer_flexbuffers_generated_data.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cmsis_nn/add.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cmsis_nn/batch_matmul.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cmsis_nn/conv.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cmsis_nn/depthwise_conv.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cmsis_nn/fully_connected.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cmsis_nn/mul.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cmsis_nn/pooling.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/cmsis_nn/softmax.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/conv_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/depthwise_conv_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/dequantize.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/fully_connected_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/kernel_runner.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/kernel_util.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/l2_pool_2d.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/l2norm.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/logistic.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/lstm_eval.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/maximum_minimum.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/micro_tensor_utils.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/mirror_pad.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/mul_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/neg.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/pack.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/pad.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/pooling_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/prelu.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/quantize.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/reduce.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/reshape.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/reshape_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/shape.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/resize_bilinear.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/resize_nearest_neighbor.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/round.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/select.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/slice.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/softmax_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/space_to_batch_nd.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/space_to_depth.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/split.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/split_v.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/squared_difference.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/squeeze.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/strided_slice.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/strided_slice_common.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/sub.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/tanh.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/transpose.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/unpack.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/var_handle.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/while.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/kernels/zeros_like.cpp

  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_helpers.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_helpers.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_planner/greedy_memory_planner.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_planner/greedy_memory_planner.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_planner/linear_memory_planner.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_planner/linear_memory_planner.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_planner/memory_plan_struct.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_planner/micro_memory_planner.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_planner/non_persistent_buffer_planner_shim.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/memory_planner/non_persistent_buffer_planner_shim.h

  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_allocation_info.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_allocation_info.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_allocator.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_allocator.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_arena_constants.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_common.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_context.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_context.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_graph.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_interpreter.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_interpreter.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_interpreter_context.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_interpreter_context.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_interpreter_graph.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_interpreter_graph.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_log.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_log.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_mutable_op_resolver.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_op_resolver.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_op_resolver.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_profiler.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_profiler.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_profiler_interface.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_resource_variable.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_resource_variable.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_time.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_time.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_utils.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/micro_utils.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/recording_micro_allocator.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/recording_micro_allocator.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/recording_micro_interpreter.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/span.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/static_vector.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/system_setup.cpp
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/micro/system_setup.h

  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/portable_type_to_tflitetype.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/schema/schema_generated.h
  ${CMAKE_CURRENT_LIST_DIR}/src/tensorflow/lite/schema/schema_utils.h

  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis/CMSIS/Core/Include/cmsis_armclang.h
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis/CMSIS/Core/Include/cmsis_clang.h
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis/CMSIS/Core/Include/cmsis_compiler.h
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis/CMSIS/Core/Include/cmsis_gcc.h
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis/CMSIS/Core/Include/cmsis_version.h
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis/CMSIS/Core/Include/core_cm0.h
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis/CMSIS/Core/Include/core_cm0plus.h

  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis_nn/Include/arm_nnfunctions.h
  ${CMAKE_CURRENT_LIST_DIR}/src/third_party/cmsis_nn/Include/arm_nnsupportfunctions.h
)