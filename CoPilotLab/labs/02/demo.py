#%%
# show image in a current foloder
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

#%%
# displaying a Matplotlib Image from current folder cat.jpeg
img = cv2.imread('cat.jpeg')
plt.imshow(img)
plt.show()


#%%
# make img a numpy array
img = cv2.imread('cat.jpeg')
img = np.array(img)
print(img.shape)

#%%
# Make img to black and white 
img = cv2.imread('cat.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(img, cmap='gray')
plt.show()


#%%
# resize img to 128*128
img = cv2.imread('cat.jpeg')
img = cv2.resize(img, (128, 128))
plt.imshow(img)
plt.show()







# %%
