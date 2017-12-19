import ExAsist.observer as ob
import configparser


def test_info():
    observer = ob.getObserver('Test')
    config = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation())
    config.read('tests/config.ini', encoding='utf8')

    observer.setConfig(config)

    observer.start()

    for i in range(1000):
        observer.info['loss'][i] = i*10
    assert 1 == 1
