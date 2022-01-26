/PROG p46
/ATTR
OWNER       = MNEDITOR;
CREATE      = DATE 100-11-20  TIME 09:43:21;
MODIFIED    = DATE 100-12-05  TIME 05:26:29;
LINE_COUNT = 44;
PROTECT     = READ_WRITE;
TCD:  STACK_SIZE    = 0,
      TASK_PRIORITY = 50,
      TIME_SLICE    = 0,
      BUSY_LAMP_OFF = 0,
      ABORT_REQUEST = 0,
      PAUSE_REQUEST = 0;
DEFAULT_GROUP   = 1,1,*,*,*;
CONTROL_CODE    = 00000000 00000000;
/MN
1: L P[1] 240cm/min CNT100 COORD  ;
2: L P[2] 240cm/min CNT100 COORD  ;
: Arc Start[2];
3: L P[3] WELD_SPEED CNT100 COORD PTH  ;
4: L P[4] WELD_SPEED CNT100 COORD PTH  ;
5: L P[5] WELD_SPEED CNT100 COORD PTH  ;
6: L P[6] WELD_SPEED CNT100 COORD PTH  ;
7: L P[7] WELD_SPEED CNT100 COORD PTH  ;
8: L P[8] WELD_SPEED CNT100 COORD PTH  ;
9: L P[9] WELD_SPEED CNT100 COORD PTH  ;
: Arc End[2];
10: L P[10] 240cm/min CNT100 COORD  ;
: Arc Start[1];
11: L P[11] WELD_SPEED CNT100 COORD PTH  ;
12: L P[12] WELD_SPEED CNT100 COORD PTH  ;
13: L P[13] WELD_SPEED CNT100 COORD PTH  ;
14: L P[14] WELD_SPEED CNT100 COORD PTH  ;
15: L P[15] WELD_SPEED CNT100 COORD PTH  ;
16: L P[16] WELD_SPEED CNT100 COORD PTH  ;
17: L P[17] WELD_SPEED CNT100 COORD PTH  ;
18: L P[18] WELD_SPEED CNT100 COORD PTH  ;
19: L P[19] WELD_SPEED CNT100 COORD PTH  ;
20: L P[20] WELD_SPEED CNT100 COORD PTH  ;
21: L P[21] WELD_SPEED CNT100 COORD PTH  ;
: Arc End[1];
22: L P[22] 240cm/min CNT100 COORD  ;
: Arc Start[1];
23: L P[23] WELD_SPEED CNT100 COORD PTH  ;
24: L P[24] WELD_SPEED CNT100 COORD PTH  ;
25: L P[25] WELD_SPEED CNT100 COORD PTH  ;
26: L P[26] WELD_SPEED CNT100 COORD PTH  ;
27: L P[27] WELD_SPEED CNT100 COORD PTH  ;
28: L P[28] WELD_SPEED CNT100 COORD PTH  ;
29: L P[29] WELD_SPEED CNT100 COORD PTH  ;
30: L P[30] WELD_SPEED CNT100 COORD PTH  ;
31: L P[31] WELD_SPEED CNT100 COORD PTH  ;
32: L P[32] WELD_SPEED CNT100 COORD PTH  ;
33: L P[33] WELD_SPEED CNT100 COORD PTH  ;
34: L P[34] WELD_SPEED CNT100 COORD PTH  ;
35: L P[35] WELD_SPEED CNT100 COORD PTH  ;
36: L P[36] WELD_SPEED CNT100 COORD PTH  ;
37: L P[37] WELD_SPEED CNT100 COORD PTH  ;
38: L P[38] WELD_SPEED CNT100 COORD PTH  ;
39: L P[39] WELD_SPEED CNT100 COORD PTH  ;
40: L P[40] WELD_SPEED CNT100 COORD PTH  ;
41: L P[41] WELD_SPEED CNT100 COORD PTH  ;
42: L P[42] WELD_SPEED CNT100 COORD PTH  ;
43: L P[43] WELD_SPEED CNT100 COORD PTH  ;
44: L P[44] WELD_SPEED CNT100 COORD PTH  ;
: Arc End[1];
/POS
P[1] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 73.2 mm, Y = 116.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[2] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[3] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 124.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[4] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 124.0 mm, Y = 142.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[5] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 117.0 mm, Y = 142.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[6] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 114.0 mm, Y = 147.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[7] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 97.3 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[8] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[9] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[10] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 124.0 mm, Y = 170.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[11] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 125.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[12] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 130.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[13] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 124.0 mm, Y = 165.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[14] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 124.0 mm, Y = 161.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[15] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 135.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[16] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 140.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[17] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 124.0 mm, Y = 156.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[18] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 124.0 mm, Y = 151.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[19] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 144.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[20] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 172.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[21] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 124.0 mm, Y = 147.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[22] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 114.0 mm, Y = 147.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[23] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 102.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[24] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 106.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[25] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 116.0 mm, Y = 144.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[26] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 117.0 mm, Y = 142.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[27] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 119.0 mm, Y = 142.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[28] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 111.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[29] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 116.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[30] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 167.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[31] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 163.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[32] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 120.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[33] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 125.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[34] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 158.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[35] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 153.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[36] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 130.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[37] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 134.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[38] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 148.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[39] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 144.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[40] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 139.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[41] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 144.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[42] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 139.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[43] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
P[44] {
   GP1:
       UF : 6, UT : 5,     CONFIG: 'N U T, 0, 0, 0',
      X = 149.0 mm, Y = 134.0 mm, Z = 155.0 mm,
      W = 0.0 deg, P = 0.0 deg, R = 0.0 deg
   GP2:
       UF : 1, UT : 2,
      J1 = 0.0 deg, J2 = 0.0 deg 
};
/END
