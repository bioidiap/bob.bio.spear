from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer

from bob.bio.base.pipelines import PipelineSimple
from bob.bio.spear.algorithm.speechbrain_interface import SpeechBrainInterface

passthrough = FunctionTransformer(lambda x: x)


pipeline = PipelineSimple(make_pipeline(passthrough), SpeechBrainInterface())
