from rest_framework import viewsets, permissions, mixins
from rest_framework.exceptions import ValidationError
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class VoteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        request = self.request
        poll = Poll.objects.filter(id=serializer.data['item']).first()
        votes = Vote.objects.filter(
            user=request.user,
            item__poll=poll,
        )

        if votes.exists():
            raise ValidationError("You have already voted.")
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        serializer.save(
            user=request.user,
            ip=ip,
        )
