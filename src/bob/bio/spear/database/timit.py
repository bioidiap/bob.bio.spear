from bob.bio.base.database import CSVDatabase
from bob.bio.spear.database.utils import create_sample_loader, get_rc


class TimitDatabase(CSVDatabase):
    """Timit database definition."""

    name = "timit"
    category = "spear"
    dataset_protocols_name = "timit.tar.gz"
    dataset_protocols_urls = [
        "https://www.idiap.ch/software/bob/databases/latest/spear/timit-7eee299f.tar.gz",
        "http://www.idiap.ch/software/bob/databases/latest/spear/timit-7eee299f.tar.gz",
    ]
    dataset_protocols_hash = "7eee299f"

    def __init__(self, protocol):
        super().__init__(
            name=self.name,
            protocol=protocol,
            transformer=create_sample_loader(
                data_path=get_rc()[f"bob.db.{self.name}.directory"],
            ),
        )
