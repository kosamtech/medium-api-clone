import logging
from collections.abc import Mapping

from rest_framework.renderers import JSONRenderer

logger = logging.getLogger(__name__)


class NoContextError(Exception):
    pass


class MediumJSONRenderer(JSONRenderer):
    charset = "utf-8"
    media_type = "application/json"
    METHODS = {
        "GET": "retrieved",
        "PUT": "updated",
        "PATCH": "updated",
        "POST": "created",
        "DELETE": "deleted",
    }
    SUCCESS = "success"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        resp = self._create_response(data, renderer_context)
        return super().render(resp, accepted_media_type, renderer_context)

    def _create_response(self, data, context):
        if context is None:
            logger.error("No context was provided to the renderer")
            status = "error"
            msg = "No context was provided to the renderer"
        else:
            try:
                """
                some endpoints may not have context['view'] resulting in Attribute Error
                e.g action endpoints
                """
                model = context["view"].basename
            except AttributeError:
                model = ""
            method = context["request"]._request.method

            if isinstance(data, dict):
                status = data.get("status", MediumJSONRenderer.SUCCESS)
            else:
                status = MediumJSONRenderer.SUCCESS

            if status != MediumJSONRenderer.SUCCESS:
                return data

            if isinstance(data, Mapping) and data.get("message") is not None:
                msg = data.pop("message")
            else:
                msg = "{} {}".format(
                    model, self.METHODS.get(method, f"{method} completed")
                )

        response = {"status": status, "message": msg, "data": data}
        return response
