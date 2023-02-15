from vision.ssd.vgg_ssd import create_vgg_ssd, create_vgg_ssd_predictor
from vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
from vision.ssd.mobilenetv1_ssd_lite import create_mobilenetv1_ssd_lite, create_mobilenetv1_ssd_lite_predictor
from vision.ssd.squeezenet_ssd_lite import create_squeezenet_ssd_lite, create_squeezenet_ssd_lite_predictor
from vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor
from vision.ssd.mobilenetv3_ssd_lite import create_mobilenetv3_large_ssd_lite, create_mobilenetv3_small_ssd_lite
from vision.utils.misc import Timer
import cv2
import sys
import yaml
import serial
import time
from playsound import playsound
import pyautogui
from screeninfo import get_monitors
from threading import Thread


class subProcess(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global execute
        global loopFlag
        global cursor_x, cursor_y
        execute = False
        while(loopFlag):
            if execute == True:
                pyautogui.moveTo(cursor_x, cursor_y, 1)
                execute = False
            time.sleep(0.1)


if len(sys.argv) < 1:
    print('Usage: python run_ssd_live_demo.py [dataset.yaml] [movie]')
    sys.exit(0)
yaml_dict = None
with open(sys.argv[1]) as f:
    yaml_dict = yaml.safe_load(f)
net_type = yaml_dict['net_type']
model_dir = yaml_dict['run']['model_dir']
model_path = model_dir + yaml_dict['run']['model']
label_path = model_dir + yaml_dict['run']['label']
# 引数はpython live.py json video

moniters = get_monitors()
moniter = moniters[0]
vrkSize = [640, 480]

if len(sys.argv) > 2:
    # cap = cv2.VideoCapture(sys.argv[4])  # capture from file
    # cap = cv2.VideoCapture(sys.argv[2])
    cap = cv2.VideoCapture(
        '')
else:
    # default = 0
    i = 0
    # cap = cv2.VideoCapture(i)   # capture from camera
    cap = cv2.VideoCapture(
        '')
    print(f"{i}:camera")
    cap.set(3, 1920)
    cap.set(4, 1080)

class_names = [name.strip() for name in open(label_path).readlines()]
num_classes = len(class_names)

if net_type == 'vgg16-ssd':
    net = create_vgg_ssd(len(class_names), is_test=True)
elif net_type == 'mb1-ssd':
    net = create_mobilenetv1_ssd(len(class_names), is_test=True)
elif net_type == 'mb1-ssd-lite':
    net = create_mobilenetv1_ssd_lite(len(class_names), is_test=True)
elif net_type == 'mb2-ssd-lite':
    net = create_mobilenetv2_ssd_lite(len(class_names), is_test=True)
elif net_type == 'mb3-large-ssd-lite':
    net = create_mobilenetv3_large_ssd_lite(len(class_names), is_test=True)
elif net_type == 'mb3-small-ssd-lite':
    net = create_mobilenetv3_small_ssd_lite(len(class_names), is_test=True)
elif net_type == 'sq-ssd-lite':
    net = create_squeezenet_ssd_lite(len(class_names), is_test=True)
else:
    print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
    sys.exit(1)
net.load(model_path)

if net_type == 'vgg16-ssd':
    predictor = create_vgg_ssd_predictor(net, candidate_size=200)
elif net_type == 'mb1-ssd':
    predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)
elif net_type == 'mb1-ssd-lite':
    predictor = create_mobilenetv1_ssd_lite_predictor(
        net, candidate_size=200)
elif net_type == 'mb2-ssd-lite' or net_type == "mb3-large-ssd-lite" or net_type == "mb3-small-ssd-lite":
    predictor = create_mobilenetv2_ssd_lite_predictor(
        net, candidate_size=200)
elif net_type == 'sq-ssd-lite':
    predictor = create_squeezenet_ssd_lite_predictor(
        net, candidate_size=200)
else:
    print("The net type is wrong. It should be one of vgg16-ssd, mb1-ssd and mb1-ssd-lite.")
    sys.exit(1)


if __name__ == '__main__':
    loopFlag = True
    subProcess = subProcess()
    subProcess.start()
    timer = Timer()
    img_count = 0
    b_count = 0
    c_count = 0
    fpsTm = cv2.TickMeter()
    fps = 0
    fps_count = 0
    fps_sum = 0
    start = time.perf_counter()
    flag = False
    fpsTm.start()
    pyautogui.FAILSAFE = False
    while True:
        ret, orig_image = cap.read()    # ret bool, orig_image frame
        if orig_image is None:
            continue
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        timer.start()
        boxes, labels, probs = predictor.predict(image, 10, 0.4)
        # interval = 0
        interval = timer.end()
        # Srial通信----------------------------------------------
        # ser.write(b'0')       #なにも検出していないとき0をバイト列でarduinoに送信
        # -------------------------------------------------------
        # 毎フレーム推論時間と検出オブジェクト数を表示するもの
        # print('Time: {:.2f}s, Detect Objects: {:d}.'.format(interval, labels.size(0)))
        # この辺でjsonに結果書き込みたい
        for i in range(boxes.size(0)):
            box = boxes[i, :]
            # print(f"{class_names[labels[i]]}: {probs[i]:.2f}, Time:{interval:.2f}")
            label = f"{class_names[labels[i]]}: {probs[i]:.2f}"
            if class_names[labels[i]] == "boar":
                b_count += 1
                flag = True
            if class_names[labels[i]] == "cervidae":
                c_count += 1
                flag = True
            cv2.rectangle(orig_image, (int(box[0]), int(
                box[1])), (int(box[2]), int(box[3])), (255, 255, 0), 4)

            cv2.putText(orig_image, label,
                        (int(box[0]+20), int(box[1]+40)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,  # font scale
                        (255, 0, 255),
                        2)  # line type
            if class_names[labels[i]] == "pa":
                cursor_x = (box[2]-box[0])/2+box[0] * \
                    (moniter.width/vrkSize[0])+moniter.x
                cursor_y = (box[3]-box[1])/2+box[1] * \
                    (moniter.width/vrkSize[0])+moniter.y
                execute = True
                # pyautogui.moveTo(x, y, 1)

        flag = False
        cv2.imshow('annotated', orig_image)
        if flag == True:
            cv2.imwrite("eval_results//result//" +
                        str(img_count).zfill(10)+".png", orig_image)
        img_count += 1
        flag = False
        # print(img_count)
        # if img_count == 4526:
        #     end = time.perf_counter()
        # print(end-start)
        # print("boar:"+str(b_count))
        # print("cervidae:"+str(c_count))
        if (img_count % 10) == 0:
            fpsTm.stop()
            fps = 10 / fpsTm.getTimeSec()
            fps_sum = fps_sum + fps
            fps_count = fps_count + 1
            end = time.perf_counter()
            fpsTm.reset()
            fpsTm.start()
            print("fps:"+str(fps)+" average:" +
                  str(fps_sum/fps_count)+" time:"+str(end-start))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    # ser.close()
    cv2.destroyAllWindows()
