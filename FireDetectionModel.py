from keras import backend as Keras_backend
from keras.layers import Conv2D
from keras.layers import Dense, Activation, Dropout
from keras.layers import Flatten
from keras.layers import MaxPooling2D
from keras.models import Sequential

img_width, img_height = 150, 150


def chose_input_shape():
    if Keras_backend.image_data_format() == 'channels_first':
        return (3, img_width, img_height)
    else:
        return (img_width, img_height, 3)


def load_model(model_name):
    input_shape = chose_input_shape()
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    model.load_weights(model_name)
    return model
