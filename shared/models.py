from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name= "Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
    class Meta:
        abstract = True

class Contact(BaseModel):
    full_name = models.CharField(
        max_length=100,
        verbose_name="Full Name")
    email = models.EmailField(
        verbose_name="Email"
    )
    subject = models.CharField(
       max_length=255,
        verbose_name="Subject"
    )
    message = models.TextField(
       verbose_name="Message"
   )
    is_read = models.BooleanField(
       default=False,
       verbose_name="Is Read"
   )
    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'contacts'
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"