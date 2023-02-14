from bob.bio.base.database import CSVDatabase
from bob.bio.spear.database.utils import create_sample_loader, get_rc


class VoicepaDatabase(CSVDatabase):
    """Voice PA database definition."""

    name = "voicepa"
    category = "spear"
    dataset_protocols_name = "voicepa.tar.gz"
    dataset_protocols_urls = [
        "https://www.idiap.ch/software/bob/databases/latest/spear/voicepa-6da95ba2.tar.gz",
        "http://www.idiap.ch/software/bob/databases/latest/spear/voicepa-6da95ba2.tar.gz",
    ]
    dataset_protocols_hash = "6da95ba2"

    def __init__(self, protocol):
        super().__init__(
            name=self.name,
            protocol=protocol,
            transformer=create_sample_loader(
                data_path=get_rc()[f"bob.db.{self.name}.directory"],
            ),
        )
