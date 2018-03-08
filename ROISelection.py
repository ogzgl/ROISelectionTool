import cv2
def selection(x, y):
    global top_X,top_Y,bot_X,bot_Y,click_flag,img
    if(click_flag==0):
        cv2.circle(img, (x,y), 3, (0, 255, 0), -1)
        cv2.circle(img, (x,y), 10, (0,255,255),0,8,0)
        click_flag+=1
    elif(click_flag==1 and validation_second(top_X,top_Y,x,y)):
        cv2.circle(img, (x,y), 3, (0, 255, 0), -1)
        cv2.circle(img, (x,y), 10, (0,255,255),0,8,0)
        cv2.rectangle(img,(top_X,top_Y),(bot_X,bot_Y),(0,0,255),2)
        click_flag+=1
    else:
        pass
def validation_second(topx,topy,botx,boty):
    if(botx>topx+10 and boty>topy+10):
        return True
    else:
        return False
def validation_first(topx,topy,botx,boty):
    if(topx<botx-10 and topy<boty-10):
        return True
    else:
        return False
def edit_check(x,y):
    global top_X,top_Y,bot_X,bot_Y,edit_mode,img
    if (((x-top_X)**2+(y-top_Y)**2)**(0.5))<=10:
        cv2.circle(img, (top_X,top_Y), 3, (255, 0, 255), -1)
        return 1
    elif (((x-bot_X)**2+(y-bot_Y)**2)**(0.5))<=10:
        cv2.circle(img, (bot_X,bot_Y), 3, (255, 0, 255), -1)
        return 2
    else:
        return -1
def edit_click(x,y,point):
    global top_X,top_Y,bot_X,bot_Y,edit_mode,img
    if(point==1):
        top_X, top_Y = x,y
        cv2.circle(img, (x,y), 3, (0, 255, 0), -1)
        cv2.circle(img, (x,y), 10, (0,255,255),0,8,0)
        cv2.circle(img, (bot_X,bot_Y), 3, (0, 255, 0), -1)
        cv2.circle(img, (bot_X,bot_Y), 10, (0,255,255),0,8,0)
        cv2.rectangle(img,(x,y),(bot_X,bot_Y),(0,0,255),2)
        edit_mode=0
    elif(point==2):
        bot_X,bot_Y = x,y
        cv2.circle(img, (top_X,top_Y), 3, (0, 255, 0), -1)
        cv2.circle(img, (top_X,top_Y), 10, (0,255,255),0,8,0)
        cv2.circle(img, (x,y), 3, (0, 255, 0), -1)
        cv2.circle(img, (x,y), 10, (0,255,255),0,8,0)
        cv2.rectangle(img,(top_X,top_Y),(x,y),(0,0,255),2)
        edit_mode=0
    else:
        pass
def save_file(object):
    file = open('roi_file.txt','w')
    file.write(object + " (" + str(top_X) + "," + str(top_Y) + ")" +"," + "(" + str(bot_X) + "," + str(bot_Y) + ")")
def mouse_callback(event,x,y,flags,params):
    global top_X,top_Y,bot_X,bot_Y, click_flag, edit_mode,point,img
    temp_img = cv2.imread("img2.jpg")
    if(event==cv2.EVENT_LBUTTONDBLCLK and click_flag==0 and edit_mode==0):
        top_X=x
        top_Y=y
        selection(top_X,top_Y)
    elif(event==cv2.EVENT_LBUTTONDBLCLK and click_flag==1 and edit_mode==0):
        bot_X=x
        bot_Y=y
        selection(bot_X,bot_Y)
    else:
        pass
    if(event==cv2.EVENT_MBUTTONDOWN and click_flag==2 and edit_mode==0):
        point = edit_check(x,y)
        if(point>0):
            edit_mode = 1
        else:
            pass
    if(event==cv2.EVENT_LBUTTONDBLCLK and edit_mode==1):
        if(validation_first(x,y,bot_X,bot_Y) and point==1):
            img = temp_img
            edit_click(x,y,point)
        elif(validation_second(top_X,top_Y,x,y) and point==2):
            img = temp_img
            edit_click(x,y,point)
    else:
        pass
global top_X, top_Y, bot_X, bot_Y,point,img
point = -1
global edit_mode
edit_mode = 0
img = cv2.imread("img2.jpg")
cv2.namedWindow("ROI")
global click_flag
click_flag = 0
cv2.setMouseCallback("ROI",mouse_callback,img)
while(1):
    k =  cv2.waitKey(1) & 0xFF
    cv2.imshow("ROI",img)
    if(k==27):
        cv2.destroyAllWindows()
        break
object_name=input("What is the object name?")
save_file(object_name)
