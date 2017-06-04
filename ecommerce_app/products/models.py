from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify


class Product(models.Model):
    title = models.CharField(max_length = 120)
    product_id = models.CharField(max_length=120, unique=True, null = False, blank = False)
    description = models.TextField(blank = True, null = True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default = True,  verbose_name="Availability ?")
    manufacturer = models.CharField(max_length =120)

    def __str__(self):
        return str(self.title)

class Variation(models.Model):
    product = models.ForeignKey(Product)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20, null=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    active = models.BooleanField(default = True)
    inventory = models.IntegerField(null = True, blank = True)

    def __str__(self):
        return str(self.title)



def product_post_save(sender, instance, created, *args, **kwargs):
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = "Default"
        new_var.price = product.price
        new_var.save()

post_save.connect(product_post_save, sender=Product)

# ------------------------ images ------------------------------------------

def image_upload_to(instance, filename):
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
    return "products/%s/%s" %(slug, new_filename)


class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to = image_upload_to)

	def __str__(self):
		return self.product.title
