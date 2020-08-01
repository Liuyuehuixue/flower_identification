from skimage import io,transform
import tensorflow as tf
from werkzeug.utils import secure_filename
import cv2
import time
import json
from datetime import timedelta
from flask import Flask, render_template, request, make_response, jsonify
from werkzeug.utils import secure_filename
import os
import base64

# 设置允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])

# 控制文件格式接口
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


path = "E:/python/PycharmProject/flower_identification/static/assets/img/upload_img/test.jpg"
model_path = "E:/python/PycharmProject/flower_identification/model/model.ckpt.meta"
flower_dict = {0:'dasiy',1:'dandelion',2:'roses',3:'sunflowers',4:'tulips'}

# 调用模型识别图片接口
def getType(path):
    w = 100
    h = 100
    c = 3
    img = io.imread(path)
    data = []
    data.append(transform.resize(img,(w,h,c)))

    with tf.Session() as sess1:
        saver = tf.train.import_meta_graph('E:/python/PycharmProject/flower_identification/model/model.ckpt.meta')
        saver.restore(sess1, tf.train.latest_checkpoint('E:/python/PycharmProject/flower_identification/model/'))
        graph = tf.get_default_graph()
        x = graph.get_tensor_by_name("x:0")
        feed_dict = {x: data}

        logits = graph.get_tensor_by_name("logits_eval:0")

        classification_result = sess1.run(logits, feed_dict)
        # 打印出预测矩阵每一行最大值的索引
        print(classification_result)
        output = tf.argmax(classification_result, 1).eval()

    return flower_dict[output[0]]


app = Flask(__name__)

# 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_ACE_DEFAULT'] = timedelta(seconds=1)

# 首页路由
@app.route('/')
def index():
    return render_template("index.html", data=None)


# 获取本机文件路由
@app.route('/local', methods=['GET', 'POST'])
def local():
    return render_template("local.html", data=None)


# 拍照路由
@app.route('/camera', methods=['GET', 'POST'])
def camera():
    cap = cv2.VideoCapture(0)
    flag = cap.isOpened()
    while (flag):
        ret, frame = cap.read()
        cv2.imshow("S:take a photo Q:exit", frame)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('s'):  # 按下s键，进入下面的保存图片操作
            cv2.imwrite("E:/python/PycharmProject/flower_identification/static/assets/img/upload_img/" + "test.jpg", frame)
            print(cap.get(3))
            print(cap.get(4))
            print("save" + "test.jpg successfuly!")
            print("-------------------------")
        elif k == ord('q'):  # 按下q键，程序退出
            break
    cap.release()
    cv2.destroyAllWindows()
    return render_template("upload_show.html", val1=time.time())


# 继续识别
@app.route('/continueUpload', methods=['GET', 'POST'])
def continueUpload():
    return render_template("index.html", data=None)


# 保存并显示图片
@app.route('/show', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        f = request.files['file']

        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        basepath = os.path.dirname(__file__)  # 当前文件所在路径

        upload_path = os.path.join(basepath, 'static/assets/img/upload_img', secure_filename(f.filename))

        f.save(upload_path)

        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/assets/img/upload_img', 'test.jpg'), img)

        return render_template('upload_show.html', val1=time.time())


# 识别
@app.route('/upload', methods=['GET', 'POST'])  # 添加路由
def upload():
    type = getType(path)
    res = "您想识别图片的类型是：" + type
    return json.dumps(res, ensure_ascii=False)


if __name__ == '__main__':
    app.run()