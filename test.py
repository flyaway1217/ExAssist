import observer as ob
import configparser

observer = ob.getObserver('Test')
config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
config.read('config.ini', encoding='utf8')

observer.setConfig(config)

observer.start()

for i in range(1000):
    observer.info['loss'][i] = i*10

while True:
    i = 1
