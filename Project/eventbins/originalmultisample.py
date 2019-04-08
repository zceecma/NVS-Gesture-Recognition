from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing

plt.gcf().clear()
plt.clf()
plt.cla()
plt.close()

def readfile(fname):
    file = open("events/" + fname)
    events = []
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for line in file:
        data = line.split(' ')
        data[0] = int(data[0])
        if data[0] < min_x:
            min_x = data[0]
        if data[0] > max_x:
            max_x = data[0]
        data[1] = int(data[1])
        if data[1] < min_y:
            min_y = data[1]
        if data[1] > max_y:
            max_y = data[1]
        data[2] = int(data[2])
        data[3] = int(data[3].replace('\n',''))
        events.append(data)      #x_pixel, y_pixel, time_interval, Polarity
    file.close()
    return sorted(events,key=lambda x: x[2]), max_x, max_y, min_x, min_y

time_interval = 256
def process_video (fname,generation_interval):
    events, max_x, max_y, min_x, min_y = readfile(fname)
    fname = fname.replace(".txt","")
    folder = "generated_images" + str(generation_interval) + "_sampled"
    if not os.path.exists(folder + "/pos/" + fname):
        os.makedirs(folder + "/pos/" + fname)
    if not os.path.exists(folder + "/neg/" + fname):
        os.makedirs(folder + "/neg/" + fname)
    if not os.path.exists(folder + "/both/" + fname):
        os.makedirs(folder + "/both/" + fname)
    for start_entry in np.arange(0, len(events), generation_interval):
        frame_start = events[start_entry][2]
        pos = Image.new("L", (max_x+1-min_x, max_y+1-min_y),color=0)      # "1 for single bit"
        neg = Image.new("L", (max_x+1-min_x, max_y+1-min_y),color=0)      # "1 for single bit"
        both = Image.new("L", (max_x+1-min_x, max_y+1-min_y),color=0)      # "1 for single bit"
        for window in range(256):
            n = start_entry
            window_start = (255-window)*time_interval+frame_start
            window_end = (256-window)*time_interval+frame_start
            while n<len(events)-1 and events[n][2]<=window_end:
                if events[n][2]>=window_start:
                    both.putpixel((events[n][0]-min_x,events[n][1]-min_y),window)
                    if events[n][3] == 1:
                        pos.putpixel((events[n][0]-min_x,events[n][1]-min_y),window)
                    else:
                        neg.putpixel((events[n][0]-min_x,events[n][1]-min_y),window)
                n += 1
        pos = pos.transpose(Image.FLIP_TOP_BOTTOM)
        pos.save(folder + "/pos/" + fname + "/" + str(int(start_entry//generation_interval)) + ".png", "PNG")
        neg = neg.transpose(Image.FLIP_TOP_BOTTOM)
        neg.save(folder + "/neg/" + fname + "/" + str(int(start_entry//generation_interval)) + ".png", "PNG")
        both = both.transpose(Image.FLIP_TOP_BOTTOM)
        both.save(folder + "/both/" + fname + "/" + str(int(start_entry//generation_interval)) + ".png", "PNG")

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    jobs = []
    for fname in os.listdir("Events"):
        pool.apply_async(process_video, args=(fname,512))
    pool.close()
    pool.join()