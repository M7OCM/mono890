## Mono890 Evolution custom firmware for Radtel RT-890 PCB2.0/PCB2.1

WARNING DO NOT USE ON PCB2.1Q VERSION, the original manufacturer has started using a GC9106 LCD making all custom firmware currently available, not just my version, incompatible as the firmware is written for the ST7735S LCD.

I have a PCB2.1Q model I purchased from Radtel but the custom driver does not work and render correctly. Despite reverse engineering a decompiled firmware and sourcing the correct init sequence, positional data etc, there is currently no way to fully integrate the entire ST7735S UI without some serious changes which take time and effort.

Rest assured I have not given up entirely on creating a working Q version. No idea if/when a functioning firmware will be available though, as there is no specific 890 firmware information available barring Galaxy Core's specification PDF and a basic init command list. To me it looks very much like GC9106 code is wrapped up in existing st7735.c/h infrastructure,and it needs unraveling.

As always use custom firmware at own risk.

Radtel has kindly provided the OEM PCB2.1Q update flasher which is here to fix the display issue.

The mono/evo series is specifically designed to reduce RF interference caused by the colour screen refreshing. It is also highly visible under direct sunlight (when using the light theme).

## 13 August 26 Evolution X for the PCB2.0/PCB2.1 revisions of the RT-890

Important notes regarding Evolution X firmware.

Ensure you are using the correct PCB version. Menu item 81 is where the revisions reside. Select the correct one, the radio will reboot. If you are unsure try both in order, but check 144.0 Mhz and note the signal strength (eg -122). If the signal is something like -144, it's a sign you are using PCB2.1 on a PCB2.0 890.

Menu 22 check Prohibit TX is on for TX and off if using as a receive only rig.

Menu item 6/7 Antenna Trim. This needs to be reset on first flash. If the dB level is changed it is saved to memory. It's common that the first flash will insert a garbage figure like -20dB so please do reset using Menu item 7. If users switch to alternative firmware ensure the trim is zero before flashing to stock for example.

If this isn't done Dynamic AM Fix (DAF) and AM Hysteresis will not work correctly. For most users leaving the trim setting at 0 (zero dB) is fine. If using a high gain tuned antenna or an external antenna small adjustments will be required. I currently have been running a airband dipole in the loft and have the trim set to 1dB which helps the Dynamic AM Fix respond faster to extreme gain changes . Negative dB has the opposite effect, response time is longer - useful for more distant transmissions where the gain changes more slowly.

AM Hysteresis is a feature that allows users to experiment with 6 presets for faster or slower reaction to increased gain and gain decay. Default is Narrow for the fastest response on airband, experiment to find your sweet spot.

Of course there is only so much you can do with firmware when there is no dedicated (proper) AM hardware and very extreme fast gain changes will overload the radio. To take that into account there is a watchdog feature which monitors outrageous overloads (requiring correction, within the range: -98dB to -40dB) and resets the gain to a safe index after 3000ms. In practice this is effective as the gain of the formerly 'hot' signal will likely drop and DAF will kick in again. Sure the signal may flutter a bit #facepalm but it's safeguarding the radio from getting stuck at a high negative dB value (oh, it's gone deaf type scenario).

For airband monitoring both civil and military I personally recommend using this radio as a handheld device and not a base station! This type of telescopic antenna (see pic below), is perfect, sold as dual bander, it literally works better on airband for under $2 from AliExpress. I use these and results are excellent.

<img width="682" height="1014" alt="1000245182" src="https://github.com/user-attachments/assets/978ac5e9-affb-42b1-805c-13e5d5b4d97b" />

The WFM feature in the Spectrum is to be regarded as an experimental bonus lol To use, enter a FM broadcast frequency in VFO (eg 099.3000) it does not matter if it's in AM mode or bandwidth is N or W. It's disregarded as the BK4819 is bypassed on first spectrum initialisation - note: only if the range entered is 88-108 MHz where the BK1080 starts/ends. Note on first try it may not work, reboot, a power cycle fixes that. Most of my less abused 890s worked first time but the old ones didn't. Set Ch step to 100 kHz and hone in on the signals in glorious 160 resolution lol To continue using the spectrum it is advisable to power cycle and set the VFO outside the 88-108 MHz band to reset the reg.

<img width="2067" height="2042" alt="1000246628" src="https://github.com/user-attachments/assets/9783bfd3-32d0-4b54-9d65-d1a24f532283" />

Additional spectrum changes: AM Fix is now prohibited from spectrum, if it's selected in VFO/Ch mode previously it will turn off. 

Keys 6/9 no longer control squelch bar - these are now on Sidekey 1 (up) and Sidekey 2 (down). Continually holding will advance either operation. Key 6 is now for changing spectrum colour views, Menu and Exit keys are back to normal in this build.

Dual Watch only works in dual display, if single frequency display is selected it will automatically turn off. Single mode is more useful for the additional information provided by the S-meter and registers.

Scan freq range. Functional and easy on coding - set the range in Menu 23/34. On first flash the range defaults to 10-999 MHz. Any changes after this will be saved to memory. There is no blacklist function as the code is simple and robust. I recommend changing the scan mode from Carrier Op (CO) to Timed Op (TO) as any annoying stuck freqs will get passed in 2.5s. Because the code utilises the existing scan/search stock parameters, 'bands' will override the scan start range. In practice this means if searching Airband 118-137 MHz, enter 118.00000 in VFO to ensure the scanning doesn't start at the wrong place. Once in range the scan loops until stopped.

The menu has been reordered as follows:

GROUP 1: Radio

- 1 Squelch Level
- 2 Freq Step
- 3 Modulation
- 4 Bandwidth
- 5 AM Hysteresis
- 6 Antenna Trim
- 7 Reset Ant Trim
- 8 VHF Cutoff
- 9 Mic Gain
- 10 TX Power
- 11 TX Priority
- 12 Repeater Mode
- 13 Tail Tone
- 14 TX Tone

GROUP 2: Squelch Codes/Security
- 15 CTCSS/DCS
- 16 RX CTCSS/DCS
- 17 TX CTCSS/DCS
- 18 Busy Lock
- 19 Invert Speech
- 20 DCS Encrypt
- 21 Mute Code
- 22 Prohibit TX

GROUP 3: Scanning
- 23 Scan Start
- 24 Scan Finish
- 25 Scan Resume
- 26 Scan >Dir<
- 27 Bank-> Scan
- 28 Ch -> Bank 1
- 29 Ch -> Bank 2
- 30 Ch -> Bank 3
- 31 Ch -> Bank 4
- 32 Ch -> Bank 5
- 33 Ch -> Bank 6
- 34 Ch -> Bank 7
- 35 Ch -> Bank 8

GROUP 4: Channel Management
- 36 Channel Name
- 37 Save Channel
- 38 Delete Channel

GROUP 5: VOX
- 39 VOX Level
- 40 VOX Delay

GROUP 6: DTMF
- 41 DTMF Mode
- 42 DTMF Select
- 43 DTMF Delay
- 44 DTMF Interval
- 45 DTMF Display

GROUP 7: Key Assignments
- 46 Side Key 1 LP
- 47 Side Key 1 SP
- 48 Side Key 2 LP
- 49 Side Key 2 SP
- 50 Key 0 LP
- 51 Key 1 LP
- 52 Key 2 LP
- 53 Key 3 LP
- 54 Key 4 LP
- 55 Key 5 LP
- 56 Key 6 LP
- 57 Key 7 LP
- 58 Key 8 LP
- 59 Key 9 LP
- 60 Key * LP
- 61 Key # LP
- 62 Key Menu LP
- 63 Key Exit LP
- 64 Reset Keys

GROUP 8: Display/LED/UI
- 65 Dual Display
- 66 Dark Theme
- 67 Startup Logo
- 68 Startup Text
- 69 Cell Voltage
- 70 Backlight
- 71 Scan LED
- 72 LED Heartbeat
- 73 Startup Tone
- 74 Voice Prompt
- 75 Key Beep
- 76 FSK ID

GROUP 9: Radio Behaviour
- 77 FM Standby
- 78 Power Save
- 79 Lock Time
- 80 Time of Talk

GROUP 10: System
- 81 PCB Revision
- 82 Reboot
- 83 Firmware

These instructions are a guide and are a WIP so I'll add more and update in due course.

Coming soon Evolution X (10). Release TBC. Update: testing is now complete on PCB2.0/PCB2.1 and will be released this week (w/c 10 August 26).

This update focuses on fine tuning airband AM using hysteresis to adjust speed and gain hold times (5 presets), integrated within Dynamic AM Fix (DAF). Also a new Antenna Trim function works alongside DAF for RSSI dB trimming for specific purposes eg high gain outdoor antennae. A real experimenters option that.

Scan Range. A first for OEFW, Start/Finish ie 118-137 MHz, any mode, freq step etc default is 10-999MHz as its always been on OEFWCOM.

TX Prohibit on/off for RX only.

Fixed a long-standing startup logo issue - pixels rendering white when they should be black and vice versa. All image imports now show correctly.

VHF Cut for changing the cut off point of the VHF filter: 240 MHz (stock), 260 MHz and 300 MHz for SATCOM testing primarily.

Because timing in the AM enhancements required specific tuning the clock speed has returned to stock/OEFW 72 MHz which helped with calculations and flash space.

Firmware revisions PCB2.0 and PCB2.1 (but not Q) are now selectable within the menu so no need for two bins.

<img width="2307" height="1432" alt="1000242274" src="https://github.com/user-attachments/assets/49662a42-e31d-49f1-9b3e-3fab159206d5" />

The spectrum can now receive proper WFM broadcasts (88-108 MHz), this has no other benefit other than looking 😎 It does require a reboot to guarantee the BK4819 chip is switched to the FM chip BK1080. Likewise it is advised to boot the radio (power cycle) to use other non FM broadcast bands.

I can now confirm that PCB2.1Q will be a standalone firmware version. The original LCD driver st7735s has been removed and replaced with the new driver. Space is at a premium and combining 3 PCB revisions is not practical in one binary unfortunately.

Due to the new items I have decided to rework the menu, more info on that later.

**Evolution V (5)**

June 20 2026

Updates include low power mod based on the work of developer Omegatee, PMR446 fixed at low power regardless of setting, output measured between 0.3W-0.5W, other bands reasonably reduced when low power is selected (mileage varies on band, not perfect but an improvement).

AT32F421 MCU (ARM Cortex-M4) fully optimised to work at 120MHz (stock 72 MHz). My versions always used 120 MHz but it was never optimised before.

A new look calibrated S-meter, 9 white pips S1-S9 and 4 red pips denote S9+10, S9+20, S9+30 and S9+40>

<img width="1729" height="2757" alt="1000211529" src="https://github.com/user-attachments/assets/38eecd99-e320-432f-863a-6f616a7954bd" />

Spectrum has a colour option included and key [MENU] is used for cycling. [EXIT] key leave spectrum - in addition the current active spectrum frequency is copied to VFO. See new key layout below. Reset all keys Menu #66 Global backlight timer has been added to spectrum which is set in Menu #13 and is a useful battery saver if set to 5s. Squelch activated light on, any key light on. Turn off Backlight timer in main menu for backlight always on.

The scanner function has been modified to take into account CTCSS/DCS tone detection which failed miserably with fast scanning. This version scans as fast as before, but if a programmed channel has Tone Sql on RX and TX the radio slows the scan down to the sweet spot for detection (220-250ms). Works like stock but with added versatility for users that just scan non tone freqs and require the fastest possible scan rate.

Limited colours have returned but no significant SPI bus noise from the screen has been noted.

**Spectrum**

Enter by pressing side key 2 LP

- [Up] Increase frequency range
- [Down] Decrease frequency range
- [1] Change scan step (16, 32, 64 or 128)
- [2] Restore blacklisted frequencies
- [3] Change modulation FM, AM or SB (SSB)
- [4] Change step size (0.25kHz - 1MHz)
- [5] Blacklist nuisance frequency (50)
- [6] Increase squelch level
- [7] Hold/Search (in Hold, use up/down to adjust main frequency)
- [8] Reg edit
- [9] Decrease squelch level
- [0] Toggle VHF/UHF band filter (F = On, X = Off)
- [*] Change scan delay (0 - 12ms)
- [#] Toggle bandwidth (W = 25.0kHz, N = 12.5kHz)
- [MENU] Switch spectrum colour modes
- [EXIT] Jump to VFO mode with current frequency and bandwidth to allow TX (FM TX only)

May 2026

Spectrum now has a blacklist function for nuisance frequencies, max 50 frequencies can be blacklisted during spectrum search.

<img width="2559" height="1770" alt="1000182971" src="https://github.com/user-attachments/assets/7a40b64d-0c93-4eff-9e0f-c15602003080" />

130.000 is a well known internally generated noise issue as seen above, photo below using the blacklist function to remove it.

<img width="2465" height="1804" alt="1000182972" src="https://github.com/user-attachments/assets/da27617f-9188-4ac2-9055-35cbe6402874" />

To blacklist a frequency press Key 5. To restore all blacklisted frequencies press Key 2.

Blacklisted frequencies persist (in spectrum for the radio session) unless restored or power is cycled.

Key 8 opens the BK4819 register during spectrum - useful to fine tune gain on the fly (active carrier and squelch open).

Key 5 has also been added to the register edit screen globally. That enables/disables AM Fix. This should be off in Spectrum as AM Fix is not suitable for that mode. The indicator AF ON shows when active, when off battery voltage will show.

Squelch line response has been made faster.

VHF airband

8.33kHz logic has been improved in VFO mode so the spacing counts up and down correctly. While VFO 8.33 works perfectly, the spectrum rounds frequencies to the nearest digit. It's not perfect but acceptable given the radios overall performance.

<img width="4877" height="3038" alt="1000182937" src="https://github.com/user-attachments/assets/62aab7d7-ddae-47b2-b383-0ce879a113d9" />

This and subsequent versions do not include NOAA frequencies, only UK MCA MSI channels.

Keyboard commands for new features:

Register Editor

Choose a shortcut key to launch Register Editor or use within spectrum. The screen shows the current register values. The register currently being edited will display in a larger font.

- [Up] Move editor to next register
- [Down] Move to previous register
- [1] Change RF Gain Control (AGC 3, FGC 3/2/1/0/7/6/5/4); If AM Fix is on, use AGC 3 (default). Turn AM Fix off if using FGC
- [2] Decrease value of current register's setting by 1
- [3] Increase value of current register's setting by 1
- [5] AM Fix on/off (should be set off in spectrum)
- [EXIT] Return to spectrum

AGC = Auto Gain Control. FGC = Fixed Gain Control.

FGC is a manual option

LNAS Coarse attenuator (short)
LNA Fine tuning attenuator
PGA Programmable threshold amplifier
MIX Mixer gain
BW Bandwidth filter
WK Weak signal threshold

Use FGC mode to select exact dB by adjusting the parameters in reg edit

Order is LNAS, LNA, MIX, PGA

0000 ... -98dB

0010 ... -96dB

1000 ... -95dB

0100 ... -93dB

0001 ... -92dB

0110 ... -91dB

0011 ... -90dB

1001 ... -89dB

0120 ... -88dB

1030 ... -87dB

0002 ... -86dB

1120 ... -85dB

0031 ... -84dB

0300 ... -83dB

1130 ... -82dB

1031 ... -81dB

0230 ... -80dB

1201 ... -79dB

0320 ... -78dB

1400 ... -77dB

1131 ... -76dB

0023 ... -75dB

1301 ... -74dB

1600 ... -73dB

0710 ... -72dB

0620 ... -71dB

2131 ... -70dB

0312 ... -69dB

0006 ... -68dB

0521 ... -67dB

0016 ... -66dB

1232 ... -65dB

2113 ... -64dB

1730 ... -63dB

1303 ... -62dB

0125 ... -61dB

2024 ... -60dB

1631 ... -59dB

1205 ... -58dB

2502 ... -57dB

2621 ... -56dB

0523 ... -55dB

2026 ... -54dB

0306 ... -53dB

0604 ... -52dB

0316 ... -51dB

1235 ... -50dB

0515 ... -49dB

0335 ... -48dB

0624 ... -47dB

1524 ... -46dB

3013 ... -45dB

0616 ... -44dB

1525 ... -43dB

0427 ... -42dB

2227 ... -41dB

2524 ... -40dB

2335 ... -39dB

1635 ... -38dB

2516 ... -37dB

3331 ... -36dB

3232 ... -35dB

2526 ... -34dB

3016 ... -33dB

3007 ... -32dB

2536 ... -31dB

3332 ... -30dB

2636 ... -29dB

3205 ... -28dB

3503 ... -27dB

3304 ... -26dB

3117 ... -25dB

3423 ... -24dB

3404 ... -23dB

3207 ... -22dB

3713 ... -21dB

3623 ... -20dB

3533 ... -19dB

3334 ... -18dB

3614 ... -17dB

3605 ... -16dB

3714 ... -15dB

3237 ... -14dB

3534 ... -13dB

3417 ... -12dB

3706 ... -11dB

3517 ... -10dB

3725 ... -9dB

3626 ... -8dB

3536 ... -7dB

3726 ... -6dB

3636 ... -5dB

3537 ... -4dB

3727 ... -3dB

3637 ... -2dB

3737 ... 0dB

Spectrum

- Enter by pressing side key 2 LP (default), reset keys if not
- [Up] Increase frequency range
- [Down] Decrease frequency range
- [1] Change scan step (16, 32, 64 or 128)
- [2] Restore all previously blacklisted frequencies
- [3] Change modulation FM, AM or SB (SSB)
- [4] Change step size (10Hz- 1MHz)
- [5] Blacklist frequency, max 50 per session, restore with key [2], resets on power cycle
- [6] Increase squelch level (response 50ms)
- [7] Hold/Search (in hold, use up/down to adjust main frequency - useful to avoid RFI)
- [8] Enter Reg Edit, [EXIT] to return to spectrum
- [9] Decrease squelch level (response 50ms)
- [0] Toggle VHF/UHF band filter (F = On, X = Off)
- [*] Change scan delay (0 - 12ms)
- [#] Toggle bandwidth (25.0K = wide, 12.5K = narrow)
- [MENU] Jump to VFO mode with current frequency and bandwidth (to allow TX FM only)
- [EXIT] Return to main
- SP [#] switch between VFO-CH mode

Default Keys

- Side Key [1SP] Monitor
- Side Key [1LP] Freq Detect
- Side Key [2SP] Scan/Advance Scan Bank/- Scan Stop (LP)
- Side Key [2LP] Spectrum

SP = Short Press; LP = Long Press

The following keypad keys are all LP

- [1] Step Size
- [2] Modulation
- [3] Bandwidth
- [4] TX Power
- [5] AM Fix
- [6] Dual Watch
- [7] Repeater/Talkaround
- [8] DTMF
- [9] Add or remove a channel to current scan bank
- [0] FMB
- [*] Edit TX Freq
- [#] Lock
- [MENU] Squelch
- [EXIT] Single/Dual Display

End of latest update

20 December 2025 - m7ocm-rt-890-pcb-all-msi-uk-users.zip - UK only MSI edition RT-890 PCB2.0 & PCB2.1

I have removed the NOAA channels/alerts and replaced them with the three VHF MCA HM Coastguard Maritime Safety Information (MSI) broadcast channels: (Ch 62) 160.725, (Ch 63) 160.775 and (Ch 64) 160.825. [See here for more information](https://www.gov.uk/maritime-safety-weather-and-navigation)

To use this feature firstly designate a shortcut long press key (eg #5 which is default AM Fix). Select HMCG MSI WX from shortcuts menu. Long press to activate. It will scan these 3 channels until and a broadcast is received. To exit press PTT once.

No other changes, so if you don't care (lol) or use NOAA in the US/Canada, don't download it! I find it useful as I live a few clicks from the North Sea ⛵ Happy Days ⛵

30 Nov 2025 Binary file archive of my recent RT-890 custom firmware for PCB2.0 and PCB2.1. It's the firmware I currently use. Note previous VHF issues with older PCB2.1 firmware was resolved a long time ago (v3.2 on Radtels website). Thanks to Marcus Dudley and Kelvin.

<img width="8192" height="4433" alt="1000182947" src="https://github.com/user-attachments/assets/02c94d2c-9a91-4605-a927-609fdb3d6cea" />

Use at own risk, my personal project, back up SPI before proceeding, no warranty anything works, may destroy your radio etc etc My only advice here is don't expect miracles and expect severe overloading if using external antennas. I use regular whips, and telescopic antennae, I also use bandpass filters, digital attenuators and modest SMA inline attenuators, 10dB is a good choice to knock the edge off on AM. AM mode really needs register changes to get the best out of it - I cannot advise on what may or may not work as your setup will differ greatly from mine.

<img width="4454" height="8163" alt="1000182950" src="https://github.com/user-attachments/assets/b29da4ad-982d-4ad8-ac92-4455e857cf13" />

SATCOM results are good (breaks squelch with decent length telescopic). Experiment with squelch open and edit registers while listening to changes (new feature by dev motorello), better... worse etc its all quite straightforward and resets on reboot so nothing ventured nothing gained is the attitude lol

Other than that its a figure it out yourself approach, I'm afraid, it's what amateur radio is all about right? Strictly no requests, open source available for further tinkering (see credits for the users involved in this project).

When compiling the binary, ensure the correct PCB board is set in the Makefile 

- 0 = PCB2.0
- 1 = PCB2.1

Important note, the 10 character name tag font is UPPER CASE English alphanumeric only and special characters/punctuation: . : - = < > @ ? This is a limitation of the standard small font used. No lower case.

No colour versions (shock horror!) strictly mono for reduced interference from screen updates. Works better outside too. RSSI refresh rate reduced to 2000ms, plus a host of great additions from developer [motorello](https://github.com/motorello/RT-890-OEFW-more) 8.33kHz spacing, extended step sizes in the spectrum, reduced long press hold for faster interaction. Standard OEM squelch (sod it, back to basics lol), refined display items for less interference from screen refresh updates. SIGREP (Signal Report/S meter) introduced in single freq mode (OEFWCOM mod - see below), AM Fix indicator in single freq mode.

S meter
- S9 + 70 dB -23 dBm (maxed out)
- S9 + 60 dB 	-33 dBm
- S9 + 50 dB 	-43 dBm
- S9 + 40 dB 	-53 dBm
- S9 + 30 dB 	-63 dBm
- S9 + 20 dB 	-73 dBm
- S9 + 10 dB 	-83 dBm

... note S0-S9 will display as such however S9+ readings will display like this: '9.nn' actual dBm eg (S)9(+).75(dBm)

- S9 			-93 dBm
- S8 			-99 dBm
- S7 			-105 dBm
- S6 			-111 dBm
- S5 			-117 dBm
- S4 			-123 dBm
- S3 			-129 dBm
- S2 			-135 dBm
- S1 			-141 dBm
- S0 			-147 dBm

Please see 890 and 890 II repos for additional instructions, M7OCM Chirp driver, Dual Tachyon 890 flasher and SPI restore tools. A lot of the info applies to this firmware but there have been lots of changes (see above for some) since the last update (v3.2 on Radtels website) not least the mono display.

Credits

[DualTachyon](https://github.com/dualtachyon)

[OEFWCOM](https://github.com/OEFW-community/RT-890-custom-firmware)

[CR7BLE](https://github.com/jcalado)

LCiccio

Marcos

[motorello](https://github.com/motorello/RT-890-OEFW-more)

[Omegatee APRS HW Mod](https://github.com/omegatee/RT-890-APRS-GPS-Feat)

[Psy97x](https://github.com/Psy97x)

[Reppad](https://github.com/Reppad)

[Superogira](https://github.com/superogira)

[TAC Operator](https://youtube.com/@tac-operator?si=EO7oGX7O0n-RAlkQ)

[Tunas1337](https://github.com/tunas1337)

[Xawen](https://github.com/xawen)

Many thanks to them all, especially Dual Tachyon the legend that reverse engineered the OEM firmware👍

73

M7OCM

[Supporting Open Edition Firmware](https://ko-fi.com/dualtachyon)🔚
