from Model import Model
from time import time

T1 = time()
buf = open('./models/fastspeech_quant.tflite', 'rb').read()
buf = bytearray(buf)
Models = Model.GetRootAsModel(buf, 0)
print(Models.OperatorCodesLength())
for i in range(Models.OperatorCodesLength()):
    print(Models.OperatorCodes(i).DeprecatedBuiltinCode())

T2 = time() - T1
print(T2)