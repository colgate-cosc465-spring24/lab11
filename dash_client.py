# Built-in modules
import argparse
import os
import socket
import threading
import time

# Extra modules
import cv2
from ffpyplayer.player import MediaPlayer
import numpy
import requests

class Buffer():
    def __init__(self):
        # Prepare producer end of buffer
        self._last_time_produced = 0
        try:
            os.unlink("./buffer")
        except:
            pass
        self._producer_sock = socket.socket(socket.AF_UNIX)
        self._producer_sock.bind("./buffer")
        threading.Thread(target=self._init_helper).start()

        # Prepare consumer end of buffer
        self._last_time_consumed = 0
        self._consumer_sock = socket.socket(socket.AF_UNIX)
        self._consumer_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536*16) 
        self._consumer_sock.connect("./buffer")
        self._player = None
        self._player = MediaPlayer("pipe:{}".format(self._consumer_sock.fileno()), paused=True)
        self._player.set_pause(True)

    """Function to help with initializing buffer"""
    def _init_helper(self):
        self._producer_sock.listen()
        new_sock, _ = self._producer_sock.accept() 
        new_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536*16) 
        self._producer_sock.close()
        self._producer_sock = new_sock

    """Return the duration of video in the buffer"""
    @property
    def duration_buffered(self):
        return round(self._last_time_produced - self._last_time_consumed, 2)

    """Add a video segment to the buffer"""
    def add_segment(self, data, duration):
        self._producer_sock.send(data)
        self._last_time_produced += duration

    """Get the next frame from the buffer"""
    def get_frame(self):
        frame, duration = self._player.get_frame()
        if frame is None:
            return (None, duration, None)
        else:
            frame, timestamp = frame
            self._last_time_consumed = timestamp
            return (frame, duration, timestamp)

"""Main function for video player"""
def player(buffer):
    # Create playback window
    cv2.namedWindow("DASH", cv2.WINDOW_NORMAL)
    img = cv2.imread('buffering_screen.png')
    cv2.imshow('DASH',img)
    cv2.waitKey(1)

    # TODO: display video frames, pausing to buffer as necessary

    # Destroy playback window
    cv2.destroyAllWindows()
    return

    
def display_frame(frame, duration):
    cv2.imshow('DASH',convert_image(frame))
    cv2.waitKey(max(1, int(duration * 1000)))

'''Convert video image so it can be displayed'''
def convert_image(img):
    w = img.get_size()[0]
    h = img.get_size()[1]
    arr = numpy.uint8(numpy.asarray(list(img.to_bytearray()[0])).reshape(h,w,3))
    arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return arr

'''Pause the player to buffer'''
def pause_to_buffer(buffer, threshold):
    buffer._player.set_pause(True)
    img = cv2.imread('buffering_screen.png')
    cv2.imshow('DASH',img)
    while buffer.duration_buffered < threshold:
        print("Buffering...\tBuffered:", buffer.duration_buffered)
        cv2.waitKey(500)
    buffer._player.set_pause(False)

'''Fill the buffer from the network'''
def fill_from_network(buffer, base_url='http://picard.cs.colgate.edu/dash/bbb_'):
    data = fetch(base_url, '320x180', 'init')
    if data is not None:
        buffer.add_segment(data, 0)
    else:
        return

    # TODO: Fetch all 30 segments, using buffer occupany to determine resolution

'''Fetch a video segment'''
def fetch(base_url, resolution, segment):
    # URL to fetch
    url = base_url+resolution+segment+"."+("mp4" if segment=="init" else "m4s")
    
    # TODO: Issue request and simulate transmission delay based on bandwidth
    return None

def main():
    parser = argparse.ArgumentParser(description='DASH client')
    parser.add_argument('-b', '--bandwidth', type=int, default='500',
        help='Bandwidth in Kbps (default: 500)')
    args = parser.parse_args()

    # Store bandwidth setting
    global bandwidth
    bandwidth = args.bandwidth / 8 * 1000

    # Create buffer
    buffer = Buffer() 

    # Start filling buffer
    filler = threading.Thread(target=fill_from_network, args=[buffer])
    filler.start()

    # Run video player
    player(buffer)

if __name__ == "__main__":
    main()