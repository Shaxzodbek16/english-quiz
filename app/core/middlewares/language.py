from pyexpat.errors import messages

from aiogram.utils.i18n.middleware import I18nMiddleware as I18nMiddlewareBase


class I18nMiddleware(I18nMiddlewareBase):  # noqa
    pass


_ = I18nMiddlewareBase.gettext

messages.answer(_(""))
