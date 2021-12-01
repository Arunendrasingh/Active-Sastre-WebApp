from decimal import Decimal
from django.db import models
from django.dispatch import receiver
# from django.db.models.base import Model
# from django.db.models.aggregates import Max
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
# from django.db.models.fields import TimeField
# from django.db.models.fields import DateTimeField
from django.dispatch.dispatcher import NO_RECEIVERS
# from django.db.models.fields.related import ForeignKey
# from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, integer_validator


from django.utils import tree

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=100, default="", null=True)
    img = models.ImageField(upload_to='product_categery')
    description = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self) -> str:
        return self.name

class Product_detail(models.Model):
    category = models.ForeignKey(category,default="", null=True ,on_delete=models.CASCADE)
    name = models.CharField((u"Product Name"), max_length=200)
    price = models.DecimalField(
        (u"Product Price"),
        decimal_places=2,
        null=True,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    new_price = models.DecimalField(
        (u"Aftr discount Price"),
        decimal_places=2,
        default=0,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    discount = models.IntegerField((u'Discount On Product in "%"'), null=True)
    total_num = models.IntegerField((u"Total Product"), null=True)
    best_for = models.CharField(max_length=200)
    thumbnail_image = models.ImageField(
        upload_to="Thumbnail Image", default=None, null=True
    )
    Specification = models.TextField()
    design_pattern = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True, null=True)


    def save(self, *args, **kwargs):
        if self.price:
            self.new_price = self.price - (self.price * self.discount) / 100
            super(Product_detail, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Product_Img(models.Model):
    product = models.ForeignKey(Product_detail, default=None, on_delete=CASCADE)
    image = models.ImageField((u"Product Image"), upload_to="Product_Img")
    date_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return self.product.name

    # def image_tag(self):
    #         return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.image))

    # image_tag.short_description = 'Image'


class Design(models.Model):
    name = models.CharField((u"Design Name"), max_length=150)
    type = models.CharField((u"Design Type"), max_length=150)
    specification = models.CharField((u"Specification"), max_length=200, null=True)
    thumbnail = models.ImageField(
        (u"Thumbnail Image"), upload_to="Design_Img", default=None
    )
    price = models.DecimalField(
        (u"Design Price"),
        decimal_places=2,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    product = models.ManyToManyField(Product_detail)
    date_time = models.DateTimeField(auto_now_add=True, null=True)


class Design_Img(models.Model):
    Design = models.ForeignKey(Design, default=None, on_delete=CASCADE)
    image = models.ImageField((u"Design Image"), upload_to="Design_Img")
    date_time = models.DateTimeField(auto_now_add=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField((u"Contact No"), max_length=30, blank=True)
    image = models.ImageField(upload_to="Profile_Img")
    date_time = models.DateTimeField(auto_now_add=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Referral(models.Model):
    user = models.OneToOneField(User,null=True, default=" ", on_delete=models.CASCADE)
    your_referral_id = models.CharField(null=True, max_length=150)
    is_shared = models.BooleanField(default=False)
    referral_id = models.CharField(max_length=150, null=True)
    share_by = models.IntegerField(null=True)
    is_applied = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    total_active_coin = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    used_time = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_referral(sender, instance, created, **kwargs):
        if created:
            Referral.objects.create(user=instance)
        else:
            Referral.objects.update_or_create(user=instance)

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name

    @receiver(post_save, sender=User)
    def save_user_referral(sender, instance, **kwargs):
        instance.referral.save()


class Bonus(models.Model):
    user = models.ForeignKey(User, null=True, default=" ", on_delete=models.CASCADE)
    product_detail = models.IntegerField(null=True)
    order_detail = models.IntegerField(null=True)
    total_order = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    bonus_price = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    bonus_on_product = models.CharField((u'Bonus On Product in (%)'), default="", max_length=10)
    date_of_order = models.DateTimeField(auto_now_add=True, null=True)
    date_of_delivery = models.DateTimeField(null=True)
    bonus_referr_to = models.IntegerField(null=True)
    delivery_status = models.BooleanField(default=False)
    is_added = models.BooleanField(default=False)
    total_bonus = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    def __str__(self) -> str:
        return self.user.first_name + " " + self.user.last_name

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    contact_no = models.CharField(max_length=20)
    pin_code = models.IntegerField()
    state = models.CharField(max_length=70)
    city = models.CharField(max_length=150)
    house_no = models.TextField()
    area_landmark = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True, null=True)


class MyCart(models.Model):
    cart_cost = models.CharField(max_length=20)
    user_id = models.IntegerField(default=1)
    product_id = models.IntegerField(default=1)
    design_id = models.IntegerField(default=1)
    prod_quantity = models.IntegerField(default=1)
    prod_amount = models.FloatField(default=0)
    design_amount = models.FloatField(default=0)
    totalamount = models.FloatField(default=0)


class Wishlist(models.Model):
    profile = models.ForeignKey(Product_detail, null=True, on_delete=models.CASCADE)
    user_id = models.IntegerField(null=True)
    product_id = models.IntegerField(null=True)
    design_id = models.IntegerField(null=True)


class size_detail(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField((u"Size Detail"), max_length=100)
    gender = models.CharField((u"Gender"), max_length=10)
    design_type = models.CharField((u"Design Type Of clothes"), max_length=50)
    date_time = models.DateTimeField(auto_now_add=True, null=True)


class blouse(models.Model):
    size_detail = models.ForeignKey(size_detail, null=True, on_delete=models.CASCADE)
    shoulders = models.FloatField()
    shouldersfull_lenght = models.FloatField()
    front_neck_depth = models.FloatField()
    chest_around = models.FloatField()
    waist_around = models.FloatField()
    back_neck_depth = models.FloatField()
    blouse_length = models.FloatField()
    sleeve_length = models.FloatField()
    sleeve_around = models.FloatField()
    armhole_around = models.FloatField()


class kurti(models.Model):
    size_detail = models.ForeignKey(size_detail, null=True, on_delete=models.CASCADE)
    dress_length = models.FloatField()
    sleev_length = models.FloatField()
    neckline = models.FloatField()
    upper_bust = models.FloatField()
    chest_bust = models.FloatField()
    stomach = models.FloatField()
    hip = models.FloatField()
    shoulder = models.FloatField()
    arm_hole = models.FloatField()
    waist = models.FloatField()
    thigh = models.FloatField()
    knee = models.FloatField()
    calf = models.FloatField()
    ankel_hem = models.FloatField()


class for_lahenga(models.Model):
    size_detail = models.ForeignKey(size_detail, null=True, on_delete=models.CASCADE)
    front_neck_depth = models.FloatField()
    around_bust = models.FloatField()
    neck_to_shoulder = models.FloatField()
    upper_waist = models.FloatField()
    blouse_length = models.FloatField()
    shoulder = models.FloatField()
    back_neck_depth = models.FloatField()
    around_armholes = models.FloatField()
    # around_arm = models.FloatField()
    sleeve_length = models.FloatField()
    waist = models.FloatField()
    hips = models.FloatField()
    waist_to_ankel = models.FloatField()
    full_body = models.FloatField()


class for_gown(models.Model):
    size_detail = models.ForeignKey(size_detail, null=True, on_delete=models.CASCADE)
    gown_length = models.FloatField()
    upper_chest = models.FloatField()
    chest = models.FloatField()
    waist = models.FloatField()
    stomach = models.FloatField()
    hips = models.FloatField()
    shoulder = models.FloatField()
    front_neck_depth = models.FloatField()
    sleeve_length = models.FloatField()
    sleeve_round = models.FloatField()
    arm_hole = models.FloatField()


class male_pantshirt(models.Model):
    size_detail = models.ForeignKey(size_detail, null=True, on_delete=models.CASCADE)
    p_length = models.FloatField()
    p_Waist = models.FloatField()
    p_Hips = models.FloatField()
    p_Thigh = models.FloatField()
    p_Knee = models.FloatField()
    p_Leg_Opening = models.FloatField()
    p_Crotch_Or_Rise = models.FloatField()
    p_In_Seam = models.FloatField()
    s_Shirt_lenght = models.FloatField()
    s_Sleeve_Length = models.FloatField()
    s_Shoulders = models.FloatField()
    s_Chest = models.FloatField()
    s_Overarm = models.FloatField()
    s_Waistcoat_Length = models.FloatField()
    s_Bicep_Loose = models.FloatField()
    s_Front_Chest = models.FloatField()
    s_Front_Stomach = models.FloatField()
    s_Front_Hips = models.FloatField()
    s_Wrist = models.FloatField()
    s_Neck = models.FloatField()
    date_time = models.DateTimeField(auto_now_add=True, null=True)


class Femail_size_Chart(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100,
        null=True,
    )
    gender = models.CharField(
        max_length=50,
        null=True,
    )
    dress_type = models.CharField(max_length=100, null=True)
    gown_length = models.FloatField()
    upper_chest = models.FloatField(null=True)
    chest = models.FloatField((u"Chest(Around)"))
    waist = models.FloatField((u"Waist(Around)"))
    upper_waist = models.FloatField()
    stomach = models.FloatField()
    hips = models.FloatField()
    shoulder = models.FloatField()
    front_neck_depth = models.FloatField()
    back_neck_depth = models.FloatField()
    neck_to_solider = models.FloatField()
    sleeve_length = models.FloatField()
    sleev_around = models.FloatField()
    around_bust = models.FloatField()
    blouse_length = models.FloatField()
    arm_hole = models.FloatField()
    waist_to_ankel_length = models.FloatField()
    full_body_lenght = models.FloatField()
    dress_length = models.FloatField()
    neck_line = models.FloatField()
    upper_bust = models.FloatField()
    chest_bust = models.FloatField()
    thigh = models.FloatField()
    knee = models.FloatField()
    calf = models.FloatField((u"Calf/Ankel"))
    ankel_hem = models.FloatField((u"Ankel Hem"), null=True)
    shoulder_full_lenght = models.FloatField()


class Oreder_Detail(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=CASCADE)
    review = models.BooleanField(default=False)
    user_name = models.CharField((u"User Name"), null=True, max_length=200)
    # address detail for specific order
    address_id = models.TextField(null=True)
    address = models.TextField(null=True)

    # Product detail
    Product_Id = models.IntegerField((u"Product Id"), null=True)
    pro_name = models.CharField((u"Product Name"), null=True, max_length=200)
    Product_quantity = models.IntegerField((u"Product Quantity"), null=True)
    Pro_price = models.DecimalField(
        (u"Product Price"),
        default=0,
        decimal_places=2,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    # Size Detail
    size_id = models.IntegerField(null=True)
    size_name = models.CharField(max_length=150, null=True)
    size_detail = models.TextField((u"Size Detail"), null=True)
    total_price = models.DecimalField(
        (u"Total Product~ Price"),
        null=True,
        decimal_places=2,
        max_digits=20,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    # Referal Status
    refral_status = models.BooleanField(default=False)
    # Status Of Product
    order_status = models.CharField((u"Order Status"), null=True, max_length=100)
    status = models.BooleanField((u"Delivered Or Not"), default=False)
    date_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return str(self.id) + " Ordered Product Name:-  " + self.pro_name

    def save(self, *args, **kwargs):
        if self.status:
            self.order_status = "Delivered"
            super(Oreder_Detail, self).save(*args, **kwargs)
        else:
            self.order_status = "Pending"
            super(Oreder_Detail, self).save(*args, **kwargs)


class user_feedback(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=CASCADE)
    order = models.ForeignKey(Oreder_Detail, null=True, on_delete=CASCADE)
    product = models.ForeignKey(Product_detail, default=None, on_delete=CASCADE)
    stiching_quality = models.IntegerField()
    product_quality = models.IntegerField()
    fitting_quality = models.IntegerField()
    liked = models.IntegerField()
    message = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True, null=True)