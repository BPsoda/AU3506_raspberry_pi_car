import cv2
import numpy as np
im = np.zeros((2,2))
cv2.imshow(' ', im)
while 1:
    val = cv2.waitKey()    
    print('val == {}'.format(val))