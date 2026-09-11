import GPUtil

for gpu in GPUtil.getGPUs():
    print(gpu.name)
    print("显存:", gpu.memoryTotal, "MB")