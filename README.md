## Mono890 Series 4 and Evolution custom firmware for Radtel RT-890 PCB2.0/PCB2.1

<img width="1702" height="2508" alt="1000182942" src="https://github.com/user-attachments/assets/fa95b192-c6ca-4eaa-8432-96581b4a1e8d" />

The mono/evo series is specifically designed to reduce RF interference caused by the colour screen refreshing. It is also highly visible under direct sunlight (when using the light theme).

Evolution V (5)

June 18 2026

TBA firmware to be released soon

Updates include low power mod based on the work of developer Omegatee, PMR446 fixed at low power regardless of setting, output measured between 0.3W-0.5W, other bands reasonably reduced when low power is selected (mileage varies on band, not perfect but an improvement).

A new look calibrated S-meter, 9 white pips S1-S9 and 4 red pips denote S9+10, S9+20, S9+30 and S9+40>

<img width="1729" height="2757" alt="1000211529" src="https://github.com/user-attachments/assets/aed10255-b5fe-43ef-b379-001d0bac6486" />

Spectrum has a colour option included and key Exit is used for cycling. Menu key is the exit out of spectrum and the current spectrum frequency is copied to VFO.

The scanner function has been modified to take into account CTCSS/DCS tone detection which failed miserably with fast scanning. This version scans as fast as before, but if a programmed channel has a Tone Sql tone on RX and TX the radio slows the scan down to the sweet spot for detection 220-250ms. Works like stock but with added versatility for users that just scan non tone freqs and require the fastest possible scan rate.

Just for the record there is no Evolution II-IIII, thoses versions were for testing new features and were not released. Version V is the culmination of these versions. Limited colours have been used but no significant SPI bus noise from the screen has been noted.

16 May 2026 Evolution I

Spectrum now has a blacklist function for nuisance frequencies, max 50 frequencies can be blacklisted during spectrum search.

<img width="2559" height="1770" alt="1000182971" src="https://github.com/user-attachments/assets/7a40b64d-0c93-4eff-9e0f-c15602003080" />

130.000 is a well known internally generated noise issue as seen above, photo below using the blacklist function to remove it.

<img width="2465" height="1804" alt="1000182972" src="https://github.com/user-attachments/assets/da27617f-9188-4ac2-9055-35cbe6402874" />

To blacklist a frequency press Key 5. To restore all blacklisted frequencies press Key 2.

Blacklisted frequencies persist (in spectrum for the radio session) unless restored or power is cycled.

Key 8 opens the BK4819 register during spectrum - useful to fine tune gain on the fly (active carrier and squelch open).

Key 5 has also been added to the register edit screen globally. That enables/disables AM Fix. This should be off in Spectrum as AM Fix is not suitable for that mode. The indicator AF ON shows when active, when off battery voltage will show.

Squelch line response has been shortened.

VHF airband

8.33kHz logic has been improved in VFO mode so the spacing counts up and down correctly. While VFO 8.33 works perfectly, the spectrum rounds frequencies to the nearest digit. It's not perfect but acceptable given the radios overall performance.

<img width="4877" height="3038" alt="1000182937" src="https://github.com/user-attachments/assets/62aab7d7-ddae-47b2-b383-0ce879a113d9" />

This version does not include NOAA frequencies, only UK MCA MSI channels.

Keyboard commands for new features:

Register Editor

Choose a shortcut key to launch Register Editor or use within spectrum. The screen shows the current register values. The register currently being edited will display in a larger font.

- [Up] Move editor to next register
- [Down] Move to previous register
- [1] Change RF Gain Control (AGC 3, FGC 3/2/1/0/7/6/5/4); If AM Fix is on, use AGC 3 (default). Turn AM Fix off if using FGC
- [2] Decrease value of current register's setting by 1
- [3] Increase value of current register's setting by 1
- [5] AM Fix on/off (should be set off in spectrum)
- [EXIT] Return to main/Change spectrum colour (Evolution V+)

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

[Tunas1337](https://github.com/tunas1337)

[Xawen](https://github.com/xawen)

Many thanks to them all, especially Dual Tachyon the legend that reverse engineered the OEM firmware👍

73

M7OCM

[Supporting Open Edition Firmware](https://ko-fi.com/dualtachyon)🔚
