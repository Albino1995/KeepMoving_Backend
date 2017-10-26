import xadmin
from .models import UserFav, UserLeavingMessage, UserAddress


class UserFavAdmin():
    list_display = ['user', 'goods', "add_time"]


class UserLeavingMessageAdmin():
    list_display = ['user', 'message_type', "message", "add_time"]


class UserAddressAdmin():
    list_display = ["signer_name", "signer_mobile", "district", "address"]


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)