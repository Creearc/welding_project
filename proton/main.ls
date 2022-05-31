/PROG main
/ATTR
OWNER       = MNEDITOR;
CREATE      = DATE 100-11-20  TIME 09:43:21;
MODIFIED    = DATE 100-12-05  TIME 05:26:29;
LINE_COUNT = 999;
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
:! main task ;
: R[32]=0;
: LBL[2];
: R[33]=1;
: ;
: IF R[32]=2, JMP LBL[3];
: IF R[32]=6, JMP LBL[9];
: JMP LBL[5];
: ;
: LBL[9];
: Arc End[1];
: R[32]=0;
: JMP LBL[5];
: LBL[3];
: Arc End[1];
: R[32]=3;
: ;
: LBL[5];
: ;
: WAIT R[33]=3;
: R[33]=2;
: ;
: IF R[32]=3, JMP LBL[4];
: IF R[32]=5, JMP LBL[10];
: JMP LBL[6];
: LBL[10];
: Arc Start[1];
: R[32]=7;
: JMP LBL[6];
: LBL[4];
: Arc Start[1];
: R[32]=2;
: JMP LBL[6];
: LBL[6];
: ;
: CALL SR[20];
: ;
: JMP LBL[R[33]];
: ;
: ;
: LBL[98];
: Arc End[1];
: LBL[99];
: R[33]=0;
/POS
/END



