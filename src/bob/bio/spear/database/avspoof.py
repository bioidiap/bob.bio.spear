from bob.bio.base.database import CSVDatabase
from bob.bio.spear.database.utils import create_sample_loader, get_rc


class AvspoofDatabase(CSVDatabase):
    """AV Spoof database definition."""

    name = "avspoof"
    category = "spear"
    dataset_protocols_name = "avspoof.tar.gz"
    dataset_protocols_urls = [
        "https://www.idiap.ch/software/bob/databases/latest/spear/avspoof-d58a537b.tar.gz",
        "http://www.idiap.ch/software/bob/databases/latest/spear/avspoof-d58a537b.tar.gz",
    ]
    dataset_protocols_hash = "d58a537b"

    def __init__(self, protocol):
        super().__init__(
            name=self.name,
            protocol=protocol,
            transformer=create_sample_loader(
                data_path=get_rc()[f"bob.db.{self.name}.directory"],
            ),
        )
