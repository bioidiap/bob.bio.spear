#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Thu 01 Jul 2021 10:41:55 UTC+02

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

from bob.io.audio import reader as AudioReader
from bob.pipelines import Sample
from bob.pipelines.sample import SampleBatch


class AudioReaderToSample(BaseEstimator, TransformerMixin):
    """Transforms a Sample's data containing an audio reader to an audio signal.

    The Sample's metadata are updated.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # dict[Sample attribute name, AudioReader field name]
        self.metadata_keys = {
            "sample_rate": "rate",
            "number_of_samples": "number_of_samples",
            "number_of_channels": "number_of_channels",
            "bits_per_sample": "bits_per_sample",
            "audio_duration": "duration",
            "audio_encoding": "encoding",
            "audio_sample_type": "type",
            "audio_compression_factor": "compression_factor",
        }

    def extract_from_reader(self, reader: AudioReader) -> dict:
        """Extracts a set of metadata from a reader object"""
        results = {"data": reader.load()}
        for metadata, reader_key in self.metadata_keys.items():
            results[metadata] = getattr(reader, reader_key)
        return results

    def populate_from_reader(self, sample: Sample) -> Sample:
        """Loads from the AudioReader of the Sample and set its fields accordingly."""
        extracted = self.extract_from_reader(sample.data)
        kwargs = {e: extracted[e] for e in extracted if e != "data"}
        new_sample = Sample(data=extracted["data"], parent=sample, **kwargs)
        return new_sample

    def transform(self, samples: SampleBatch):
        output = []
        for sample in samples:
            output.append(self.populate_from_reader(sample))
        return output

    def fit(self, X, y=None, **fit_params):
        return self

    def _more_tags(self):
        tags = super()._more_tags()
        update = {
            "stateless": True,
            "requires_fit": False,
        }
        return {**tags, **update}
