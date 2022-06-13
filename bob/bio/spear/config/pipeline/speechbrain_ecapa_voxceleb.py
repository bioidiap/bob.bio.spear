from sklearn.pipeline import make_pipeline

from bob.bio.base.algorithm import Distance
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.extractor import SpeechbrainEmbeddings

# from bob.bio.spear.transformer import Resample
from bob.pipelines import wrap

transformer_pipeline = make_pipeline(
    # wrap(["sample"], Resample(target_sample_rate=16000)),
    wrap(["sample"], SpeechbrainEmbeddings()),
)

pipeline = PipelineSimple(
    transformer_pipeline, Distance(average_on_enroll=True)
)
