# Lab 09: Video streaming client

## Overview
In this lab, you will implement a Dynamic Adaptive Streaming over HTTP (DASH) client. 

### Learning objectives
After completing this lab, you should be able to:
* Use the `requests` Python library to issue HTTP requests
* Explain how Dynamic Adaptive Streaming over HTTP (DASH) works

## Getting started
Clone your repository on **your own Mac laptop** or a **department-owned Mac laptop**. You will need to run the Python code on a local machine, **not** a `tigers` server, so you can see the video.

Install the necessary Python packages:
```bash
pip3 install cv2 ffpyplayer numpy requests
```

To run the video streaming client, run:
```
python3 ./dash_client.py
```

You can also include the optional `-b` argument to specify the simulated network bandwidth in Kbps.

## Part 1: `fetch`
Your first task is to complete the `fetch` function. 

The `fetch` function needs to use Python [`requests` library](https://docs.python-requests.org/en/latest/) to issue an HTTP **GET** request for the `url` and return the **binary** response. The function should return `None` if an HTTP error occurs.

The `fetch` function must also introduce artificial transmission delay based on the `bandwidth` and content length. First, obtain the content, then use [`time.sleep`](https://docs.python.org/3/library/time.html#time.sleep) to simulate transmission delay before returning the content from the `fetch` function.

## Part 2: `fill_from_network`
Your second task is to complete the `fill_from_network` function. This function needs to use the `fetch` function you completed in Part 1 to request video segments and add them to the provided `buffer`. 

There are three different video resolutions to choose from: `320x180`, `640x360`, and `854x480`. You should fetch a `320x180` resolution segment if the buffer contains less than 5 seconds of video data, a `640x360` resolution segment if the buffer contains less than 10 seconds of video data, and a `854x480` resolution segment if the video buffer contains 10 or more seconds of video data.

Segments are numbered sequentially, starting from `1`. You should fetch segments until no more segments are available. 

## Part 3: `player`
Your final task is to complete the `player` function. 

This function needs to use the `buffer`'s `get_frame` function to obtain the next video frame from the buffer and the `display_frame` function to display the frame. Notice that `get_frame` returns three values: the actual frame (i.e., image) to display, how long to display the frame (in seconds) before getting the next frame, and the timestamp of the frame (in seconds) relative to the start of the video. 

If `get_frame` returns `None` for the frame **and** a display time of `0`, then this means the rendering of video frames is behind, and you should simply fetch the next frame. (Note: the rendering approach used in the code is suboptimal, so it is likely the rendering will occasionally fall behind if you try to play many frames at the highest resolution; if you want to know more about rendering, take computer graphics with Prof. Fourquet!)

If the frame is `None` and the display time is not `0`, then you need to pause playback to allow more data to be buffered by calling `pause_to_buffer` with a minimum duration of video data that must be present in the buffer in order to resume playback. Choose a value between `2` and `10` seconds, depending on whether you prefer more frequent, shorter buffering pauses or less frequent, longer buffering pauses. 

## Submission instructions
When you are done, commit and push your changes to GitHub.
