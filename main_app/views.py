from typing import OrderedDict

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
    MailSize,
    Product_Img,
    MyCart,
    Wishlist,
    blouse,
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

    size_obj = Femail_size_Chart.objects.filter(user=user_obj.id)
    product_obj = Product_detail.objects.filter(id=p_id)[0]
    get_size_mail = MailSize.objects.filter(user=request.user)
    cart_obj = MyCart.objects.filter(product_id=p_id)[0]
    main_info = {
        "address": address_obj,
        "size": size_obj,
        "product_obj": product_obj,
        "malesize": get_size_mail,
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
        # gender = request.POST['gender']
        prod_price = request.POST["prod_price"]
        total_product = request.POST["product_num"]
        total_price = request.POST["total_price"]
        user_name = request.POST["user_name"]
        user = request.user.first_name + "  " + request.user.last_name
        if value[1] == "female":
            size_obj = Femail_size_Chart.objects.filter(id=int(value[0]))[0]
            size_name = size_obj.name
            size_detail = (
                "Shoulder:-"
                + str(size_obj.shoulder)
                + ", Shoulder Full Lenght:-"
                + str(size_obj.shoulder_full_lenght)
                + ", Front Neck Depth:-"
                + str(size_obj.front_neck_depth)
                + ", Back Neck Depth:-"
                + str(size_obj.back_neck_depth)
                + ", Sleeve Length:-"
                + str(size_obj.sleeve_length)
                + ", Sleeve Around:-"
                + str(size_obj.sleev_around)
                + ", Armhole(around):-"
                + str(size_obj.arm_hole)
                + ", Dress Length:-"
                + str(size_obj.gown_length)
                + ", Neck Line:-"
                + str(size_obj.neck_line)
                + ", Upper Bust:-"
                + str(size_obj.upper_bust)
                + ", Chest/Bust:-"
                + str(size_obj.chest)
                + ", Stomach:-"
                + str(size_obj.stomach)
                + ", Hip:-"
                + str(size_obj.hips)
                + ", Thigh:-"
                + str(size_obj.thigh)
                + ", Chest Around:-"
                + str(size_obj.chest)
                + ", Waist:-"
                + str(size_obj.waist)
                + ", Blouse Length:-"
                + str(size_obj.blouse_length)
                + ", Knee:-"
                + str(size_obj.knee)
                + ", Calf:-"
                + str(size_obj.calf)
                + ", Ankel Hem:-"
                + str(size_obj.arm_hole)
                + ", Upper Chest:-"
                + str(size_obj.chest)
                + ", Neck to Solider:-"
                + str(size_obj.neck_to_solider)
                + ", Gown Length:-"
                + str(size_obj.gown_length)
                + ", Around Bust:-"
                + str(size_obj.around_bust)
                + ", upper_waist:-"
                + str(size_obj.upper_waist)
                + ", Waist to Ankel Length:-"
                + str(size_obj.waist_to_ankel_length)
                + ", Full Body Lenght:-"
                + str(size_obj.full_body_lenght)
            )
        else:
            size_obj = MailSize.objects.filter(id=int(value[0]))[0]
            size_name = size_obj.name
            size_detail = (
                "Paint Length:-"
                + str(size_obj.p_length)
                + ", Paint Waist:-"
                + str(size_obj.p_Waist)
                + ", Paint Hips:-"
                + str(size_obj.p_Hips)
                + ", Paint Thigh:-"
                + str(size_obj.p_Thigh)
                + ", Knee:-"
                + str(size_obj.p_Knee)
                + ", Leg Opening:-"
                + str(size_obj.p_Leg_Opening)
                + ", Crotch/Rise:-"
                + str(size_obj.p_Crotch_Or_Rise)
                + ", In-Seam:-"
                + str(size_obj.p_In_Seam)
                + ", Shirt Length:-"
                + str(size_obj.s_Shirt_lenght)
                + ", Sleeve Length:-"
                + str(size_obj.s_Sleeve_Length)
                + ", Shoulders:-"
                + str(size_obj.s_Shoulders)
                + ", Chest:-"
                + str(size_obj.s_Chest)
                + ", Overarm:-"
                + str(size_obj.s_Overarm)
                + ", Waistcoat Length:-"
                + str(size_obj.s_Waistcoat_Length)
                + ", Bicep(Loose):-"
                + str(size_obj.s_Bicep_Loose)
                + ", Chest:-"
                + str(size_obj.s_Front_Chest)
                + ", Stomach:-"
                + str(size_obj.s_Front_Stomach)
                + ", Front - Hip:-"
                + str(size_obj.s_Front_Hips)
                + ", Wrist:-"
                + str(size_obj.s_Wrist)
                + ", Neck:-"
                + str(size_obj.s_Neck)
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
            size_name=size_name,
            size_detail=size_detail,
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
    get_size_femail = Femail_size_Chart.objects.filter(user=request.user)
    get_size_mail = MailSize.objects.filter(user=request.user)
    get_user = User.objects.filter(id=request.user.id)[0]
    get_profile = Profile.objects.filter(user=get_user)[0]
    pass_data = {
        "totaladdress": len(get_address),
        "address": get_address,
        "totalsize": len(get_size_femail),
        "femalesize": get_size_femail,
        "malesize": get_size_mail,
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


class user_profile:
    def signup(request):
        if request.method == "POST":
            first_name = request.POST["fname"].capitalize()
            last_name = request.POST["lname"].capitalize()
            # user_name = request.POST['username']
            phone = request.POST["phone"]
            user_email = request.POST["email"]
            user_password1 = request.POST["pass"]
            user_password2 = request.POST["conpass"]
            # pro_img = request.FILES['prof_img']
            if user_password1 == user_password2:
                if User.objects.filter(
                    Q(username__iexact=user_email) | Q(email__iexact=user_email)
                ).exists():
                    messages.success(request, "User Name Or Email  alredy registerd")
                    return redirect("/signup")
                else:
                    user = User.objects.create_user(
                        username=user_email,
                        first_name=first_name,
                        last_name=last_name,
                        email=user_email,
                        password=user_password2,
                    )
                    user.save()
                    subject = "welcome to Active Sastre"
                    message = (
                        f"Hi {first_name}, thank you for registering in Active Sastre."
                    )
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [
                        user_email,
                    ]
                    send_mail(subject, message, email_from, recipient_list)
                    user_profile = Profile.objects.get(user=user)
                    user_profile.phone = phone
                    # user_profile.image = pro_img
                    user_profile.save()
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
            email = request.POST["email"]
            phone = request.POST["mobile"]
            user_pro = User.objects.get(id=id)
            get_profile = Profile.objects.get(user=user_pro)
            user_pro.first_name = fname
            user_pro.last_name = lname
            user_pro.email = email
            # user_pro.username = email
            user_pro.save()
            get_profile.phone = phone
            get_profile.save()
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
        if request.method == "POST":
            user_obj = User.objects.filter(id=request.user.id)[0]
            if request.POST["gender"] == "female":
                if request.POST["design"] == "blouse":
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

                        obj_size = size_detail.objects.filter(
                            user=user_obj,
                            name=request.POST["name"],
                            gender=request.POST["gender"],
                            design_type=request.POST["design"],
                        )[0]
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
                else:
                    print("fsdgsdfg")
            else:
                size_obj_mail = MailSize(
                    user=user_obj,
                    gender=request.POST["femail"],
                    name=request.POST["name"],
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
        if g_id == "female":
            del_size = Femail_size_Chart.objects.get(user=request.user, id=id)
            del_size.delete()
        else:
            del_size = MailSize.objects.get(user=request.user, id=id)
            del_size.delete()
        messages.info(request, "Size is Deleted Successfully!")
        return redirect("/profile")

    @login_required(login_url="/login")
    def view_size(request, s_id, s_ge):
        if s_ge == "female":
            obj = Femail_size_Chart.objects.filter(id=s_id)[0]
        else:
            obj = MailSize.objects.filter(id=s_id)[0]

        size_cart = {
            "sizechart": obj,
        }
        return render(request, "size_m.html", size_cart)

    @login_required(login_url="/login")
    def update_size(request, s_id, s_ge):
        if request.method == "POST":
            if s_ge == "femail":
                obj = Femail_size_Chart.objects.filter(id=s_id)[0]
                obj.name = request.POST["name"]
                obj.gender = request.POST["femail"]
                obj.gown_length = request.POST["gown_length"]
                obj.upper_chest = request.POST["upper_Chest"]
                obj.chest = request.POST["chest"]
                obj.waist = request.POST["waist"]
                obj.upper_waist = request.POST["upper_waist"]
                obj.stomach = request.POST["stomach"]
                obj.hips = request.POST["hips"]
                obj.shoulder = request.POST["shoulder"]
                obj.front_neck_depth = request.POST["front_neck_depth"]
                obj.back_neck_depth = request.POST["back_neck_depth"]
                obj.neck_to_solider = request.POST["neck_to_solider"]
                obj.sleeve_length = request.POST["sleeve_length"]
                obj.sleev_around = request.POST["sleeve_around"]
                obj.around_bust = request.POST["around_bust"]
                obj.blouse_length = request.POST["blouse_length"]
                obj.arm_hole = request.POST["arm_hole"]
                obj.waist_to_ankel_length = request.POST["waist_to_ankel_length"]
                obj.full_body_lenght = request.POST["full_body_lenght"]
                obj.dress_length = request.POST["dress_length"]
                obj.neck_line = request.POST["neck_line"]
                obj.upper_bust = request.POST["upper_bust"]
                obj.chest_bust = request.POST["chest_bust"]
                obj.thigh = request.POST["thigh"]
                obj.knee = request.POST["knee"]
                obj.calf = request.POST["calf"]
                obj.ankel_hem = request.POST["ankel_hem"]
                obj.shoulder_full_lenght = request.POST["shoulder_full_lenght"]
                obj.save()
                messages.info(request, "Female Size is Changed Successfully!")
                return redirect("/profile")
            else:
                obj = MailSize.objects.filter(id=s_id)[0]
                obj.gender = request.POST["femail"]
                obj.name = request.POST["name"]
                obj.p_length = request.POST["p_Length"]
                obj.p_Waist = request.POST["p_Waist"]
                obj.p_Hips = request.POST["p_Hips"]
                obj.p_Thigh = request.POST["p_Thigh"]
                obj.p_Knee = request.POST["p_Knee"]
                obj.p_Leg_Opening = request.POST["p_LegOpening"]
                obj.p_Crotch_Or_Rise = request.POST["p_Crotch"]
                obj.p_In_Seam = request.POST["p_Seam"]
                obj.s_Shirt_lenght = request.POST["s_ShirtLen"]
                obj.s_Sleeve_Length = request.POST["s_Sleeve"]
                obj.s_Shoulders = request.POST["s_Shoulders"]
                obj.s_Chest = request.POST["s_Chest"]
                obj.s_Overarm = request.POST["s_Overarm"]
                obj.s_Waistcoat_Length = request.POST["Waistcoat"]
                obj.s_Bicep_Loose = request.POST["s_Bicep"]
                obj.s_Front_Chest = request.POST["s_FrontChest"]
                obj.s_Front_Stomach = request.POST["s_Stomach"]
                obj.s_Front_Hips = request.POST["s_Hips"]
                obj.s_Wrist = request.POST["s_Wrist"]
                obj.s_Neck = request.POST["s_Neck"]
                obj.save()
                messages.info(request, "Male Size is Changed Successfully!")
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
