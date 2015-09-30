from django.conf.urls import patterns, url, include
from views.iframe import IFrameView


_urlpatterns = patterns(
    "",
    url(r"^ipage",
        IFrameView.as_view(),
        name="djinn_pages_iframeview"),

    )

urlpatterns = patterns(
    '',
    (r'^djinn_pages/', include(_urlpatterns)),
)
