# Tencent is pleased to support the open source community by making TNN available.
#
# Copyright (C) 2020 THL A29 Limited, a Tencent company. All rights reserved.
#
# Licensed under the BSD 3-Clause License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSD-3-Clause
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from utils import cmd
from utils import checker
from onnx_converter import onnx2tnn
import os


def hack_name(names: str):
    hacked_names = ""
    name_list = names.split(',')
    for name in name_list:
        if name.endswith(":0"):
            hacked_names = hacked_names + name + ","
        else:
            hacked_names = hacked_names + name + ":0,"
    return hacked_names[:-1]


def tf2onnx(tf_path, input_names, output_name, onnx_path):
    work_dir = "./"
    command = "python3 -m tf2onnx.convert  --graphdef " + tf_path
    command = command + " --inputs " + hack_name(input_names)
    command = command + " --inputs-as-nchw " + hack_name(input_names)
    command = command + " --outputs " + hack_name(output_name)
    command = command + " --output " + onnx_path
    command = command + " --opset 11"
    print(command)
    result = cmd.run(command, work_dir=work_dir)
    if result == 0:
        return True
    else:
        return False


def convert(tf_path, input_names, output_names, output_dir, version, optimize, half):
    checker.check_file_exist(tf_path)
    model_name = os.path.basename(tf_path)
    if output_dir is None or not os.path.isdir(output_dir):
        output_dir = os.path.dirname(tf_path)
    checker.check_file_exist(output_dir)
    model_name = model_name[:-len(".pb")]
    onnx_path = os.path.join(output_dir, model_name + ".onnx")
    if tf2onnx(tf_path, input_names, output_names, onnx_path) is False:
        print("Oh No, tf2onnx failed")
    else:
        print("congratulations! tf2onnx succeed!")
    if version is None:
        version = "v1.0"
    checker.check_file_exist(onnx_path)
    onnx2tnn.convert(onnx_path, output_dir, version, optimize, half)
