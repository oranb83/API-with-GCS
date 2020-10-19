import os
import logging

from google.cloud import storage

logger = logging.getLogger(__name__)


class GCS:
    """
    This class handles Google Cloud Storage list, download & upload commands.
    """
    def __init__(self, bucket):
        self.bucket = storage.Client.create_anonymous_client().get_bucket(bucket)

    def download(self, source_blob_filename, destination_filename):
        """
        Download a specific file.

        @type source_blob_filename: str
        @param source_blob_filename: gcs sub-path (everything after the bucket name)
        @type destination_filename: str
        @param destination_filename: local dir to file
        @rtype: str
        @return: output file full path
        @note: return the output path, since we might manipulate this path later on, that way the
               code doesn't need to change
        """
        logger.info('Downloading from %s to %s', source_blob_filename, destination_filename)
        blob = self.bucket.blob(source_blob_filename)

        # Note: consider moving the creation of the destination path outside of this class.
        #       I prefer not to use it with logic
        os.makedirs(os.path.dirname(destination_filename), exist_ok=True)

        blob.download_to_filename(destination_filename)
        logger.info('Download completed')

        return destination_filename

    def upload(self, source_filename, destination_blob_name):
        """
        Upload a specific file.

        @type source_filename: str
        @param source_filename: local path to file
        @type destination_blob_name: str
        @param destination_blob_name: gcs sub-path (everything after the bucket name)
        """
        logger.info('Uploading from %s to %s', source_filename, destination_blob_name)
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_filename)
        logger.info('Upload completed')
