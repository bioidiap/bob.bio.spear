#!/usr/bin/env python
# @author: Yannick Dayer <yannick.dayer@idiap.ch>
# @date: Tue 22 Jun 2021 14:53:03 UTC+02

from pathlib import Path

import pkg_resources

from click.testing import CliRunner

from bob.bio.spear.script.db_download import download_voxforge
from bob.extension.scripts.click_helper import assert_click_runner_result


def test_download_voxforge():

    dataset_protocol = pkg_resources.resource_filename(
        "bob.bio.spear.test", "data/dummy_dataset.tar.gz"
    )
    list_file = f"{dataset_protocol}:dummy/data_files_urls.csv"
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            download_voxforge,
            args=[
                "--list-file",
                list_file,
                "--destination",
                "dummy_files",
            ],
        )
        assert_click_runner_result(result)

        result_path = Path("dummy_files")
        assert result_path.exists()
        assert (result_path / "Dcoetzee-20110429-bne.tgz").exists()
        assert (result_path / "Dcoetzee-20110429-bne").exists()
        assert len(list(result_path.glob("*"))) == 20
