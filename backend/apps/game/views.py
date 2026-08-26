from django.db.models import F
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import PlayerProgress
from .serializers import ProgressSerializer,LeaderboardSerializer
class StateView(generics.RetrieveAPIView):
    serializer_class=ProgressSerializer
    def get_object(self): return PlayerProgress.objects.get(user=self.request.user)

class SyncView(generics.GenericAPIView):
    serializer_class=ProgressSerializer
    def post(self,request):
        progress=PlayerProgress.objects.get(user=request.user); value=int(request.data.get('score',0))
        if value < progress.score: value=progress.score
        progress.score=value; progress.save(update_fields=['score','updated_at']); return Response(self.get_serializer(progress).data)
    
class LeaderboardView(generics.GenericAPIView):
    # El ranking es público: no requiere ni procesa credenciales JWT.
    authentication_classes = []
    permission_classes=[permissions.AllowAny]; serializer_class=LeaderboardSerializer
    def get(self,request):
        rows=PlayerProgress.objects.select_related('user').order_by('-score','user__nickname')[:20]
        return Response([{'position':i,'nickname':row.user.nickname,'score':row.score} for i,row in enumerate(rows,1)])
