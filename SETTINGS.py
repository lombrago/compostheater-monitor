#!/usr/bin/env python

# Ezeket a beallitasokat hasznalja a komposztkazan mero es szabalyozo program
# Keszitette: ebaltgy

# Altalanos beallitas
MIN_TEMP_OF_WATER = 40.0
MAX_TEMP_REDUCE = 2.0
MAX_LITER_OF_WATER = 300
MAX_RUN_TIME = 900 

# Fajlok elerese
HOME_DIR	= "/home/pi/compostHeater/"	# Program helye 
LOG_ROOT 	= "/var/log/compost/"		# Eltarolt adatok helye  

# Komposztkazan ki es bemenetei (feher a meleg)
TEMP_COMP_OUT 	= "28.19C05C060000"      # Komposztkazan kimeneti MELEG homero cime
TEMP_COMP_IN	= "28.68AA5B060000"      # Komposztkazan bemeneti HIDEG homero cime
CH_COMP_MAIN	= 8                      # Komposztkazan ki es bemeneti homerok csatornaja

# Komposztkazan hocsereloje 
TEMP_COMP_SPIRAL_1 	= "28.B5665C060000"  # Komposztkazan hocserelo 
CH_COMP_SPIRAL		= 7 

# Komposztkazan belso homeroi
TEMP_COMP_LINE_A	= ['28.FF1611650400','28.FF5F09610400','28.FFED0D650400']
TEMP_COMP_LINE_B	= ['28.FF0B0D650400','28.FF4512650400','28.FFD602630400']
TEMP_COMP_LINE_C	= ['28.FF2F11650400','28.FF1711650400','28.FF3802650400']
CH_COMP_LINE_A		= 0 
CH_COMP_LINE_B		= 1 
CH_COMP_LINE_C		= 2 

# Melegagyas homeroi
TEMP_FLOWER_LINE_A	= ['28.FFF103630400','28.FF5809610400','28.FF060D650400']	# Foliahaz melegagyas
TEMP_FLOWER_LINE_B	= ['28.FFE20F650400','28.FF0108610400','28.FF3603630400']	# Foliahaz hidegagyas
CH_FLOWER_LINE_A	= 3 
CH_FLOWER_LINE_B	= 4 

# Foliahaz homeroi
TEMP_INDOOR_LOW         = "28.FF370D650400"     # Belso homerseklet (1m)
TEMP_INDOOR_HIGH        = "28.FF1703630400"     # Belso homerseklet (2.5m)
TEMP_INDOOR_GROUND      = "28.FF4F08610400"     # Belso talaj (-0.2m)
CH_LINE_INDOOR          = 5 

# Egyeb homerok
TEMP_OUTDOOR		= "28.FF4002650400"	# Kulso homerseklet (1m)
TEMP_OUTDOOR_GROUND	= "28.FF5512650400"	# Kulso talaj (-0.2m)
CH_LINE_OUTDOOR		= 6 

# GPIO beallitasok
# +-----+-----+---------+------+---+--B Plus--+---+------+---------+-----+-----+
# | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
# |   2 |   8 |   SDA.1 | ALT0 | 1 |  3 || 4  |   |      | 5V      |     |     |
# |   3 |   9 |   SCL.1 | ALT0 | 1 |  5 || 6  |   |      | 0v      |     |     |
# |   4 |   7 | GPIO. 7 |   IN | 0 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
# |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
# |  17 |   0 | GPIO. 0 |  OUT | 0 | 11 || 12 | 0 | OUT  | GPIO. 1 | 1   | 18  |
# |  27 |   2 | GPIO. 2 |  OUT | 0 | 13 || 14 |   |      | 0v      |     |     |
# |  22 |   3 | GPIO. 3 |  OUT | 1 | 15 || 16 | 1 | OUT  | GPIO. 4 | 4   | 23  |
# |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
# |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
# |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
# |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 0 | IN   | CE0     | 10  | 8   |
# |     |     |      0v |      |   | 25 || 26 | 0 | IN   | CE1     | 11  | 7   |
# |   0 |  30 |   SDA.0 |   IN | 0 | 27 || 28 | 0 | IN   | SCL.0   | 31  | 1   |
# |   5 |  21 | GPIO.21 |   IN | 0 | 29 || 30 |   |      | 0v      |     |     |
# |   6 |  22 | GPIO.22 |   IN | 0 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
# |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
# |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 1 | OUT  | GPIO.27 | 27  | 16  |
# |  26 |  25 | GPIO.25 |   IN | 1 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
# |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
# +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
# | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
# +-----+-----+---------+------+---+--B Plus--+---+------+---------+-----+-----+

# Atfolyasmero (BCM szamot kell megadni)
BCM_COUNTER_1 = 21		# Komposztkazan atfolyasmeroje
GPIO_COUNTER_1 = 29             # Komposztkazan atfolyasmeroje  

# Keringeto szivattyu (wPi szamot kell megadni)
GPIO_PUMP_1 = 28                # Komposztkazan keringeto szivattyuja

# Multiplexer, avagy digitalis kapcsolo az erzekelok kivalasztasahoz (wPi szamot kell megadni) 
GPIO_MULTIPLEXER_0 = 0		# Ne valtoztasd meg! Multipexer A (1)
GPIO_MULTIPLEXER_1 = 1          # Ne valtoztasd meg! Multipexer B (2) 
GPIO_MULTIPLEXER_2 = 2          # Ne valtoztasd meg! Multipexer C (4) 
GPIO_MULTIPLEXER_3 = 3          # Ne valtoztasd meg! Multipexer D (8) 

