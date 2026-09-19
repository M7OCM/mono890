# Copyright 2023 Jim Unroe <rock.unroe@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import struct
import logging

from chirp import chirp_common, directory, memmap
from chirp import bitwise, errors, util
from chirp.settings import RadioSetting, RadioSettingGroup, \
    RadioSettingValueInteger, RadioSettingValueList, \
    RadioSettingValueBoolean, RadioSettingValueString, \
    RadioSettingValueFloat, RadioSettings

LOG = logging.getLogger(__name__)

MEM_FORMAT = """
struct memory {
  ul32 rxfreq;      // RX Frequency          00-03
  ul16 rx_tone;     // PL/DPL Decode         04-05
  ul32 txfreq;      // TX Frequency          06-09
  ul16 tx_tone;     // PL/DPL Encode         0a-0b
  ul24 mutecode;    // Mute Code             0c-0e
  u8 unknown_0:2,   //                       0f
     mutetype:2,    // Mute Type
     unknown_1:4;   //
  u8 isnarrow:1,    // Bandwidth             00
     lowpower:1,    // Power
     scan:1,        // Scan Add
     bcl:2,         // Busy Lock
     modulation_type:2,  // RX Modulation Type 
     unknown_4:1;   //
  u8 unknown_5;     //                       01
  u8 scramblecode;  // Scrambler Code        02
  u8 bank8:1,   //                       03
     bank7:1,
     bank6:1,
     bank5:1,
     bank4:1,
     bank3:1,
     bank2:1,
     bank1:1;
  u8 unknown_6[2];  //                       04-05
  char name[10];    //                       06-0f
};

#seekto 0x1000;
struct memory channels[999];

#seekto 0x0000;
struct {
  char startuplabel[32];  // Startup Label         0000-001f
  char personalid[16];    // Personal ID           0020-002f
  u8 displaylogo:1,       // Display Startup Logo  0030
     displayvoltage:1,    // Display Voltage
     displaylabel:1,      // Display Startup Label
     whatisthis:1,        // firmware names this bit "WhatIsThis" - undocumented, not Tail Tone (see 0044 below)
     startupringtone:1,   // Startup Ringtone
     voiceprompt:1,       // Voice Prompt
     keybeep:1,           // Key Beep
     unknown_0:1;
  u8 txpriority:1,        // TX Priority           0031
     rogerbeep:2,         // Roger Beep
     savemode:1,          // Save Mode
     frequencystep:4;     // Frequency Step
  u8 squelch:4,           // Squelch               0032
     talkaround:2,        // Talkaround
     noaaalarm:1,         // NOAA Alarm
     dualdisplay:1;       // Dual Display
  u8 displaytimer;        // Display Timer         0033
  u8 locktimer;           // Lock Timer            0034
  u8 timeouttimer;        // Timeout Timer         0035
  u8 voxlevel:4,          // VOX Level             0036
     voxdelay:4;          // Delay
  ul16 tonefrequency;     // Tone Frequency        0037-0038
  ul16 fmfrequency;       // FM Frequency          0039-003a
  u8 fmstandby:1,         // FM Standby            003b
     dualstandby:1,       // Dual Standby
     standbyarea:1,       // Standby Area
     scandirection:1,     // Scan Direction
     unknown_2:2,
     workmode:1,          // Work Mode
     unknown_3:1;
  ul16 areaach;           // Area A CH             003c-003d
  ul16 areabch;           // Area B CH             003e-003f
  u8 key1long;             // Key 1 Long            0040
  u8 key1short;            // Key 1 Short           0041
  u8 key2long;             // Key 2 Long            0042
  u8 key2short;            // Key 2 Short           0043
  u8 unknown_10:1,         //                       0044
     bflock:1,
     currentvfo:1,
     tailtone:1,           // Tail Tone (verified: gSettings 0x14 bit4)
     vox:1,                // VOX
     lock:1,
     benabledisplay:1,
     buseVHF:1;
  u8 xposition;           // X position (0-159)    0045
  u8 yposition;           // Y position (0-110)    0046
  ul16 unknown_bordercolor; // was Border Color, now hardcoded  0047-0048
  u8 unknown_6[7];        // 0x00                  0049-004f
  u8 bandinfo[8];         // per-band identity map 0050-0057
                          // (BAND_136/400/64/174/240/320/480MHz -
                          // see radio/frequencies.h; NOT a TX-permit
                          // flag, deliberately not exposed as a
                          // setting here - see get_settings())
  u8 unused_4[20];        // 0xFF                  0058-006b
  u8 dtmfstate;           // DTMF Kill/Stun state  006c
  u8 unknown_9[3];        // 0x00                  006d-006f
  ul16 quickch2;          // Quick CH 2            0070-0071
  ul16 quickch1;          // Quick CH 1            0072-0073
  ul16 quickch4;          // Quick CH 4            0074-0075
  ul16 quickch3;          // Quick CH 3            0076-0077
} settings;

#seekto 0x8D20;
struct {
  u8 senddelay;           // Send Delay            8d20
  u8 sendinterval;        // Send Interval         8d21
  u8 unused_0:6,          //                       8d22
     sendmode:2;          // Send Mode
  u8 unused_2:4,          //                       8d23
     sendselect:4;        // Send Select
  u8 unused_3:7,          //                       8d24
     recvdisplay:1;       // Recv Display
  u8 encodegain;          // Encode Gain           8d25
  u8 decodeth;            // Decode TH             8d26
} dtmf;

#seekto 0x8D30;
struct {
  char code[14];          // DTMF code
  u8 unused_ff;
  u8 code_len;            // DTMF code length
} dtmfcode[16];

#seekto 0x8E30;
struct {
  char kill[14];          // Remotely Kill         8e30-8e3d
  u8 unknown_0;           //                       8e3e
  u8 kill_len;            // Remotely Kill Length  83ef
  char stun[14];          // Remotely Stun         8e40-834d
  u8 unknown_1;           //                       8e4e
  u8 stun_len;            // Remotely Stun Length  8e4f
  char wakeup[14];        // Wake Up               8e50-8e5d
  u8 unknown_2;           //                       8e5e
  u8 wakeup_len;          // Wake Up Length        8e5f
} dtmf2;

#seekto 0xA000;
struct {
  u8 currentbank:3,   // Current Bank (Toggle Bank target) a000
     scanblink:1,         // Scan Blink
     darkmode:1,          // Dark Mode
     amfixenabled:1,      // AM Fix Enabled
     scanresume:2;        // Scan Resume
  u8 keyshortcut[14];     // 0-9/*/#/Menu/Exit key long-press      a001-a00e
  u8 txprohibit:1,        // TX Prohibit (blocks all TX)           a00f
     micgainlevel:6,      // Mic Gain (0-31 valid; field is 6 bits)
     scanall:1;           // Scan All
  u8 unknown_pcbpad:1,    // undeclared padding bit in firmware    a010
     pcbversion:1,        // PCB Revision (0=2.0, 1=2.1)
     vhfcutoff:2,         // VHF Filter Cutoff
     amfixhysteresis:3,   // AM Fix Hysteresis profile
     ledheartbeat:1;      // LED Heartbeat
  i8 amfixrssitrimdb;     // AM Fix Antenna RSSI Trim (dB)         a011
  ul32 scanrangestart;    // Scan Range Start (raw, x10Hz)         a012-a015
  ul32 scanrangefinish;   // Scan Range Finish (raw, x10Hz)        a016-a019
  u8 unused_ext[102];     // pads out to the 0x80 block read/written a01a-a07f
} extsettings;

"""

CMD_ACK = b"\x06"

DTCS_CODES = tuple(sorted(chirp_common.DTCS_CODES + (645,)))

_STEP_LIST = [0.01, 0.25, 1.25, 2.5, 5., 6.25, 8.33, 10., 12.5, 25., 50., 100., 500.,
              1000., 5000.]

LIST_AB = ["A", "B"]
LIST_BCL = ["Off", "Carrier", "CTC/DCS"]
LIST_DELAY = ["%s ms" % x for x in range(0, 2100, 100)]
LIST_DIRECTION = ["Up", "Down"]
LIST_FREQSTEP = ["0.01", "0.25K", "1.25K", "2.5K", "5K", "6.25K", "8.33K", "10K", "12.5K",
                 "20K", "25K", "50K", "100K", "500K", "1M", "5M"]
LIST_INTERVAL = ["%s ms" % x for x in range(30, 210, 10)]
LIST_MUTETYPE = ["Off", "-", "23b", "24b"]
LIST_ROGER = ["Off", "Roger 1", "Roger 2", "Send ID"]
LIST_SENDM = ["Off", "TX Start", "TX End", "Start and End"]
LIST_SENDS = ["DTMF %s" % x for x in range(1, 17)]
# Verified against task/keyaction.h in the EVOLUTION X source (the
# `enum { ACTION_NONE = 0, ACTION_MONITOR, ... ACTION_TX_PROHIBIT,
# ACTIONS_COUNT }` block) - index here must match enum order exactly,
# since the radio stores the raw enum value.
LIST_SKEY = ["None", "Monitor", "Frequency Detect", "Repeater Mode",
             "Preset Channel", "Local Alarm", "Remote Alarm",
             "NOAA Channel", "Send Tone", "Roger Beep", "FM Radio",
             "Scan", "Flashlight", "AM Fix", "VOX", "TX Power",
             "SQ Level", "Dual Standby", "Backlight", "Freq Step",
             "Beep", "Toggle Bank", "DTMF Decode", "Dual Display",
             "TX Freq", "Lock", "Spectrum", "Dark Mode", "AGC Mode",
             "Reg Edit", "Mic Gain", "Modulation", "Band Width",
             "TX CTCSS/DCS", "TX Priority", "TX Prohibit"]


def _dynamic_options(base_list, raw_value, unknown_fmt="Unknown (%d)"):
    """Extend base_list so raw_value is always representable.

    Several small enum-ish fields in this radio (key functions, AM Fix
    Hysteresis, VHF cutoff, etc.) have more raw values possible than
    this driver has names for - either because the field is wider than
    the number of options currently defined, or because of an erased-
    flash sentinel (0xFF). Clamping an unrecognized value down to the
    nearest known one is lossy: since CHIRP always uploads the entire
    memory image, that clamped value gets written straight back to the
    radio, silently overwriting whatever was actually there. Extending
    the option list on the fly instead means an unrecognized value
    round-trips untouched.
    """
    options = list(base_list)
    for i in range(len(options), max(raw_value, len(options) - 1) + 1):
        options.append(unknown_fmt % i)
    return options


def _skey_options(raw_value):
    """Build the key-function option list for a single key setting.

    key1long/key1short/key2long/key2short are full bytes (0-255) in
    the actual firmware (gSettings.Actions[4], verified in
    task/keyaction.c) - not 4-bit nibbles as an earlier version of
    this driver assumed. That earlier nibble-width mismatch meant any
    action value >= 16 was unrepresentable, and every settings upload
    silently truncated the byte down to its low nibble - corrupting
    any key assigned to one of the many functions this firmware added
    past the original 10 (FM Radio, Spectrum, TX Prohibit, etc).

    LIST_SKEY now covers all 36 actions this firmware defines; see
    _dynamic_options for how anything beyond that is handled.
    """
    return _dynamic_options(LIST_SKEY, raw_value, "Unknown Function (%d)")


LIST_REPEATER = ["Off", "Talkaround", "Frequency Reversal"]
LIST_TIMER = ["Off", "5 seconds", "10 seconds"] + [
              "%s seconds" % x for x in range(15, 615, 15)]
LIST_TXPRI = ["Edit", "Busy"]
LIST_WORKMODE = ["Frequency", "Channel"]
LIST_DTMFSTATE = ["Normal", "Stunned", "Killed"]
LIST_SCANRESUME = ["Carrier", "Time", "No"]
LIST_AMFIXHYST = ["Narrow", "Tight", "Default", "Relaxed", "Wide"]
LIST_VHFCUTOFF = ["240 MHz", "280 MHz", "300 MHz"]
LIST_PCBVERSION = ["PCB 2.0", "PCB 2.1"]
LIST_BANK8 = ["Bank %d" % n for n in range(1, 9)]
KEYSHORTCUT_LABELS = ["0 Key Long", "1 Key Long", "2 Key Long",
                      "3 Key Long", "4 Key Long", "5 Key Long",
                      "6 Key Long", "7 Key Long", "8 Key Long",
                      "9 Key Long", "* Key Long", "# Key Long",
                      "Menu Key Long", "Exit Key Long"]

LIST_BANK = ["No", "Yes"]

VALID_CHARS = chirp_common.CHARSET_ALPHANUMERIC + \
    "`{|}!\"#$%&'()*+,-./:;<=>?@[]^_"
DTMF_CHARS = list("0123456789ABCD*#")


def _checksum(data):
    cs = 0
    for byte in data:
        cs += byte
    return cs % 256


def _enter_programming_mode(radio):
    serial = radio.pipe

    exito = False
    for i in range(0, 5):
        serial.write(radio.magic)
        ack = serial.read(1)

        try:
            if ack == CMD_ACK:
                exito = True
                break
        except Exception:
            LOG.debug("Attempt #%s, failed, trying again" % i)
            pass

    # check if we had EXITO
    if exito is False:
        msg = "The radio did not accept program mode after five tries.\n"
        msg += "Check you interface cable and power cycle your radio."
        raise errors.RadioError(msg)


def _exit_programming_mode(radio):
    serial = radio.pipe
    try:
        serial.write(b"58" + b"\x05\xEE\x60")
    except Exception:
        raise errors.RadioError("Radio refused to exit programming mode")


def _read_block(radio, block_addr, block_size):
    serial = radio.pipe

    cmd = struct.pack(">BH", ord(b'R'), block_addr + radio.READ_OFFSET)

    ccs = bytes([_checksum(cmd)])

    expectedresponse = b"R" + cmd[1:]

    cmd = cmd + ccs

    LOG.debug("Reading block %04x..." % block_addr)

    try:
        serial.write(cmd)
        response = serial.read(3 + block_size + 1)

        cs = _checksum(response[:-1])

        if response[:3] != expectedresponse:
            raise Exception("Error reading block %04x." % block_addr)

        chunk = response[3:]

        if chunk[-1] != cs:
            raise Exception("Block failed checksum!")

        block_data = chunk[:-1]
    except Exception:
        raise errors.RadioError("Failed to read block at %04x" % block_addr)

    return block_data


def _write_block(radio, block_addr, block_size):
    serial = radio.pipe

    # map the upload address to the mmap start and end addresses
    start_addr = block_addr * block_size
    end_addr = start_addr + block_size

    data = radio.get_mmap()[start_addr:end_addr]

    cmd = struct.pack(">BH", ord(b'I'), block_addr)

    cs = bytes([_checksum(cmd + data)])
    data += cs

    LOG.debug("Writing Data:")
    LOG.debug(util.hexprint(cmd + data))

    try:
        serial.write(cmd + data)
        if serial.read(1) != CMD_ACK:
            raise Exception("No ACK")
    except Exception:
        raise errors.RadioError("Failed to send block "
                                "to radio at %04x" % block_addr)


def _read_ext_block(radio):
    """Read the one extended-settings block (gExtendedSettings, firmware
    r2+). This lives at flash 0x3D5000, outside the primary window the
    rest of this driver reads, so it needs its own read address - same
    generic 'R' read command as _read_block, just a fixed offset since
    there's only ever this one block."""
    serial = radio.pipe

    cmd = struct.pack(">BH", ord(b'R'), radio.EXT_READ_OFFSET)
    ccs = bytes([_checksum(cmd)])
    expectedresponse = b"R" + cmd[1:]
    cmd = cmd + ccs

    LOG.debug("Reading extended settings block...")

    try:
        serial.write(cmd)
        response = serial.read(3 + radio.EXT_BLOCK_SIZE + 1)

        cs = _checksum(response[:-1])

        if response[:3] != expectedresponse:
            raise Exception("Error reading extended settings block.")

        chunk = response[3:]

        if chunk[-1] != cs:
            raise Exception("Extended settings block failed checksum!")

        block_data = chunk[:-1]
    except Exception:
        raise errors.RadioError("Failed to read extended settings block")

    return block_data


def _write_ext_block(radio):
    """Write the one extended-settings block. Requires firmware r2's new
    UART command (0x4A) - the existing 'I' write command only erases and
    rewrites the primary region's 10 pages, and has no reach to flash
    0x3D5000. Firmware erases the whole 4KB page for this command, and
    nothing else lives on that page (verified against the r2 source), so
    sending the full 128-byte block every time is safe even though only
    the first 26 bytes (sizeof gExtendedSettings_t) are meaningful."""
    serial = radio.pipe

    data = radio.get_mmap()[radio.EXT_LOCAL_ADDR:
                            radio.EXT_LOCAL_ADDR + radio.EXT_BLOCK_SIZE]

    cmd = struct.pack(">BH", radio.EXT_WRITE_CMD, 0)

    cs = bytes([_checksum(cmd + data)])
    data += cs

    LOG.debug("Writing extended settings block:")
    LOG.debug(util.hexprint(cmd + data))

    try:
        serial.write(cmd + data)
        if serial.read(1) != CMD_ACK:
            raise Exception("No ACK")
    except Exception:
        raise errors.RadioError("Failed to send extended settings block")


def do_download(radio):
    LOG.debug("download")
    _enter_programming_mode(radio)

    data = b""

    status = chirp_common.Status()
    status.msg = "Cloning from radio"

    status.cur = 0
    status.max = radio.END_ADDR + 1

    for addr in range(radio.START_ADDR, radio.END_ADDR, 1):
        status.cur = addr
        radio.status_fn(status)

        block = _read_block(radio, addr, radio.BLOCK_SIZE)
        data += block

        LOG.debug("Address: %04x" % addr)
        LOG.debug(util.hexprint(block))

    status.cur = radio.END_ADDR
    radio.status_fn(status)
    data += _read_ext_block(radio)

    _exit_programming_mode(radio)

    return memmap.MemoryMapBytes(data)


def do_upload(radio):
    status = chirp_common.Status()
    status.msg = "Uploading to radio"

    _enter_programming_mode(radio)

    status.cur = 0
    status.max = radio._memsize

    # The OEM software reads the 1st block from the radio before commencing
    # with the upload. That behavior will be mirrored here.
    _read_block(radio, radio.START_ADDR, radio.BLOCK_SIZE)

    for start_addr, end_addr in radio._ranges:
        for addr in range(start_addr, end_addr, 1):
            status.cur = addr * radio.BLOCK_SIZE
            radio.status_fn(status)
            _write_block(radio, addr, radio.BLOCK_SIZE)

    status.cur = radio.EXT_LOCAL_ADDR
    radio.status_fn(status)
    if radio._confirmed_r2_plus:
        _write_ext_block(radio)
    else:
        LOG.warning(
            "Skipping extended-settings write: r2+ not confirmed for "
            "this upload (see the 'EVOLUTION X: Read Me First' group). "
            "Everything else was uploaded normally.")

    _exit_programming_mode(radio)


def _split(rf, f1, f2):
    """Returns False if the two freqs are in the same band (no split)
    or True otherwise"""

    # determine if the two freqs are in the same band
    for low, high in rf.valid_bands:
        if f1 >= low and f1 <= high and \
                f2 >= low and f2 <= high:
            # if the two freqs are on the same Band this is not a split
            return False

    # if you get here is because the freq pairs are split
    return True


class IradioUV5118plus(chirp_common.CloneModeRadio):
    """Radtel RT-890 Custom"""
    VENDOR = "Radtel"
    MODEL = "RT-890 Custom"
    NAME_LENGTH = 10
    BAUD_RATE = 115200
    NEEDS_COMPAT_SERIAL = False

    BLOCK_SIZE = 0x80
    magic = b"58" + b"\x05\x10\x82"

    VALID_BANDS = [(10000000, 136000000),  # RX only (Air Band)
                   (136000000, 174000000),  # TX/RX (VHF)
                   (174000000, 240000000),  # TX/RX
                   (240000000, 320000000),  # TX/RX
                   (320000000, 400000000),  # TX/RX
                   (400000000, 480000000),  # TX/RX (UHF)
                   (480000000, 1300000000)]  # TX/RX

    POWER_LEVELS = [chirp_common.PowerLevel("High", watts=2.00),
                    chirp_common.PowerLevel("Low", watts=0.50)]

    # Radio's write address starts at 0x0000
    # Radio's write address ends at 0x0140
    START_ADDR = 0
    END_ADDR = 0x0140
    # Radio's read address starts at 0x7820
    # Radio's read address ends at 0x795F
    READ_OFFSET = 0x7820

    _ranges = [
               (0x0000, 0x0140),
              ]
    _memsize = 0xA080  # 0xA000 primary (0x0140 * 0x80) + 0x80 extended

    # gExtendedSettings (AM Fix Hysteresis, VHF cutoff, PCB revision,
    # TX Prohibit, Mic Gain, Scan Range, numpad shortcuts, etc.) lives
    # at flash 0x3D5000 - well outside the 0x3C1000-0x3CB000 window
    # above, and on its own isolated flash page (verified nothing else
    # is stored in 0x3D5000-0x3D7FFF). Reachable on read with the same
    # generic 'R' command via a different offset; writing it needs
    # firmware r2's new command 0x4A, since the existing write command
    # ('I') only erases/writes the primary window's 10 pages.
    # Handled as a genuinely separate region (own read/write helpers,
    # appended after the primary loop) rather than folded into one
    # bigger linear range, so the primary download/upload - the fast,
    # already-working path - is untouched and doesn't slow down.
    EXT_BLOCK_SIZE = 0x80
    EXT_READ_OFFSET = 0x7AA0    # 0x3D5000 // 128
    EXT_WRITE_CMD = 0x4A
    EXT_LOCAL_ADDR = 0xA000     # where this region sits in our own mmap

    # Writing the extended-settings block (command 0x4A) requires r2+
    # firmware. There's no way to query firmware version over this
    # protocol, and an unrecognized command doesn't fail visibly - on
    # r1 firmware it would write 128 bytes to flash address 0x000000
    # (Page/Count default to 0 when Command matches no case - verified
    # against r1's app/uart.c), corrupting the start of the region
    # command 0x40 owns. Defaults False every session; only an
    # explicit, un-memory-backed checkbox in Settings sets it True, so
    # uploading to an unconfirmed/older radio silently skips this one
    # block rather than risk it.
    _confirmed_r2_plus = False

    _upper = 999

    def get_features(self):
        rf = chirp_common.RadioFeatures()
        rf.has_settings = True
        rf.has_bank = False
        rf.has_ctone = True
        rf.has_cross = True
        rf.has_rx_dtcs = True
        rf.has_tuning_step = False
        rf.can_odd_split = True
        rf.has_name = True
        rf.valid_name_length = self.NAME_LENGTH
        rf.valid_characters = chirp_common.CHARSET_ASCII
        # A genuinely empty list is what actually hides this column
        # (memedit.py: "if not col_def.valid: self._grid.HideCol(col)",
        # and ChirpSkipColumn.valid returns this list directly) -
        # [""] is still a non-empty (truthy) list, so it doesn't hide
        # anything, just leaves a blank dropdown - confirmed on
        # hardware. ScanAdd (the bit "skip" maps to) is written as a
        # default when a channel is created but never actually read by
        # the scan task - confirmed against radio/channels.c,
        # task/scanner.c and app/menu.c. Scan inclusion is entirely
        # governed by bank membership (IsInscanList) instead.
        rf.valid_skips = []
        rf.valid_tmodes = ["", "Tone", "TSQL", "DTCS", "Cross"]
        rf.valid_cross_modes = ["Tone->Tone", "Tone->DTCS", "DTCS->Tone",
                                "->Tone", "->DTCS", "DTCS->", "DTCS->DTCS"]
        rf.valid_power_levels = self.POWER_LEVELS
        rf.valid_duplexes = ["", "-", "+", "split"]
        rf.valid_modes = ["FM", "NFM", "AM", "LSB", "USB"]  # FM:25 kHz, NFM:12.5 kHz.
        rf.valid_dtcs_codes = DTCS_CODES
        rf.memory_bounds = (1, self._upper)
        rf.valid_tuning_steps = _STEP_LIST
        rf.valid_bands = self.VALID_BANDS

        return rf

    def process_mmap(self):
        if len(self._mmap) < self._memsize:
            # A file saved before the extended-settings region existed
            # (pre-r2 firmware/driver) is exactly the old 0xA000 bytes -
            # channels and the original settings are all still valid,
            # they just predate gExtendedSettings entirely. Pad with
            # zeroed defaults rather than let the parser hit the end of
            # the buffer the moment the Settings tab reads that region.
            LOG.warning(
                "Loaded image is %d bytes, expected %d - looks like a "
                "file saved before the extended-settings region existed "
                "(pre-r2). Padding with defaults; review the EVOLUTION X "
                "settings groups before uploading this file." %
                (len(self._mmap), self._memsize))
            padded = self._mmap.get_packed() + bytes(
                self._memsize - len(self._mmap))
            self._mmap = memmap.MemoryMapBytes(padded)
        self._memobj = bitwise.parse(MEM_FORMAT, self._mmap)

    def sync_in(self):
        """Download from radio"""
        try:
            data = do_download(self)
        except errors.RadioError:
            # Pass through any real errors we raise
            raise
        except Exception:
            # If anything unexpected happens, make sure we raise
            # a RadioError and log the problem
            LOG.exception('Unexpected error during download')
            raise errors.RadioError('Unexpected error communicating '
                                    'with the radio')
        self._mmap = data
        self.process_mmap()

    def sync_out(self):
        """Upload to radio"""
        try:
            do_upload(self)
        except Exception:
            # If anything unexpected happens, make sure we raise
            # a RadioError and log the problem
            LOG.exception('Unexpected error during upload')
            raise errors.RadioError('Unexpected error communicating '
                                    'with the radio')

    def get_raw_memory(self, number):
        return repr(self._memobj.memory[number - 1])

    @staticmethod
    def _decode_tone(toneval):
        # DCS examples:
        # D023N - 1013 - 0001 0000 0001 0011
        #                   ^-DCS
        # D023I - 2013 - 0010 0000 0001 0100
        #                  ^--DCS inverted
        # D754I - 21EC - 0010 0001 1110 1100
        #    code in octal-------^^^^^^^^^^^
        #
        # Channels created via CHIRP always get an explicit 0x3000
        # "no tone" sentinel (see set_memory's set_raw() call below),
        # so this round-trips cleanly. Channels created directly on
        # the radio's own keypad don't necessarily get that same
        # explicit initialization - the tone bytes can be left as
        # whatever was previously in that flash address (erased NOR
        # reads as 0xFFFF, or stale bytes from a prior channel). Only
        # ~1000 of the 65536 possible raw values correspond to a code
        # this radio can ever legitimately have set (DTCS_CODES here,
        # or a standard CTCSS tone), so anything else is treated as
        # "no tone" rather than surfaced as a bogus DCS/CTCSS value.

        if toneval == 0x3000:
            return '', None, None
        elif toneval & 0x1000:
            # DTCS N
            code = int('%o' % (toneval & 0x1FF))
            if code not in DTCS_CODES:
                return '', None, None
            return 'DTCS', code, 'N'
        elif toneval & 0x2000:
            # DTCS R
            code = int('%o' % (toneval & 0x1FF))
            if code not in DTCS_CODES:
                return '', None, None
            return 'DTCS', code, 'R'
        else:
            freq = toneval / 10.0
            if freq not in chirp_common.TONES:
                return '', None, None
            return 'Tone', freq, None

    @staticmethod
    def _encode_tone(mode, val, pol):
        if not mode:
            return 0x3000
        elif mode == 'Tone':
            return int(val * 10)
        elif mode == 'DTCS':
            code = int('%i' % val, 8)
            if pol == 'N':
                code |= 0x1800
            if pol == 'R':
                code |= 0x2800
            return code
        else:
            raise errors.RadioError('Unsupported tone mode %r' % mode)

    def get_memory(self, number):
        mem = chirp_common.Memory()
        _mem = self._memobj.channels[number - 1]
        mem.number = number

        mem.freq = int(_mem.rxfreq) * 10

        # We'll consider any blank (i.e. 0 MHz frequency) to be empty
        if mem.freq == 0:
            mem.empty = True
            return mem

        if _mem.rxfreq.get_raw(asbytes=False) == "\xFF\xFF\xFF\xFF":
            mem.freq = 0
            mem.empty = True
            return mem

        # Freq and offset
        mem.freq = int(_mem.rxfreq) * 10
        # TX freq set
        offset = (int(_mem.txfreq) * 10) - mem.freq
        if offset != 0:
            if _split(self.get_features(), mem.freq, int(
                      _mem.txfreq) * 10):
                mem.duplex = "split"
                mem.offset = int(_mem.txfreq) * 10
            elif offset < 0:
                mem.offset = abs(offset)
                mem.duplex = "-"
            elif offset > 0:
                mem.offset = offset
                mem.duplex = "+"
        else:
            mem.offset = 0

        mem.name = str(_mem.name).rstrip(" ").replace("\xFF", " ")

        mem.mode = "NFM" if _mem.isnarrow else ["FM", "AM", "LSB", "USB"][_mem.modulation_type]

        chirp_common.split_tone_decode(mem,
                                       self._decode_tone(_mem.tx_tone),
                                       self._decode_tone(_mem.rx_tone))

        mem.power = self.POWER_LEVELS[_mem.lowpower]

        # Skip is hidden (see valid_skips above) - ScanAdd is vestigial,
        # never read by the scan task on this firmware, so there's
        # nothing meaningful to surface here.

        mem.extra = RadioSettingGroup("Extra", "extra")

        rs = RadioSettingValueList(LIST_BCL, LIST_BCL[_mem.bcl])
        rset = RadioSetting("bcl", "Busy Channel Lockout", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_MUTETYPE, LIST_MUTETYPE[_mem.mutetype])
        rset = RadioSetting("mutetype", "Mute Type", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueInteger(0, 16777215, _mem.mutecode)
        rset = RadioSetting("mutecode", "Mute Code (0-16777215)", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueInteger(0, 8, _mem.scramblecode)
        rset = RadioSetting("scramblecode", "Scrambler Code (0=Off, 1-8)", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_BANK, LIST_BANK[_mem.bank1])
        rset = RadioSetting("bank1", "Bank 1", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_BANK, LIST_BANK[_mem.bank2])
        rset = RadioSetting("bank2", "Bank 2", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_BANK, LIST_BANK[_mem.bank3])
        rset = RadioSetting("bank3", "Bank 3", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_BANK, LIST_BANK[_mem.bank4])
        rset = RadioSetting("bank4", "Bank 4", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_BANK, LIST_BANK[_mem.bank5])
        rset = RadioSetting("bank5", "Bank 5", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_BANK, LIST_BANK[_mem.bank6])
        rset = RadioSetting("bank6", "Bank 6", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_BANK, LIST_BANK[_mem.bank7])
        rset = RadioSetting("bank7", "Bank 7", rs)
        mem.extra.append(rset)

        rs = RadioSettingValueList(LIST_BANK, LIST_BANK[_mem.bank8])
        rset = RadioSetting("bank8", "Bank 8", rs)
        mem.extra.append(rset)

        return mem

    def set_memory(self, mem):
        LOG.debug("Setting %i(%s)" % (mem.number, mem.extd_number))
        _mem = self._memobj.channels[mem.number - 1]

        # if empty memory
        if mem.empty:
            _mem.set_raw("\xFF" * 22 + "\x20" * 10)
            return

        _mem.set_raw("\xFF" * 4 + "\x00\x30" + "\xFF" * 4 + "\x00\x30" +
                     "\x00" * 10 + "\x20" * 10)

        _mem.rxfreq = mem.freq / 10

        if mem.duplex == "split":
            _mem.txfreq = mem.offset / 10
        elif mem.duplex == "+":
            _mem.txfreq = (mem.freq + mem.offset) / 10
        elif mem.duplex == "-":
            _mem.txfreq = (mem.freq - mem.offset) / 10
        else:
            _mem.txfreq = mem.freq / 10

        _mem.name = mem.name.rstrip('\xFF').ljust(10, '\x20')

        # _mem.scan (ScanAdd) is never read by the scan task on this
        # firmware (see get_memory() above) - set unconditionally to
        # match the radio's own default for a newly-created channel,
        # rather than derive it from the now-hidden Skip field.
        _mem.scan = True
        _mem.isnarrow = mem.mode == "NFM"
        _mem.modulation_type = 0 if _mem.isnarrow else ["FM", "AM", "LSB", "USB"].index(mem.mode)


        # dtcs_pol = ["N", "N"]

        txtone, rxtone = chirp_common.split_tone_encode(mem)
        _mem.tx_tone = self._encode_tone(*txtone)
        _mem.rx_tone = self._encode_tone(*rxtone)

        _mem.lowpower = mem.power == self.POWER_LEVELS[1]

        for setting in mem.extra:
            setattr(_mem, setting.get_name(), setting.value)

    def get_settings(self):
        _dtmf = self._memobj.dtmf
        _dtmf2 = self._memobj.dtmf2
        _settings = self._memobj.settings
        _ext = self._memobj.extsettings
        evosafety = RadioSettingGroup("evosafety", "EVOLUTION X: Read Me First")
        basic = RadioSettingGroup("basic", "Basic Settings")
        dtmf = RadioSettingGroup("dtmf", "DTMF Settings")
        startup = RadioSettingGroup("startup", "Startup Settings")
        evoscan = RadioSettingGroup("evoscan", "EVOLUTION X: Scan / AM Fix")
        evohw = RadioSettingGroup("evohw", "EVOLUTION X: Hardware")
        evokeys = RadioSettingGroup("evokeys", "EVOLUTION X: Numpad Shortcuts")
        top = RadioSettings(evosafety, basic, dtmf, startup, evoscan, evohw,
                            evokeys)

        # Not backed by the memory image at all - this always starts
        # unchecked, every time this tab is opened, on purpose. See
        # _confirmed_r2_plus above for why: writing the extended-
        # settings block to a radio still on r1 firmware can corrupt
        # unrelated flash, and there's no reliable way to detect the
        # radio's firmware version over this protocol to check it for
        # you. Ticking this and uploading is how you confirm it
        # yourself; leaving it unchecked uploads everything else as
        # normal and just skips the extended-settings block.
        rs = RadioSettingValueBoolean(False)
        rset = RadioSetting(
            "confirmed_r2_plus",
            "I have flashed EVOLUTION X r2 or later on this radio "
            "(required before uploading the settings below the basic "
            "DTMF/Startup groups)", rs)
        rset.set_apply_callback(
            lambda setting, radio: setattr(
                radio, "_confirmed_r2_plus", bool(setting.value)),
            self)
        evosafety.append(rset)

        # Basic Settings

        # Menu 21 - Personal ID
        _codeobj = _settings.personalid
        _code = str(_codeobj).rstrip('\x20')
        rs = RadioSettingValueString(0, 16, _code, True)
        rset = RadioSetting("personalid", "Personal ID", rs)
        basic.append(rset)

        rs = RadioSettingValueList(LIST_WORKMODE,
                                   LIST_WORKMODE[_settings.workmode])
        rset = RadioSetting("workmode", "Work Mode", rs)
        basic.append(rset)

        # Menu 05 - Voice Prompt
        rs = RadioSettingValueBoolean(_settings.voiceprompt)
        rset = RadioSetting("voiceprompt", "Voice Prompt", rs)
        basic.append(rset)

        # Menu 06 - Key Beep
        rs = RadioSettingValueBoolean(_settings.keybeep)
        rset = RadioSetting("keybeep", "Key Beep", rs)
        basic.append(rset)

        # Menu 07 - Roger Beep
        rs = RadioSettingValueList(LIST_ROGER,
                                   LIST_ROGER[_settings.rogerbeep])
        rset = RadioSetting("rogerbeep", "Roger Beep", rs)
        basic.append(rset)

        # Menu 09 - TX Priority
        rs = RadioSettingValueList(LIST_TXPRI,
                                   LIST_TXPRI[_settings.txpriority])
        rset = RadioSetting("txpriority", "TX Priority", rs)
        basic.append(rset)

        # Menu 10 - Save Mode
        rs = RadioSettingValueBoolean(_settings.savemode)
        rset = RadioSetting("savemode", "Save Mode", rs)
        basic.append(rset)

        # Menu 11 - Freq Step
        val = min(_settings.frequencystep, 0x0D)
        rs = RadioSettingValueList(LIST_FREQSTEP, LIST_FREQSTEP[val])
        rset = RadioSetting("frequencystep", "Frequency Step", rs)
        basic.append(rset)

        # Menu 12 - SQ Level
        val = min(_settings.squelch, 0x09)
        rs = RadioSettingValueInteger(0, 9, val)
        rset = RadioSetting("squelch", "Squelch Level (0-9)", rs)
        basic.append(rset)

        # Menu 13 - LED Timer
        val = min(_settings.displaytimer, 0x2A)
        rs = RadioSettingValueList(LIST_TIMER, LIST_TIMER[val])
        rset = RadioSetting("displaytimer", "Display Timer", rs)
        basic.append(rset)

        # Menu 14 - Lcok Timer
        val = min(_settings.locktimer, 0x2A)
        rs = RadioSettingValueList(LIST_TIMER, LIST_TIMER[val])
        rset = RadioSetting("locktimer", "Lock Timer", rs)
        basic.append(rset)

        # Menu 15 - TOT
        val = min(_settings.timeouttimer, 0x2A)
        rs = RadioSettingValueList(LIST_TIMER, LIST_TIMER[val])
        rset = RadioSetting("timeouttimer", "Timeout Timer", rs)
        basic.append(rset)

        rs = RadioSettingValueBoolean(_settings.vox)
        rset = RadioSetting("vox", "VOX", rs)
        basic.append(rset)

        # Menu 16 - VOX Level
        val = min(_settings.voxlevel, 0x09)
        rs = RadioSettingValueInteger(0, 9, val)
        rset = RadioSetting("voxlevel", "VOX Level (0-9)", rs)
        basic.append(rset)

        # Menu 17 - VOX Delay
        val = min(_settings.voxdelay, 0x09)
        rs = RadioSettingValueInteger(0, 9, val)
        rset = RadioSetting("voxdelay", "VOX Delay (0-9)", rs)
        basic.append(rset)

        # Menu 18 - NOAA Monitor
        rs = RadioSettingValueBoolean(_settings.noaaalarm)
        rset = RadioSetting("noaaalarm", "NOAA Alarm", rs)
        basic.append(rset)

        # Menu 19 - FM Standby
        rs = RadioSettingValueBoolean(_settings.fmstandby)
        rset = RadioSetting("fmstandby", "FM Standby", rs)
        basic.append(rset)

        def myset_freq(setting, obj, atrb, mult):
            """ Callback to set frequency by applying multiplier"""
            value = int(float(str(setting.value)) * mult)
            setattr(obj, atrb, value)
            return

        def apply_scanrange_freq(setting, obj, atrb, mult, original_raw):
            """Like myset_freq, but for Scan Range Start/Finish specifically.

            The widget here is capped at 999.99999 MHz to match what the
            radio's own 8-digit keypad can actually enter - but the field
            itself (and firmware's own "full range" default) can genuinely
            hold up to 1300 MHz, which is exactly what an untouched radio
            has. Without this, simply opening Settings and uploading
            anything else would silently narrow every untouched radio's
            Scan Range Finish from 1300MHz down to 999.99999MHz. Writing
            back the true original raw value whenever the user hasn't
            actually edited this field avoids that.
            """
            if setting.changed():
                value = int(float(str(setting.value)) * mult)
            else:
                value = original_raw
            setattr(obj, atrb, value)
            return

        # FM Broadcast Settings
        val = _settings.fmfrequency
        val = val / 10.0
        if val < 64.0 or val > 108.0:
            val = 90.4
        rx = RadioSettingValueFloat(64.0, 108.0, val, 0.1, 1)
        rset = RadioSetting("fmfrequency", "Broadcast FM Freq (MHz)", rx)
        rset.set_apply_callback(myset_freq, _settings, "fmfrequency", 10)
        basic.append(rset)

        # Menu 20 - Tail Tone
        rs = RadioSettingValueBoolean(_settings.tailtone)
        rset = RadioSetting("tailtone", "Tail Tone", rs)
        basic.append(rset)

        # Menu 21 - Scan DIR
        rs = RadioSettingValueList(LIST_DIRECTION,
                                   LIST_DIRECTION[_settings.scandirection])
        rset = RadioSetting("scandirection", "Scan Direction", rs)
        basic.append(rset)

        # Menu 08 - Dual Display
        rs = RadioSettingValueBoolean(_settings.dualdisplay)
        rset = RadioSetting("dualdisplay", "Dual Display", rs)
        basic.append(rset)

        # Menu 23 - Repeater Mode
        val = min(_settings.talkaround, 0x02)
        rs = RadioSettingValueList(LIST_REPEATER, LIST_REPEATER[val])
        rset = RadioSetting("talkaround", "Talkaround", rs)
        basic.append(rset)

        # Menu 37 - K1 Short
        val = int(_settings.key1short)
        rs = RadioSettingValueList(_skey_options(val), current_index=val)
        rset = RadioSetting("key1short", "Key 1 Short", rs)
        basic.append(rset)

        # Menu 36 - K1 Long
        val = int(_settings.key1long)
        rs = RadioSettingValueList(_skey_options(val), current_index=val)
        rset = RadioSetting("key1long", "Key 1 Long", rs)
        basic.append(rset)

        # Menu 39 - K2 Short
        val = int(_settings.key2short)
        rs = RadioSettingValueList(_skey_options(val), current_index=val)
        rset = RadioSetting("key2short", "Key 2 Short", rs)
        basic.append(rset)

        # Menu 38 - K2 Long
        val = int(_settings.key2long)
        rs = RadioSettingValueList(_skey_options(val), current_index=val)
        rset = RadioSetting("key2long", "Key 2 Long", rs)
        basic.append(rset)

        rs = RadioSettingValueInteger(0, 20000, _settings.tonefrequency)
        rset = RadioSetting("tonefrequency", "Tone Frequency (0-2000)", rs)
        basic.append(rset)

        rs = RadioSettingValueBoolean(_settings.dualstandby)
        rset = RadioSetting("dualstandby", "Dual Standby", rs)
        basic.append(rset)

        rs = RadioSettingValueList(LIST_AB,
                                   LIST_AB[_settings.standbyarea])
        rset = RadioSetting("standbyarea", "Standby Area", rs)
        basic.append(rset)

        rs = RadioSettingValueInteger(1, 999, _settings.areaach + 1)
        rset = RadioSetting("areaach", "Area A CH (1-999)", rs)
        basic.append(rset)

        rs = RadioSettingValueInteger(1, 999, _settings.areabch + 1)
        rset = RadioSetting("areabch", "Area B CH (1-999)", rs)
        basic.append(rset)

        rs = RadioSettingValueInteger(1, 999, _settings.quickch1 + 1)
        rset = RadioSetting("quickch1", "Quick CH 1 (1-999)", rs)
        basic.append(rset)

        rs = RadioSettingValueInteger(1, 999, _settings.quickch2 + 1)
        rset = RadioSetting("quickch2", "Quick CH 2 (1-999)", rs)
        basic.append(rset)

        rs = RadioSettingValueInteger(1, 999, _settings.quickch3 + 1)
        rset = RadioSetting("quickch3", "Quick CH 3 (1-999)", rs)
        basic.append(rset)

        rs = RadioSettingValueInteger(1, 999, _settings.quickch4 + 1)
        rset = RadioSetting("quickch4", "Quick CH 4 (1-999)", rs)
        basic.append(rset)

        # Border Color used to be settable here, but is now hardcoded
        # in firmware (r2+) - the byte is still reserved in the memory
        # map below (unused, no longer read by firmware) so nothing
        # downstream shifts, but it's no longer exposed as a setting.

        # DTMF Settings

        rs = RadioSettingValueList(LIST_DTMFSTATE,
                                   LIST_DTMFSTATE[_settings.dtmfstate])
        rset = RadioSetting("dtmfstate", "Radio State (Kill/Stun)", rs)
        dtmf.append(rset)

        # Menu 40 - DTMF Delay
        val = min(_dtmf.senddelay, 0x14)
        rs = RadioSettingValueList(LIST_DELAY, LIST_DELAY[val])
        rset = RadioSetting("dtmf.senddelay", "Send Delay", rs)
        dtmf.append(rset)

        # Menu 41 - DTMF Interval
        val = min(_dtmf.sendinterval, 0x11)
        rs = RadioSettingValueList(LIST_INTERVAL, LIST_INTERVAL[val])
        rset = RadioSetting("dtmf.sendinterval", "Send Interval", rs)
        dtmf.append(rset)

        # Menu 42 - DTMF Mode
        rs = RadioSettingValueList(LIST_SENDM,
                                   LIST_SENDM[_dtmf.sendmode])
        rset = RadioSetting("dtmf.sendmode", "Send Mode", rs)
        dtmf.append(rset)

        # Menu 43 - DTMF Select
        rs = RadioSettingValueList(LIST_SENDS,
                                   LIST_SENDS[_dtmf.sendselect])
        rset = RadioSetting("dtmf.sendselect", "Send Select", rs)
        dtmf.append(rset)

        # Menu 44 - DTMF Display
        rs = RadioSettingValueBoolean(_dtmf.recvdisplay)
        rset = RadioSetting("dtmf.recvdisplay", "Receive Display", rs)
        dtmf.append(rset)

        val = min(_dtmf.encodegain, 0x7F)
        rs = RadioSettingValueInteger(0, 127, val)
        rset = RadioSetting("dtmf.encodegain", "Encode Gain (0-127)", rs)
        dtmf.append(rset)

        val = min(_dtmf.decodeth, 0x3F)
        rs = RadioSettingValueInteger(0, 63, val)
        rset = RadioSetting("dtmf.decodeth", "Decode TH (0-63)", rs)
        dtmf.append(rset)

        for i in range(0, 16):
            _codeobj = self._memobj.dtmfcode[i].code
            _code = str(_codeobj).rstrip('\xFF')
            rs = RadioSettingValueString(0, 14, _code, False)
            rs.set_charset(DTMF_CHARS)
            rset = RadioSetting("dtmfcode/%i.code" % i,
                                "Code %i" % (i + 1), rs)

            def apply_code(setting, obj, length):
                code = ""
                for char in str(setting.value):
                    if char in DTMF_CHARS:
                        code += char
                    else:
                        code += ""
                obj.code_len = len(str(code))
                obj.code = code.ljust(length, chr(255))
            rset.set_apply_callback(apply_code, self._memobj.dtmfcode[i], 14)
            dtmf.append(rset)

        _codeobj = _dtmf2.kill
        _code = str(_codeobj).rstrip('\xFF')
        rs = RadioSettingValueString(0, 14, _code, False)
        rs.set_charset(DTMF_CHARS)
        rset = RadioSetting("dtmf2.kill",
                            "Remotely Kill", rs)

        def apply_code(setting, obj, length):
            code = ""
            for char in str(setting.value):
                if char in DTMF_CHARS:
                    code += char
                else:
                    code += ""
            obj.kill_len = len(str(code))
            obj.kill = code.ljust(length, chr(255))
        rset.set_apply_callback(apply_code, _dtmf2, 14)
        dtmf.append(rset)

        _codeobj = _dtmf2.stun
        _code = str(_codeobj).rstrip('\xFF')
        rs = RadioSettingValueString(0, 14, _code, False)
        rs.set_charset(DTMF_CHARS)
        rset = RadioSetting("dtmf2.stun",
                            "Remotely Stun", rs)

        def apply_code(setting, obj, length):
            code = ""
            for char in str(setting.value):
                if char in DTMF_CHARS:
                    code += char
                else:
                    code += ""
            obj.stun_len = len(str(code))
            obj.stun = code.ljust(length, chr(255))
        rset.set_apply_callback(apply_code, _dtmf2, 14)
        dtmf.append(rset)

        _codeobj = _dtmf2.wakeup
        _code = str(_codeobj).rstrip('\xFF')
        rs = RadioSettingValueString(0, 14, _code, False)
        rs.set_charset(DTMF_CHARS)
        rset = RadioSetting("dtmf2.wakeup",
                            "Wake Up", rs)

        def apply_code(setting, obj, length):
            code = ""
            for char in str(setting.value):
                if char in DTMF_CHARS:
                    code += char
                else:
                    code += ""
            obj.wakeup_len = len(str(code))
            obj.wakeup = code.ljust(length, chr(255))
        rset.set_apply_callback(apply_code, _dtmf2, 14)
        dtmf.append(rset)

        # Startup Settings

        _codeobj = _settings.startuplabel
        _code = str(_codeobj).rstrip('\x20')
        rs = RadioSettingValueString(0, 32, _code, True)
        rset = RadioSetting("startuplabel", "Startup Label", rs)
        startup.append(rset)

        # Menu 04 - Prompt Text
        rs = RadioSettingValueBoolean(_settings.displaylabel)
        rset = RadioSetting("displaylabel", "Display Startup Label", rs)
        startup.append(rset)

        # Menu 02 - Voltage
        rs = RadioSettingValueBoolean(_settings.displayvoltage)
        rset = RadioSetting("displayvoltage", "Display Voltage", rs)
        startup.append(rset)

        # Menu 01 - Startup Logo
        rs = RadioSettingValueBoolean(_settings.displaylogo)
        rset = RadioSetting("displaylogo", "Display Startup Logo", rs)
        startup.append(rset)

        # Menu 03 - Ringtone
        rs = RadioSettingValueBoolean(_settings.startupringtone)
        rset = RadioSetting("startupringtone", "Startup Ringtone", rs)
        startup.append(rset)

        val = min(_settings.xposition, 0x9F)
        rs = RadioSettingValueInteger(0, 159, val)
        rset = RadioSetting("xposition", "X Position (0-159)", rs)
        startup.append(rset)

        val = min(_settings.yposition, 0x6E)
        rs = RadioSettingValueInteger(16, 110, val)
        rset = RadioSetting("yposition", "Y Position (16-110)", rs)
        startup.append(rset)

        # NOTE: the old "TX Allow Settings" group (range174_240,
        # range240_320, range320_400, range480_560, writing 0xFF/0x00 as
        # "RX Only"/"TX/RX") has been removed. Those 4 bytes are actually
        # gSettings.BandInfo[4..7] - a per-hardware-band identity/mapping
        # table (see BAND_136MHz..BAND_480MHz in radio/frequencies.h),
        # not a TX-permit toggle. Writing 0xFF or 0x00 into it wrote an
        # invalid or wrong enum value into real band-calibration data.
        # BandInfo isn't exposed here yet - its correct/intended values
        # per band need confirming before it's safe to exit as a setting.

        # EVOLUTION X extended settings (firmware r2+, flash 0x3D5000 -
        # see EXT_* constants and _read_ext_block/_write_ext_block above)

        rs = RadioSettingValueBoolean(_ext.amfixenabled)
        rset = RadioSetting("extsettings.amfixenabled", "AM Fix Enabled", rs)
        evoscan.append(rset)

        val = int(_ext.amfixhysteresis)
        rs = RadioSettingValueList(_dynamic_options(LIST_AMFIXHYST, val),
                                   current_index=val)
        rset = RadioSetting("extsettings.amfixhysteresis",
                            "AM Fix Hysteresis", rs)
        evoscan.append(rset)

        val = max(-20, min(20, int(_ext.amfixrssitrimdb)))
        rs = RadioSettingValueInteger(-20, 20, val)
        rset = RadioSetting("extsettings.amfixrssitrimdb",
                            "AM Fix Antenna RSSI Trim (dB)", rs)
        evoscan.append(rset)

        val = int(_ext.scanresume)
        # Firmware validates this on every boot now (settings.c) - a raw
        # 0 gets corrected to 1/Carrier before CHIRP ever talks to a live
        # radio, so this is always 1-3 in practice. Storage is 1-indexed
        # (1=Carrier/2=Time/3=No - see radio/settings.h); map that to a
        # plain 0-indexed 3-item list here rather than exposing 0 as a
        # selectable option at all. Falls back to displaying Carrier for
        # the (now defensive-only) case of an unrebooted radio still
        # showing raw 0, matching firmware's own correction.
        rs = RadioSettingValueList(LIST_SCANRESUME,
                                   current_index=max(val - 1, 0))
        rset = RadioSetting("extsettings.scanresume", "Scan Resume", rs)

        def apply_scanresume(setting, obj):
            obj.set_value(int(setting.value) + 1)
        rset.set_apply_callback(apply_scanresume, _ext.scanresume)
        evoscan.append(rset)

        rs = RadioSettingValueBoolean(_ext.scanall)
        rset = RadioSetting("extsettings.scanall", "Scan All", rs)
        evoscan.append(rset)

        rs = RadioSettingValueBoolean(_ext.scanblink)
        rset = RadioSetting("extsettings.scanblink", "Scan Blink", rs)
        evoscan.append(rset)

        val = int(_ext.currentbank)
        rs = RadioSettingValueList(LIST_BANK8, current_index=val)
        rset = RadioSetting("extsettings.currentbank",
                            "Current Bank (Toggle Bank target)", rs)
        evoscan.append(rset)

        # Scan Range Start/Finish are stored raw x10Hz (matches channel
        # frequency encoding elsewhere); firmware validates Start<Finish
        # and 10MHz<=range<=1.3GHz on load, resetting to full range
        # otherwise - mirror that same fallback here on read. Firmware's
        # own on-radio entry is an 8-digit MHz.decimal format (3 whole +
        # 5 fractional digits, i.e. 10Hz/0.00001MHz resolution) - use the
        # same precision here rather than whole-MHz only.
        start_val = int(_ext.scanrangestart)
        finish_val = int(_ext.scanrangefinish)
        if start_val >= finish_val or start_val < 1000000 \
                or finish_val > 130000000:
            start_val, finish_val = 1000000, 130000000

        rs = RadioSettingValueFloat(10.0, 999.99999,
                                    min(start_val, 99999999) / 100000.0,
                                    resolution=0.00001, precision=5)
        rset = RadioSetting("extsettings.scanrangestart",
                            "Scan Range Start (MHz)", rs)
        rset.set_apply_callback(apply_scanrange_freq, _ext, "scanrangestart",
                                100000, start_val)
        evoscan.append(rset)

        rs = RadioSettingValueFloat(10.0, 999.99999,
                                    min(finish_val, 99999999) / 100000.0,
                                    resolution=0.00001, precision=5)
        rset = RadioSetting("extsettings.scanrangefinish",
                            "Scan Range Finish (MHz)", rs)
        rset.set_apply_callback(apply_scanrange_freq, _ext, "scanrangefinish",
                                100000, finish_val)
        evoscan.append(rset)

        # Hardware

        rs = RadioSettingValueList(LIST_PCBVERSION,
                                   current_index=int(_ext.pcbversion))
        rset = RadioSetting("extsettings.pcbversion", "PCB Revision", rs)
        evohw.append(rset)

        val = int(_ext.vhfcutoff)
        rs = RadioSettingValueList(_dynamic_options(LIST_VHFCUTOFF, val),
                                   current_index=val)
        rset = RadioSetting("extsettings.vhfcutoff", "VHF Filter Cutoff", rs)
        evohw.append(rset)

        rs = RadioSettingValueBoolean(_ext.ledheartbeat)
        rset = RadioSetting("extsettings.ledheartbeat", "LED Heartbeat", rs)
        evohw.append(rset)

        rs = RadioSettingValueBoolean(_ext.darkmode)
        rset = RadioSetting("extsettings.darkmode", "Dark Mode", rs)
        evohw.append(rset)

        val = min(int(_ext.micgainlevel), 31)
        rs = RadioSettingValueInteger(0, 31, val)
        rset = RadioSetting("extsettings.micgainlevel", "Mic Gain (0-31)", rs)
        evohw.append(rset)

        rs = RadioSettingValueBoolean(_ext.txprohibit)
        rset = RadioSetting("extsettings.txprohibit",
                            "TX Prohibit (blocks all TX)", rs)
        evohw.append(rset)

        # Numpad long-press shortcuts (0-9, *, #, Menu, Exit)

        for i in range(14):
            val = int(_ext.keyshortcut[i])
            rs = RadioSettingValueList(_skey_options(val), current_index=val)
            rset = RadioSetting("extsettings.keyshortcut/%i" % i,
                                KEYSHORTCUT_LABELS[i], rs)
            rset.set_apply_callback(
                lambda setting, obj: obj.set_value(int(setting.value)),
                _ext.keyshortcut[i])
            evokeys.append(rset)

        return top

    def set_settings(self, settings):
        for element in settings:
            if not isinstance(element, RadioSetting):
                self.set_settings(element)
                continue
            else:
                try:
                    name = element.get_name()
                    if "." in name:
                        bits = name.split(".")
                        obj = self._memobj
                        for bit in bits[:-1]:
                            if "/" in bit:
                                bit, index = bit.split("/", 1)
                                index = int(index)
                                obj = getattr(obj, bit)[index]
                            else:
                                obj = getattr(obj, bit)
                        setting = bits[-1]
                    else:
                        obj = self._memobj.settings
                        setting = element.get_name()

                    if element.has_apply_callback():
                        LOG.debug("Using apply callback")
                        element.run_apply_callback()
                    elif setting in ["areaach",
                                     "areabch",
                                     "quickch1",
                                     "quickch2",
                                     "quickch3",
                                     "quickch4"
                                     ]:
                        setattr(obj, setting, int(element.value) - 1)
                    elif element.value.get_mutable():
                        LOG.debug("Setting %s = %s" % (setting, element.value))
                        setattr(obj, setting, element.value)
                except Exception as e:
                    LOG.debug(element.get_name(), e)
                    raise

    @classmethod
    def match_model(cls, filedata, filename):
        # This radio has always been post-metadata, so never do
        # old-school detection
        return False


@directory.register
class RuyageUV58PlusRadio(IradioUV5118plus):
    """Radtel RT-890 OEFWCOM"""
    VENDOR = "Radtel"
    MODEL = "RT-890 M7OCM"
