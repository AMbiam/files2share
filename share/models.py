from django.db import models
import os

# Create your models here.
from django.contrib.auth.models import User


#Dynamic Pathing for Saving files.
def user_directory_path(instance, filename):
    return 'uploads/user_{0}/{1}'.format(instance.user.username, filename)

def user_public_upload_path(instance, filename):
    return 'public/uploads/u{0}_{1}'.format(instance.user.username, filename)

class File(models.Model):
    title = models.CharField(max_length=80)
    filename = models.CharField(max_length=80) #Remove or Rename
    file = models.FileField(upload_to=user_directory_path, default='uploads/anonymous.jpg')
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
        return len(self.access.all())



class Access(models.Model):
    fileobj = models.ForeignKey(File, on_delete=models.CASCADE, related_name="access")
    filecode = models.CharField(max_length=12) #Change variable name to  Filecode
    accesscode = models.CharField(max_length=20) #Change variable name to accesscode
    attempts = models.IntegerField(default=3)
    attempt_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('filecode', 'accesscode')

    def get_Object(file,passcode):
        return Access.objects.filter(filecode=file).filter(accesscode=passcode).first()
    
    def get_FileObject(self):
        return self.fileobj
    
    def get_File(self):
        filepath = ''
        if self.attempts > self.attempt_count:
            filepath = self.fileobj.get_FilePath()
            self.countAttempt()
        
        return filepath
    
    def countAttempt(self):
        self.attempt_count = self.attempt_count + 1
        self.save()

    
