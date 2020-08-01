#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from skimage import io,transform
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 测试图片的地址
path1 = "E:/img_test/1.jpg"
path2 = "E:/img_test/2.jpg"
path3 = "E:/img_test/3.jpg"
path4 = "E:/img_test/4.jpg"
path5 = "E:/img_test/5.jpg"

flower_dict = {0:'dasiy',1:'dandelion',2:'roses',3:'sunflowers',4:'tulips'}

# resize图片(宽，高，通道数）
w = 100
h = 100
c = 3

# 读取图片
def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h))
    return np.asarray(img)

# 调用模型识别
with tf.Session() as sess:
    data = []
    data1 = read_one_image(path1)
    data2 = read_one_image(path2)
    data3 = read_one_image(path3)
    data4 = read_one_image(path4)
    data5 = read_one_image(path5)
    data.append(data1)
    data.append(data2)
    data.append(data3)
    data.append(data4)
    data.append(data5)

    saver = tf.train.import_meta_graph('E:/python/PycharmProject/flower_identification/model/model.ckpt.meta')
    saver.restore(sess,tf.train.latest_checkpoint('E:/python/PycharmProject/flower_identification/model'))

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    feed_dict = {x:data}

    logits = graph.get_tensor_by_name("logits_eval:0")

    classification_result = sess.run(logits,feed_dict)

    # 打印出预测矩阵
    print(classification_result)
    # 打印出预测矩阵每一行最大值的索引
    print(tf.argmax(classification_result,1).eval())
    # 根据索引通过字典对应花的分类
    output = []
    output = tf.argmax(classification_result,1).eval()
    for i in range(len(output)):
        plt.imshow(data[i])
        plt.show()
        print("第",i+1,"朵花预测:"+flower_dict[output[i]])


