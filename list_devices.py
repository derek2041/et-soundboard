import sounddevice as sd

device_data = sd.query_devices()

print("==============================================================================================================")
for device in device_data:
    print("")
    print(device)
    print("")
print("==============================================================================================================")
