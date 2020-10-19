import os
import sys
import json
import base64
import logging

import numpy as np
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)


def b64d(b):
    return base64.b64decode(b)


def should_b64d_k(k):
    return k.endswith('_b64')


def json_to_packets(json_file):
    if not json_file.endswith('.json'):
        logger.info("Failed, json file must end with '.json'")
        sys.exit(1)

    with open(json_file, 'r') as jsonf:
        packets = json.load(jsonf)

    def new_k(k):
        return k[:-len('_b64')] if should_b64d_k(k) else k

    def new_v(k, v):
        return b64d(v) if should_b64d_k(k) else v

    packets_b64_decoded = [{new_k(k): new_v(k, v) for k, v in packet.items()} for packet in packets]
    return packets_b64_decoded


def load_testbus_buffer(packet):
    def get_iq(data):
        Q = (np.bitwise_and(data, 0xff800000) >> 23).astype(np.int32)
        I = (np.bitwise_and(data, 0x007fc000) >> 14).astype(np.int32)
        return I, Q

    data = np.frombuffer(packet, dtype=np.uint32)
    I, Q = get_iq(data)

    I[I > 255] -= (2 ** 9)
    Q[Q > 255] -= (2 ** 9)
    IQ = I + 1j * Q

    return IQ


def plot_packet(packet, output_file):
    iq = load_testbus_buffer(packet['samples'])
    plt.plot(np.abs(iq))
    plt.savefig(output_file)
    plt.clf()


if __name__ == '__main__':
    json_file = sys.argv[1]
    packets = json_to_packets(json_file)
    plot_packet(packets[0], 'bla.png')

