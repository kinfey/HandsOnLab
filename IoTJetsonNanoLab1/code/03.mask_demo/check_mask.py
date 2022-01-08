
import tensorflow.keras
import numpy as np
import cv2
import time
import platform as plt

def get_label(label_path):

    label = {}
    with open(label_path) as f:
        for line in f.readlines():
            idx,name = line.strip().split(' ')
            label[int(idx)] = name
    return label


def main(win_title='test'):

    print('Setting ...')
    np.set_printoptions(suppress=True)

    print('Load Model & Labels ...')
    model = tensorflow.keras.models.load_model('tf/mymodel.model')
    label = get_label('tf/labels.txt')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    print('Start Stream ...')
    fps = -1
    stream = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=%d, height=%d, format=(string)NV12, framerate=(fraction)%d/1 !nvvidconv flip-method=%d ! nvvidconv ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! appsink' % (640, 480, 60,0, 640, 480)

    cap = cv2.VideoCapture(stream,cv2.CAP_GSTREAMER)
    while(True):

        t_start = time.time()

        ret, frame = cap.read()

        size = (224, 224)
        frame_resize = cv2.resize(frame, size)
        
        frame_norm = (frame_resize.astype(np.float32) / 127.0) - 1

        data[0] = frame_norm

        prediction = model.predict(data)[0]

        idx = int(np.argmax(prediction))

        result = '{} : {:.3f}, FPS {}'.format(label[idx], prediction[idx], fps)

        cv2.putText(frame, result, (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0 , 0, 255), 4)

        cv2.imshow(win_title, frame)

        if cv2.waitKey(1) == ord('q'):
            break

        fps = int(1/(time.time() - t_start))

    cap.release()
    cv2.destroyAllWindows()

    print('Quit ...')
	
if __name__=='__main__':

    main(plt.system()+' - Tensorflow')
