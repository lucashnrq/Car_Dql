# Importação das bibliotecas
import RPi.GPIO as GPIO
import time

# Pinos do motor
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

# Pinos do modulo RGB
LED_R = 22
LED_G = 27
LED_B = 24

# Definir os pinos dos módulos ultrassônicos
EchoPinC = 0
TrigPinC = 1
EchoPinR = 6
TrigPinR = 17
EchoPinL = 7
TrigPinL = 12

# Definir a porta GPIO para o modo de codificação BCM
GPIO.setmode(GPIO.BCM)

# Ignorar avisos de perigo
GPIO.setwarnings(False)


def RGB_init():
    global pwmRed
    global pwmGreen
    global pwmBlue
    # Iniciar os pinos RGB como saída
    GPIO.setup(LED_R, GPIO.OUT)
    GPIO.setup(LED_G, GPIO.OUT)
    GPIO.setup(LED_B, GPIO.OUT)
    # Definir a frequência em 200hz e os pinos como PWM (Pulse Width Modulation)
    pwmRed = GPIO.PWM(LED_R, 200)
    pwmGreen = GPIO.PWM(LED_G, 200)
    pwmBlue = GPIO.PWM(LED_B, 200)
    # Iniciar os pinos RGB
    pwmRed.start(0)
    pwmGreen.start(0)
    pwmBlue.start(0)


def white():
    pwmRed.ChangeDutyCycle(100)
    pwmGreen.ChangeDutyCycle(100)
    pwmBlue.ChangeDutyCycle(100)


def red():
    pwmRed.ChangeDutyCycle(100)
    pwmGreen.ChangeDutyCycle(0)
    pwmBlue.ChangeDutyCycle(0)


def green():
    pwmRed.ChangeDutyCycle(0)
    pwmGreen.ChangeDutyCycle(100)
    pwmBlue.ChangeDutyCycle(0)


def blue():
    pwmRed.ChangeDutyCycle(0)
    pwmGreen.ChangeDutyCycle(0)
    pwmBlue.ChangeDutyCycle(100)


# Iniciar os pinos do motor
def motor_init():
    global pwm_ENA
    global pwm_ENB
    global delaytime
    GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
    # Iniciar os pinos dos sensores ultrassônicos
    GPIO.setup(EchoPinC, GPIO.IN)
    GPIO.setup(TrigPinC, GPIO.OUT)
    GPIO.setup(EchoPinR, GPIO.IN)
    GPIO.setup(TrigPinR, GPIO.OUT)
    GPIO.setup(EchoPinL, GPIO.IN)
    GPIO.setup(TrigPinL, GPIO.OUT)
    # Definir a frequência em 2000hz e os pinos como PWM (Pulse Width Modulation)
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)


# Frente
def run(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    white()  # LED branco
    pwm_ENA.ChangeDutyCycle(25)
    pwm_ENB.ChangeDutyCycle(25)
    time.sleep(delaytime)


# Freio
def brake(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    red()  # LED vermelho
    pwm_ENA.ChangeDutyCycle(25)
    pwm_ENB.ChangeDutyCycle(25)
    time.sleep(delaytime)


# Direita
def right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    green()  # LED verde
    pwm_ENA.ChangeDutyCycle(25)
    pwm_ENB.ChangeDutyCycle(25)
    time.sleep(delaytime)


# Esquerda
def left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    blue()  # LED azul
    pwm_ENA.ChangeDutyCycle(25)
    pwm_ENB.ChangeDutyCycle(25)
    time.sleep(delaytime)


# Giro para a direita
def spin_right(delaytime):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    green()  # LED verde
    pwm_ENA.ChangeDutyCycle(25)
    pwm_ENB.ChangeDutyCycle(25)
    time.sleep(delaytime)


# Giro para a esquerda
def spin_left(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    blue()  # LED azul
    pwm_ENA.ChangeDutyCycle(25)
    pwm_ENB.ChangeDutyCycle(25)
    time.sleep(delaytime)


'''
# Ré
def back(delaytime):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    red()  # LED vermelho
    pwm_ENA.ChangeDutyCycle(25)
    pwm_ENB.ChangeDutyCycle(25)
    time.sleep(delaytime)
'''


# Função de distância do sensor ultrassônico
def ultra_c():
    GPIO.output(TrigPinC, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPinC, GPIO.LOW)
    while not GPIO.input(EchoPinC):
        pass
    t1 = time.time()
    while GPIO.input(EchoPinC):
        pass
    t2 = time.time()
    distance = ((t2 - t1) * 340 / 2) * 100
    print("A distância C é %d " % distance)
    time.sleep(0.2)
    return distance


def ultra_r():
    GPIO.output(TrigPinR, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPinR, GPIO.LOW)
    while not GPIO.input(EchoPinR):
        pass
    t1 = time.time()
    while GPIO.input(EchoPinR):
        pass
    t2 = time.time()
    distance = ((t2 - t1) * 340 / 2) * 100
    print("A distância R é %d " % distance)
    time.sleep(0.2)
    return distance


def ultra_l():
    GPIO.output(TrigPinL, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPinL, GPIO.LOW)
    while not GPIO.input(EchoPinL):
        pass
    t1 = time.time()
    while GPIO.input(EchoPinL):
        pass
    t2 = time.time()
    distance = ((t2 - t1) * 340 / 2) * 100
    print("A distância L é %d " % distance)
    time.sleep(0.2)
    return distance


# Parar o funcionamento
def stop():
    pwm_ENA.stop()
    pwm_ENB.stop()


# Limpar as configurações da placa
def clean():
    GPIO.cleanup()
