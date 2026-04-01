import logging
import socketserver
from typing import Any

import signalflow
from bitstring import ConstBitStream

import protocol
from patch import NotePatch

HOST = '0.0.0.0'
PORT = 4000
LOG_LEVEL = 0

logging.basicConfig(level=LOG_LEVEL)


class RPiSynthServer(socketserver.UDPServer):
    _graph: signalflow.AudioGraph
    _voices: dict[int, NotePatch]
    _settings: dict[str, Any]

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        self._graph = signalflow.AudioGraph()
        self._graph.poll(1.0)
        self._voices = {}
        self._settings = {
            'osc1_type': 0,
            'osc1_offset': 0.0,
            'osc1_amplitude': 0.0,
            'osc2_type': 0,
            'osc2_offset': 0.0,
            'osc2_amplitude': 0.0,
            'osc3_type': 0,
            'osc3_offset': 0.0,
            'osc3_amplitude': 0.0
        }
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)


class RPiSynthServerHandler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        data = self.request[0]
        if len(data) == 0:
            return

        try:
            bs = ConstBitStream(data)

            version = bs.read('uint8')
            if version != protocol.VERSION:
                logging.warning('Invalid protocol version={}'.format(version))
                return

            oc = bs.read('uint8')
            match oc:
                case 1:
                    self._patch(bs)
                case 2:
                    self._key_down(bs)
                case 3:
                    self._key_up(bs)
                case 4:
                    self._reset(bs)
                case _:
                    logging.warning('Unknown op_code={}'.format(oc))
        except Exception as e:
            logging.error('Failed to decode bytes: {} {}'.format(data, repr(e)))

    def _patch(self, bs: ConstBitStream) -> None:
        logging.debug('_patch()')

        d = protocol.oc1_decode(bs)

        self.server._settings = d
        for voice in self.server._voices.values():
            for k, v in self.server._settings.items():
                voice.set_input(k, v)

    def _key_down(self, bs: ConstBitStream) -> None:
        logging.debug('_key_down()')

        d = protocol.oc2_decode(bs)

        voices = self.server._voices
        
        if len(voices.keys()) > 6:
            logging.debug('Voices limit reached. Ignoring.')
            return
        
        if d['key'] not in voices.keys():
            patch = NotePatch()
            patch.set_input('note', d['key'])
            for k, v in self.server._settings.items():
                patch.set_input(k, v)
            patch.play()
            voices[d['key']] = patch

    def _key_up(self, bs: ConstBitStream) -> None:
        logging.debug('_key_up()')

        d = protocol.oc3_decode(bs)

        voices = self.server._voices
        if d['key'] in voices.keys():
            voices[d['key']].stop()
            del voices[d['key']]

    def _reset(self, bs: ConstBitStream) -> None:
        logging.debug('_reset()')

        d = protocol.oc3_decode(bs)

        voices = self.server._voices
        for k in list(voices.keys()):
            voices[k].stop()
            del voices[k]


def main():
    with RPiSynthServer((HOST, PORT), RPiSynthServerHandler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()


if __name__ == '__main__':
    main()
