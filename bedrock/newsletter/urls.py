# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.urls import path, re_path

from bedrock.mozorg.util import page
from bedrock.newsletter import views
from bedrock.utils.views import VariationTemplateView

# A UUID looks like: f81d4fae-7dec-11d0-a765-00a0c91e6bf6
# Here's a regex to match a UUID:
uuid_regex = r"[0-Fa-f]{8}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{4}-[0-Fa-f]{12}"


urlpatterns = (
    # view.existing allows a user who has a link including their token to
    # subscribe, unsubscribe, change their preferences. Each newsletter
    # includes that link for them.
    re_path("^newsletter/existing/(?P<token>[^/]*)/?$", views.existing, name="newsletter.existing.token"),
    # After submitting on the `existing` page, users end up on the
    # `updated` page.  There are optional query params; see the view.
    path("newsletter/updated/", views.updated, name="newsletter.updated"),
    # Confirm subscriptions
    re_path("^newsletter/confirm/(?P<token>%s)/$" % uuid_regex, views.confirm, name="newsletter.confirm"),
    path("newsletter/confirm/thanks/", views.confirm_thanks, name="newsletter.confirm.thanks"),
    # Update country
    re_path("^newsletter/country/(?P<token>[^/]*)/?$", views.set_country, name="newsletter.country"),
    # Request recovery message with link to manage subscriptions
    path("newsletter/recovery/", views.recovery, name="newsletter.recovery"),
    # Receives POSTs from all subscribe forms
    path("newsletter/", views.newsletter_subscribe, name="newsletter.subscribe"),
    # Welcome program opt-out confirmation page (bug 1442129)
    path("newsletter/opt-out-confirmation/", views.recovery, name="newsletter.opt-out-confirmation"),
    # Branded signup pages for individual newsletters
    page("newsletter/mozilla/", "newsletter/mozilla.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/firefox/", "newsletter/firefox.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/developer/", "newsletter/developer.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/fxa-error/", "newsletter/fxa-error.html", ftl_files=["mozorg/newsletters"]),
    path(
        "newsletter/knowledge-is-power/",
        VariationTemplateView.as_view(
            template_name="newsletter/knowledge-is-power.html", template_context_variations=["rise25"], ftl_files=["mozorg/newsletters"]
        ),
        name="newsletter.knowledge-is-power",
    ),
    re_path("^newsletter/knowledge-is-power/confirm/(?P<token>[^/]*)/?$", views.kip_confirm, name="newsletter.knowledge-is-power.confirm"),
    page("newsletter/family/", "newsletter/family.html", ftl_files=["mozorg/newsletters"], active_locales=["en-US"]),
    page("newsletter/security-and-privacy/", "newsletter/security-privacy-news.html", ftl_files=["mozorg/newsletters"]),
    page("newsletter/security-and-privacy/online-harassment/", "newsletter/online-harassment.html"),
    page("newsletter/monitor-waitlist/", "newsletter/monitor-waitlist.html", ftl_files=["mozorg/newsletters"]),
    path("newsletter/newsletter-all.json", views.newsletter_all_json, name="newsletter.all"),
    path("newsletter/newsletter-strings.json", views.newsletter_strings_json, name="newsletter.strings"),
)
