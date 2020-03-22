# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import os
import sys

from bugbug_http import ALLOW_MISSING_MODELS
from bugbug_http.models import MODELS_NAMES, get_model

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def check_models():
    for model_name in MODELS_NAMES:
        # Try loading the model
        try:
            get_model(model_name)
        except FileNotFoundError:
            if ALLOW_MISSING_MODELS:
                LOGGER.info(
                    "Missing %r model, skipping because ALLOW_MISSING_MODELS is set"
                    % model_name
                )
                return None
            else:
                raise


if __name__ == "__main__":

    should_check_models = os.environ.get("CHECK_MODELS", "1")

    if should_check_models == "0":
        LOGGER.info("Skipping checking models as instructed by env var $CHECK_MODELS")
        sys.exit(0)

    try:
        check_models()
    except Exception:
        LOGGER.warning(
            "Failed to validate the models, please run `python download_models.py`",
            exc_info=True,
        )
        sys.exit(1)
