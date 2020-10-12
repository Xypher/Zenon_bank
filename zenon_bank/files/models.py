from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_str
import os

# Create your models here


content_type = {

    "pdf" : "application/pdf",
    "mp4" : "video/mp4",
    "mpeg" : "video/mpeg",
    "webm" : "video/webm",
    "gif" : "image/gif",
    "jpeg" : "image/jpeg",
    "jpg" : "image/jpeg",
    "png" :  "image/png",
    "mp3" : "audio/mp3",
    "wav" : "audio/wav",
}



class File(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="files")
    name = models.CharField(max_length=100 ,blank=True)
    file = models.FileField(upload_to='files/%Y/%m/%d/')
    upload_date = models.DateTimeField(auto_now_add=True)
    download_count= models.IntegerField(default=0)

    login_required_to_view = models.BooleanField(default=False)


    cat1_options = [

        'Computer',
        'Electrical',
        'Science'
    ]


    cat2_options = [

        'Logic',
        'Java',
        'Empedded',
        'Amplifier',
        'Antennas',
        'Calculus',
        'Chemistry 1',
    ]


    cat3_options = [

        'Calculus 1',
        'Calculus 2',
        'Calculus 3',
        'Java Lab',
        'Past Pappers',
        'TextBooks',
    ]


    #status options:
    accepted = "A",
    pending = "P",
    denied = "D"

    state = models.CharField(

        max_length=10,
        choices=(
            (str(accepted), "Accepted"),
            (str(pending), "Pending"),
            (str(denied), "Denied"),
        ), 
        default=denied
    )




    catagory1 = models.CharField(
        max_length=100,

        choices = [
            (cat, cat) for cat in cat1_options
        ],
        blank=True
    )


    catagory2 = models.CharField(
        max_length=100,

        choices = [
            (cat, cat) for cat in cat2_options
        ],
        blank=True
    )
    
    catagory3 = models.CharField(
        max_length=100,

        choices = [
            (cat, cat) for cat in cat3_options
        ],
        blank=True
    )

    description = models.TextField(blank=True)


    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension[1:]

    def filename(self):
        path = self.file.name
        return os.path.basename(path)

    def content_type(self):
        global content_type
        ext = self.extension()

        content = content_type[ext] if ext in content_type else "text/html"
        return content

    def file_type(self):
        global content_type
        ext = self.extension()
        file_type = content_type[ext][0:content_type[ext].find('/')] if ext in content_type else "others"

        return file_type

    def get_absolute_url(self):
        return "https://zenonbank.blob.core.windows.net/media/" + self.file.name





class StudentFavorateFile(models.Model):
    student = models.ForeignKey(to=User, on_delete=models.CASCADE ,related_name = "favorate_files")
    file = models.ForeignKey(to=File, on_delete=models.CASCADE)
        


        