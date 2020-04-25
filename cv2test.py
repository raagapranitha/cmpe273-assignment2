import cv2
from skimage.measure import compare_ssim
import numpy as np
from PIL import Image
WIDTH = 1000
HEIGHT = 1000

def getOption(xleft,yleft,w,h):
	new_dict ={}
	xcen = round((xleft+w/2))
	ycen =round((yleft+h/2))
	xright = xleft+w
	yright = yleft+h
	spaceY = 22
	xdist = 43
	x0 = 172
	y0=225
	for i in range(0,50):
		if yleft<ycen and (ycen < (h+y0+i*spaceY) and ycen <yright):
			break
	ques_no=i+1
	ans_options= {0:'A',1:'B',2:'C',3:'D',4:'E'}
	option = round((xleft-x0)/(xdist))
	new_dict[str(ques_no)] = ans_options[option]

	# xleft=188
	# yleft =231
	# yLen = 22
	# xDist = 43
	
	# new_dict ={}
	# ques_no = round((yAns-yleft)/(yLen))
	# print((yAns-yleft)/(yLen))
	# print(ques_no)
	# option = round((xAns-xleft)/(xDist))
	
	# for i in range(1,51):
	# 	if str(i) not in new_dict:
	# 		new_dict[str(i)] = '*'
	return new_dict

def isInAnswerRegion(x,y):
	xl=138
	yl=215
	xr=391
	yr=1295
	if xl<x<xr and yl<y<yr:
		return True
	return False



def getContours(img):

	print("In get contours")
	before = cv2.imread('scantron-100.jpg')
	after = cv2.imread(img)
	# cv2.namedWindow('before',cv2.WINDOW_NORMAL)
	# cv2.namedWindow('after',cv2.WINDOW_NORMAL)


	before_gray = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
	after_gray = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

	(score, diff) = compare_ssim(before_gray, after_gray, full=True)
	print("Image similarity", score)

	diff = (diff * 255).astype("uint8")
	im = Image.fromarray(diff)
	im.save("diff_image.jpeg")
	# diff.save("diff.jpg")

	thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = contours[0] if len(contours) == 2 else contours[1]

	mask = np.zeros(before.shape, dtype='uint8')
	filled_after = after.copy()
	ans={}

	i=0
	for c in contours:
	    area = cv2.contourArea(c)
	    
	    if area > 150 :
	        x,y,w,h = cv2.boundingRect(c)
	        if not isInAnswerRegion(x,y):
	        	continue
	        print("Before func call getOption")
	        # print(x,y,w,h)
	        ans.update(getOption(x,y,w,h))
	        print("after_func call get option")
	        cv2.rectangle(before, (x, y), (x + w, y + h), (36,255,12), 1)
	        cv2.rectangle(after, (x, y), (x + w, y + h), (36,255,12), 1)
	        cv2.drawContours(mask, [c], 0, (0,255,0), -1)
	        cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)
	        i+=1

	print(i)
	# cv2.imshow('before', before)
	# cv2.resizeWindow('before', WIDTH, HEIGHT)
	# cv2.imshow('after', after)
	# cv2.resizeWindow('after', WIDTH, HEIGHT)
	# cv2.imshow('diff',diff)
	# cv2.resizeWindow('diff', WIDTH, HEIGHT)
	# cv2.imshow('mask',mask)
	# cv2.resizeWindow('mask', WIDTH, HEIGHT)
	# cv2.imshow('filled after',filled_after)
	# cv2.resizeWindow('filled after', WIDTH, HEIGHT)
	# cv2.waitKey(0)
	print(ans)
	for i in range(1,51):
		if str(i) not in ans.keys():
			ans[str(i)]='*'
	print(ans)
	# cv2.destroyAllWindows()
	return ans

getContours('scantron_marked.jpg')

# cv2.imshow('thresh', thresh)
# cv2.resizeWindow('thresh', WIDTH, HEIGHT)







# def click_event(event,x,y,flags,param):
# 	if event == cv2.EVENT_LBUTTONDOWN:
# 		print(str(x)+", "+str(y))
# cv2.setMouseCallback('before',click_event)


# cv2.waitKey(0)
# table_coOrdinates(x1,y1) = 3242, 273
# table_coOrdinates(x2,y2) =5609, 914