#importing python modules
import numpy as np
import cv2

class PaintApp():

    def __init__(self):
        self.drawing=True
        self.blueLower = np.array([100, 60, 60])
        self.blueUpper = np.array([140, 255, 255])

        self.kernel = np.ones((5, 5), np.uint8)

        self.roi_size=10

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        self.colorIndex = 0

        self.imageindex=0

        self.r=0
        self.g=0
        self.b=255

        self.size=2

        self.img = np.zeros((240,400, 3), np.uint8)

        self.initpaintwindow()
        self.frame=None
        self.camera = cv2.VideoCapture(0)

    def nothing(self,x):
        pass

    def initpaintwindow(self):
        #self.paintWindow = np.zeros((680,840, 3),np.uint8)
        #self.paintWindow = np.zeros((471,636,3),np.uint8) + 255
        self.paintWindow = np.zeros((720,1280, 3),np.uint8)
        self.paintWindow[:, :, :] = 255
        self.paintWindow = cv2.circle(self.paintWindow, (35, 50), 20, (0, 0, 0), -1)
        self.paintWindow = cv2.circle(self.paintWindow, (35, 170), 20, self.colors[0], -1)
        self.paintWindow = cv2.circle(self.paintWindow, (35, 285), 20, self.colors[1], -1)
        self.paintWindow = cv2.circle(self.paintWindow, (35, 400), 20, self.colors[2], -1)
        self.paintWindow = cv2.circle(self.paintWindow, (35, 525), 20, self.colors[3], -1)
        self.paintWindow = cv2.circle(self.paintWindow, (35, 630), 20, (210,210,210), -1)

        cv2.putText(self.paintWindow, "CLEAR", (1, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2,
                    cv2.LINE_AA)
        cv2.putText(self.paintWindow, "BLUE", (1, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "GREEN", (1, 303), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "RED", (6, 425), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "YELLOW", (1, 570), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "ERASER", (1, 645), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)
        # Lets create some trackbars for PaintTM:P
        cv2.namedWindow('paint_selector')  # creates an openCv window

        cv2.createTrackbar('R', 'paint_selector', 255, 255, self.nothing)
        cv2.createTrackbar('G', 'paint_selector', 255, 255, self.nothing)
        cv2.createTrackbar('B', 'paint_selector', 255, 255, self.nothing)  # remember 0 is default value, not start range
        cv2.createTrackbar('Size', 'paint_selector', 3, 20, self.nothing)


    def what_menu_button_pressed(self,center):
        if center[0]>65:
            return None
        if 40 <= center[1] <= 140:  # Clear All
            return "CLEAR"
        elif 160 <= center[1] <= 255:
            return "BLUE"
        elif 275 <= center[1] <= 370:
            return "GREEN"
        elif 390 <= center[1] <= 485:
            return "RED"
        elif 505 <= center[1] <= 600:
            return "YELLOW"
        elif 601 <= center[1] <= 700:
            return "ERASER"
        return None




    def calibrate(self):

        # Roi size
        r = self.roi_size

        # Calibration count
        i = 0

        while self.drawing:

            # Grab the current web frame
            self.frame = self.camera.read()[1]

            # Deep copy
            img = self.frame.copy()

            # Size of frame
            y, x, _ = np.shape(img)

            # Image locations
            if i == 0:
                xx, yy = int(x - x / 10), int(y / 8)  # Upper Left
            elif i == 1:
                xx, yy = int(x - x / 10), int(y - y / 2)  # Center Left
            elif i == 2:
                xx, yy = int(x - x / 10), int(y - y / 8)  # Lower Left
            elif i == 3:
                xx, yy = int(x - x / 2), int(y / 8)  # Upper Center
            elif i == 4:
                xx, yy = int(x - x / 2), int(y - y / 2)  # Center Center
            elif i == 5:
                xx, yy = int(x - x / 2), int(y - y / 8)  # Lower Center
            elif i == 6:
                xx, yy = int(x / 10), int(y / 8)  # Upper Right
            elif i == 7:
                xx, yy = int(x / 10), int(y - y / 2)  # Center Right
            elif i == 8:
                xx, yy = int(x / 10), int(y - y / 8)  # Lower Right

            # Draw square
            cv2.rectangle(img, (xx - r, yy - r), (xx + r, yy + r), (0, 0, 255), 2)

            # Flip frame to help with movement
            img = cv2.flip(img, 1)

            # Show the frame
            cv2.imshow('Frame', img)

            # exit on escape
            k = cv2.waitKey(5) & 0xFF

            # Capture color on c
            if k == 99:
                roi = self.frame[yy - r:yy + r, xx - r:xx + r]

                # Append the hsv data for statistics
                if 'hsv' in locals():
                    np.append(hsv, cv2.cvtColor(roi, cv2.COLOR_BGR2HSV))
                else:
                    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                i += 1

                if i == 9:
                    break

        image_mean = np.ceil(hsv.mean(axis=(0, 1)))
        image_std = np.ceil(hsv.std(axis=(0, 1)))

        self.blueLower = image_mean - image_std*3
        self.blueLower[0:1] -= 15
        self.blueLower[1:2] -= 15
        self.blueLower[2:3] = 20
        self.blueUpper = image_mean + image_std*3
        self.blueUpper[0:1] += 15
        self.blueUpper[1:2] += 15
        self.blueUpper[2:3] = 220
        cv2.destroyWindow("Frame")

    def find_largest_contour(self, contours):
        number_of_contours = len(contours)
        largest_contour_area = -1
        index_of_largest_contour=-1
        if number_of_contours > 0:  # if you have found atleast 1 countours
            # loop through the contours and find the largest one which we consider is the hand
            for i in range(number_of_contours):
                current_contour_area = cv2.contourArea(contours[i])
                if current_contour_area > largest_contour_area:
                    largest_contour_area = current_contour_area
                    index_of_largest_contour = i
            largest_contour = contours[index_of_largest_contour]
            return largest_contour
        else:
            return None

    def draw(self,pcenter,center,temp):
        #print(self.r, self.g, self.b)
        #colr=(int(self.b),int(self.g),int(self.r),255)
        colr=(self.b,self.g,self.r)
        cv2.line(self.paintWindow, pcenter,center,colr, self.size)
        cv2.line(temp, pcenter,center,colr, self.size)

    def capture(self):
        self.camera.set(3, 1920)
        self.camera.set(4, 1080)
        #self.camera.set(3,640);
        #self.camera.set(4,360);
        #cv2.resizeWindow("frame", 1080, 720) 
        first=False
        self.calibrate()
        while True:

            (grabbed,self.frame)=self.camera.read()
            self.frame = cv2.flip(self.frame, 1)
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            temp=self.paintWindow.copy()
            # Add the coloring options to the frame
            self.frame = cv2.circle(self.frame, (35, 50), 20, (122, 122, 122), -1)
            self.frame = cv2.circle(self.frame, (35, 170), 20, self.colors[0], -1)
            self.frame = cv2.circle(self.frame, (35, 285), 20, self.colors[1], -1)
            self.frame = cv2.circle(self.frame, (35, 400), 20, self.colors[2], -1)
            self.frame = cv2.circle(self.frame, (35, 515+10), 20, self.colors[3], -1)
            self.frame = cv2.circle(self.frame, (35, 620 + 10), 20, (210,210,210), -1)
            cv2.putText(self.frame, "CLEAR", (1, 65+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(self.frame, "BLUE", (1, 185+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(self.frame, "GREEN", (1, 298+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(self.frame, "RED", (1+5, 420+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(self.frame, "YELLOW", (1, 515+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(self.frame, "ERASER", (1, 620 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2,
                        cv2.LINE_AA)

            if not grabbed:
                break


                # Determine which pixels fall within the blue boundaries and then blur the binary image
            #self.blueLower = np.array([100, 60, 60])
            #self.blueUpper = np.array([140, 255, 255])
            blueMask = cv2.inRange(hsv, self.blueLower, self.blueUpper)
            blueMask = cv2.erode(blueMask, self.kernel, iterations=2)
            blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, self.kernel)
            blueMask = cv2.dilate(blueMask, self.kernel, iterations=1)

            # Find contours in the image
            (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
                                            cv2.CHAIN_APPROX_SIMPLE)
            contour= self.find_largest_contour(cnts)
            if contour is None :
                pass

            else:
                ((x, y), radius) = cv2.minEnclosingCircle(contour)
                # Draw the circle around the contour
                cv2.circle(self.frame, (int(x), int(y)), int(radius), (255, 0, 255), 2)
                # Get the moments to calculate the center of the contour (in this case Circle)
                M = cv2.moments(contour)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                if first == False :
                    first=True
                    pcenter=center
                area = self.what_menu_button_pressed(center)
                if area == "CLEAR":
                    self.paintWindow[:, 67:, :] = 255
                    temp[:, 67:, :] = 255
                elif area == "BLUE":
                    self.b=255
                    self.g=0
                    self.r=0
                elif area == "GREEN":
                    self.g = 255
                    self.b = 0
                    self.r = 0
                elif area == "RED":
                    self.r = 255
                    self.b = 0
                    self.g = 0
                elif area == "YELLOW":
                    self.r = 255
                    self.b = 0
                    self.g = 255
                elif area=="ERASER":
                    self.r=255
                    self.g=255
                    self.b=255
                else:
                    if self.drawing == True :
                        self.draw(pcenter, center,temp)
                        pcenter = center
                    cv2.circle(self.paintWindow, center,self.size, (self.b, self.g, self.r), -1)

            k = cv2.waitKey(1) & 0xFF

            img1 = self.img.copy()
            img1[:] = [self.b, self.g, self.r]  # the track window's color will display the color of my brush:
            if k == ord("s"):
                if self.drawing == True:
                    self.drawing = False
                else:
                    self.drawing = True
                pcenter = None
                first=False

            elif k == ord("q"):
                break

            elif k == ord("p"):
                cv2.imwrite("frame%d.jpg" % self.imageindex, self.paintWindow)
                self.imageindex += 1
            elif k == ord("m"):
                if self.size < 50:
                    self.size += 2
            elif k == ord("n"):
                if self.size > 2:
                    self.size -= 2
            elif k == ord("l"):
                self.r = cv2.getTrackbarPos('R', 'paint_selector')
                self.g = cv2.getTrackbarPos('G', 'paint_selector')
                self.b = cv2.getTrackbarPos('B', 'paint_selector')
                #print(self.r, self.g, self.b)
                self.size = cv2.getTrackbarPos('Size', 'paint_selector')
            cv2.imshow('paint_selector', img1)
            cv2.imshow("Tracking",self.frame)
            cv2.imshow("Paint",self.paintWindow)
            self.paintWindow=temp   
        self.camera.release()

app=PaintApp()
app.capture()
cv2.destroyAllWindows()