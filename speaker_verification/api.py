from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser

from speaker_verification.models import User
from speaker_verification.serializers import UserSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse

from .apps import SpeakerVerificationConfig

from collections import Counter
import requests
import numpy as np

from deep_speaker.audio import read_mfcc
from deep_speaker.batcher import sample_from_mfcc
from deep_speaker.constants import SAMPLE_RATE, NUM_FRAMES
from deep_speaker.test import batch_cosine_similarity

class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all friends except yourself
        # self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
                    self.queryset.filter(Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


def predict(embedding, k=1):
    embeddings = []
    names = []
    data = requests.get('http://127.0.0.1:8000/speaker_verification/api/v1/user/')
    print(f"OOOO {data.json()}")

    for user in data.json():
        names.append(user['username'])
        f = user['embedding']
        f = f.replace('http://127.0.0.1:8000', str(settings.BASE_DIR))
        print(f'FFFFF {f}')
        mfcc = sample_from_mfcc(read_mfcc(f, SAMPLE_RATE), NUM_FRAMES)
        user_embedding = SpeakerVerificationConfig.DeepSpeakerModel.m.predict(np.expand_dims(mfcc, axis=0))
        embeddings.append(user_embedding)
        
    embeddings = np.array(embeddings)
    names = np.array(names)

    results = []
    for embeddingSpeaker, speaker in zip(embeddings, names):
        cosine = batch_cosine_similarity(embeddingSpeaker, embedding)
        results.append((cosine, speaker))
    results = sorted(results, reverse = True)
    temp =[(first - 0.1, second) for (first, second) in results[:10]]
    temp = np.array(temp).reshape(-1,1)
    mostVotes = [second for first, second in results[:k]]
    mostVotes = Counter(mostVotes)
    return mostVotes.most_common(1)[0][0], temp


class Predict(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request):
        # serializer =  UserSerializer(data=request.DATA, files=request.FILES)
        wav_file = request.FILES['file']
        mfcc = sample_from_mfcc(read_mfcc(wav_file, SAMPLE_RATE), NUM_FRAMES)
        embedding = SpeakerVerificationConfig.DeepSpeakerModel.m.predict(np.expand_dims(mfcc, axis=0))
        className, probability = predict(embedding)
        response = {
            'className': className
        }
        return JsonResponse(response)


