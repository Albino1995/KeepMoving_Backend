import xadmin
from xadmin import views
from .models import VerifyCode


class BaseSetting():
    enable_themes = True
    use_bootswatch = True


class GlobalSettings():
    site_title = "KeepMoving后台"
    site_footer = "KeepMoving"


class VerifyCodeAdmin():
    list_display = ['code', 'mobile', "add_time"]


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
