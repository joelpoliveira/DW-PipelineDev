import numpy as np


class Modeler:
    def __init__(self):
        self.models=None
        self.model=None

    def parseModel(self, model:str):
        if self.models==None:
            return None
        
        for m in self.models:
            if m in model:
                self.model = self.models[m]
                return self
        self.model = np.nan
        return self

    def get_model(self) -> str:
        return self.model
    
    def get_fuel_type(self) -> str:
        pass


class Acura(Modeler):
    """
    Class with information about multiple Acura Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "ilx":"ilx",
            "md-x":"mdx",
            "mdx":"mdx",
            "nsx":"nsx",
            "ns-x":"nsx",
            "rdx":"rdx",
            "rd-x":"rdx",
            "rl":"rl",
            "rlx":"rlx",
            "rl-x":"rlx",
            "rsx":"rsx",
            "rs-x":"rsx",
            "tlx":"tlx",
            "tl-x":"tlx",
            "tl":"tl",
            "tls":"tls",
            "tl-s":"tls",
            "sl-x":"slx",
            "slx":"slx",
            "ts-x":"tsx",
            "tsx":"tsx",
            "type-s":"type-s",
            "type s":"type-s",
            "zdx":"zdx",
            "zd-x":"zdx"
        }


class AlfaRomeo(Modeler):
    """
    Class with information about multiple Alfa-Romeo Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "164":"164",
            "2000":"2000",
            "giulia":"giulia",
            "graduate":"spider",
            "gtv":"gtv",
            "spider":"spider",
            "stelvio":"stelvio",
        }


class AstonMartin(Modeler):
    """
    Class with information about multiple Aston Martin Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "db11":"db11",
            "db9":"db9",
            "db7":"db7",
            "rapide":"rapide",
            "vantage":"vantage",
        }


class Audi(Modeler):
    """
    Class with information about multiple Audi Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            f"a{i}":f"a{i}" for i in range(1,8+1)
        } | {
            f"a {i}":f"a{i}" for i in range(1,8+1)
        } | {
            f"a-{i}":f"a{i}" for i in range(1,8+1)
        } | {
            f"s{i}":f"s{i}" for i in range(1,8+1)
        } | {
            f"s {i}":f"s{i}" for i in range(1,8+1)
        } | {
            f"s-{i}":f"s{i}" for i in range(1,8+1)
        } | {
            f"rs{i}":f"rs{i}" for i in range(2,7+1)
        } | {
            f"rs {i}":f"rs{i}" for i in range(2,7+1)
        } | {
            f"rs-{i}":f"rs{i}" for i in range(2,7+1)
        } | {
            f"q{i}":f"q{i}" for i in range(2,8+1)
        } | {
            f"q {i}":f"q{i}" for i in range(2,8+1)
        } | {
            f"q-{i}":f"q{i}" for i in range(2,8+1)
        } | {
            "tt":"tt",
            "tts":"tts",
            "80":"80",
            "100":"100",
            "60":"60",
            "5000":"5000",
            "cabriolet":"cabriolet",
            "r8":"r8"
        } 


class BMW(Modeler):
    """
    Class with information about multiple BMW Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "1-series":"1-series",
            "1 series":"1-series",
            "1series":"1-series",
            #"109":"109",
            #"128":"128",
            
        }
