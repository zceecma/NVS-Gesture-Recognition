from PIL import Image
import os
import numpy as np
import multiprocessing

def readfile(fname):
    file = open("events/" + fname)
    events = []
    for line in file:
        data = line.split(' ')
        data[0] = int(data[0])
        data[1] = int(data[1])
        data[2] = int(data[2])
        data[3] = int(data[3].replace('\n',''))
        events.append(data)      #x_pixel, y_pixel, time_interval, Polarity
    file.close()
    return sorted(events,key=lambda x: x[2])


generate_time=512
def process_video (fname,time_interval):
    events = readfile(fname)
    fname = fname.replace(".txt","")
    folder = "D:/Project/eventbins/generated_images_timeSampled_" + str(time_interval)
    if not os.path.exists(folder + "/pos/" + fname):
        os.makedirs(folder + "/pos/" + fname)
    if not os.path.exists(folder + "/neg/" + fname):
        os.makedirs(folder + "/neg/" + fname)
    frame_num = 0
    generate_interval =  len(events)//64 +1
    if generate_interval < generate_time:
        generate_interval = generate_time
    for start_entry in np.arange(generate_interval, len(events), generate_interval):
        frame_start = events[start_entry][2] #time of start entry
        pos = Image.new("L", (176, 100),color=0)      # "1 for single bit"
        neg = Image.new("L", (176, 100),color=0)      # "1 for single bit"
        curr_entry = start_entry
        while curr_entry>0 and events[curr_entry+1][2]>frame_start-time_interval*255:
            curr_entry -=1
        while curr_entry<start_entry:
            if events[curr_entry][3] == 1:
                pos.putpixel((events[curr_entry][0],events[curr_entry][1]),255-(frame_start-events[curr_entry][2])//time_interval)
            else:
                neg.putpixel((events[curr_entry][0],events[curr_entry][1]),255-(frame_start-events[curr_entry][2])//time_interval)
            curr_entry += 1
        pos = pos.transpose(Image.FLIP_TOP_BOTTOM)
        pos.save(folder + "/pos/" + fname + "/" + str(int(frame_num)) + ".png", "PNG")
        neg = neg.transpose(Image.FLIP_TOP_BOTTOM)
        neg.save(folder + "/neg/" + fname + "/" + str(int(frame_num)) + ".png", "PNG")
        frame_num += 1

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    jobs = []
    for fname in os.listdir("Events"):
        pool.apply_async(process_video, args=(fname,1024))
    for fname in os.listdir("Events"):
        pool.apply_async(process_video, args=(fname,390))
    pool.close()
    pool.join()