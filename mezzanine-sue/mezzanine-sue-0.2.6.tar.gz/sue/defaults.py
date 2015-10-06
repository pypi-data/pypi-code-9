from __future__ import unicode_literals

from mezzanine.conf import register_setting
from django.utils.translation import ugettext_lazy as _

register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("The ability to set different themes"),
    editable=False,
    default=("THEME_SKINS", "SEARCH_CONSOLE",),
    append=True,
)

register_setting(
    name="THEME_SKINS",
    label=_("Theme skins"),
    description=_("The theme's skin changer"),
    editable=True,
    default=_("bootstrap_cyborg_dark.css",),
    choices=(
        (_("bootstrap_journal_light.css"), _("bootstrap_journal_light.css")),
        (_("bootstrap_lumen.css"), _("bootstrap_lumen.css")),
        (_("bootstrap_cyborg_dark.css"), _("bootstrap_cyborg_dark.css")),
        (_("bootstrap_cerulean.css"), _("bootstrap_cerulean.css")),
        (_("bootstrap_cosmo.css"), _("bootstrap_cosmo.css")),
        (_("bootstrap_darkly.css"), _("bootstrap_darkly.css")),
        (_("bootstrap_flatly.css"), _("bootstrap_flatly.css")),
        (_("bootstrap_paper.css"), _("bootstrap_paper.css")),
        (_("bootstrap_readable.css"), _("bootstrap_readable.css")),
        (_("bootstrap_sandstone.css"), _("bootstrap_sandstone.css")),
        (_("bootstrap_simplex.css"), _("bootstrap_simplex.css")),
        (_("bootstrap_slate.css"), _("bootstrap_slate.css")),
        (_("bootstrap_spacelab.css"), _("bootstrap_spacelab.css")),
        (_("bootstrap_superhero.css"), _("bootstrap_superhero.css")),
        (_("bootstrap_united.css"), _("bootstrap_united.css")),
        (_("bootstrap_yeti.css"), _("bootstrap_yeti.css")),
    ),
)

register_setting(
    name="SEARCH_CONSOLE",
    label=_("Google Search Console Verification"),
    description=_("Search console meta tag verification code, ommit any HTML"),
    editable=True,
    default="",
)



