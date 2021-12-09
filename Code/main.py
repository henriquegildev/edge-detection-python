from cv2 import cv2
import numpy as np

"""
Fetch data
"""
sample = cv2.imread("TestImages/man.jpg", 0)

"""
Convolution Transform
TODO: Explain this code and write documentation
"""


def conv_transform(image):
    image_copy = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image_copy[i][j] = image[image.shape[0] - i - 1][image.shape[1] - j - 1]
    return image_copy


"""
Convolution
TODO: Explain this code and write documentation
"""


def conv(image, kernel_conv):
    kernel_conv = conv_transform(kernel_conv)
    image_h = image.shape[0]
    image_w = image.shape[1]

    kernel_h = kernel_conv.shape[0]
    kernel_w = kernel_conv.shape[1]

    h = kernel_h // 2
    w = kernel_w // 2

    image_conv = np.zeros(image.shape)
    for i in range(h, image_h - h):
        for j in range(w, image_w - w):
            sum_k = 0
            for m in range(kernel_h):
                for n in range(kernel_w):
                    sum_k = (sum_k + kernel_conv[m][n] * image[i - h + m][j - w + n])

            image_conv[i][j] = sum_k
    # cv2.imshow('Convolved_image', image_conv)
    return image_conv


"""
Normalization of data, fetches array from the image
"""


def norm(img1, img2):
    img_copy = np.zeros(img1.shape)
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            q = (img1[i][j] ** 2 + img2[i][j] ** 2) ** (1 / 2)  # G = sqrt(Gx^2 + Gy^2)
            if q > 220:  # Threshold
                img_copy[i][j] = 255  # Obtains a binary image
            else:
                img_copy[i][j] = 0
    return img_copy


# Set size (col, line) of Kernel. Matrix 3x3
kernel = np.zeros(shape=(3, 3))
# Set values of Kernel
# Matrix = [x,y]
# 1, 0, -1  | (0,0) ; (1,0) ; (2,0)
# 2, 0, -2  | (0,1) ; (1,1) ; (2,1)
# 1, 0, -1  | (0,2) ; (1,2) ; (2,2)

kernel[0, 0] = 1
kernel[0, 1] = 2
kernel[0, 2] = 1

kernel[1, 0] = 0
kernel[1, 1] = 0
kernel[1, 2] = 0

kernel[2, 0] = -1
kernel[2, 1] = -2
kernel[2, 2] = -1

gy = conv(sample, kernel)

# cv2.imshow("gradient_y", gy)

kernel[0, 0] = 1
kernel[0, 1] = 0
kernel[0, 2] = -1

kernel[1, 0] = 2
kernel[1, 1] = 0
kernel[1, 2] = -2

kernel[2, 0] = 1
kernel[2, 1] = 0
kernel[2, 2] = -1

gx = conv(sample, kernel)
# cv2.imshow("gradient_x", gx)
g_sobel = norm(gx, gy)
"""
Displays resulting image, destroys window on close.
"""
cv2.imshow("Sobel_edge", g_sobel)
cv2.waitKey(0)
cv2.destroyAllWindows()
