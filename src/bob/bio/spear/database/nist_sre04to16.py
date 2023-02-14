from bob.bio.base.database import CSVDatabase
from bob.bio.spear.database.utils import create_sample_loader, get_rc


class NistSRE04To16Database(CSVDatabase):
    """NIST-SRE (2004 - 2016) database definition."""

    name = "nist_sre04to16"
    category = "spear"
    dataset_protocols_name = "nist_sre04to16.tar.gz"
    dataset_protocols_urls = [
        "https://www.idiap.ch/software/bob/databases/latest/spear/nist_sre04to16-8bebb8d3.tar.gz",
        "http://www.idiap.ch/software/bob/databases/latest/spear/nist_sre04to16-8bebb8d3.tar.gz",
    ]
    dataset_protocols_hash = "8bebb8d3"

    def __init__(self, protocol):
        super().__init__(
            name=self.name,
            protocol=protocol,
            transformer=create_sample_loader(
                data_path=get_rc()[f"bob.db.{self.name}.directory"],
                data_ext=".sph",
                force_sample_rate=16000,
            ),
        )
