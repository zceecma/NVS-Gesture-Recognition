import os
from PIL import Image

def readfile(fname):
    file = open(fname)
    events = []
    max_x = 0
    max_y = 0
    for line in file:
        data = line.split(' ')
        data[0] = int(data[0])
        if (data[0] > max_x):
            max_x = data[0]
        data[1] = int(data[1])
        if (data[1] > max_y):
            max_y = data[1]
        data[2] = int(data[2])
        data[3] = int(data[3].replace('\n',''))
        events.append(data)      #x_pixel, y_pixel, time_interval, Polarity
    file.close()
    return sorted(events,key=lambda x: x[2]), max_x, max_y


aggregation_time = 10000
val_change = 255
generation_interval = 512

fname = "1.mp4.txt"
events, max_x, max_y = readfile(fname)
fname = fname.replace(".txt","")
if not os.path.exists("generated_event_images/pos/" + fname):
    os.makedirs("generated_event_images/pos/" + fname)
if not os.path.exists("generated_event_images/neg/" + fname):
    os.makedirs("generated_event_images/neg/" + fname)
for i in range(len(events)):
    if i%generation_interval == 0:
        n = i
        time = 0
        start = events[n][2]
        pos = Image.new("1", (max_x+1, max_y+1),color=0)      # "1 for single bit"
        pix = pos.load()
        neg = Image.new("1", (max_x+1, max_y+1),color=0)      # "1 for single bit"
        pix = neg.load()
        while time - start <aggregation_time and n<len(events):
            time = events[n][2]
            pos.putpixel((events[n][0],events[n][1]),val_change*(events[n][3]))
            neg.putpixel((events[n][0],events[n][1]),val_change*(1-events[n][3]))
            n += 1
        pos = pos.transpose(Image.FLIP_TOP_BOTTOM)
        pos.save("generated_event_images/pos/" + fname + "/" + str(i//generation_interval) + ".png", "PNG")
        neg = neg.transpose(Image.FLIP_TOP_BOTTOM)
        neg.save("generated_event_images/neg/" + fname + "/" + str(i//generation_interval) + ".png", "PNG")