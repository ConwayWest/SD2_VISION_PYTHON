import tkinter
import PIL.Image, PIL.ImageTk
import cv2
import time

vid_view = 0

def VideoSwitch(num):
    global vid_view
    vid_view = num

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.vid_view = 0

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, heigh = self.vid.height)
        self.canvas.pack()
        myButtonOne = tkinter.Button(window, text="Raw Video", command=lambda *args: VideoSwitch(0)).pack()
        myButtonTwo = tkinter.Button(window, text="Canny Edge", command=lambda *args: VideoSwitch(1)).pack()
        myButtonThree = tkinter.Button(window, text="Final", command=lambda *args: VideoSwitch(2)).pack()

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

            self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            greyFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # sobel = cv2.Sobel(greyFrame, cv2.CV_64F, 1, 1, 5)
            edges = cv2.Canny(greyFrame, 50, 50)

            if ret and vid_view == 0:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            elif ret and vid_view == 1:
                return (ret, cv2.cvtColor(edges, cv2.COLOR_BGR2RGB))
            elif ret and vid_view == 2:
                contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                cv2.drawContours(frame, contours, -1, (0,0,255), 2)
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Canny Edge in Tkinter")
