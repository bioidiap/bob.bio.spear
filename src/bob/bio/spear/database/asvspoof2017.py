"""Database interface for ASV Spoof 2017

This database has a custom class as there is only probe data in the sets (instead of
enrollment and probes).
It was defined for PAD experiments and should not belong in a bio package.

WIP YD 2022
"""

# "asvspoof2017": {
#     "local_filename": "asvspoof2017.tar.gz",
#     "definition_file": "asvspoof2017-db087bb7.tar.gz",  # TODO new format
#     "crc": "db087bb7",
# },


# from bob.pipelines import FileListDatabase
# from typing import Optional
# from sklearn.pipeline import make_pipeline

# from bob.bio.spear.transformer import PathToAudio

# def ASVSpoof2017CSVDatabase(
#     name:str = "ASVSpoof2017",
#     protocol: Optional[str] = None,
#     dataset_protocols_path: Optional[str] = None,
#     data_path: Optional[str] = None,
#     data_ext: str = ".wav",
#     annotations_path: Optional[str] = None,
#     annotations_ext: str = ".json",
#     force_sample_rate: Optional[int] = None,
#     force_channel: Optional[int] = None,
#     **kwargs,
# ) -> FileListDatabase:

#     # Load a path into the data of the sample
#     sample_loader = FileSampleLoader( # TODO: use a non-biometric class
#         data_loader=path_loader,
#         dataset_original_directory=data_path,
#         extension=data_ext,
#     )

#     # Read the file at path and set the data and metadata of a sample
#     path_to_sample = PathToAudio(
#         forced_channel=force_channel, forced_sr=force_sample_rate
#     )
#     return FileListDatabase(
#         protocol=protocol,
#         dataset_protocols_path=dataset_protocols_path,
#         transformer=path_to_sample,
#     )
