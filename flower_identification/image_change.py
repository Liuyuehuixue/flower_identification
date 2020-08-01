from skimage import io,transform
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 测试图片的地址
path1 = "E:/img_test/2.jpg"

# resize图片(宽，高，通道数）
w = 100
h = 100
c = 3


# 读取图片
def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h))
    return np.asarray(img)

with tf.Session() as sess:
    data=[]
    data1 = read_one_image(path1)
    data.append(data1)
    plt.imshow(data1)
    plt.show()
    data2 = io.imread(path1)

    data3 = tf.image.random_brightness(data2,max_delta=0.1)
    plt.imshow(data3.eval())
    plt.show()



