from django.db import models
import os

# Create your models here.
from django.contrib.auth.models import User
# for throwing exceptions
from django.core.exceptions import ValidationError


file_type_executables = [".exe", ".php", ".bsh", ".sh", ".ksh", ".py"]
file_type_compressedarchives = [".zip", ".tar", ".tar.gz"]
file_type_images = [".png", ".jpeg", ".jpg"]
file_type_blacklist = []+file_type_executables
file_type_whitelist = []

def validate_no_executable_files(content):
    if any([fileType in content.lower() for fileType in file_type_blacklist]):
        raise ValidationError("Unacceptable upload type.")


def hex_to_int(value):
    if value is None:
        return None
    return int(value, 16)

def int_to_hex(value):
    hexValue = format(value,"X")
    hexValue = '0'*(6-len(hexValue)) + hexValue
    return hexValue

#Dynamic Pathing for Saving files.
def user_directory_path(instance, filename):
    return 'uploads/user_{0}/{1}'.format(instance.user.username, filename)

def user_public_upload_path(instance, filename):
    return 'public/uploads/u{0}_{1}'.format(instance.user.username, filename)

#Custom Field Class
class RGBColorField(models.CharField):
    description = "A field holding RGB colors" #How to write a class description
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 6 #Set Maximum length to 6
        self.validators = []
        self.validators.append(self.validate_all_values_hex)
        super().__init__(*args, **kwargs)

    def validate_all_values_hex(self, value):
        try:
            hex_to_int(value)
        except:
            raise ValidationError("{} - Not a hex value.".format(value))
        
    #Database functions may be problematic based on type of database.
    def db_type(self, connection):
        return 'UNSIGNED INTEGER(3)'
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return None
        return int_to_hex(value)

    def get_prep_value(self, value):
        return hex_to_int(value)



class File(models.Model):
    title = models.CharField(max_length=80)
    filename = models.CharField(max_length=80) #Remove or Rename
    file = models.FileField(upload_to=user_directory_path, default='uploads/anonymous.jpg', validators=[validate_no_executable_files])
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
        if self.attemptAvailable():
            filepath = self.fileobj.get_FilePath()
            self.countAttempt()
        
        return filepath
    
    def countAttempt(self):
        self.attempt_count = self.attempt_count + 1
        self.save()

    def attemptAvailable(self):
        return self.attempts > self.attempt_count

    
