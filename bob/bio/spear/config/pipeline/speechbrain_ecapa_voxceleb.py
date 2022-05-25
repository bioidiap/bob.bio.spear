from sklearn.pipeline import make_pipeline

from bob.bio.base.algorithm import Distance
from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.extractor.speechbrain_embeddings import SpeechbrainEmbeddings
from bob.pipelines import wrap

transformer_pipeline = make_pipeline(
    wrap(["sample"], SpeechbrainEmbeddings()),
)

pipeline = PipelineSimple(
    transformer_pipeline, Distance(average_on_enroll=True)
)
