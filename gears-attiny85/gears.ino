#define PIN_DIR PIN_B0
#define PIN_STEP PIN_B1
#define PIN_SLEEP PIN_B2

// Don't initialise these on reset
int Wave __attribute__ ((section (".noinit")));
unsigned int Freq __attribute__ ((section (".noinit")));

typedef void (*wavefun_t)();

// Direct Digital Synthesis **********************************************

volatile unsigned int Acc, Jump;

void SetupDDS () {
  // Enable 64 MHz PLL and use as source for Timer1
  PLLCSR = 1<<PCKE | 1<<PLLE;     

  // Set up Timer/Counter1 for PWM output
  TIMSK = 0;                               // Timer interrupts OFF
  TCCR1 = 1<<PWM1A | 2<<COM1A0 | 1<<CS10;  // PWM A, clear on match, 1:1 prescale
  pinMode(1, OUTPUT);                      // Enable PWM output pin

  // Set up Timer/Counter0 for 20kHz interrupt to output samples.
  TCCR0A = 3<<WGM00;                       // Fast PWM
  TCCR0B = 1<<WGM02 | 2<<CS00;             // 1/8 prescale
  TIMSK = 1<<OCIE0A;                       // Enable compare match, disable overflow
  OCR0A = 60;                              // Divide by 61
}

void Sawtooth () {
  Acc = Acc + Jump;
  OCR1A = Acc >> 8;
}

void Square () {
  Acc = Acc + Jump;
  int8_t temp = Acc>>8;
  OCR1A = temp>>7;
}

void Rectangle () {
  Acc = Acc + Jump;
  int8_t temp = Acc>>8;
  temp = temp & temp<<1;
  OCR1A = temp>>7;
}

void Triangle () {
  int8_t temp, mask;
  Acc = Acc + Jump;
  temp = Acc>>8;
  mask = temp>>7;
  temp = temp ^ mask;
  OCR1A = temp<<1;
}

void Chainsaw () {
  int8_t temp, mask, top;
  Acc = Acc + Jump;
  temp = Acc>>8;
  mask = temp>>7;
  top = temp & 0x80;
  temp = (temp ^ mask) | top;
  OCR1A = temp;
}

void Pulse () {
  Acc = Acc + Jump;
  int8_t temp = Acc>>8;
  temp = temp & temp<<1 & temp<<2 & temp<<3;
  OCR1A = temp>>7;
}

void Noise () {
  int8_t temp = Acc & 1;
  Acc = Acc >> 1;
  if (temp == 0) Acc = Acc ^ 0xB400;
  OCR1A = Acc;
}

const int nWaves = 7;
wavefun_t Waves[nWaves] = {Triangle, Sawtooth, Square, Rectangle, Pulse, Chainsaw, Noise};
wavefun_t Wavefun;

ISR(TIMER0_COMPA_vect) {
  Wavefun();
}

void setup() {
  pinMode(PIN_DIR, OUTPUT);
  pinMode(PIN_SLEEP, OUTPUT);
    
  digitalWrite(PIN_DIR, 1);
  digitalWrite(PIN_SLEEP, 1); 

  Wave = 2; Freq = 100;     // Start with 100Hz Square
  Wavefun = Waves[Wave];
  MCUSR = 0;
  SetupDDS();
  Jump = Freq*4;
}

uint8_t readADC()
{
    ADMUX =
            (1 << ADLAR) |     // left shift result
            (0 << REFS1) |     // Sets ref. voltage to VCC, bit 1
            (0 << REFS0) |     // Sets ref. voltage to VCC, bit 0
            (1 << MUX1)  |     // use ADC3 for input (PB3), MUX bits 11
            (1 << MUX0);

    ADCSRA =
            (1 << ADEN)  |     // Enable ADC
            (1 << ADPS2) |     // set prescaler to 64, bit 2
            (1 << ADPS1) |     // set prescaler to 64, bit 1
            (0 << ADPS0);      // set prescaler to 64, bit 0

    ADCSRA |= (1 << ADSC);         // start ADC measurement
    while (ADCSRA & (1 << ADSC) ); // wait till conversion complete

    return ADCH;
}

void loop() {
  uint8_t pot;
  
  while (1)  {
    pot = readADC();
    Freq = int(pot&0xFC) * 12 + 1; // maximum of around 750 hz at 1/4 microstep
    
    Jump = Freq * 4;
    } 
}
