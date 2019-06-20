"""
neural network api of the alert system project.

Created by BrayanRojas0630, Elkin77, on June 2019.
Copyright (c) 2019 BrayanRojas0630, Elkin77 Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.
"""
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, StreamingHttpResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from network.models import Upload, Image, Processing, Alert
import os
from os.path import dirname, exists
from sys import argv
from zipfile import BadZipfile, ZipFile
from django.conf import settings
from django.utils.timezone import localtime
import json
import boto3
from threading import Thread
import tensorflow as tf
import os
import skimage
import numpy as np
from skimage import transform
from skimage.color import rgb2gray
import random
import matplotlib.pyplot as plt

class UploadImages(APIView):
    """
    This class
    """
    authentication_classes = (TokenAuthentication,)
    def post(self, request):
       
        file = request.FILES['file']
        file_name = file.name
        file_ext = file_name.split('.')

        new_upload = Upload()
        new_upload.file_name = file.name
        new_upload.output_file = file
        new_upload.create_at = datetime.now()
        new_upload.created_by_id = 4
        new_upload.save()
        pwd = None
        path_budrot = "%s%s/%s" %(settings.MEDIA_ROOT, 'cnnTesisTf','PlantVillage')
        path_testing = "%s/%s/%s" %(str(path_budrot),'Testing','1')
        for file in os.listdir(path_testing):
            file_path = "%s/%s" %(path_testing,file)
            os.remove(file_path)
        with ZipFile(new_upload.output_file) as f:
        	try:
        		f.extractall(path_testing)
        	except RuntimeError:
        		pwd = raw_input("Clave para %s: " % new_upload.output_file)
        		decompress(new_upload.output_file , pwd=pwd)
        for file in os.listdir(path_testing):
        	image_split = file.split(".")
        	if image_split[1] != 'zip':
        		new_image = Image()
        		new_image.image_name = image_split[0]
        		new_image.output_file = os.path.join(path_testing,file)
        		new_image.upload = new_upload
        		new_image.create_at = datetime.now()
        		new_image.created_by_id = 4
        		new_image.save()
        path_zip_remove = "%s%s" %(settings.MEDIA_ROOT , new_upload.output_file)
        print ("antes de borrar.......", path_zip_remove)
        os.remove(path_zip_remove)
        return HttpResponse("Success!")

status_validatefile={"0":"carga exitosa", "1":"Error","2":"En Procesamiento",
"3":"Finalizado", "4": "palma afectada"}

class GetUploadList(APIView):

    def post(self, request):
        data = request.data
        file_list = []
        upload_obj = Upload.objects.filter(status = True)
        for upload in upload_obj:
            obj = {}
            obj['id'] = upload.id
            obj['name'] = upload.file_name
            obj['creation_date'] = localtime(upload.create_at).strftime("%Y-%d-%m %I:%M %p")
            obj['status'] = self.parse_status_validatefile(upload.status_file)
            obj['username'] = upload.created_by.username
            file_list.append(obj)
        context = {
            'file_list':file_list
        }        
        return HttpResponse(json.dumps(context), content_type="application/json")

    def parse_status_validatefile(self, num):
    	if status_validatefile.get(str(num)):
    		return status_validatefile.get(str(num))
    	else:
    		return "Desconocido"


class RunThread(APIView):

    def post(self, request):
        data = request.data
        multi_start = data['multi_start']
        upload_objs = Upload.objects.filter(id = data['id'],
             status_file=0).first()
        if upload_objs:
            if multi_start == True:
                print (".................")
                status = self.multi_start(upload_objs)
            else:
                status = self.start(upload_objs)

        return HttpResponse(json.dumps({'status':status}), content_type="application/json")

    def multi_start(self, upload_objs):
        new_thread = ProcessingThread(upload_objs)
        new_thread.start()
        status = 'Hilo Lanzado'
        return status

    def start(self, upload_objs):
        processing_obj = Processing.objects.filter(thread_is_run = True)
        if processing_obj:
            status = 'Error, Hilo Ocupado'
        else:
            new_thread = ProcessingThread(upload_objs)
            new_thread.start()
            status = 'Hilo Lanzado'
        return status


class GetAlertList(APIView):
    def get(self, request):
        file_list = []
        alert_obj = Alert.objects.filter(status = True)
        for alert in alert_obj:
            obj = {}
            obj['id'] = alert.id
            obj['number'] = alert.number
            obj['context'] = alert.context
            obj['log'] = alert.log_aws
            obj['create_at'] = localtime(alert.create_at).strftime("%Y-%d-%m %I:%M %p")
            file_list.append(obj)
        
        context = {
            'file_list':file_list
        }
        return HttpResponse(json.dumps(context), content_type="application/json")


class ProcessingThread(Thread):
    def __init__ (self, upload):
        Thread.__init__(self)
        self.upload = upload

    def run(self):
        new_processing = Processing()
        new_processing.thread_is_run = True
        new_processing.upload = self.upload
        new_processing.create_at = datetime.now()
        new_processing.created_by_id = 4
        new_processing.save()
        path_extract = "%s%s/%s" %(settings.MEDIA_ROOT, 'cnnTesisTf','PlantVillage')
        print ("test1---------------", path_extract)
        path_testing = "%s/%s" %(str(path_extract),'Testing')
        print ("test2---------------", path_testing)
        path_training = "%s/%s" %(str(path_extract),'Testing')
        print ("test3---------------", path_training)
        self.upload.status_file = 2
        self.upload.save()
        self.start_neural_network(self.upload, path_extract, path_testing, path_training, new_processing)



    #Carga las imagenes dinamicamente de la carpeta con sus anotaciones
    def load_ml_data(self, data_directory):
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


    def start_neural_network(self, upload, path_extract, path_testing, path_training, new_processing):

        #Ruta de las carpetas donde se alojaran las imagenes para entrenamiento y para prueba
        main_dir = path_extract
        train_data_dir = path_testing
        test_data_dir = path_training

        #carga las imagenes y anotaciones en las dos variables
        images, labels = self.load_ml_data(train_data_dir)

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

        #sample_idx = random.sample(range(len(images30)), 16)
        #sample_images = [images30[i] for i in sample_idx]
        #sample_labels = [labels[i] for i in sample_idx]

        #prediction = sess.run([final_pred], feed_dict={x: sample_images})
        #Probar red neuronal

        test_images, test_labels = self.load_ml_data(test_data_dir)

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
        

        if porcentaje > 50:
            upload.status_file = 4
            alert_message = "%s %s %s %s" %("Se ha detectado PC, en el cultivo:",
                upload.file_name, "con una incidencia del", porcentaje)
            new_notify = Notify()
            new_notify.notify_send(alert_message)
        else:
            upload.status_file = 3
        message_processing = "%s %s %s %s %s %s" % ("Imagenes Afectadas:", numAffect,
            "Imagenes Sanas:",numSafe, "Porcentaje imagenes Afectadas:", porcentaje)
        upload.message_file = message_processing
        new_processing.context = message_processing
        new_processing.thread_is_run = False
        new_processing.save()
        upload.save()


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

class Notify(APIView):
    def notify_send(self, alert_message):
        new_alert = Alert()
        new_alert.number = "+573194036743"
        new_alert.context = alert_message 
        new_alert.create_at = datetime.now()
        new_alert.created_by_id = 4
        new_alert.save()
        try:
            client = boto3.client(
                "sns",
                aws_access_key_id=settings.AWSID,
                aws_secret_access_key=settings.AWSKEY,
                region_name="us-east-1"
            )
            # Send your sms message.
            response = client.publish(
                PhoneNumber="+573194036743",
                Message=alert_message
            )
        except:
            response = "Error en AWS"
        new_alert.log_aws = response
        new_alert.save()















