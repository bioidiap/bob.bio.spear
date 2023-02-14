from bob.bio.base.database import CSVDatabase
from bob.bio.spear.database.utils import create_sample_loader, get_rc


class AsvspoofDatabase(CSVDatabase):
    """ASV Spoof database definition."""

    name = "asvspoof"
    category = "spear"
    dataset_protocols_name = "asvspoof.tar.gz"
    dataset_protocols_urls = [
        "https://www.idiap.ch/software/bob/databases/latest/spear/asvspoof-24ec0e06.tar.gz",
        "http://www.idiap.ch/software/bob/databases/latest/spear/asvspoof-24ec0e06.tar.gz",
    ]
    dataset_protocols_hash = "24ec0e06"

    def __init__(self, protocol):
        super().__init__(
            name=self.name,
            protocol=protocol,
            transformer=create_sample_loader(
                data_path=get_rc()[f"bob.db.{self.name}.directory"],
            ),
        )
