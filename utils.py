import os 
import re 
from Model_schema import Model

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

def tflite_op(tflite_path, opcode_set):
    model_path = tflite_path
    buf = open(model_path, 'rb').read()
    buf = bytearray(buf)
    Models = Model.GetRootAsModel(buf, 0)
    for i in range(Models.OperatorCodesLength()):
        opcode_set.add(Models.OperatorCodes(i).DeprecatedBuiltinCode())
    return opcode_set


def tflite_ops(tflite_path, tflite_name):
    # find tflite文件
    model_path = tflite_path
    model_name = tflite_name
    os.system("flatc.exe -t ./schema.fbs -- %s"%(model_path))
    json_file = "%s.json"%(model_name)
    operators_codes_dict = "{ \n"
    # to speed up, we only handle the line from operator_codes: [ to the first ],
    can_start = False
    with open(json_file, 'r+') as f:
        for _, i in enumerate(f.readlines()):
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

    # remove the tmp json file
    os.remove(json_file)

    operator_dicts = eval(operators_codes_dict)["operator_codes"]
    operator_code_list = []
    for dic in operator_dicts:
        try:
            operator_code_list.append(dic["deprecated_builtin_code"])
        except:
            operator_code_list.append(0)
    return operator_code_list

def tflite_str(operator_list, main_window = None):
    operator_list = list(operator_list)
    operator_enums = []
    with open("./operators_enum.txt") as f:
        for i, l in enumerate(f.readlines()):
            operator_enums += [l.split(" ")[0]]

    difference = list(set(operator_list) - set(main_window.a_list))
    if difference != []:
        difference_operator = []
        for op in difference:
            difference_operator += [operator_enums[op]]
        main_window.warning(difference_operator)
        return "There are certain operators are not supported!"
    
    # use a tmpl to init out output file
    output_file_ctx = open("model_ops_micro_tmpl.cpp").read()
    # here is the replace key: s_microOpResolver.
    # find the function from this, and then write this string
    need_reg_nodes = ""
    operator_enum = []
    with open("./micro_mutable_op_resolver.h") as f:
        ctx = f.readlines()
        for op_code in operator_list:
            # try:
            #     op_code = operator_dict["deprecated_builtin_code"]
            # except:
            #     #TODO: waiting check, if only has a dict, but none contents, maybe a 0, means an Add
            #     op_code = 0
            operator_enum += [operator_enums[op_code]]
        function_names = find_function(ctx, operator_enum)
        # the join method will ignore the first elements, need to add it manually
        need_reg_nodes += "s_microOpResolver." + "    s_microOpResolver.".join([name + ";\n" for name in function_names])
        f.close()
    
    output_file_ctx = output_file_ctx.replace("tOpCount", "%d"%(len(operator_list)))
    output_file_ctx = output_file_ctx.replace("OPRESOLVER_PLACEHOLDER", need_reg_nodes)
    
    return output_file_ctx
