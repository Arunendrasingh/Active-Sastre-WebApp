from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


from typing import OrderedDict
from django.http.response import HttpResponseRedirect

# from django.http.response import HttpResponse
from django.shortcuts import render, redirect

# from django.http import request
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from main_app.models import (
    Address,
    Femail_size_Chart,
    Oreder_Detail,
    Product_detail,
    Profile,
    male_pantshirt,
    Product_Img,
    MyCart,
    Wishlist,
    blouse,
    for_gown,
    for_lahenga,
    kurti,
    size_detail,
    user_feedback,
)
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q


# Create your views here.


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:  # to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


def index(request):
    get_product = Product_detail.objects.all()
    for product in get_product:
        productprice = int(product.price)
        total_price = productprice - (int(productprice) * int(product.discount)) / 100
        # actual_price.append(productprice - total_price)
        product.new_price = total_price
        product.save()
    All_detail = {
        "product": get_product,
    }
    return render(request, "index.html", All_detail)


def all_product(request):
    get_product = Product_detail.objects.all()[::-1]
    return render(request, "all_product.html", {"all_product": get_product})


def about(request):
    return render(request, "about.html")


@login_required(login_url="/login")
def checkout(request, p_id):
    user_obj = Profile.objects.get(id=request.user.id)
    address_obj = Address.objects.filter(user=user_obj.id)
    product_obj = Product_detail.objects.filter(id=p_id)[0]
    get_size = size_detail.objects.filter(user=request.user)
    cart_obj = MyCart.objects.filter(product_id=p_id)[0]
    main_info = {
        "address": address_obj,
        "product_obj": product_obj,
        "size": get_size,
        "cart_obj": cart_obj,
    }
    return render(request, "checkout.html", main_info)


@login_required(login_url="/login")
def place_order(request):
    if request.method == "POST":
        cart_id = request.POST["cart_id"]
        address = request.POST["address"]
        size = request.POST["size"]
        value = size.split()
        prod_id = request.POST["prod_id"]
        prod_name = request.POST["prod_name"]
        prod_price = request.POST["prod_price"]
        total_product = request.POST["product_num"]
        total_price = request.POST["total_price"]
        user_name = request.POST["user_name"]
        user = request.user.first_name + "  " + request.user.last_name
        size_obj = size_detail.objects.filter(id=value[0])[0]
        if value[1] == "female":
            if size_obj.design_type == "blouse":
                design_det = blouse.objects.filter(size_detail=size_obj)[0]
                size_data = (
                    "Blouse Front"
                    + "Shoulder:-"
                    + str(design_det.shoulders)
                    + ", Shoulder Full Lenght:-"
                    + str(design_det.shouldersfull_lenght)
                    + ", Front Neck Depth:-"
                    + str(design_det.front_neck_depth)
                    + ", Chest (Around):-"
                    + str(design_det.chest_around)
                    + ", Waist (Around):-"
                    + str(design_det.waist_around)
                    + "Blouse Back"
                    + ", Back Neck Depth:-"
                    + str(design_det.back_neck_depth)
                    + ", Blouse Length:-"
                    + str(design_det.blouse_length)
                    + ", Sleeve Length:-"
                    + str(design_det.sleeve_length)
                    + ", Sleeve Around:-"
                    + str(design_det.sleeve_around)
                    + ", Armhole(around):-"
                    + str(design_det.armhole_around)
                )
            elif size_obj.design_type == "kurti":
                design_det = kurti.objects.filter(size_detail=size_obj)[0]
                size_data = (
                    "Upper Side"
                    + "Dress Length:-"
                    + str(design_det.dress_length)
                    + ", Sleeve Length:-"
                    + str(design_det.sleev_length)
                    + ", Neckline:-"
                    + str(design_det.neckline)
                    + ", Upper Bust:-"
                    + str(design_det.upper_bust)
                    + ", Chest/Bust:-"
                    + str(design_det.chest_bust)
                    + ", Stomach:-"
                    + str(design_det.stomach)
                    + ", Hips:-"
                    + str(design_det.hip)
                    + ", Shoulder:-"
                    + str(design_det.shoulder)
                    + ", Arm Hole:-"
                    + str(design_det.arm_hole)
                    + ", Waist:-"
                    + str(design_det.waist)
                    + "Lower Side"
                    + ", Thigh:-"
                    + str(design_det.back_neck_depth)
                    + ", Knee:-"
                    + str(design_det.blouse_length)
                    + ", Calf:-"
                    + str(design_det.sleeve_length)
                    + ", Ankel Hem:-"
                    + str(design_det.sleeve_around)
                )
            elif size_obj.design_type == "lahenga":
                design_det = for_lahenga.objects.filter(size_detail=size_obj)[0]
                size_data = (
                    "Blouse Measurement"
                    + "Front Neck Depth:-"
                    + str(design_det.front_neck_depth)
                    + ", Around Bust:-"
                    + str(design_det.around_bust)
                    + ", Neck to Shoulder:-"
                    + str(design_det.neck_to_shoulder)
                    + ", Upper Waist:-"
                    + str(design_det.upper_waist)
                    + ", Blouse Length:-"
                    + str(design_det.blouse_length)
                    + ", Shoulder:-"
                    + str(design_det.shoulder)
                    + ", Back Neck Depth:-"
                    + str(design_det.back_neck_depth)
                    + ", Shoulder:-"
                    + str(design_det.shoulder)
                    + ", Around Arm Hole:-"
                    + str(design_det.around_armholes)
                    + ", Sleeve Length:-"
                    + str(design_det.sleeve_length)
                    + "Lahenga Measurement"
                    + ", Waist:-"
                    + str(design_det.waist)
                    + ", Hips:-"
                    + str(design_det.hips)
                    + ", Waist to Ankel Length:-"
                    + str(design_det.waist_to_ankel)
                    + ", Full Body:-"
                    + str(design_det.full_body)
                )
            elif size_obj.design_type == "gown":
                design_det = for_gown.objects.filter(size_detail=size_obj)[0]
                size_data = (
                    "All Measurement"
                    + ", Gown Length:-"
                    + str(design_det.gown_length)
                    + ", Upper Chest:-"
                    + str(design_det.upper_chest)
                    + ", Chest:-"
                    + str(design_det.chest)
                    + ", Waist:-"
                    + str(design_det.waist)
                    + ", Stomach:-"
                    + str(design_det.stomach)
                    + ", Hips:-"
                    + str(design_det.hips)
                    + ", Shoulder:-"
                    + str(design_det.shoulder)
                    + "Front Neck Depth:-"
                    + str(design_det.front_neck_depth)
                    + ", Sleeve Length:-"
                    + str(design_det.sleeve_length)
                    + ", Sleeve Round:-"
                    + str(design_det.sleeve_round)
                    + ",Arm Hole:-"
                    + str(design_det.arm_hole)
                )
        else:
            if size_obj.design_type == "pantshirt":
                design_det = male_pantshirt.objects.filter(size_detail=size_obj)[0]
                size_data = (
                    "Paint Length:-"
                    + str(design_det.p_length)
                    + ", Paint Waist:-"
                    + str(design_det.p_Waist)
                    + ", Paint Hips:-"
                    + str(design_det.p_Hips)
                    + ", Paint Thigh:-"
                    + str(design_det.p_Thigh)
                    + ", Knee:-"
                    + str(design_det.p_Knee)
                    + ", Leg Opening:-"
                    + str(design_det.p_Leg_Opening)
                    + ", Crotch/Rise:-"
                    + str(design_det.p_Crotch_Or_Rise)
                    + ", In-Seam:-"
                    + str(design_det.p_In_Seam)
                    + ", Shirt Length:-"
                    + str(design_det.s_Shirt_lenght)
                    + ", Sleeve Length:-"
                    + str(design_det.s_Sleeve_Length)
                    + ", Shoulders:-"
                    + str(design_det.s_Shoulders)
                    + ", Chest:-"
                    + str(design_det.s_Chest)
                    + ", Overarm:-"
                    + str(design_det.s_Overarm)
                    + ", Waistcoat Length:-"
                    + str(design_det.s_Waistcoat_Length)
                    + ", Bicep(Loose):-"
                    + str(design_det.s_Bicep_Loose)
                    + ", Chest:-"
                    + str(design_det.s_Front_Chest)
                    + ", Stomach:-"
                    + str(design_det.s_Front_Stomach)
                    + ", Front - Hip:-"
                    + str(design_det.s_Front_Hips)
                    + ", Wrist:-"
                    + str(design_det.s_Wrist)
                    + ", Neck:-"
                    + str(design_det.s_Neck)
                )

        obj_order = Oreder_Detail(
            user_id=request.user.id,
            user_name=user_name,
            address=address,
            Product_Id=prod_id,
            pro_name=prod_name,
            Product_quantity=total_product,
            Pro_price=prod_price,
            size_id=int(value[0]),
            size_name=(size_obj.design_type).upper(),
            size_detail=size_data,
            total_price=total_price,
            order_status="pending",
        )
        obj_order.save()
        if obj_order.save:
            # mail for order detail to user
            subject = "Regarting to Product Order On Active Sastre"
            message = f"Dear  \"{user}\" Your Order For Product '{prod_name}' has been placed successfully."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = (request.user.email,)
            send_mail(subject, message, email_from, recipient_list)
            # end mail
            cart_obj = MyCart.objects.filter(id=cart_id)[0]
            cart_obj.delete()
        messages.info(
            request,
            "Your Order For Product" + prod_name + "has been placed successfully!",
        )
        return redirect("/cart")
    else:
        return redirect("/cart")


def product(request, pid):
    Product_info = Product_detail.objects.filter(id=pid)[0]
    prod_img = Product_Img.objects.filter(product=Product_info)
    rateing_obj = user_feedback.objects.filter(product=Product_info)
    get_product = Product_detail.objects.all()[::-1]
    deatils = {
        "product_info": Product_info,
        "all_product": get_product,
        "pro_img": prod_img,
        "rateing_obj": rateing_obj,
    }
    return render(request, "product.html", deatils)


@login_required(login_url="/login")
def profile(request):
    get_address = Address.objects.filter(user=request.user)
    get_size = size_detail.objects.filter(user=request.user)
    get_user = User.objects.filter(id=request.user.id)[0]
    get_profile = Profile.objects.filter(user=get_user)[0]
    pass_data = {
        "totaladdress": len(get_address),
        "address": get_address,
        "totalsize": len(get_size),
        "size": get_size,
        "get_user": get_user,
        "get_profile": get_profile,
    }
    return render(request, "profile.html", pass_data)


@login_required(login_url="/login")
def add_to_wishlist(request, p_id):
    if Wishlist.objects.filter(product_id=p_id, user_id=request.user.id).exists():
        messages.info(request, "Product is already in Wishlist!")
        return redirect("/wishlist")
    else:
        wish_obj = Wishlist(product_id=p_id, user_id=request.user.id)
        wish_obj.save()
        messages.info(request, "Product is Successfully! Add to your Wishlist")
        return redirect("/wishlist")


@login_required(login_url="/login")
def delete_from_wishlist(request, w_id):
    wishlist_item = Wishlist.objects.filter(id=w_id)[0]
    wishlist_item.delete()
    messages.info(request, "Product is successfully! Deleted From your Wishlist")
    return redirect("/wishlist")


@login_required(login_url="/login")
def wishlist(request):
    wishlist = Wishlist.objects.filter(user_id=request.user.id)
    num_wishlist = len(wishlist)
    prods = []
    for wishlist1 in wishlist:
        Product_id = wishlist1.product_id
        # design_id = wishlist.design_id
        prods.append(
            {
                "product_detail": Product_detail.objects.filter(id=Product_id)[0],
                "wishlist": wishlist1,
            }
        )

    return render(
        request, "wishlist.html", {"Product_Detail": prods, "num_wish": num_wishlist}
    )


@login_required(login_url="/login")
def cart(request):
    cart_obj = MyCart.objects.filter(user_id=request.user.id)
    prods = []
    for cart in cart_obj:
        if Product_detail.objects.filter(id=cart.product_id).exists():
            prods.append(
                {
                    "prods": Product_detail.objects.filter(id=cart.product_id)[0],
                    "cartdtls": cart,
                }
            )
    n_cartprods = len(cart_obj)
    carttotal = 0
    for item in cart_obj:
        carttotal += item.prod_amount
    return render(
        request,
        "cart.html",
        {"product": prods, "ncart": n_cartprods, "total_price": carttotal},
    )


@login_required(login_url="/login")
def add_to_cart(request, pid):
    pro_detail = Product_detail.objects.filter(id=pid)[0]
    pro_id = pro_detail.id
    pro_amount = pro_detail.new_price
    user_id = request.user.id
    if MyCart.objects.filter(product_id=pid, user_id=user_id).exists():
        prods1 = MyCart.objects.filter(product_id=pid)
        for item in prods1:
            if item in prods1:
                quantity = item.prod_quantity + 1
                item.prod_quantity = quantity
                item.prod_amount = quantity * pro_detail.new_price
                item.save()
        messages.info(
            request, "One more Product" + pro_detail.name + " added to your cart"
        )
        return redirect("/cart")
    else:
        cart_obj = MyCart(user_id=user_id, prod_amount=pro_amount, product_id=pid)
        cart_obj.save()
        messages.info(request, pro_detail.name + " added to your cart")
        return redirect("/cart")


@login_required(login_url="/login")
def incresequantity(request, cid):
    cartitem = MyCart.objects.filter(id=cid)[0]
    prod = Product_detail.objects.filter(id=cartitem.product_id)[0]
    quantity = cartitem.prod_quantity + 1
    cartitem.prod_quantity = quantity
    cartitem.prod_amount += float(prod.new_price)
    cartitem.save()
    return redirect("/cart")


@login_required(login_url="/login")
def decresequantity(request, cid):
    cartitem = MyCart.objects.filter(id=cid)[0]
    prod = Product_detail.objects.filter(id=cartitem.product_id)[0]
    quantityold = cartitem.prod_quantity
    if quantityold > 1:
        quantity = quantityold - 1
        cartitem.prod_quantity = quantity
        cartitem.prod_amount = quantity * prod.new_price
        cartitem.save()
    else:
        cartitem.delete()
    return redirect("/cart")


def contact(request):
    return render(request, "contact.html")


def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # login(request, user)
            messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
            return redirect('/')
            # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')
class user_profile:

    def signup(request):
        if request.method == "POST":
            first_name = request.POST["fname"].capitalize()
            last_name = request.POST["lname"].capitalize()
            phone = request.POST["phone"]
            user_email = request.POST["email"]
            user_password1 = request.POST["pass"]
            user_password2 = request.POST["conpass"]
            if user_password1 == user_password2:
                if User.objects.filter(
                    Q(username__iexact=user_email) | Q(email__iexact=user_email)
                ).exists():
                    messages.success(request, "User Name Or Email  already registerd")
                    return redirect("/signup")
                elif Profile.objects.filter(phone=phone).exists():
                    messages.success(request, "Phone number is already registerd")
                    return redirect("/signup")
                else:
                    user = User.objects.create_user(
                        username=user_email,
                        first_name=first_name,
                        last_name=last_name,
                        email=user_email,
                        is_active = False,
                        password=user_password2,
                    )
                    user.save()
                    user_profile = Profile.objects.get(user=user)
                    user_profile.phone = phone
                    user_profile.save()

                    """Code for sending verification link to user"""
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your blog account.'
                    message = render_to_string('acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token':account_activation_token.make_token(user),
                    })
                    to_email = user_email
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return HttpResponse('Please confirm your email address to complete the registration')
                    # subject = "welcome to Active Sastre"
                    # message = (
                    #     f"Hi {first_name}, thank you for registering in Active Sastre."
                    # )
                    # email_from = settings.EMAIL_HOST_USER
                    # recipient_list = [
                    #     user_email,
                    # ]
                    # send_mail(subject, message, email_from, recipient_list)
                    messages.success(request, "Yor are registerd successfully")
                    return redirect("/login")
            else:
                messages.warning(request, "Password is not matching")
                return redirect("/signup")
        else:
            return render(request, "signup.html")

    @login_required(login_url="/login")
    def change_profile(request, id):
        if request.method == "POST":
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            user_pro = User.objects.get(id=id)
            # get_profile = Profile.objects.get(user=user_pro)
            user_pro.first_name = fname
            user_pro.last_name = lname
            user_pro.save()
            messages.success(request, "Your Profile Is saved successfully!")
            return redirect("/profile")
        else:
            return redirect("/profile")


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            USER_ID = request.POST["username"]
            password = request.POST["pass"]
            user = auth.authenticate(username=USER_ID, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Invalid Username or Password")
                return redirect("/login")
        else:
            return render(request, "login.html")


@login_required(login_url="/login")
def logout(request):
    auth.logout(request)
    return redirect("/")


class address:
    @login_required(login_url="/login")
    def SaveAddress(request):
        if request.method == "POST":
            name = request.POST["addname"]
            mobile = request.POST["mobile"]
            pin = request.POST["pin"]
            state = request.POST["state"]
            city = request.POST["city"]
            house_no = request.POST["house_no"]
            area = request.POST["area"]
            user_pro = User.objects.filter(id=request.user.id)[0]
            addresss_info = Address(
                user=user_pro,
                name=name,
                contact_no=mobile,
                pin_code=pin,
                state=state,
                city=city,
                house_no=house_no,
                area_landmark=area,
            )
            addresss_info.save()
            messages.info(request, "Address is Added Successfully!")
            return redirect("/profile")
        else:
            return redirect("/profile")

    @login_required(login_url="/login")
    def change_address(request, id):
        if request.method == "POST":
            try:
                address = Address.objects.get(user=request.user.id, id=id)
                address.name = request.POST["addname"]
                address.contact_no = request.POST["mobile"]
                address.pin_code = request.POST["pin"]
                address.state = request.POST["state"]
                address.city = request.POST["city"]
                address.house_no = request.POST["house_no"]
                address.area_landmark = request.POST["area"]
                address.save()
                messages.info(request, "Address is Changed Successfully!")
                return redirect("/profile")
            except:
                messages.info(request, "No Address Found!")
                return redirect("/profile")
        else:
            return redirect(request.META["HTTP_REFERER"])

    @login_required(login_url="/login")
    def delete_address(request, id):
        del_size = Address.objects.get(user=request.user, id=id)
        del_size.delete()
        messages.info(request, "Address is Deleted Successfully!")
        return redirect(request.META["HTTP_REFERER"])


def add_size(request):
    if request.method == "POST":
        paint_length = request.POST["werw"]
    else:
        return render(request, "size_m.html")


class size:
    @login_required(login_url="/login")
    def addsize(request):
        def getsizeobj(_user_obj, _name, _gender, _design):
            obj_size = size_detail.objects.filter(
                user=_user_obj, name=_name, gender=_gender, design_type=_design
            )[0]
            return obj_size

        if request.method == "POST":
            user_obj = User.objects.filter(id=request.user.id)[0]
            if size_detail.objects.filter(
                user=user_obj,
                name=request.POST["name"],
                gender=request.POST["gender"],
                design_type=request.POST["design"],
            ).exists():
                messages.info(request, "Size is already exists!")
                redirect(request.META["HTTP_REFERER"])
            else:
                size_obj = size_detail(
                    user=user_obj,
                    name=request.POST["name"],
                    gender=request.POST["gender"],
                    design_type=request.POST["design"],
                )
                size_obj.save()
                if request.POST["gender"] == "female":
                    if request.POST["design"] == "blouse":
                        obj_size = getsizeobj(
                            user_obj,
                            request.POST["name"],
                            request.POST["gender"],
                            request.POST["design"],
                        )
                        design_size = blouse(
                            size_detail=obj_size,
                            shoulders=request.POST["shoulder"],
                            shouldersfull_lenght=request.POST["shoulder_full_lenght"],
                            front_neck_depth=request.POST["front_neck_depth"],
                            chest_around=request.POST["chest_around"],
                            waist_around=request.POST["waist_around"],
                            back_neck_depth=request.POST["back_neck_depth"],
                            blouse_length=request.POST["blouse_length"],
                            sleeve_length=request.POST["sleeve_length"],
                            sleeve_around=request.POST["sleeve_around"],
                            armhole_around=request.POST["arm_hole_around"],
                        )
                        design_size.save()
                        messages.info(
                            request, "Female Size for blouse is added Successfully!"
                        )
                        return redirect("/profile")
                    elif request.POST["design"] == "kurti":
                        obj_size = getsizeobj(
                            user_obj,
                            request.POST["name"],
                            request.POST["gender"],
                            request.POST["design"],
                        )
                        kurti_size = kurti(
                            size_detail=obj_size,
                            dress_length=request.POST["dress_length"],
                            sleev_length=request.POST["sleeve_length"],
                            neckline=request.POST["neck_line"],
                            upper_bust=request.POST["upper_bust"],
                            chest_bust=request.POST["chest_bust"],
                            stomach=request.POST["stomach"],
                            hip=request.POST["p_Hips"],
                            shoulder=request.POST["shoulder"],
                            arm_hole=request.POST["arm_hole"],
                            waist=request.POST["waist"],
                            thigh=request.POST["thigh"],
                            knee=request.POST["p_Knee"],
                            calf=request.POST["calf"],
                            ankel_hem=request.POST["ankel_hem"],
                        )
                        kurti_size.save()
                        messages.info(
                            request, "Female Size for Kurti is added Successfully!"
                        )
                        return redirect("/profile")
                    elif request.POST["design"] == "gown":
                        obj_size = getsizeobj(
                            user_obj,
                            request.POST["name"],
                            request.POST["gender"],
                            request.POST["design"],
                        )

                        gown_data = for_gown(
                            size_detail=obj_size,
                            gown_length=request.POST["gown_length"],
                            upper_chest=request.POST["upper_Chest"],
                            chest=request.POST["s_Chest"],
                            waist=request.POST["waist"],
                            stomach=request.POST["stomach"],
                            hips=request.POST["p_Hips"],
                            shoulder=request.POST["shoulder"],
                            front_neck_depth=request.POST["front_neck_depth"],
                            sleeve_length=request.POST["sleeve_length"],
                            sleeve_round=request.POST["sleeve_around"],
                            arm_hole=request.POST["arm_hole"],
                        )
                        gown_data.save()
                        messages.info(
                            request, "Female Size for Gown is added Successfully!"
                        )
                        return redirect("/profile")
                    elif request.POST["design"] == "lahenga":
                        obj_size = getsizeobj(
                            user_obj,
                            request.POST["name"],
                            request.POST["gender"],
                            request.POST["design"],
                        )
                        lahenga_data = for_lahenga(
                            size_detail=obj_size,
                            front_neck_depth=request.POST["front_neck_depth"],
                            around_bust=request.POST["around_bust"],
                            neck_to_shoulder=request.POST["neck_to_solider"],
                            upper_waist=request.POST["upper_waist"],
                            blouse_length=request.POST["blouse_length"],
                            shoulder=request.POST["shoulder"],
                            back_neck_depth=request.POST["back_neck_depth"],
                            around_armholes=request.POST["arm_hole"],
                            # around_arm=request.POST["sleeve_length"],
                            sleeve_length=request.POST["sleeve_length"],
                            waist=request.POST["waist"],
                            hips=request.POST["p_Hips"],
                            waist_to_ankel=request.POST["waist_to_ankel_length"],
                            full_body=request.POST["full_body_lenght"],
                        )
                        lahenga_data.save()
                        messages.info(
                            request, "Female Size for Lahenga is added Successfully!"
                        )
                        return redirect("/profile")
                else:
                    if request.POST["design"] == "pantshirt":
                        obj_size = getsizeobj(
                            user_obj,
                            request.POST["name"],
                            request.POST["gender"],
                            request.POST["design"],
                        )
                        size_obj_mail = male_pantshirt(
                            size_detail=obj_size,
                            p_length=request.POST["p_Length"],
                            p_Waist=request.POST["p_Waist"],
                            p_Hips=request.POST["p_Hips"],
                            p_Thigh=request.POST["p_Thigh"],
                            p_Knee=request.POST["p_Knee"],
                            p_Leg_Opening=request.POST["p_LegOpening"],
                            p_Crotch_Or_Rise=request.POST["p_Crotch"],
                            p_In_Seam=request.POST["p_Seam"],
                            s_Shirt_lenght=request.POST["s_ShirtLen"],
                            s_Sleeve_Length=request.POST["s_Sleeve"],
                            s_Shoulders=request.POST["s_Shoulders"],
                            s_Chest=request.POST["s_Chest"],
                            s_Overarm=request.POST["s_Overarm"],
                            s_Waistcoat_Length=request.POST["Waistcoat"],
                            s_Bicep_Loose=request.POST["s_Bicep"],
                            s_Front_Chest=request.POST["s_FrontChest"],
                            s_Front_Stomach=request.POST["s_Stomach"],
                            s_Front_Hips=request.POST["s_Hips"],
                            s_Wrist=request.POST["s_Wrist"],
                            s_Neck=request.POST["s_Neck"],
                        )
                        size_obj_mail.save()
                        messages.info(request, "Male Size is added Successfully!")
                    return redirect("/profile")
        else:
            return redirect("/profile")

    @login_required(login_url="/login")
    def delete_size(request, id, g_id):
        del_size = size_detail.objects.get(user=request.user, id=id)
        del_size.delete()
        messages.info(request, "Size is Deleted Successfully!")
        return redirect("/profile")

    @login_required(login_url="/login")
    def view_size(request, s_id):
        obj = size_detail.objects.filter(id=s_id)[0]
        if obj.design_type == "pantshirt":
            size_value = male_pantshirt.objects.filter(size_detail=obj)[0]
        elif obj.design_type == "blouse":
            size_value = blouse.objects.filter(size_detail=obj)[0]
        elif obj.design_type == "kurti":
            size_value = kurti.objects.filter(size_detail=obj)[0]
        elif obj.design_type == "lahenga":
            size_value = for_lahenga.objects.filter(size_detail=obj)[0]
        elif obj.design_type == "gown":
            size_value = for_gown.objects.filter(size_detail=obj)[0]
        size_cart = {
            "sizechart": obj,
            "chartsize": size_value,
        }
        return render(request, "size_m.html", size_cart)

    @login_required(login_url="/login")
    def update_size(request, s_id, s_ge):
        if request.method == "POST":

            def getsizeobj(_user_obj, _name, _gender, _design):
                obj_size = size_detail.objects.filter(
                    id=_user_obj, name=_name, gender=_gender, design_type=_design
                )[0]
                return obj_size

            if request.POST["gender"] == "female":
                if request.POST["design"] == "blouse":
                    obj_size1 = getsizeobj(
                        s_id,
                        request.POST["name"],
                        request.POST["gender"],
                        request.POST["design"],
                    )
                    design_size = blouse.objects.filter(id=s_ge, size_detail=obj_size1)[
                        0
                    ]
                    design_size.shoulders = request.POST["shoulder"]
                    design_size.shouldersfull_lenght = request.POST[
                        "shoulder_full_lenght"
                    ]
                    design_size.front_neck_depth = request.POST["front_neck_depth"]
                    design_size.chest_around = request.POST["chest_around"]
                    design_size.waist_around = request.POST["waist_around"]
                    design_size.back_neck_depth = request.POST["back_neck_depth"]
                    design_size.blouse_length = request.POST["blouse_length"]
                    design_size.sleeve_length = request.POST["sleeve_length"]
                    design_size.sleeve_around = request.POST["sleeve_around"]
                    design_size.armhole_around = request.POST["arm_hole_around"]
                    design_size.save()
                    messages.info(request, "Female Size for blouse is added Updated!")
                    return redirect("/profile")
                elif request.POST["design"] == "kurti":
                    obj_size1 = getsizeobj(
                        s_id,
                        request.POST["name"],
                        request.POST["gender"],
                        request.POST["design"],
                    )
                    kurti_size = kurti.objects.filter(id=s_ge, size_detail=obj_size1)[0]
                    kurti_size.dress_length = request.POST["dress_length"]
                    kurti_size.sleev_length = request.POST["sleeve_length"]
                    kurti_size.neckline = request.POST["neck_line"]
                    kurti_size.upper_bust = request.POST["upper_bust"]
                    kurti_size.chest_bust = request.POST["chest_bust"]
                    kurti_size.stomach = request.POST["stomach"]
                    kurti_size.hip = request.POST["p_Hips"]
                    kurti_size.shoulder = request.POST["shoulder"]
                    kurti_size.arm_hole = request.POST["armhole"]
                    kurti_size.waist = request.POST["waist"]
                    kurti_size.thigh = request.POST["thigh"]
                    kurti_size.knee = request.POST["p_Knee"]
                    kurti_size.calf = request.POST["calf"]
                    kurti_size.ankel_hem = request.POST["ankel_hem"]
                    kurti_size.save()
                    messages.info(
                        request, "Female Size for Kurti is Updated Successfully!"
                    )
                    return redirect("/profile")
                elif request.POST["design"] == "gown":
                    obj_size1 = getsizeobj(
                        s_id,
                        request.POST["name"],
                        request.POST["gender"],
                        request.POST["design"],
                    )
                    gown_data = for_gown.objects.filter(id=s_ge, size_detail=obj_size1)[
                        0
                    ]
                    # size_detail=obj_size,
                    gown_data.gown_length = (request.POST["gown_length"],)
                    gown_data.upper_chest = (request.POST["upper_Chest"],)
                    gown_data.chest = (request.POST["s_Chest"],)
                    gown_data.waist = (request.POST["waist"],)
                    gown_data.stomach = (request.POST["stomach"],)
                    gown_data.hips = (request.POST["p_Hips"],)
                    gown_data.shoulder = (request.POST["shoulder"],)
                    gown_data.front_neck_depth = (request.POST["front_neck_depth"],)
                    gown_data.sleeve_length = (request.POST["sleeve_length"],)
                    gown_data.sleeve_round = (request.POST["sleeve_around"],)
                    gown_data.arm_hole = (request.POST["arm_hole"],)
                    gown_data.save()
                    messages.info(
                        request, "Female Size for Gown is added Successfully!"
                    )
                    return redirect("/profile")
                elif request.POST["design"] == "lahenga":
                    obj_size1 = getsizeobj(
                        s_id,
                        request.POST["name"],
                        request.POST["gender"],
                        request.POST["design"],
                    )
                    lahenga_data = for_lahenga.objects.filter(
                        id=s_ge, size_detail=obj_size1
                    )[0]
                    # size_detail=obj_size,
                    lahenga_data.front_neck_depth = (request.POST["front_neck_depth"],)
                    lahenga_data.around_bust = (request.POST["around_bust"],)
                    lahenga_data.neck_to_shoulder = (request.POST["neck_to_solider"],)
                    lahenga_data.upper_waist = (request.POST["upper_waist"],)
                    lahenga_data.blouse_length = (request.POST["blouse_length"],)
                    lahenga_data.shoulder = (request.POST["shoulder"],)
                    lahenga_data.back_neck_depth = (request.POST["back_neck_depth"],)
                    lahenga_data.around_armholes = (request.POST["arm_hole"],)
                    lahenga_data.sleeve_length = (request.POST["sleeve_length"],)
                    lahenga_data.waist = (request.POST["waist"],)
                    lahenga_data.hips = (request.POST["p_Hips"],)
                    lahenga_data.waist_to_ankel = (
                        request.POST["waist_to_ankel_length"],
                    )
                    lahenga_data.full_body = (request.POST["full_body_lenght"],)
                    lahenga_data.save()
                    messages.info(
                        request, "Female Size for Lahenga is added Successfully!"
                    )
                    return redirect("/profile")
            else:
                if request.POST["design"] == "pantshirt":
                    obj_size1 = getsizeobj(
                        s_id,
                        request.POST["name"],
                        request.POST["gender"],
                        request.POST["design"],
                    )
                    size_obj_mail = male_pantshirt.objects.filter(
                        id=s_ge, size_detail=obj_size1
                    )[0]
                    # size_detail=obj_size,
                    size_obj_mail.p_length = (request.POST["p_Length"],)
                    size_obj_mail.p_Waist = (request.POST["p_Waist"],)
                    size_obj_mail.p_Hips = (request.POST["p_Hips"],)
                    size_obj_mail.p_Thigh = (request.POST["p_Thigh"],)
                    size_obj_mail.p_Knee = (request.POST["p_Knee"],)
                    size_obj_mail.p_Leg_Opening = (request.POST["p_LegOpening"],)
                    size_obj_mail.p_Crotch_Or_Rise = (request.POST["p_Crotch"],)
                    size_obj_mail.p_In_Seam = (request.POST["p_Seam"],)
                    size_obj_mail.s_Shirt_lenght = (request.POST["s_ShirtLen"],)
                    size_obj_mail.s_Sleeve_Length = (request.POST["s_Sleeve"],)
                    size_obj_mails_Shoulders = (request.POST["s_Shoulders"],)
                    size_obj_mail.s_Chest = (request.POST["s_Chest"],)
                    size_obj_mail.s_Overarm = (request.POST["s_Overarm"],)
                    size_obj_mail.s_Waistcoat_Length = (request.POST["Waistcoat"],)
                    size_obj_mail.s_Bicep_Loose = (request.POST["s_Bicep"],)
                    size_obj_mail.s_Front_Chest = (request.POST["s_FrontChest"],)
                    size_obj_mail.s_Front_Stomach = (request.POST["s_Stomach"],)
                    size_obj_mail.s_Front_Hips = (request.POST["s_Hips"],)
                    size_obj_mail.s_Wrist = (request.POST["s_Wrist"],)
                    size_obj_mail.s_Neck = (request.POST["s_Neck"],)
                    size_obj_mail.save()
                    messages.info(request, "Male Size is added Successfully!")
                    return redirect("/profile")


@login_required(login_url="/login")
def your_order(request):
    order_obj = Oreder_Detail.objects.filter(user_id=request.user.id)
    rateing_obj = user_feedback.objects.filter(user_id=request.user.id)
    orders = []
    for detail in order_obj:
        orders.append(
            {
                "prod_detail": Product_detail.objects.filter(id=detail.Product_Id)[0],
                "order_obj1": detail,
            }
        )
    send_detail = {"order_obj": orders, "rateing_obj": rateing_obj}
    return render(request, "your_order.html", send_detail)


@login_required(login_url="/login")
def rate_product(request, p_id, or_id):
    order_obj = Oreder_Detail.objects.filter(
        user_id=request.user.id, Product_Id=p_id, id=or_id
    )[0]
    if order_obj.review == False:
        if request.method == "POST":
            stiching = request.POST["stiching_quality"]
            product_quality = request.POST["product_quality"]
            fitting = request.POST["fitting"]
            like_product = request.POST["like_product"]
            review = request.POST["review"]
            feedback_obj = user_feedback(
                stiching_quality=stiching,
                order=order_obj,
                user_id=request.user.id,
                product=Product_detail.objects.filter(id=p_id)[0],
                product_quality=product_quality,
                fitting_quality=fitting,
                liked=like_product,
                message=review,
            )
            feedback_obj.save()
            order_obj.review = True
            order_obj.save()
            messages.info(request, "Your Feedback is submitted Successfully!")
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        return redirect(request.META.get("HTTP_REFERER"))


def delete_feedback(request, r_id, o_id):
    feedback_obj = user_feedback.objects.filter(id=r_id)[0]
    feedback_obj.delete()
    order_obj = Oreder_Detail.objects.filter(id=o_id)[0]
    order_obj.review = False
    order_obj.save()
    messages.info(request, "Your Feedback is Deleted Successfully!")
    return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="/login")
def change_password(request, u_id):
    if request.method == "POST":
        user = auth.authenticate(
            id=u_id,
            username=request.user.username,
            password=request.POST["oldpassword"],
        )
        if user is not None:
            user_obj = User.objects.filter(id=u_id)[0]
            if request.POST["newpassword"] == request.POST["conpassword"]:
                user_obj.set_password(request.POST["newpassword"])
                user_obj.save()
                messages.info(request, "Password is changed successfully!")
                return redirect("/profile")
            else:
                messages.info(request, "Both password is not Matched")
                return redirect("/profile")
        else:
            messages.info(request, "Invalid Old Password!")
            return redirect("/profile")


def reset_password(request):
    return render(request, "password/password_reset.html")


def password_reset_confirm(request):
    if request.method == "POST":
        user_email = request.POST["email"]
        phone = request.POST["phone"]
        if User.objects.filter(
            Q(username__iexact=user_email) | Q(email__iexact=user_email)
        ).exists():
            user_data = User.objects.filter(
                Q(username__iexact=user_email) | Q(email__iexact=user_email)
            )[0]
            if Profile.objects.filter(user=user_data, phone=phone).exists():
                user_data = User.objects.filter(
                    Q(username__iexact=user_email) | Q(email__iexact=user_email)
                )[0]
                return redirect("/password_reset_done/" + str(user_data.id))
            else:
                messages.info(request, "Phone is not exists")
                return redirect("/reset_password")
        else:
            messages.info(request, "Username Or Email is not exists")
            return redirect("/reset_password")


def password_reset_done(request, u_id):
    if request.method == "POST":
        user_obj = User.objects.filter(id=u_id)[0]
        if request.POST["newpassword"] == request.POST["conpassword"]:
            user_obj.set_password(request.POST["newpassword"])
            user_obj.save()
            messages.info(request, "Password is changed successfully!")
            return redirect("/profile")
        else:
            messages.info(request, "Both password is not Matched")
            return redirect("/profile")
    else:
        if User.objects.filter(id=u_id).exists():
            user_obj = User.objects.filter(id=u_id)[0]
            return render(
                request, "password/password_reset_done.html", {"user": user_obj}
            )
        else:
            return redirect("/login")
