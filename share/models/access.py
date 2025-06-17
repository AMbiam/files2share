from django.db import models
import os

from share.models.file import File

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

    