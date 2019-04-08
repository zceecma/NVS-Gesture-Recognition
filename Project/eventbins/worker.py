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
"""
def create_frames(aggregation_time):
    generation_interval = 800
    frame_pos_events_frequency = []
    frame_neg_events_frequency = []
    folder = "generated_images" + str(generation_interval) + "_" + str(aggregation_time)
    for fname in os.listdir("Events"):
        events, max_x, max_y = readfile(fname)
        fname = fname.replace(".txt","")
        if not os.path.exists(folder + "/pos/" + fname):
            os.makedirs(folder + "/pos/" + fname)
        if not os.path.exists(folder + "/neg/" + fname):
            os.makedirs(folder + "/neg/" + fname)
        if not os.path.exists(folder + "/both/" + fname):
            os.makedirs(folder + "/both/" + fname)
        for i in range(len(events)):
            if i%generation_interval == 0:
                pos_events = 0
                neg_events = 0
                n = i
                frame_start = events[i][2]
                pos = Image.new("1", (max_x+1, max_y+1),color=0)      # "1 for single bit"
                neg = Image.new("1", (max_x+1, max_y+1),color=0)      # "1 for single bit"
                both = Image.new("1", (max_x+1, max_y+1),color=0)      # "1 for single bit"
                while events[n][2]-frame_start<aggregation_time and n<len(events)-1:
                    both.putpixel((events[n][0],events[n][1]),1)
                    if events[n][3] == 1:
                        pos.putpixel((events[n][0],events[n][1]),1)
                        pos_events += 1
                    else:
                        neg.putpixel((events[n][0],events[n][1]),1)
                        neg_events += 1
                    n += 1
                pos = pos.transpose(Image.FLIP_TOP_BOTTOM)
                pos.save(folder + "/pos/" + fname + "/" + str(int(i//generation_interval)) + ".png", "PNG")
                neg = neg.transpose(Image.FLIP_TOP_BOTTOM)
                neg.save(folder + "/neg/" + fname + "/" + str(int(i//generation_interval)) + ".png", "PNG")
                both = both.transpose(Image.FLIP_TOP_BOTTOM)
                both.save(folder + "/both/" + fname + "/" + str(int(i//generation_interval)) + ".png", "PNG")
                if len(frame_pos_events_frequency)<max(pos_events,neg_events)+1:
                    for _ in range(max(pos_events,neg_events)+1-len(frame_pos_events_frequency)):
                        frame_pos_events_frequency.append(0)
                        frame_neg_events_frequency.append(0)
                frame_pos_events_frequency[pos_events] += 1
                frame_neg_events_frequency[neg_events] += 1
    plt.figure(figsize=(15,10))
    plt.bar(list(range(len(frame_pos_events_frequency))), frame_pos_events_frequency, color = "g" , label = "Positive events")
    plt.bar(list(range(len(frame_neg_events_frequency))), frame_neg_events_frequency, bottom = frame_pos_events_frequency, color = "r" , label = "Negative events")
    plt.ylabel('Frequency')
    plt.legend()
    plt.title('Frequency of Events in Frames')
    plt.savefig(folder + '/event_freq.png')
    plt.gcf().clear()

if __name__ == '__main__':
    jobs = []
    for i in np.linspace(1000,10000,10,dtype=int):
        p = multiprocessing.Process(target=create_frames, args=(i,))
        jobs.append(p)
        p.start()
"""
def process_video (fname,generation_interval,aggregation_time,folder):
    events, max_x, max_y, min_x, min_y = readfile(fname)
    fname = fname.replace(".txt","")
    if not os.path.exists(folder + "/pos/" + fname):
        os.makedirs(folder + "/pos/" + fname)
    if not os.path.exists(folder + "/neg/" + fname):
        os.makedirs(folder + "/neg/" + fname)
    if not os.path.exists(folder + "/both/" + fname):
        os.makedirs(folder + "/both/" + fname)
    for i in range(len(events)):
        if i%generation_interval == 0:
            pos_events = 0
            neg_events = 0
            n = i
            frame_start = events[i][2]
            pos = Image.new("1", (max_x+1-min_x, max_y+1-min_y),color=0)      # "1 for single bit"
            neg = Image.new("1", (max_x+1-min_x, max_y+1-min_y),color=0)      # "1 for single bit"
            both = Image.new("1", (max_x+1-min_x, max_y+1-min_y),color=0)      # "1 for single bit"
            while events[n][2]-frame_start<aggregation_time and n<len(events)-1:
                both.putpixel((events[n][0]-min_x,events[n][1]-min_y),1)
                if events[n][3] == 1:
                    pos.putpixel((events[n][0]-min_x,events[n][1]-min_y),1)
                    pos_events += 1
                else:
                    neg.putpixel((events[n][0]-min_x,events[n][1]-min_y),1)
                    neg_events += 1
                n += 1
            pos = pos.transpose(Image.FLIP_TOP_BOTTOM)
            pos.save(folder + "/pos/" + fname + "/" + str(int(i//generation_interval)) + ".png", "PNG")
            neg = neg.transpose(Image.FLIP_TOP_BOTTOM)
            neg.save(folder + "/neg/" + fname + "/" + str(int(i//generation_interval)) + ".png", "PNG")
            both = both.transpose(Image.FLIP_TOP_BOTTOM)
            both.save(folder + "/both/" + fname + "/" + str(int(i//generation_interval)) + ".png", "PNG")

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    jobs = []
    for aggregation_time in np.linspace(1000,10000,10,dtype=int):
        generation_interval = 800
        folder = "generated_images" + str(generation_interval) + "_" + str(aggregation_time)
        for fname in os.listdir("Events"):
            pool.apply_async(process_video, args=(fname,generation_interval,aggregation_time,folder))
    pool.close()
    pool.join()