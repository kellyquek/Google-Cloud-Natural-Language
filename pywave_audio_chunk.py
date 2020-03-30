import csv
import os
import PyWave
import math

# Indicate the number of seconds to split
seconds = 59

natives = {}
with open ('listofwavfiles.csv', r) as f:
    reader = csv.reader(f)

    for row in reader:
        native = row[0]
        filename = row[1]

        fn = filename
        if native in natives:
            natives[native].append(fn)
        else:
            natives[native] = [fn]

for k, v in natives.items():
    fp = k
    for fn in v:
        # get filename alone
        fnname = fn.split('/')[-1].split('.')[0]
        # create folder
        os.makedirs(fp + '/' + fname + '_output', exist_ok = True)


for file_name in v:
    wf = PyWave.open(fp + "/" + file_name)
    counter = 1
    file_name_without_ext = file_name.split(".")[0]

    # total number of bits
    total_num_of_bytes = wf.samples

    # no. of seconds
    num_of_sec = (wf.samples * wf.bits_per_sample) / wf.bitrate

    # bytes per second
    bytes_per_second = total_num_of_bytes/num_of_sec

    # num of bytes in 59 seconds
    number_of_bytes_60_sec = math.ceil((total_num_of_bytes/num_of_sec) * float(seconds))

    total_loop = math.ceil(num_of_sec / seconds)

    if num_of_sec < seconds:
        total_loop = 1

    for index in range(total_loop):

        wf_chunk = PyWave.open(fp + '/' + file_name_without_ext + '_output/' + str(counter) + "wav", 
        mode = 'w',
        channels = wf.channels,
        frequency=wf.frequency,
        bits_per_sample=wf.bits_per_sample,
        format=wf.format)

        wf_chunk.write(wf.read(number_of_bytes_60_sec))
        wf_chunk.close()

        counter += 1

wf.close()
