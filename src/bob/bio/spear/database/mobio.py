from bob.bio.base.database import CSVDatabase
from bob.bio.spear.database.utils import create_sample_loader, get_rc


class MobioDatabase(CSVDatabase):
    """Mobio-audio database definition."""

    name = "mobio"
    category = "spear"
    dataset_protocols_name = "mobio.tar.gz"
    dataset_protocols_urls = [
        "https://www.idiap.ch/software/bob/databases/latest/spear/mobio-fb456ae5.tar.gz",
        "http://www.idiap.ch/software/bob/databases/latest/spear/mobio-fb456ae5.tar.gz",
    ]
    dataset_protocols_hash = "fb456ae5"

    def __init__(self, protocol):
        super().__init__(
            name=self.name,
            protocol=protocol,
            transformer=create_sample_loader(
                data_path=get_rc().get("bob.db.mobio.audio.directory", None),
            ),
        )
