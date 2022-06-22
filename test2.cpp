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
    static tflite::MicroMutableOpResolver<50> s_microOpResolver(errorReporter);

    s_microOpResolver.AddAdd();
    s_microOpResolver.AddAveragePool2D();
    s_microOpResolver.AddBatchToSpaceNd();
    s_microOpResolver.AddCast();
    s_microOpResolver.AddConcatenation();
    s_microOpResolver.AddConv2D();
    s_microOpResolver.AddDepthwiseConv2D();
    s_microOpResolver.AddDequantize();
    s_microOpResolver.AddExp();
    s_microOpResolver.AddExpandDims();
    s_microOpResolver.AddFill();
    s_microOpResolver.AddFloorMod();
    s_microOpResolver.AddFullyConnected();
    s_microOpResolver.AddGather();
    s_microOpResolver.AddGreaterEqual();
    s_microOpResolver.AddLeakyRelu();
    s_microOpResolver.AddLess();
    s_microOpResolver.AddLog();
    s_microOpResolver.AddLogistic();
    s_microOpResolver.AddMaximum();
    s_microOpResolver.AddMaxPool2D();
    s_microOpResolver.AddMean();
    s_microOpResolver.AddMul();
    s_microOpResolver.AddNotEqual();
    s_microOpResolver.AddPack();
    s_microOpResolver.AddPad();
    s_microOpResolver.AddReduceMax();
    s_microOpResolver.AddReshape();
    s_microOpResolver.AddResizeNearestNeighbor();
    s_microOpResolver.AddRound();
    s_microOpResolver.AddRsqrt();
    s_microOpResolver.AddShape();
    s_microOpResolver.AddSlice();
    s_microOpResolver.AddSoftmax();
    s_microOpResolver.AddSpaceToBatchNd();
    s_microOpResolver.AddSplit();
    s_microOpResolver.AddSqueeze();
    s_microOpResolver.AddStridedSlice();
    s_microOpResolver.AddSub();
    s_microOpResolver.AddTanh();
    s_microOpResolver.AddTransposeConv();
    s_microOpResolver.AddTranspose();
		1
    return s_microOpResolver;
}
