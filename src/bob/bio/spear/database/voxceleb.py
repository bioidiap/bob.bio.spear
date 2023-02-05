from bob.bio.base.database import CSVDatabase
from bob.bio.spear.database.utils import create_sample_loader, get_rc


class VoxcelebDatabase(CSVDatabase):
    """VoxCeleb database definition."""

    name = "voxceleb"
    category = "spear"
    dataset_protocols_name = "voxceleb.tar.gz"
    dataset_protocols_urls = [
        "https://www.idiap.ch/software/bob/databases/latest/spear/voxceleb-4e0ba09d.tar.gz",
        "http://www.idiap.ch/software/bob/databases/latest/spear/voxceleb-4e0ba09d.tar.gz",
    ]
    dataset_protocols_hash = "4e0ba09d"

    def __init__(self, protocol):
        super().__init__(
            name=self.name,
            protocol=protocol,
            transformer=create_sample_loader(
                data_path=get_rc()[f"bob.db.{self.name}.directory"],
            ),
        )
