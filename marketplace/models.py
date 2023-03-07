from django.db import models
from django.conf import settings
import os
from django.core.validators import FileExtensionValidator


User = settings.AUTH_USER_MODEL

def marketplace_directory_path(instance, filename):
    banner_pic_name='marketplace/products/{0}/{1}'.format(instance.name, filename)
    full_path = os.path.join(settings.MEDIA_ROOT, banner_pic_name)

    if os.path.exists(full_path):
        os.remove(full_path)

    return banner_pic_name

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(blank=True, null=True, upload_to=marketplace_directory_path)
    
    #Slug es el URL que va a tener el producto
    slug = models.SlugField(unique=True)

    #si el producto es digital, colocamos esto para que la persona cuando lo pague, pueda descargar lo que haya comprado
    content_url = models.URLField(blank=True, null=True)
    # content_file = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    content_file = models.FileField(blank=True, null=True)

    #esto es para saber si el producto esta activo o modo draft
    active = models.BooleanField(default=False)
    
    #para saber el precio del producto (100 del default significa 1$)
    price = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name

    #hacer que se vea bonito el precio
    def price_display(self):
        return "{0:.2f}".format(self.price / 100)

#ya tenemos el producto, ahora ¿que pasa cuando compramos un producto? debemos tener otro modelo que sea cuando el producto ya es comprado

class PurchasedProduct(models.Model):
    #el email va a ser el del usuario que compro, este o no registrado en la pagina
    email = models.EmailField()
    #tambien queremos el producto por lo que se coloca
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #La fecha que fue comprado el producto
    date_purchased = models.DateTimeField(auto_now_add=True)

    #finalmente queremos ver el producto comprado por Email
    def __str__(self):
        return self.email
