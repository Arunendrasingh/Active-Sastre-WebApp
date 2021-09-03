from django.urls import path
from django.conf.urls import url

# from django.urls.resolvers import URLPattern
from . import views

# Your all urls here

urlpatterns = [
    path("", views.index, name="First page"),
    path("About", views.about, name="About Us"),
    path("cart", views.cart, name="Cart"),
    path("checkout/<int:p_id>", views.checkout, name="Checkout"),
    path("product/<int:pid>", views.product, name="Product"),
    path("profile", views.profile, name="Profile"),
    path("all_product", views.all_product, name="all_product"),
    path("incresequantity/<int:cid>", views.incresequantity, name="incresequantity"),
    path("decresequantity/<int:cid>", views.decresequantity, name="decresequantity"),
    path("add_to_wishlist/<int:p_id>", views.add_to_wishlist, name="Wishlist"),
    path("add_size", views.add_size, name="add_size"),
    path("delete_from/<int:w_id>", views.delete_from_wishlist, name="Wishlist"),
    path("change_password/<int:u_id>", views.change_password, name="change_password"),
    path("delete/<int:r_id>/<int:o_id>", views.delete_feedback, name="delete_feedback"),
    path("wishlist", views.wishlist, name="Wishlist"),
    path("contact", views.contact, name="Contact Us"),
    path("place_order", views.place_order, name="place_order"),
    path("signup", views.user_profile.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("view_size/<int:s_id>", views.size.view_size, name="view_size"),
    path(
        "update_size<int:s_id>/<int:s_ge>", views.size.update_size, name="update_size"
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
    path("reset_password", views.reset_password, name="Reset Password"),
    path(
        "password_reset_confirm",
        views.password_reset_confirm,
        name="Password Reset Confirm",
    ),
    path(
        "password_reset_done/<str:u_id>",
        views.password_reset_done,
        name="Password Reset Done",
    ),
    # url(r'^$', views.home, name='home'),
    # url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        views.activate, name='activate'),
]
