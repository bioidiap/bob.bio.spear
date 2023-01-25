from bob.bio.spear.extractor.pytorch_embeddings import PyTorchModel


class WavLM(PyTorchModel):
    def __init__(self):
        super().__init__()

    def _load_model(self) -> None:

        self.model = None  # TODO
