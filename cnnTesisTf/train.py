"""
neural network train file of the alert system project.

Created by BrayanRojas0630, Elkin77, on June 2019.
Copyright (c) 2019 BrayanRojas0630, Elkin77 Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.
"""

import tensorflow as tf
import os
import skimage
import numpy as np
from skimage import transform
from skimage.color import rgb2gray
import random
import matplotlib.pyplot as plt

#Carga las imagenes dinamicamente de la carpeta con sus anotaciones
def load_ml_data(data_directory):
    dirs = [d for d in os.listdir(data_directory)
            if os.path.isdir(os.path.join(data_directory,d))]

    labels = []
    images = []

    for d in dirs:
        label_dir = os.path.join(data_directory, d)
        file_names = [os.path.join(label_dir, f)
                      for f in os.listdir(label_dir)
                      if f.endswith(".JPG")]

        for f in file_names:
            images.append(skimage.data.imread(f))
            labels.append(int(d))

    return images, labels

#Ruta de las carpetas donde se alojaran las imagenes para entrenamiento y para prueba
main_dir = "PlantVillage/"
train_data_dir = os.path.join(main_dir, "Training")
test_data_dir = os.path.join(main_dir, "Testing")

#carga las imagenes y anotaciones en las dos variables
images, labels = load_ml_data(train_data_dir)

images = np.array(images)
labels = np.array(labels)


#Como las imagenes no son del mismo tamaño, se convierten al mismo tamaño
w = 9999
h = 9999
for image in images:
    if image.shape[0] < h:
        h = image.shape[0]
    if image.shape[1] < w:
        w = image.shape[1]
print("Tamaño mínimo: {0}x{1}".format(h, w))

#transforma las imagenes a un tamaño 30x30
images30 = [transform.resize(image, (30,30)) for image in images]


#Convertir a escala de grises VERIFICAR SI DEJAR ESTO!!
images30 = np.array(images30)
images30 = rgb2gray(images30)


#CREACION DEL MODELO DE RED NEURONAL

#Creacion de los tensores
x = tf.placeholder(dtype=tf.float32, shape=[None, 30,30])
y = tf.placeholder(dtype=tf.int32, shape=[None])

#Clasificacion
images_flat = tf.contrib.layers.flatten(x)
logits = tf.contrib.layers.fully_connected(images_flat, 62, tf.nn.relu)

loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits))

train_opt = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

final_pred = tf.argmax(logits, 1)

accuracy = tf.reduce_mean(tf.cast(final_pred, tf.float32))


#ENTRENAMIENTO

tf.set_random_seed(1234)

sess = tf.Session()

sess.run(tf.global_variables_initializer())

for i in range(300):

    _, accuracy_val = sess.run([train_opt, accuracy],
                               feed_dict={
                                   x: images30,
                                   y: list(labels)
                               })

    _, loss_val = sess.run([train_opt, loss],
                               feed_dict={
                                   x: images30,
                                   y: list(labels)
                               })

    if i%10 == 0:
        print("Epoch", i)
        print("Efficacy: ", loss_val)
        print("Loss:", accuracy_val)



#Evaluacion de la red neuronal

sample_idx = random.sample(range(len(images30)), 16)
sample_images = [images30[i] for i in sample_idx]
sample_labels = [labels[i] for i in sample_idx]

prediction = sess.run([final_pred], feed_dict={x: sample_images})


#Probar red neuronal

test_images, test_labels = load_ml_data(test_data_dir)

test_images30 = [transform.resize(im,(30,30)) for im in test_images]

test_images30 = rgb2gray(np.array(test_images30))

prediction = sess.run([final_pred], feed_dict={x:test_images30})[0]

match_count = sum([int(l0 == lp) for l0, lp in zip(test_labels, prediction)])
match_count

#Eficacia
acc = match_count/len(test_labels)*100
print("Eficacia de la red neuronal: {:.2f}".format(acc))


#Imagenes que estan afectadas y sanas
numAffect = 0
numSafe = 0

for i in range(len(test_images30)):
    truth = test_labels[i]
    predi = prediction[i]
    if predi == 1:
        numAffect = numAffect + 1
    else:
        if predi == 2:
            numSafe = numSafe + 1


print("Imagenes Afectadas: ", numAffect)
print("Imagenes Sanas: ", numSafe)


#Porcentaje de imagenes afectadas
porcentaje = ((numAffect * 100) / len(test_images30))
print("Porcentaje imagenes Afectadas: {:.2f}".format(porcentaje))


"""
#Figuras graficas, si se puede mostrar esto al sistema dejarlo, de lo contrario dejar comentareado
plt.figure(figsize=(16,20))
for i in range(len(test_images30)):
    truth = test_labels[i]
    predi = prediction[i]
    plt.subplot(10,4,i+1)
    plt.axis("off")
    color = "green" if truth==predi else "red"
    plt.text(32,15, "Real:         {0}\nPrediccion:{1}".format(truth, predi),
            fontsize = 14, color = color)
    plt.imshow(sample_images[i], cmap="gray")
plt.show()
"""





















