import ExAsist.observer as ob
import configparser


def test_host():
    observer = ob.getObserver('Test')
    config = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation())
    config.read('tests/config.ini', encoding='utf8')

    observer.setConfig(config)

    observer.start()
    assert 1 == 1
