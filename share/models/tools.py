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
    if any([fileType in content.name.lower() for fileType in file_type_blacklist]):
        raise ValidationError("Unacceptable upload type.")
    
def validate_compressed_archive(content):
    if not any([fileType in content.name.lower() for fileType in file_type_compressedarchives]):
        raise ValidationError("Not an archive.")  


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

