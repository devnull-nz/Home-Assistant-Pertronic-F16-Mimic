import socket
import traceback
import logging
import time

from threading import Thread
from .CustomFormatter import CustomFormatter

__version__ = "0.1"
_LOGGER = logging.getLogger(__name__)


class PertronicMimic:
    def __init__(self, ip=None, port=None, timeout=5, full_name=None, short_name=None):
        # Logging Setup
        self.log = logging.getLogger("PertronicMimic")
        self.log.setLevel(logging.DEBUG)
        self.log.debug("Loading...")
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(CustomFormatter())
        self.log.addHandler(ch)

        self._ip = ip
        self._port = port
        self._timeout = timeout

        self._full_name = full_name
        self._short_name = short_name

        self._run_thread = None

        self._run = False

        self._zone_states = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        self._zones_none = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        self._is_normal = None
        self._is_defect = None
        self._is_fire = None
        self._is_sprinkler = None

        self._handlers_normal = []
        self._handlers_defect = []
        self._handlers_fire = []
        self._handlers_sprinkler = []
        self._handlers_zone = []

    def get_name(self) -> str:
        return self._full_name

    def get_short_name(self) -> str:
        return self._short_name

    def test_connection(self, ip=None, port=None):
        if ip is None and port is None:
            ip = self._ip
            port = self._port

        self.log.info("Testing connection to TCP://{0}:{1}".format(ip, port))

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self._timeout)
                s.connect((ip, port))
                s.close()
                self.log.info("Connection Successful")
                return True

        except Exception as e:
            self.log.error("Connection Test Failed")
            self.log.error(e)
        return False

    def start(self):
        self.log.debug("Starting COMMS thread")

        if self.test_connection():
            self._run = True
            self.__do_callbacks(None, None, None, None, self._zones_none)
            self._run_thread = Thread(target=self.__run, args=())
            self._run_thread.start()

    def stop(self):
        self.log.debug("Stopping...")
        self._run = False
        self.__do_callbacks(None, None, None, None, self._zones_none)

    def __run(self):
        while self._run is True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(self._timeout)
                    s.connect((self._ip, self._port))
                    self.log.debug("New Connection")
                    while self._run is True:
                        self.__process_packet(s.recv(1024))
                    s.close()
            except Exception as e:
                s.close()
                self.log.error(e)
                self.__do_callbacks(None, None, None, None, self._zones_none)
                time.sleep(1)

    def __process_packet(self, data):
        # Packets
        # LED Mimic
        # 0  1  2  3  4  5  6  7  8  9  10
        # 10 09 00 00 00 00 00 00 EC 34 C5
        #
        # 0: Address
        # 1: Unknown
        # 2: Defect(0100 0000), Fire(1000 0000), Sprinkler(0001 0000), Normal (0000 0000)
        # 3: Unknown
        # 4: Zone indications 1-8 (binary encoded boolean, ie zone 2 = 02(0000 0010) )
        # 5: Zone indications 9-16 (binary encoded boolean, ie zone 2 = 02(0000 0010) )
        # 6: Zone indications 17-24 (binary encoded boolean, ie zone 2 = 02(0000 0010) )
        # 7: Zone indications 25-32 (binary encoded boolean, ie zone 2 = 02(0000 0010) )
        # 8:  Unknown
        # 9:  Checksum
        # 10: Checksum

        if len(data) == 11 and data[0] == 0x10 and data[1] == 0x09:
            zone_states = [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ]

            for j in range(4):
                for i in range(8):
                    op = 1 << i
                    zone_states[(j * 4) + i] = (data[4 + j] & op) == op

            self.__do_callbacks(
                data[2] == 0,
                (data[2] & 0x40) == 0x40,
                (data[2] & 0x80) == 0x80,
                (data[2] & 0x10) == 0x10,
                zone_states,
            )
        else:
            # print(data)
            pass

    def force_callbacks(self):
        self.__do_callbacks(
            self._is_normal,
            self._is_defect,
            self._is_fire,
            self._is_sprinkler,
            self._zone_states,
        )

    def __do_callbacks(self, is_normal, is_defect, is_fire, is_sprinkler, zones):
        if is_normal != self._is_normal:
            self._is_normal = is_normal
            for i in range(len(self._handlers_normal)):
                try:
                    self._handlers_normal[i](is_normal)
                except Exception as e:
                    self.log.error(e)

        if is_defect != self._is_defect:
            self._is_defect = is_defect
            for i in range(len(self._handlers_defect)):
                try:
                    self._handlers_defect[i](is_defect)
                except Exception as e:
                    self.log.error(e)

        if is_fire != self._is_fire:
            self._is_fire = is_fire
            for i in range(len(self._handlers_fire)):
                try:
                    self._handlers_fire[i](is_fire)
                except Exception as e:
                    self.log.error(e)

        if is_sprinkler != self._is_sprinkler:
            self._is_sprinkler = is_sprinkler
            for i in range(len(self._handlers_sprinkler)):
                try:
                    self._handlers_sprinkler[i](is_sprinkler)
                except Exception as e:
                    self.log.error(e)

        if zones != self._zone_states:
            self._zone_states = zones
            for i in range(len(self._handlers_zone)):
                try:
                    self._handlers_zone[i](zones)
                except Exception as e:
                    self.log.error(e)

        # print(self)

    def get_normal(self):
        return self._is_normal

    def get_defect(self):
        return self._is_defect

    def get_fire(self):
        return self._is_fire

    def get_sprinkler(self):
        return self._is_sprinkler

    def get_zone(self, zone):
        if zone < len(self._zone_states):
            return self._zone_states[zone]
        else:
            return None

    def get_zones(self):
        return self._zone_states

    def register_normal_callback(self, handler):
        self._handlers_normal.append(handler)

    def register_defect_callback(self, handler):
        self._handlers_defect.append(handler)

    def register_fire_callback(self, handler):
        self._handlers_fire.append(handler)

    def register_sprinkler_callback(self, handler):
        self._handlers_sprinkler.append(handler)

    def register_zone_callback(self, handler):
        self._handlers_zone.append(handler)

    def __str__(self):
        return "Normal:{}, Defect:{}, Fire:{}, Sprinkler:{}".format(
            self._is_normal, self._is_defect, self._is_fire, self._is_sprinkler
        )
