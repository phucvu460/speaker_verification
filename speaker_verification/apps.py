from django.apps import AppConfig
from django.conf import settings
from deep_speaker.conv_models import DeepSpeakerModel

class SpeakerVerificationConfig(AppConfig):
    name = 'speaker_verification'

    DeepSpeakerModel = DeepSpeakerModel()
    DeepSpeakerModel.m.load_weights('/home/jax/SPEAKER_RECOGNITION/speaker_recognition_project/deep_speaker/ResCNN_triplet_training_checkpoint_265.h5', by_name=True)

