import simplejson as json

from .models import get_model_path, LogEntry


class LoggingMethodMixin:
    """
    Adds methods that log changes made to users' data.

    To use this, subclass it and ModelViewSet, and override _get_logging_user(). Ensure
    that the viewset you're mixing this into has `self.model` and `self.serializer_class`
    attributes.
    """

    def _get_logging_user(self):
        """Return the user of this logged item. Needs overriding in any subclass."""
        raise NotImplementedError

    def extra_data(self, data):
        """Hook to append more data."""
        return {}

    def log(self, operation, data):
        data.update(self.extra_data(data))
        LogEntry.objects.create(
            creator=self.request.user,
            data=json.dumps(data, use_decimal=True),
            model_path=get_model_path(self.model),
            operation=operation,
            user=self._get_logging_user(),
        )

    def _log_on_create(self, serializer):
        """Log the up-to-date serializer.data."""
        self.log(operation=LogEntry.OPERATION_ADDED, data=serializer.validated_data)

    def _log_on_update(self, serializer):
        """Log data from the updated serializer instance."""
        self.log(operation=LogEntry.OPERATION_MODIFIED, data=serializer.data)

    def _log_on_destroy(self, instance):
        """Log data from the instance before it gets deleted."""
        data = self.serializer_class(
            instance=instance,
            context={'request': self.request},
        ).data
        self.log(operation=LogEntry.OPERATION_REMOVED, data=data)


class LoggingViewSetMixin(LoggingMethodMixin):
    """
    A viewset that logs changes made to users' data.

    To use this, subclass it and ModelViewSet, and override _get_logging_user(). Ensure
    that the viewset you're mixing this into has `self.model` and `self.serializer_class`
    attributes.

    If you modify any of the following methods, be sure to call super() or the
    corresponding _log_on_X method:
    - perform_create
    - perform_update
    - perform_destroy
    """
    def perform_create(self, serializer):
        """Create an object and log its data."""
        super().perform_create(serializer)
        self._log_on_create(serializer)

    def perform_update(self, serializer):
        """Update the instance and log the updated data."""
        super().perform_update(serializer)
        self._log_on_update(serializer)

    def perform_destroy(self, instance):
        """Delete the instance and log the deletion."""
        super().perform_destroy(instance)
        self._log_on_destroy(instance)
