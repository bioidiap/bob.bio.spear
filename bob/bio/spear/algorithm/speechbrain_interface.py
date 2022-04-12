import logging

# Download pretrained SpeakerRecognition from SpeechBrain
from speechbrain.pretrained import SpeakerRecognition

from bob.bio.base.pipelines import BioAlgorithm

logger = logging.getLogger(__name__)


class SpeechBrainInterface(BioAlgorithm):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.verification = SpeakerRecognition.from_hparams(
            source="speechbrain/spkrec-ecapa-voxceleb",
            savedir="pretrained_models/spkrec-ecapa-voxceleb",
        )

    def enroll(self, data):
        return data

    def score(self, model, data):

        scores = []
        for _model in model:
            score, _ = self.verification.verify_files(_model, data)
            scores.append(score)

        return scores
