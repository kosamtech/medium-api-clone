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
    ERROR = "error"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        resp = self._create_response(data, renderer_context)
        return super().render(resp, accepted_media_type, renderer_context)

    def _create_response(self, data, context):
        status, msg = self.SUCCESS, None
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

            status_code = context["response"].status_code
            if status_code not in range(200, 300):
                status = self.ERROR

            if isinstance(data, Mapping):
                if data.get("message"):
                    msg = data.pop("message")
                else:
                    msg = self._format_message(status, model, method)
            else:
                msg = self._format_message(status, model, method)

        response = {"status": status, "message": msg, "data": data}
        return response

    def _format_message(self, status, model, method):
        if status == self.SUCCESS:
            msg = "{} {}".format(model, self.METHODS.get(method, f"{method} completed"))
        else:
            msg = "{} {}".format(
                model, "not " + self.METHODS.get(method, f"{method} not completed")
            )
        return msg
