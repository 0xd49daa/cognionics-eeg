from enum import IntEnum

class Channels(IntEnum):
	F7=0
	Fp1=1
	Fp2=2
	F8=3
	F3=4
	Fz=5
	F4=6
	C3=7
	Cz=8
	P8=9
	P7=10
	Pz=11
	P4=12
	T3=13
	P3=14
	O1=15
	O2=16
	C4=17
	T4=18
	A2=19
	IMPEDANCE=20
	BATTERY=21
	DEVICE_COUNT=22
	FRAME=23

COLUMNS = ['F7', 'Fp1', 'Fp2',	'F8', 'F3', 'Fz', 'F4', 'C3', 'Cz', 'P8', 'P7', 'Pz', 'P4', 'T3', 'P3', 'O1', 'O2', 'C4', 'T4', 'A2', 'IMPEDANCE', 'BATTERY', 'FRAME']