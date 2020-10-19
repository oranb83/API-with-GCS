import os
import logging

from helpers import plot_packet

logger = logging.getLogger(__name__)


class Plot:
    """
    Handles the convertion from packets to plots.
    """
    def  __init__(self, json_file):
        self.json_file = json_file

    def create_plots(self, root_dir):
        """
        Get json file, break it down to packets and generate a plot per packet.

        @type root_dir: str
        @param root_dir: plots main directory
        @rtype: tuple(<bool, str>)
        @return is_success: True if all packets has plots, otherwise False (see the TODO's)
        @return dirname: plots directory
        """
        # TODO: @oran - we need to send each packet or batch of packets to other services to deal
        #       with big files or we might have mem issues - anyway the server will be chocked.
        #       Let's assume it's ok for a POC.
        # Note: the json to packets should have return an iterator to at least avoid the mem
        #       issues.
        filename = os.path.splitext(os.path.basename(self.json_file))[0]
        dirname = os.path.join(root_dir, filename)
        is_success = True
        for i, packet in enumerate(packets):
            output_path = os.path.join(plot_directory, dirname, f'packet_{i}.png')
            # TODO: @oran - retries & handle bad packets.
            # Q: what to do in case of partial success - need to test and deal with this.
            try:
                plot_packet(packet, output_path)
            except Exception as e:
                # TODO: @oran - too broad exception, check which exceptions can be thrown here.
                logger.error('bad packet in file %s: %s', self.json_file, packet)
                is_success = False

        # TODO: @oran - use NamedTuple instead of tuple
        return is_success, dirname
