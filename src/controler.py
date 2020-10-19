import os

from src.gcs import GCS
from src.helpers import json_to_packets
from src.zipper import Zip
from src.plot import Plot

# TODO: @oran - all the constants should be in KMS so I can manage my environment -
#       bare minimum is to use a config file.
# TODO: @oran - do I need to change the "Small" prefix via code, is there a huristic I can use
#       instead or get it from the client - I prefer the client will not be aware to buckets paths
#       for security reasons and in case I want to make API changes instead of releasing a new API
#       version.
PROJECT_NAME = ''
BACKET_NAME = 'levl-backend-file-examples'
BACKET_PREFIX = 'Small/{}'
BACKET_PREFIX_PLOTS = 'Small/plots/{}'
LOCAL_PLOT_DIRECTORY = 'tmp/plots/'

storage_client = GCS(PROJECT_NAME, BACKET_NAME)
ziper = Zip()


class Controler:
    """
    This class is part of MVC approach.
    """
    def create_plot(self, filename):
        """
        This method does the following (which is too much):
            1. Update the DB to "in progress" (not done)
            2. Verify that the file exist in GCS (not done)
            3. Download the file from GCS.
            4. Do convertion from json file to packets.
            5. Plot per packet.
            6. Upload plots to a new bucket (we will use the only bucket I have with a dirname of
               the json file for all of it's packet plots).
            7. Update the DB to "success" (not done)
               Also need to update the DB to "fail" if any other step failed (not done)

        @note: need to send data to SQL DB upon start (in progress) and change it to
               in_progress / success / failed later. I did not get any open DB in GCP so this part
               will not be done!
        @note: need to return status and failed parts of the process: file or problematic packets,
               depands on the implementation of the the TODOs
        """
        download_source_file = BACKET_PREFIX.format(filename)
        download_destination_file = os.path.join(LOCAL_PLOT_DIRECTORY, filename)

        # Download file from GCS
        json_file = storage_client.download(download_source_file, download_destination_file)

        # Get packets
        packets = iter(json_to_packets(json_file))

        # Create plot from packets
        # TODO: @oran - we need to send each packet or batch of packets to other services to
        #       deal with big files or we might have mem issues - I used iter above but it should
        #       have been done in the helpers.py and not in the above line - too late!.
        #       Let's assume it's ok for a POC.
        is_success, plots_dir = Plot(LOCAL_PLOT_DIRECTORY).create_plots(json_file, packets)
        if not is_success:
            logger.warning('Not all packets where successfuly parsed in this file: %s', filename)

        # Zipping the directory
        # TOOD: @oran - what happends if one package is corrupted? - need to deal with this case:
        #       either fail all or return the problematic package.
        #       (I prefer to fail it with a good log) - we should have all the failed processes in
        #       the db, so we can add another script to scan and fix them or decide what to do with
        #       them if we can't fix them. For example a status api would have easily helped us to
        #       write code to deal with this issue with some logic.
        upload_source_file = ziper.zipdir(plots_dir)

        # Uploading file to GCS
        upload_destination_file = os.path.join(BACKET_PREFIX_PLOTS.format(upload_source_file), BACKET_PREFIX.format(filename))
        storage_client.upload(upload_source_file, upload_destination_file)

        # TODO: @oran - remove the local data, json file and plot

    def get_plots(self, filename):
        """
        Steps:
            1. Need to list the filename in GCS
            2. Sending a hash that will be used by another API to download the plot.
        Note: hash is the best practice, since it will be harder to sniff our buckets names
              in GCS. I am aware that we are using HTTPS, but the trigger to download the file and
              select it's location is under the client responsiblity (FE). Best practices should be
              maintained even if the API is backend facing since we don't know what we want to do
              in the future. Maybe a client will use the API as SDK to build his own interface or
              maybe we will.
              If we want do the hashing we will need to return the filepath in GCS,
              so the client can download via browser - at that point we are exposed!.
              So to hide it we will send a hash of the filepath location in GCS. We can easily
              revert by using Salt for example: two way hashing with unique encryption key.
        """
        pass
