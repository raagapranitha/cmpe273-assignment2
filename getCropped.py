import cv2
WIDTH = 1000
HEIGHT = 1000


def click_event(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		print(str(x)+", "+str(y))

after = cv2.imread('rotatedImage.jpg')
cv2.namedWindow('after',cv2.WINDOW_NORMAL)
cv2.resizeWindow('after', WIDTH, HEIGHT)
cv2.imshow('after', after)
cv2.setMouseCallback('after',click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()

