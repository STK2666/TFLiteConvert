/*
 * Copyright 2021 NXP
 * All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include "tensorflow/lite/micro/kernels/micro_ops.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"

tflite::MicroOpResolver &MODEL_GetOpsResolver(tflite::ErrorReporter* errorReporter)
{
    static tflite::MicroMutableOpResolver<21> s_microOpResolver(errorReporter);

    s_microOpResolver.AddAdd();
    s_microOpResolver.AddBatchToSpaceNd();
    s_microOpResolver.AddConcatenation();
    s_microOpResolver.AddConv2D();
    s_microOpResolver.AddDequantize();
    s_microOpResolver.AddExpandDims();
    s_microOpResolver.AddFloorMod();
    s_microOpResolver.AddLeakyRelu();
    s_microOpResolver.AddMul();
    s_microOpResolver.AddPack();
    s_microOpResolver.AddPad();
    s_microOpResolver.AddShape();
    s_microOpResolver.AddSlice();
    s_microOpResolver.AddSpaceToBatchNd();
    s_microOpResolver.AddSplit();
    s_microOpResolver.AddSqueeze();
    s_microOpResolver.AddStridedSlice();
    s_microOpResolver.AddSub();
    s_microOpResolver.AddTanh();
    s_microOpResolver.AddTransposeConv();
    s_microOpResolver.AddTranspose();

    return s_microOpResolver;
}
