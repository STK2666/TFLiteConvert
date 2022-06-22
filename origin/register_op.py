import os 
import re 
import shutil 
import numpy as np 
import time

# sometime we need to ignore the first char
def find_element(line, key, drop_first):
    _word = re.search(key, line)
    if(_word):
        s = _word.start() 
        e = _word.end()
        word = line[s+drop_first:e-1].strip()
        return word
    return None

def find_function(ctx_lines, op_enum):
    function_lists = []
    for idx, line in enumerate(ctx_lines):
        cur_op_enum = find_element(line, "\(.+?,", True) if "AddBuiltin" in line else None
        if(cur_op_enum):
            # find one, check if in op_enum
            if(cur_op_enum in op_enum):
                # got one, then find the Addxx names
                # Addxx always at the -1 line, but in case we ignore, find until the first /n
                i = 1
                function_line = ctx_lines[idx-i]
                names = None
                while(function_line != "\n"):
                    i = i + 1
                    if("AddAdd" in function_line):
                        print()
                    names = find_element(function_line, "Add.+?\(", False)
                    if(names):
                        function_lists += [names + "()"]
                        break
                    function_line = ctx_lines[idx - i]

                if (not names): raise Exception("Fail to find the function name for %s"%line)

        if(len(function_lists) == len(op_enum)):
            # we got all the operators, can leave
            break
    return function_lists


if __name__ == "__main__":
    # find tflite文件
    T1 = time.time()
    model_path = r"./origin"
    model_name = "fastspeech_quant"
    os.system("flatc.exe -t ./schema.fbs -- %s/%s.tflite"%(model_path, model_name))
    T2 = time.time() - T1
    json_file = "%s.json"%(model_name)
    operators_codes_dict = "{ \n"
    # to speed up, we only handle the line from operator_codes: [ to the first ],
    can_start = False
    with open(json_file, 'r+') as f:
        for idx, i in enumerate(f.readlines()):
            if "operator_codes" in i: can_start = True
            if can_start:
                _word = re.search(".+:", i)
                if(_word):
                    s = _word.start() 
                    e = _word.end()
                    word = i[s:e-1].strip()
                    operators_codes_dict += i.replace(word, '"' + word + '"' )
                else:
                    operators_codes_dict += i
                    if "]," in i:
                        # stop here
                        operators_codes_dict += "}\n"
                        break
        f.close()
    T3 = time.time() - T2 - T1
    # remove the tmp json file
    os.remove(json_file)

    operator_dicts = eval(operators_codes_dict)["operator_codes"]

    operator_enums = []
    with open("./operators_enum.txt") as f:
        for i, l in enumerate(f.readlines()):
            operator_enums += [l.split(" ")[0]]

    # use a tmpl to init out output file
    output_file_ctx = open("model_ops_micro_tmpl.cpp").read()
    output_file = open("model_ops_micro.cpp", "w+")

    # here is the replace key: s_microOpResolver.
    # find the function from this, and then write this string
    need_reg_nodes = ""
    operator_enum = []
    T4 = time.time()
    with open("./micro_mutable_op_resolver.h") as f:
        ctx = f.readlines()
        for operator_dict in operator_dicts:
            try:
                op_code = operator_dict["deprecated_builtin_code"]
            except:
                #TODO: waiting check, if only has a ditc, but none contents, maybe a 0, means an Add
                op_code = 0
            operator_enum += [operator_enums[op_code]]
        function_names = find_function(ctx, operator_enum)
        # the join method will ignore the first elements, need to add it manually
        need_reg_nodes += "s_microOpResolver." + "    s_microOpResolver.".join([name + ";\n" for name in function_names])
        f.close()
    T5 = time.time() - T4
    output_file_ctx = output_file_ctx.replace("tOpCount", "%d"%(len(operator_enum)))
    output_file_ctx = output_file_ctx.replace("OPRESOLVER_PLACEHOLDER", need_reg_nodes)
    output_file.write(output_file_ctx)
    output_file.close()

    # if you need to update your library only, not compile it all, open below comment
    # gcc/keil are both OK, specify the path
    #compiler_path = r"C:\NXP\MCUXpressoIDE_11.5.0_7232\ide\plugins\com.nxp.mcuxpresso.tools.win32_11.5.0.202107051138\tools\bin\arm-none-eabi-gcc.exe"
    # compiler_path = r"C:\Keil_v5\ARM\ARMCLANG\bin\armclang.exe" + " --target=arm-arm-none-eabi"
    # libtf_lib_path = model_path + "\libtf_eiq.lib"
    
    # cmd_line = open("./cmd_line.txt").read()
    # os.system(compiler_path + cmd_line + " ./model_ops_micro.cpp -o ./model_ops_micro.o")
    # os.system("zip.exe -r " + libtf_lib_path + " ./model_ops_micro.o")
    # os.remove("./model_ops_micro.o")

    # if os.path.exists(model_path + "/model_ops_micro.cpp"):
    #     os.remove(model_path + "/model_ops_micro.cpp")
    # shutil.move("./model_ops_micro.cpp", model_path)
