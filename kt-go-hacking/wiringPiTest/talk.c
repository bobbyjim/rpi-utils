#include <wiringPi.h>
#include <stdio.h>

// delay timings:
// 30 = 100 pulses / 6 seconds = 16 bits/s
// 20 = 100 pulses / 4 seconds = 25 bits/s
// 10 = 1000 pulses / 20 seconds = 50 bits/s
// 5  = 1000 pulses / 10 seconds = 100 bits/s
// 2  = 1000 pulses / 5 seconds = 200 bits/s
// 1  = 10,000 pulses / 20 seconds = 500 bits/s

#define		XMIT_DELAY	100

char* message = "hello world!\n";
int   charpos = 0;
long  count   = 0;

int main(void)
{
   wiringPiSetup();
   pinMode(0, OUTPUT);
   pinMode(1, OUTPUT);
   for(;;)
   {
      digitalWrite(0, HIGH);  delay(XMIT_DELAY);
      digitalWrite(0, LOW );  delay(XMIT_DELAY);

      ++count;
      if (count % 1000 == 0)
         fprintf(stderr, "%ld\n", count);
   }
   return 0;
}
