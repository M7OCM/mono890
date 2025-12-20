## Mono890 Series 4 custom firmware for Radtel RT-890 PCB2.0/PCB2.1

![Screenshot_20251125-102122](https://github.com/user-attachments/assets/db0a8dda-40b7-42dc-842d-0999b9ccf2be)

Radtel RT-890 custom firmware Series 4.

20 December 2025 - m7ocm-rt-890-pcb-all-msi-uk-users.zip - UK only MSI edition RT-890 PCB2.0 & PCB2.1

I have removed the NOAA channels/alerts and replaced them with the 3 HMCG Maritime Safety Information (MSI) Broadcast Channels (92, 93 and 94). [See here for more information](https://www.gov.uk/maritime-safety-weather-and-navigation)

To use this feature firstly designate a shortcut long press key (eg #5 which is default AM Fix). Select HMCG MSI WX from shortcuts menu. Long press to activate. It will scan these 3 channels until and a broadcast is received. To exit press PTT once.

No other changes, so if you don't care (lol) or use NOAA in the US/Canada, don't download it! I find it useful as I live a few clicks from the North Sea ⛵ Happy Days ⛵

30 Nov 2025 Binary file archive of my recent RT-890 custom firmware for PCB2.0 and PCB2.1. It's the firmware I currently use. Note previous VHF issues with older PCB2.1 firmware was resolved a long time ago (v3.2 on Radtels website). Thanks to Marcus Dudley and Kelvin.

Use at own risk, my personal project, back up SPI before proceeding, no warranty anything works, may destroy your radio etc etc My only advice here is don't expect miracles and expect severe overloading if using external antennas. I use regular whips, and telescopic antennae, I also use SMA inline attenuators, 10dB is a good choice to knock the edge off on AM. AM mode really needs register changes to get the best out of it I cannot advise on what may or may not work as your setup will differ greatly from mine - AM Fix is fine but only with a stumpy on 118-137 MHz. AM Fix on 225-399.975 MHz is much more effective in my opinion.

SATCOM results are good (breaks squelch with decent length telescopic), but use NFM, it makes a world of difference. Experiment with squelch open and edit registers while listening to changes (new feature by dev motorello), better... worse etc its all quite straightforward and resets on reboot so nothing ventured nothing gained is the attitude lol

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

Many thanks to them all!

73

M7OCM

[Supporting Open Edition Firmware](https://ko-fi.com/dualtachyon)🔚
