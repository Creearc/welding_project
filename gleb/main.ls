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
: R[32]=1;
: R[31]=0;
: R[30]=1;
: LBL[1];
: IF R[31]=0, JMP LBL[5];
: IF R[30]=0, JMP LBL[5];
: Arc End[1];
: R[30]=0;
: LBL[5];
: R[26]=1;
: WAIT R[25]=1;
: R[25]=0;
: IF R[31]=0, JMP LBL[4];
: IF R[30]=0, JMP LBL[4];
: Arc Start[1];
: R[30]=0;
: LBL[4];
: JMP LBL[R[27]];
: LBL[2];
: CALL SR[20];
: JMP LBL[1];
: LBL[3];
/POS
/END


! main task ;
: R[33]=1;

: LBL[2];

: JMP LBL[R[33]];
: LBL[1];

: WAIT R[33]=3;
: R[33]=0;
: CALL SR[20];
: JMP LBL[1];


: LBL[98];
: Arc End[1];
: LBL[99];





: LBL[1];
: IF R[31]=0, JMP LBL[5];
: IF R[30]=0, JMP LBL[5];
: Arc End[1];
: R[30]=0;
: LBL[5];
: R[26]=1;
: WAIT R[25]=1;
: R[25]=0;
: IF R[31]=0, JMP LBL[4];
: IF R[30]=0, JMP LBL[4];
: Arc Start[1];
: R[30]=0;
: LBL[4];
: JMP LBL[R[27]];
: LBL[2];
: CALL SR[20];
: JMP LBL[1];
: LBL[3];