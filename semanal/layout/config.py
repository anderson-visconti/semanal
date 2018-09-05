import os

class Config(object):

    def __init__(self):

        self.meses = {
            1: 'jan',
            2: 'fev',
            3: 'mar',
            4: 'abr',
            5: 'mai',
            6: 'jun',
            7: 'jul',
            8: 'ago',
            9: 'set',
            10: 'out',
            11: 'nov',
            12: 'dez'
        }

        self.subsistemas = {
            1: 'SE/CO',
            2: 'S',
            3: 'NE',
            4: 'N'
        }

        self.config_meteo = {
            'path_chuva_acum': r'http://img0.cptec.inpe.br/~rclima/historicos/mensal/brasil/{:}/brchuvat{:%m%y}.gif',
            'path_chuva_anom': r'http://img0.cptec.inpe.br/~rclima/historicos/mensal/brasil/{:}/abrchuvat{:%m%y}.gif',
            'texto': open(
                file=os.path.join(os.path.dirname(__file__), 'layout', 'data', 'meteo.txt'),
                mode='r',
                encoding='utf-8'
            ).readlines()
        }

        self.config_hidro = {
            'path_dados': r'',
            'texto': open(
                file=os.path.join(os.path.dirname(__file__), 'layout', 'data', 'hidro.txt'),
                mode='r',
                encoding='utf-8'
            ).readlines(),
            'dados': os.path.join(os.path.dirname(__file__), 'layout', 'data', 'hidrologia.xlsx'),
        }

        self.config_arm = {
            'path_dados': r'',
            'texto': open(
                file=os.path.join(os.path.dirname(__file__), 'layout', 'data', 'arm.txt'),
                mode='r',
                encoding='utf-8'
            ).readlines(),
            'dados': os.path.join(os.path.dirname(__file__), 'layout', 'data', 'armazenamento.xlsx'),
            'rdh': r'C:\Onedrive\Middle Office\Middle\Hidrologia\Relatorios\RDH'
        }

        self.config_preco = {
            'path_dispersao': os.path.join(os.path.dirname(__file__), 'layout', 'images', 'dispersao.png'),
            'path_histograma': os.path.join(os.path.dirname(__file__), 'layout', 'images', 'histograma.png'),
            'texto': open(
                file=os.path.join(os.path.dirname(__file__), 'layout', 'data', 'preco.txt'),
                mode='r',
                encoding='utf-8'
            ).readlines(),
            'dados': os.path.join(os.path.dirname(__file__), 'layout', 'data', 'preco.xlsx')

        }

        self.config_forward = {
            'path_forward': os.path.join(os.path.dirname(__file__), 'layout', 'images', 'candle.png'),
            'texto': open(
                file=os.path.join(os.path.dirname(__file__), 'layout', 'data', 'forward.txt'),
                mode='r',
                encoding='utf-8'
            ).readlines(),
            'dados': os.path.join(os.path.dirname(__file__), 'layout', 'data', 'forward.xlsx')

        }

        self.config_reg = {
            'path_reg': os.path.join(os.path.dirname(__file__), 'layout', 'data', 'regulatorio.xlsx'),
            'texto': open(
                file=os.path.join(os.path.dirname(__file__), 'layout', 'data', 'reg.txt'),
                mode='r',
                encoding='utf-8'
            ).readlines(),
            'classes': {
                -2: 'fas fa-angle-double-down fa-2x',
                -1: 'fas fa-angle-down fa-2x',
                0: 'fas fa-minus fa-2x',
                1: 'fas fa-angle-up fa-2x',
                2: 'fas fa-angle-double-up fa-2x',
            }

        }

