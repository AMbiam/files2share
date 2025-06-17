from django.db import models
import os

from share.models.tools import *



class File(models.Model):
    title = models.CharField(max_length=80)
    filename = models.CharField(max_length=80) #Remove or Rename
    file = models.FileField(upload_to=user_directory_path, default='uploads/anonymous.jpg', validators=[validate_no_executable_files,validate_compressed_archive])
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files") 
    #New Attributes
    #filepath = models.CharField(max_length=120)
    icon = models.FileField(upload_to=user_public_upload_path, default='uploads/anonymous.jpg')

    #def save(self, *args, **kwargs):
        #self.filepath = user_directory_path(self, self.filename)
        #super(File, self).save(*args, **kwargs)

    '''
    Returns file path as a string.
    '''
    def get_FilePath(self):
        return self.file.name
    
    def get_FileIcon(self):
        #If file doesn't exist, turn generic icon object
        path = '/static/facebook.png' # TODO: Figure out how to make global variables for static and public paths.
        if os.path.exists(str(self.icon.name)):
            path = '/public/' + self.icon.name
        return path
    
    def get_ShareCount(self):
        # Inefficient because its dumping all the data into memory
        return len(self.access.all())