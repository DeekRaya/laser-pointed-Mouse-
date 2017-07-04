import numpy as np
import cv2
import time, pyautogui
'''This program is used to detect the laser pointer on the projected screen and map the corresponding mouse posiotn on the  PC '''
# vid is the video object
vid=cv2.VideoCapture(0)
#low and high are the(HSV)values the set the low and high range of pixel are specific to the laser pointer
low=np.array([0,0,255])
high = np.array([255,4,255])
#X,Y is the tuple that store the size of the PC screen
X , Y = pyautogui.size()
print X, Y

con=0
temp_x=0
temp_y=0
#fp is the file object referring to the file corners.txt which has the values  top rightmost and bottom leftmost corners of the  project screen the file is created when the set_corner.py
# program is exectued
fp = open('corners.txt','r')
#corners stores the text in the file as a string
corners = fp.read()
# corner splits the string corners to extract all the earlier specified coordinates and store it in the form of a tuple
# split function is used to split comma separted values and sotre it in form of a string
corner=map(int,corners.split(','))
# l0,l1,h0,h1 store the indiviual coordinate values
l0,l1,h0,h1 = corner
# lent stores the length of the PC screen
#bdth stores the breadth of the PC screen
lent = h0 - l0
bdth = h1 - l1
print "the length , breadth and the cordintes ",lent, bdth , l0, l1, h1 , h0
try:
    while(1):

        ret,frame=vid.read() # reading each frame from the video object  ret store the boolean values while the fram store the img in Mat object

        frame_h = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)#converting the frame from BGR to HSV i.e changing the color sapce which is apprently better for colour segmentation and storing in in frameh

        mask=cv2.inRange(frame_h, low, high)#creating a mask object which shall renders all the pixels out the limits (low,high) to RGB=(0,0,0) i.e black and others to RGB =(255,255,255)
        mask=cv2.dilate(mask,(5,5))#dialating the the mask using a 5,5 kernel
        _,cnt,hi = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#cnt stores all the contours i.e ideally the the laser pointer coordinates
        cv2.imshow('image',mask)# showing the mask in the window image for testing puposes
        if(len(cnt)==0):#cnt doest if ther is no laser pointer detected
            continue
        else:
            #computing the minimum enclosed circle of the contour
            # c store the centre of the circle which ideally estimaes the centre of the laser pointer on the projected screen

            (c_x,c_y),r=cv2.minEnclosingCircle(cnt[0])
            c = [c_x,c_y]
            #drwaing the circle with the centre a t c and of radius r and of colour (255,255,0) thickness 2
            cv2.circle(frame,(int(c_x),int(c_y)),int(r),(255,255,0),2)

        # x,y maps the c_x ,c_y ,which is the centre of the laser pointer with respec to the frame . to the actual PC screen
        x = ((c_x - l0)/float(lent))*X
        y = ((c_y - l1)/float(bdth))*Y

        #the below show statments are used for testing or debugging
        #cv2.imshow('wtf',mask)
        # cv2.imshow("mask",mask)
        # cv2.imshow("frame",frame)
        #waitKey sensures that the frmae is taken after every 1 ms delay and closes when esc is pressed
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break;
        #enter the code for pyautogui
        # the below code is used to perform various mouse operation sbased on the values of x,y
        pyautogui.moveTo(int(x),int(y))# moving the mouse pointer to the calcuated centre of the laser pointer
        # the below code is used to implement left click when the person holds the laser pointer at the same  position  (error of +5,-5 pixels shall be considered as the same positon)

        if(abs(temp_x-c_x)<=5 and abs(temp_y-c_y)<=5):# check if the laser poitner is held at the same position with an error of 5 pixels
            con+=1# and counting the number of frmaes for which the laser pointer is held at a same position
        else:
            cont=0#resetting the count to 0 in the case if the laser pointer is not held ast the same position
        if con==25:# if the the number frames where the laser pointer is held is more then 25 frames then left click shall be implemeted
            print('LEFT CLICK IMPLEMENTED')
            try:
               pyautogui.click(int(x),int(y))#implemeting left clcick note: inorder to execute in windows then
               print "the actual click"
            except:
                pass
            con=0
        temp_x,temp_y=c_x,c_y # storing the prvious centere in temp_x ,temp_y
except KeyboardInterrupt:
    print('end of program')
    cv2.destroyAllWindows()#destroying all the windows
    vid.release()#replasing the object

