"""
neural network model database of the alert system project.

Created by BrayanRojas0630, Elkin77, on June 2019.
Copyright (c) 2019 BrayanRojas0630, Elkin77 Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.
"""

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid


def create_path(instance, filename):
    """
    This method creates the path
    """
    year = instance.create_at.year
    month = instance.create_at.month
    day = instance.create_at.day
    return '/'.join([settings.PATH_IMAGES, str(year),
    str(month), str(day), str(instance.uuid), filename])

class Upload(models.Model):
    """
    Model to store image files
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=100)
    message_file = models.TextField(null=True)
    output_file = models.FileField(upload_to=create_path)
    create_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,
    	related_name="file_created_by")
    update_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE,
    	related_name="file_update_by")
    delete_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE,
    	related_name="file_delete_by")
    status = models.BooleanField(default=True)
    status_file = models.IntegerField(default=0)


class Image(models.Model):
    """
    Model to store image files
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    image_name = models.CharField(max_length=100)
    message_file = models.TextField(null=True)
    output_file = models.FileField(upload_to=create_path, max_length=500)
    upload = models.ForeignKey(Upload, on_delete = models.CASCADE,
        related_name="upload")
    create_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,
        related_name="image_created_by")
    update_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE,
        related_name="image_update_by")
    delete_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE,
        related_name="image_delete_by")
    status = models.BooleanField(default=True)
    status_file = models.IntegerField(default=0)


class Alert(models.Model):
    """
    Model to store image files
    """
    number = models.CharField(max_length = 100)
    context = models.TextField(null=True)
    create_at = models.DateTimeField()
    log_aws = models.TextField(null = True)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,
        related_name="alert_created_by")
    update_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE,
        related_name="alert_update_by")
    delete_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE,
        related_name="alert_delete_by")
    status = models.BooleanField(default=True)


class Processing(models.Model):
    """
    Model to store image files
    """
    thread_is_run = models.BooleanField(default = False)
    upload = models.ForeignKey(Upload, on_delete = models.CASCADE,
        related_name="thread_upload")
    context = models.TextField(null=True)
    create_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete = models.CASCADE,
        related_name="processing_created_by")
    update_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE,
        related_name="processing_update_by")
    delete_at = models.DateTimeField(null=True)
    deleted_by = models.ForeignKey(User, null=True, on_delete = models.CASCADE,
        related_name="processing_delete_by")
    status = models.BooleanField(default=True)