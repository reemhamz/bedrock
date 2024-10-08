# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import datetime
import re

from django.conf import settings
from django.utils.timezone import make_aware

import requests
from sentry_sdk import capture_exception


def get_articles_data(count=8):
    payload = {
        "consumer_key": settings.POCKET_CONSUMER_KEY,
        "access_token": settings.POCKET_ACCESS_TOKEN,
        "count": count,
        "detailType": "complete",
    }

    try:
        resp = requests.post(settings.POCKET_API_URL, json=payload, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        capture_exception()
        return None


def complete_articles_data(articles):
    for _, article in articles:
        # id from API should be moved to pocket_id to not conflict w/DB's id
        article["pocket_id"] = article["id"]

        # convert time_shared from unix timestamp to datetime
        article["time_shared"] = make_aware(datetime.datetime.fromtimestamp(int(article["time_shared"])), datetime.UTC)

        # remove data points we don't need
        del article["comment"]
        del article["excerpt"]
        del article["id"]
        del article["quote"]

        check_article_image(article)


def check_article_image(article):
    """Determine if external image is available"""

    # sanity check to make sure image provided by API actually exists and is https
    if article["image_src"] and re.match(r"^https://", article["image_src"], flags=re.I):
        try:
            resp = requests.get(article["image_src"])
            resp.raise_for_status()
        except Exception:
            capture_exception()
            article["image_src"] = None
    else:
        article["image_src"] = None
