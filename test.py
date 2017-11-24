import observer as ob
import configparser

observer = ob.getObserver('Test')
config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation())
config.read('config.ini', encoding='utf8')

observer.setConfig(config)

observer.start()
