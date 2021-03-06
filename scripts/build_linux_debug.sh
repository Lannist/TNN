#!/bin/bash

SHARED_LIB="ON"
ARM="ON"
OPENMP="ON"
DEBUG="ON"
OPENCL="OFF"
QUANTIZATION="OFF"
CC=gcc
CXX=g++

mkdir build_linux_debug
cd build_linux_debug
if [ -z $TNN_ROOT_PATH ]
then
      TNN_ROOT_PATH=../..
fi

cmake ${TNN_ROOT_PATH} \
    -DCMAKE_SYSTEM_NAME=Linux  \
    -DTNN_TEST_ENABLE=ON \
    -DTNN_CPU_ENABLE=ON \
    -DDEBUG=$DEBUG \
    -DCMAKE_C_COMPILER=$CC \
    -DCMAKE_CXX_COMPILER=$CXX \
    -DCMAKE_BUILD_TYPE=Release \
    -DTNN_ARM_ENABLE:BOOL=$ARM \
    -DTNN_OPENMP_ENABLE:BOOL=$OPENMP \
    -DTNN_OPENCL_ENABLE:BOOL=$OPENCL \
    -DTNN_QUANTIZATION_ENABLE:BOOL=$QUANTIZATION \
    -DTNN_UNIT_TEST_ENABLE=ON \
    -DTNN_BUILD_SHARED:BOOL=$SHARED_LIB


make -j8
