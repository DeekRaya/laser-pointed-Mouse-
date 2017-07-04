import cv2
import numpy as np
import pyautogui
'''This program shall enable  the user to manually specify the coordinates of  rightmost corner , leftmost corner of the projected PC
screen,with respect to video frames captured by the camera ,just by clicking on the coordinates as in the video displayed when the program is run'''
##########################################################################
'''
variable documentation:
x,y :are the x,y coordinates in video when the mouse is clicked . the coordinates are specified with origin at the top rightmost corner of the WINDOW ;
click :updates to 1 if mouse is clicked in on the window;
des_flag:updates with each click ;
fp : the file object which refers to the file where the corners are stored in the format rightmost_x_coordinate,rightmost_y_coordinates ,leftmost_x_coordinates,leftmost_y _coordinates ;
'''
x=0
y=0
click=0
des_flag=0
#rewriting over a file corners.txt
fp = open('corners.txt', 'w+')
#callBackfun is called when a mouse clicked by the user
def callBackFun(event,p,q,flag,_):
    global x
    global y
    global click
    global des_flag
    if(event==cv2.EVENT_LBUTTONDOWN):
        x = p
        y = q
        click=1
        des_flag+=1
        return 1


corner=list()
#creating a graphical winodw for the video to be displayed
# with the window name 'proj'
cv2.namedWindow('proj')
#creating a video capture object
cap=cv2.VideoCapture(0)

#setting a mouxe call back fucntion that specifies that the function callBackFun is called when a the user clicks on the window 'proj'
cv2.setMouseCallback('proj', callBackFun)
# this is a infinite while loop that is used to write the coordinates to the file
while(1):
    _,img=cap.read()#cap.read() give the output (bool,Mat) henc the boolean value is discarded using the underscore symbol while img stores the mat object in the
    if(click==1):   #if a click is detected then the list corner is appende by the coordinates of the click
        corner.append([x,y])
        click=0 # resetting the value of click to 0

    if(des_flag==2):#this checks if the nuber of clicks were 2
        cv2.destroyAllWindows()#closing the window
        l ,h=corner # 'l' stores the coordinates of the right most corner while 'h' sotres the left most coordinates
        x_r,y_r = tuple(l)# x_r,y_r stores resoective x and y coordinates of the right most coreners
        x_l,y_l = tuple(h)#x_l,y_l stores the respective coordintes leftmost screen corners
        
        fp.write(str(x)+','+str(y)+','+str(z)+','+str(w))#writing all the coordintes in format x_r,y_r,x_l,y_l
        fp.close()#closing the file
        #print l,h
        des_flag=0;#



    cv2.imshow('proj', img)#showing the video  in the window 'proj'
    k = cv2.waitKey(1) & 0xFF# the frames are displayed after every 1 ms and window gets closed if esc key is presed
    if k == 27:#27 is the ASCII value of the'esc'
        cap.release()        # relasing the cap object from the memory
        break;
        


