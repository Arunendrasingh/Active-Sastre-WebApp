from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

# from django.urls.resolvers import URLPattern
from . import views

# Your all urls here

urlpatterns = [
    path("", views.index, name="First page"),
    # URLS for signup/login and logout
    path("signup", views.user_profile.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    # URLS Related to Profile
    path("profile", views.profile, name="Profile"),
    path("change_password/<int:u_id>", views.change_password, name="change_password"),
    path("add_size", views.add_size, name="add_size"),
    path("About", views.about, name="About Us"),
    path("cart", views.cart, name="Cart"),
    path("wishlist", views.wishlist, name="Wishlist"),
    path("checkout/<int:p_id>", views.checkout, name="Checkout"),
    path("product/<int:pid>", views.product, name="Product"),
    path("add_to_wishlist/<int:p_id>", views.add_to_wishlist, name="Wishlist"),
    path("incresequantity/<int:cid>", views.incresequantity, name="incresequantity"),
    path("decresequantity/<int:cid>", views.decresequantity, name="decresequantity"),
    path("delete_from/<int:w_id>", views.delete_from_wishlist, name="Wishlist"),
    path("delete/<int:r_id>/<int:o_id>", views.delete_feedback, name="delete_feedback"),
    # URL for All Product View
    path("all_product", views.all_product, name="all_product"),
    # path("all_product/<int:cat_id>", views.all_product, name="all_product"),
    # URLs for basik need
    path("contact", views.contact, name="Contact Us"),
    path("place_order", views.place_order, name="place_order"),
    path("view_size/<int:s_id>", views.size.view_size, name="view_size"),
    path(
        "update_size/<int:s_id>/<int:s_ge>", views.size.update_size, name="update_size"
    ),
    path("saveaddress", views.address.SaveAddress, name="saveaddress"),
    path(
        "change_address/<int:id>", views.address.change_address, name="change_address"
    ),
    path(
        "delete_address/<int:id>", views.address.delete_address, name="delete_address"
    ),
    path("addsize", views.size.addsize, name="addsize"),
    path(
        "rate_product/<int:p_id>/<int:or_id>", views.rate_product, name="rate_product"
    ),
    path("delete_size/<int:id>/<str:g_id>", views.size.delete_size, name="delete_size"),
    path(
        "change_profile/<int:id>",
        views.user_profile.change_profile,
        name="changr_profile",
    ),
    path("add_to_cart/<int:pid>", views.add_to_cart, name="add_to_cart"),
    path("your_order", views.your_order, name="your Order"),

    # URLS For Password Resting in case of you forgate you
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),  
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    # URLS for referral
    path("bonus", views.your_bonus, name="your_bonus"),
]
