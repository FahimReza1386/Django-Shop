from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Create your models here.


class ProductStatusType(models.IntegerChoices):
    publish= 1,("نمایش")
    draft= 2,("عدم نمایش")


class ProductCategoryModel(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



class ProductModel(models.Model):
    user= models.ForeignKey("accounts.User" , on_delete=models.PROTECT)
    category= models.ManyToManyField(ProductCategoryModel)
    title= models.CharField(max_length=255)
    slug= models.SlugField(allow_unicode=True)
    status= models.IntegerField(choices=ProductStatusType.choices, default=ProductStatusType.draft.value)
    descrption = models.TextField()
    image= models.ImageField(upload_to="product/img/", default="/default/product-image.png")
    brief_description= models.TextField(null=True, blank=True)
    stock= models.PositiveIntegerField(default=0)
    price= models.DecimalField(default=0, max_digits=10, decimal_places=0)  
    discount_percent = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return f'{self.title}'
    

    def get_price_after_sale(self):
        amount_price = self.price * Decimal(self.discount_percent / 100)
        price = self.price - amount_price
        return price
    

    def is_discounted(self):
        return self.discount_percent != 0
    



class ProductImageModel(models.Model):
    product=models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="product/extra-img/")

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)