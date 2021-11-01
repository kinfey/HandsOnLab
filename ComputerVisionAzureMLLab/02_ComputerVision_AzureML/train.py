import tensorflow as tf
import numpy as np
import argparse
from sklearn.model_selection import train_test_split


from azureml.core.model import Model


def load_data (folder):
    import os
    import numpy as np
    import matplotlib.pyplot as plt

    c = 0
    features = []
    labels = np.array([])
    classnames = []
    for root, dirs, filenames in os.walk(folder):
        for d in dirs:
            classnames.append(d)
            files = os.listdir(os.path.join(root,d))
            for f in files:
                imgFile = os.path.join(root,d, f)
                img = plt.imread(imgFile)
                features.append(img)
                labels = np.append(labels, c)
            c = c + 1
    features = np.array(features)
    
    return features, labels, classnames



parser = argparse.ArgumentParser()
parser.add_argument('--data-folder', type=str, dest='data_folder', help='data folder mounting point')
args = parser.parse_args()
data_folder = args.data_folder
print('Data folder:', data_folder+'/image/')


features, labels, classnames = load_data(data_folder+'/image/')
features.shape

x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.30)

x_train = x_train.astype('float32')
x_train /= 255
x_test = x_test.astype('float32')
x_test /= 255

y_train = tf.keras.utils.to_categorical(y_train, len(classnames))
y_train = y_train.astype('float32')
y_test = tf.keras.utils.to_categorical(y_test, len(classnames))
y_test = y_test.astype('float32')


model = tf.keras.Sequential()
model.add(tf.keras.layers.Conv2D(32, (6, 6), input_shape=(x_train.shape[1], x_train.shape[2], x_train.shape[3]), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Conv2D(32, (6, 6), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Conv2D(32, (6, 6), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(len(classnames), activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
num_epochs = 20
history = model.fit(x_train, y_train, epochs=num_epochs, batch_size=64, validation_data=(x_test, y_test))



import tensorflow.keras.models

model_json = model.to_json()
with open("./outputs/starwars_model.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("./outputs/starwars_model.h5")
print("Saved model to disk")

