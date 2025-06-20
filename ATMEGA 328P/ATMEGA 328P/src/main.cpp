#define F_CPU 8000000UL
#include <avr/io.h>
#include <util/delay.h>

int main(void) {
    DDRB = 0xFF;  
    DDRD = 0xFF;  
    DDRC &= ~((1 << PC0) | (1 << PC1)); // Botones en PC0 y PC1 como entrada
    PORTC |= (1 << PC0) | (1 << PC1);   // Pull-up activado

    unsigned char columna[8] = {1, 2, 4, 8, 16, 32, 64, 128};

    int AYR[] = {
        // Mensaje: ARE YOU READY?
        0x00, 0x7E, 0x7E, 0x90, 0x90, 0x7E, 0x7E, 0x00,
        0x00, 0x7E, 0x7E, 0x58, 0x5E, 0x56, 0x72, 0x00,
        0x00, 0x7E, 0x7E, 0x5A, 0x5A, 0x5A, 0x5A, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x7C, 0x7E, 0x02, 0x02, 0x7E, 0x7C, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x7E, 0x7E, 0x58, 0x5E, 0x56, 0x72, 0x00,
        0X00, 0X7E, 0X7E, 0X66, 0X66, 0X7E, 0X7E, 0X00,
        0x00, 0x70, 0x10, 0x1F, 0x10, 0x70, 0x00, 0x00,
        0x00, 0xE0, 0x8D, 0x88, 0x88, 0xF8, 0x00, 0x00,
    };

    int go[] = {0x7E, 0x4A, 0x6E, 0x00, 0X7E, 0X42, 0X7E, 0X00};

    uint8_t jugador_pos = 3;  // Jugador empieza en la columna 3 (centro)
    int juego = 0;

    // MOSTRAR "ARE YOU READY?" UNA SOLA VEZ
     while (!(PINC & (1 << PC0))) {
    for (int i = 0; i < 73; i++) {
        for (int k = 0; k < 50; k++) {
            for (int j = 0; j < 8; j++) {
                PORTD = columna[j];
                PORTB = ~AYR[i + j];
                _delay_us(40);
            }
        }
    }}

    // ESPERAR A QUE SUELTE EL BOTÓN (por si ya estaba presionado)
    

    // ESPERAR A QUE PRESIONE EL BOTÓN
    while ((PINC & (1 << PC0))) { }

    // MOSTRAR GO
    for (int r = 0; r < 200; r++) {
        for (int j = 0; j < 8; j++) {
            PORTD = columna[j];
            PORTB = ~go[j];
            _delay_us(100);
        }
    }

    // INICIAR EL JUEGO
    juego = 1;

    while (juego == 1) {
        // Movimiento izquierda
        if (!(PINC & (1 << PC2))) {
            if (jugador_pos > 0) jugador_pos--;
            _delay_ms(10);  // antirrebote
        }

        // Movimiento derecha
        if (!(PINC & (1 << PC1))) {
            if (jugador_pos < 7) jugador_pos++;
            _delay_ms(10);  // antirrebote
        }

        // Mostrar jugador en la fila 7 (última)
        for (int j = 0; j < 8; j++) {
    PORTB= ~(1<<0);  // Activar la columna: poner en bajo (GND) para la columna deseada
    
    if (j == jugador_pos) {
        PORTD = (1 << j);  // 
    } 

    _delay_us(200);  // Retardo para visualización
}


    }
}
