import numpy as np

class CarModelParser:
    """
    Base class for the car models parser, so that the models of a certain brand are uniform for all datasets.
    This is accomplished by calling "get_model" after parsing the respective string describing the model.

    Each child class should contain a dictionary mapping substrings to string models, in the instance 'models'
    """
    def __init__(self):
        self.models:dict={}
        self.model:str=None

    def parse_model(self, model:str):
        if self.models==None:
            return None
        
        self.model = self._parse_sub_model(model, self.models)
        return self

    def _parse_sub_model(self, model:str, sub_models:dict) -> str:
        for m in sub_models:
            if m in model:
                if type(sub_models[m]) is dict:
                    parse_result = self._parse_sub_model(model, sub_models[m])
                    if np.isnan(parse_result):
                        continue
                    else:
                        return parse_result
                else:
                    return sub_models[m]
        return np.nan

    def get_model(self) -> str:
        return self.model
    
    def _get_sub_sets(self, subset:dict) -> set:
        models = set()
        for value in subset.values():
            if type(value) is str:
                models|={value}
            else:
                models|=self._get_sub_sets(value)
        return models
    
    def get_distinct_models(self) -> set:
        return self._get_sub_sets(self.models)

        
    def get_fuel_type(self) -> str:
        pass


def get_parse_from_model_str(model:str) -> CarModelParser:
    parsers = {
        "acura":Acura,
        "alfa-romeo":AlfaRomeo,
        "alpine":Alpine,
        "am-general":AMGeneral,
        "amc":AMC,
        "american-lafrance":AmericanLaFrance,
        "amphicar":Amphicar,
        "ariel":Ariel,
        "arnolt":Arnolt,
        "aston-martin":AstonMartin,
        "auburn":Auburn,
        "audi":Audi,
        "austin-healey":AustinHealey,
        "baw":Baw,
        "bentley":Bentley,
        "bertone":Bertone,
        "bmw":BMW,
        "bricklin":Bricklin,
        "bugatti":Bugatti,
        "buick":Buick,
        "cadillac":Cadillac,
        "checker":Checker,
        "chevrolet":Chevrolet,
        "chrysler":Chrysler,
        "citroen":Citroen,
        "coda":Coda,
        "corbin":Corbin,
        "daewoo":Daewoo,
        "daihatsu":Daihatsu,
        "daimler":Daimler,
        "datsun":Datsun,
        "de-tomaso":DeTomaso,
        "delorean":DeLorean,
        "desoto":Desoto,
        "diamond-t":DiamondT,
        "dkw":DKW,
        "dodge":Dodge,
        "dort":Dort,
        "dutton":Dutton,
        "edsel":Edsel,
        "excalibur":Excalibur,
        "exomotive":Exomotive,
        "factory-five":FactoryFive,
        "ferrari":Ferrari,
        "fiat":Fiat,
        "fiberfab":Fiberfab,
        "fisker":Fisker,
        "ford":Ford,
        "franklin":Franklin,
        "frazer":Frazer,
        "freightliner":Freightliner,
        "genesis":Genesis,
        "geo":Geo,
        "gmc":GMC,
        "graham-paige":GrahamPaige,
        "hans-glas":HansGlas,
        "harley-davidson":HarleyDavidson,
        "henney":Henney,
        "hillman":Hillman,
        "honda":Honda,
        "hudson":Hudson,
        "hummer":Hummer,
        "hup":Hup,
        "hyundai":Hyundai,
        "infiniti":Infiniti,
        "isuzu":Isuzu,
        "jaguar":Jaguar,
        "jeep":Jeep,
        "jensen":Jensen,
        "kaiser":Kaiser,
        "kandi":Kandi,
        "kia":Kia,
        "lada":Lada,
        "laforza":LaForza,
        "lamborghini":Lamborghini,
        "lancia":Lancia,
        "land-rover":LandRover,
        "lexus":Lexus,
        "lincoln":Lincoln,
        "lotus":Lotus,
        "maserati":Maserati,
        "maybach":Maybach,
        "mazda":Mazda,
        "mclaren":McLaren,
        "mercedes-benz":MercedesBenz,
        "mercury":Mercury,
        "messerschmitt":Messerschmitt,
        "mg":MG,
        "midget":Midget,
        "mini":Mini,
        "mitsubishi":Mitsubishi,
        "morgan":Morgan,
        "nash":Nash,
        "nissan":Nissan,
        "nsu":NSU,
        "oldsmobile":Oldsmobile,
        "opel":Opel,
        "packard":Packard,
        "peterbilt":Peterbilt,
        "pierce-arrow":PierceArrow,
        "polaris":Polaris,
        "pontiac":Pontiac,
        "porsche":Porsche,
        "puma":Puma,
        "qvale":Qvale,
        "ram":Ram,
        "renault":Renault,
        "reo":Reo,
        "riley":Riley,
        "rolls-royce":RollsRoyce,
        "saab":Saab,
        "saturn":Saturn,
        "scion":Scion,
        "shelby":Shelby,
        "siata":Siata,
        "smart":Smart,
        "sterling":Sterling,
        "studebaker":Studebaker,
        "stutz":Stutz,
        "subaru":Subaru,
        "suzuki":Suzuki,
        "tesla":Tesla,
        "toyota":Toyota,
        "triumph":Triumph,
        "tvr":Tvr,
        "volkswagen":Volkswagen,
        "volvo":Volvo,
        "yugo":Yugo,
        "zimmer":Zimmer,
    }

    try:
        current_parser = parsers[model]
        return current_parser()
    except:
        return CarModelParser()

class AC(CarModelParser):
    """
    Class with information about multiple AC Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            ""
        }

class Acura(CarModelParser):
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


class AlfaRomeo(CarModelParser):
    """
    Class with information about multiple Alfa-Romeo Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "164":"164",
            "4c":"4c",
            "berlina":"berlina",
            "alfetta":"alfetta",
            "116":"alfetta",
            "junior":"gt junior",
            "matta":"matta",
            "2000":"2000",
            "2600":"2600",
            "giulia":"giulia",
            "graduate":"spider",
            "duetto":"spider",
            "gtv":"gtv",
            "spider":"spider",
            "stelvio":"stelvio",
            "milano":"75",
            "75":"75",
            "giulietta":"giulietta",
            "giuliette":"giulietta",
            "montreal":"montreal",
        }


class Alpine(CarModelParser):
    """
    Class with information about multiple Alpine Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "a110":"a110",
            "tiger":"sunbeam tiger",
            "sunbeam":"sunbeam tiger",
            "a310":"a310",
            "a610":"a610",
        }


class AMGeneral(CarModelParser):
    """
    Class with information about multiple AM General Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "hummer":"hummer",
            "h1":"hummer",
            "h2":"hummer",
            "h3":"hummer",
            "h4":"hummer",
            "humvee":"humvee",
            "998":"humvee",
            "dj":"jeep-dj",
            "925":"m925",
            "809":"m809",
        }


class AMC(CarModelParser):
    """
    Class with information about multiple AMC Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "770":"rambler-classic",
            "660":"rambler-classic",
            "classic":"rambler-classic",
            "440":"rambler-american",
            "american":"rambler-american",
            "990":"990",
            "amx":"amx",
            "alliance":"alliance",
            "ambassador":"ambassador",
            "cj":"jeep-cj",
            "concord":"concord",
            "eagle":"eagle",
            "gremlin":"gremlin",
            "hornet":"hornet",
            "hurst":"hurst",
            "javelin":"javelin",
            "cheroke":"jeep-cherokee",
            "marlin":"rambler-marlin",
            "matador":"matador",
            "pacer":"pacer",
            "rebel":"rambler-rebel",
            "spirit":"spirit",
        }


class AmericanLaFrance(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "century":"century",
            "eagle":"eagle",
            "metropolitan":"metropolitan",
            "pioneer":"pioneer",
        }


class Amphicar(CarModelParser):
    """
    Class with information about multiple Amphicar Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "770":"770",
        }


class Ariel(CarModelParser):
    """
    Class with information about multiple Ariel Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "atom":"atom",
            "nomad":"nomad",
        }


class Arnolt(CarModelParser):
    """
    Class with information about multiple Arnolt Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "mg":"mg",
            "bristol":"bristol",
        }


class AstonMartin(CarModelParser):
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
            "lagonda":"lagonda",
            "vanquish":"vanquish",
        }


class Auburn(CarModelParser):
    """
    Class with information about multiple Auburn Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "810":"cord-810",
            "812":"cord-812",
            "speedster":"851",
            "851":"851",
            "898":"8-98",
            "8-98":"8-98",
            "8 98":"8-98",
            "phaeton":"851",
            "boattail":"851",
        }


class Audi(CarModelParser):
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
            f"rs{i}":f"rs{i}" for i in range(2,7+1)
        } | {
            f"rs {i}":f"rs{i}" for i in range(2,7+1)
        } | {
            f"rs-{i}":f"rs{i}" for i in range(2,7+1)
        } | {
            f"s{i}":f"s{i}" for i in range(1,8+1)
        } | {
            f"s {i}":f"s{i}" for i in range(1,8+1)
        } | {
            f"s-{i}":f"s{i}" for i in range(1,8+1)
        } | {
            f"q{i}":f"q{i}" for i in range(2,8+1)
        } | {
            f"q {i}":f"q{i}" for i in range(2,8+1)
        } | {
            f"q-{i}":f"q{i}" for i in range(2,8+1)
        } | {
            "tt":"tt",
            "tts":"tt",
            "80":"80",
            "90":"90",
            "100":"100",
            "200":"200",
            "60":"60",
            "4000":"4000",
            "5000":"5000",
            "cabriolet":"cabriolet",
            "r8":"r8",
        } 


class AustinHealey(CarModelParser):
    """
    Class with information about multiple Aston-Healey Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "100":"100",
            "125":"125",
            "3000":"3000",
            "mk":"3000",
            "90":{
                "a ":"a90",
                " a":"a90",
                "a90":"a90",
                "g ":"g90",
                " g":"g90",
                "g90":"g90",
            },
            "a35":"a35",
            "a105":"a105",
            "moke":"mini-moke",
            "jensen":"jensen-healey",
            "sprite":"sprite",
            "seven":"austin-mini",
            "mini":"austin-mini",
            "princess":"princess",            
            "marina":"marina",
            "leyland":"leyland",
            "gipsy":"austin-gipsy",
        }


class Baw(CarModelParser):
    """
    Class with information about multiple Baw Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "bj2023s1":"bj2023s1",
            "luba":"luba",
            "bj212":"bj212",
            "007":"yusheng",
            "yusheng":"yusheng",
        }


class Bentley(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "arnage":"arnage",
            "azure":"azure",
            "brooklands":"brooklands",
            "continental":"continental",
            "eight":"eight",
            "flying spur":"flying-spur",
            "mark":{
                "6":"mark-vi",
                "vi":"mark-vi",
                "5":"mark-v",
                "v":"mark-v",
            },
            "mk":{
                "6":"mark-vi",
                "vi":"mark-vi",
                "5":"mark-v",
                "v":"mark-v",
            },
            "mulsanne":"mulsanne",
            "s1":"s1",
            "s-1":"s1",
            "s 1":"s1",
            "s3":"s3",
            "s-3":"s3",
            "s 3":"s3",
            "siii":"s3",
            "s-iii":"s3",
            "s iii":"s3",
            "s2":"s2",
            "s-2":"s2",
            "s 2":"s2",
            "sii":"s2",
            "s-ii":"s2",
            "s ii":"s2",
            " r":"r-type",
            "r ":"r-type",
            "-r":"r-type",
            "r-":"r-type",
        }


class Bertone(CarModelParser):
    """
    Class with information about multiple Bertone Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "1/9":"x1/9"
        }


class BMW(CarModelParser):
    """
    Class with information about multiple BMW Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "2002":"2002",
            "1600":"1600",
            "2000":"2000",
            "2800":"2800",
            "3335":"335",
            "135":"m135",
            "235":"m235",
            "240":"m240",
            "340":"m340",
            "440":"m440",
            "550":"m550",
            "760":"m760",
            "850":"m850",
            "128":"128",
            "228":"228",
            "230":"230",
            "238":"238",
            "281":"281",
            "318":"318",
            "320":"320",
            "323":"323",
            "325":"325",
            "328":"328",
            "330":"330",
            "335":"335",
            "428":"428",
            "430":"430",
            "435":"435",
            "525":"525",
            "528":"528",
            "530":"530",
            "535":"535",
            "540":"540",
            "545":"545",
            "633":"633",
            "635":"635",
            "640":"640",
            "645":"645",
            "650":"650",
            "735":"735",
            "740":"740",
            "745":"745",
            "750":"750",
            "840":"840",
            "850":"850",
            "m1":"m1",
            "1m":"m1",
            "m-1":"m1",
            "1-m":"m1",
            "m2":"m2",
            "2m":"m2",
            "m-2":"m2",
            "2-m":"m2",
            "m3":"m3",
            "3m":"m3",
            "m-3":"m3",
            "3-m":"m3",
            "e36":"m3",
            "e 36":"m3",
            "e-36":"m3",
            "m4":"m4",
            "4m":"m4",
            "m-4":"m4",
            "4-m":"m4",
            "m5":"m5",
            "5m":"m5",
            "m-5":"m5",
            "5-m":"m5",
            "m6":"m6",
            "6m":"m6",
            "m-6":"m6",
            "6-m":"m6",
            "b6":"b6",
            "b-6":"b6",
            "b7":"b7",
            "b-7":"b7",
            "i3":"i3",
            "i-3":"i-3",
            "i8":"i8",
            "i-8":"i8",
            "x 1":"x1",
            "x-1":"x1",
            "x1":"x1",
            "1x":"x1",
            "1-x":"x1",
            "x 2":"x2",
            "x-2":"x2",
            "x2":"x2",
            "2x":"x2",
            "2-x":"x2",
            "x 3":"x3",
            "x-3":"x3",
            "x3":"x3",
            "3x":"x3",
            "3-x":"x3",
            "g01":"x3",
            "g1":"x3",
            "x 5":"x5",
            "5-x":"x5",
            "5x":"x5",
            "x-5":"x5",
            "g05":"x5",
            "g5":"x5",
            "6-x":"x6",
            "6x":"x6",
            "x-6":"x6",
            "g06":"x6",
            "g6":"x6",
            "3z":"z3",
            "z3":"z3",
            "3-z":"z3",
            "z-3":"z3",
            "z 3":"z3",
            "4z":"z4",
            "z4":"z4",
            "4-z":"z4",
            "z-4":"z4",
            "z 4":"z4",
        }


class Bricklin(CarModelParser):
    """
    Class with information about multiple Bricklin Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "sv1":"sv1",
            "sv-1":"sv1",
            "sv 1":"sv1",
            "sv2":"sv2",
            "sv-2":"sv2",
            "sv 2":"sv2",
         }
        

class Bugatti(CarModelParser):
    """
    Class with information about multiple Bugatti Models that will be considered in the process
    of building a data warehouse to support car sales.
    """
    def __init__(self):
        super().__init__()
        self.models = {
            "veyron":"veyron",
            "35":"type 35",
            "37":"type 37",
            "41":"type 41",
            "44":"type 44",
            "51":"type 51",
            "55":"type 55",
            "57":"type 57",
            "68":"type 68",
        }
            

class Buick(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "allure":"lacrosse",
            "apollo":"apollo",
            "caballero":"caballero",
            "la crosse":"lacrosse",
            "lacrosse":"lacrosse",
            "cascada":"cascada",
            "cutlass":"cutlass",
            "centurion":"centurion",
            "century":"century",
            "lucerne":"lucerne",
            "lucern":"lucerne",
            "electra":"electra",
            "emcore":"encore",
            "encore":"encore",
            "enclave":"enclave",
            "envision":"envision",
            "estate":"estate",
            "grand national":"grand national",
            "gs":"grand sport",
            "grand sport":"grand sport",
            "invicta":"invicta",
            "invita":"invicta",
            "lasabre":"lesabre",
            "le sabre":"lesabre",
            "lesabre":"lesabre",
            "park ave":"park avenue",
            "park avenue":"park avenue",
            "rainier":"rainier",
            "ranier":"rainier",
            "reatta":"reatta",
            "regal":"regal",
            "rendezvous":"rendezvous",
            "rendevous":"rendezvous",
            "renzendeous":"rendezvous",
            "riviera":"riviera",
            "rivera":"riviera",
            "riveria":"riviera",
            "roadmaster":"roadmaster",
            "sedanette":"sedanette",
            "skyhawk":"skyhawk",
            "skylark":"skylark",
            "special":"special",
            "super":"super",
            "terraza":"terraza",
            "terazza":"terraza",
            "verano":"verano",
            "verrano":"verano",
            "wildcat":"wildcat",
            "electra":"electra",
            "derham":"derham",
        }


class Cadillac(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "alanta":"allante",
            "allante":"allante",
            "allente":"allante",
            "ats":"ats",
            "braughm":"brougham",
            "braugham":"brougham",
            "brougham":"brougham",
            "catera":"catera",
            "cimarron":"cimarron",
            "deville":"deville",
            "de ville":"deville",
            "devile":"deville",
            "ct4":"ct4",
            "ct6":"ct6",
            "cts":"cts",
            "dts":"dts",
            "el dorado":"eldorado",
            "eldorado":"eldorado",
            "eldorodo":"eldorado",
            "elr":"elr",
            "escalade":"escalade",
            "esclade":"escalade",
            "fleetwood":"fleetwood",
            "hearse":"hearse",
            "xts":"xts",
            "saville":"seville",
            "sevile":"seville",
            "seville":"seville",
            "savile":"seville",
            "sls":"sls",
            "srx":"srx",
            "stx":"xts",
            "sts":"sts",
            "xlr":"xlr",
            "xt4":"xt4",
            "xt-4":"xt4",
            "xt5":"xt5",
            "xt-5":"xt5",
            "xt6":"xt6",
            "xt-6":"xt6",
        }


class Checker(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "a11":"marathon",
            "a12":"marathon",
            "marathon":"marathon",
            "aerobus":"aerobus",
        }


class Chevrolet(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "express":"express",
            "cargo":"express",
            "expree":"express",
            "g3500":"express",
            "g4500":"express",
            "avalanche":"avalanche",
            "avalache":"avalanche",
            "avalanch":"avalanche",
            "conversation":"conversion",
            "conversion":"conversion",
            "suburban":"suburban",
            "tahoe":"tahoe",
            "blazer":"blazer",
            "balzer":"blazer",
            "blazser":"blazer",
            "camar":"camaro",
            "camaro":"camaro",
            "camro":"camaro",
            "comaro":"camaro",
            "capitiva":"captiva",
            "capiva":"captiva",
            "captiva":"captiva",
            "capitol":"capitol",
            "caprice":"caprice",
            "cavalier":"cavalier",
            "celebrity":"celebrity",
            "chevelle":"chevelle",
            "chevette":"chevette",
            "cheyenne":"cheyenne",
            "chyenne":"cheyenne",
            "citation":"citation",
            "classic":"classic",
            "classuc":"classic",
            "cobalt":"cobalt",
            "coblat":"cobalt",
            "colorado":"colorado",
            "corvair":"corvair",
            "corvan":"greenbier",
            "cruise":"cruze",
            "cruse":"cruze",
            "crusie":"cruze",
            "cruz":"cruze",
            "cruze":"cruze",
            "deluxe":"deluxe",
            "el camino":"el camino",
            "elcamino":"el camino",
            "eqinox":"equinox",
            "equinox":"equinox",
            "equniox":"equinox",
            "fleetline":"fleetline",
            "fleetmaster":"fleetmaster",
            "master":"master",
            "geo":"geo",
            "metro":"geo",
            "gmt":"gmt400",
            "grumman":"grumman",
            "ii":"chevy ii",
            "nova":"chevy ii",
            "impala":"impala",
            "imapa":"impala",
            "imapla":"impala",
            "impalla":"impala",
            "lumima":"lumina",
            "lumina":"lumina",
            "luv":"luv",
            "mailbu":"malibu",
            "maibu":"malibu",
            "malibu":"malibu",
            "monte":"monte carlo",
            "carlo":"monte carlo",
            "monza":"monza",
            "nomad":"nomad",
            "powerglide":"powerglide",
            "prizm":"prizm",
            "raverse":"traverse",
            "travers":"traverse",
            "traversa":"traverse",
            "traverse":"traverse",
            "treverse":"traverse",
            "deluxe":"deluxe",
            "styleline":"deluxe",
            "spark":"spark",
            "stylemaster":"stylemaster",
            "suburban":"suburban",
            "suburan":"suburban",
            "susburban":"suburban",
            "szuburban":"suburban",
            "tracker":"tracker",
            "trax":"trax",
            "uplander":"uplander",
            "vega":"vega",
            "venture":"venture",
            "volt":"volt",
            "kodiack":{
                "4500":"c4500",
                "5500":"c5500",
                "6500":"c6500",
                "7500":"c7500",
                "8500":"c8500",
            },
            "kodiak":{
                "4500":"c4500",
                "5500":"c5500",
                "6500":"c6500",
                "7500":"c7500",
                "8500":"c8500",
            },
            "silverado":{
                "1500":"c1500",
                "2500":"c2500",
                "3500":"c3500",
                "4500":"4500",
                "10":"c10",
                "silverado":"c1500",
            },
            "sil":"c1500",
            "siverado":"c1500",
            "silsverado":{
                "1500":"c1500",
                "2500":"c2500",
                "3500":"c3500",
                "4500":"4500",
                "10":"c10",
                "silsverado":"c1500",
            },
            "silverao":{
                "1500":"c1500",
                "2500":"c2500",
                "3500":"c3500",
                "4500":"4500",
                "10":"c10",
                "silverao":"c1500",
            },
            "sliverado":{
                "1500":"c1500",
                "2500":"c2500",
                "3500":"c3500",
                "4500":"4500",
                "10":"c10",
                "sliverado":"c1500",
            },     
            "sivlerado":{
                "1500":"c1500",
                "2500":"c2500",
                "3500":"c3500",
                "4500":"4500",
                "10":"c10",
                "sivlerado":"c1500",
            },        
            "corvette":"corvette",
            "covette":"corvette",
            "corvete":"corvette",
            "covete":"corvette",
            "cosworth":"cosworth vega",
            "g10":"g10",
            "g 10":"g10",
            "g-10":"g10",
            "g 20":"g20",
            "g-20":"g20",
            "g20":"g20",
            "g 30":"g30",
            "g-30":"g30",
            "g30":"g30",
            "apache":"apache",
            "asto":"astro",
            "astro":"astro",
            "aveo":"aveo",
            "sonic":"aveo",
            "bel-air":"bel air",
            "bel air":"bel air",
            "belair":"bel air",
            "beretta":"beretta",
            "biscayne":"biscayne",
            "bolt":"bolt",
            "bonanza":"bonanza",
            "brookwood":"brookwood",
            "r3500":"r3500",
            "r 3500":"r3500",
            "r-3500":"r3500",
            "w3500":"w3500",
            "w 3500":"w3500",
            "w-3500":"w3500",
            "w4500":"w4500",
            "w 4500":"w4500",
            "w-4500":"w4500",
            "w5500":"w5500",
            "w 5500":"w5500",
            "w-5500":"w5500",
            "s10":"s10",
            "s 10":"s10",
            "s-10":"s10",
            "c10":"c10",
            "c 10":"c10",
            "c-10":"c10",
            "c/k 10":"c10",
            "c/10":"c10",
            "ck 10":"c10",
            "ck10":"c10",
            "ck-10":"c10",
            "k10":"c10",
            "k 10":"c10",
            "k-10":"c10",
            "c20":"c20",
            "c 20":"c20",
            "c-20":"c20",
            "c/k 20":"c20",
            "c/20":"c20",
            "ck 20":"c20",
            "ck20":"c20",
            "ck-20":"c20",
            "k20":"c20",
            "k 20":"c20",
            "k-20":"c20",
            "c30":"c30",
            "c 30":"c30",
            "c-30":"c30",
            "c/k 30":"c30",
            "c/30":"c30",
            "ck 30":"c30",
            "ck30":"c30",
            "ck-30":"c30",
            "k30":"c30",
            "k 30":"c30",
            "k-30":"c30",
            "c1500":"c1500",
            "c 1500":"c1500",
            "c-1500":"c1500",
            "c/k 1500":"c1500",
            "c/1500":"c1500",
            "ck 1500":"c1500",
            "ck1500":"c1500",
            "ck-1500":"c1500",
            "k1500":"c1500",
            "k 1500":"c1500",
            "k-1500":"c1500",
            "c2500":"c2500",
            "c 2500":"c2500",
            "c-2500":"c2500",
            "c/k 2500":"c2500",
            "c/2500":"c2500",
            "ck 2500":"c2500",
            "ck2500":"c2500",
            "ck-2500":"c2500",
            "k2500":"c2500",
            "k 2500":"c2500",
            "k-2500":"c2500",
            "c3500":"c3500",
            "c 3500":"c3500",
            "c-3500":"c3500",
            "c/k 3500":"c3500",
            "c/3500":"c3500",
            "ck 3500":"c3500",
            "ck3500":"c3500",
            "ck-3500":"c3500",
            "k3500":"c3500",
            "k 3500":"c3500",
            "k-3500":"c3500",
            "c4500":"c4500",
            "c 4500":"c4500",
            "c-4500":"c4500",
            "c/k 4500":"c4500",
            "c/4500":"c4500",
            "ck 4500":"c4500",
            "ck4500":"c4500",
            "ck-4500":"c4500",
            "k4500":"c4500",
            "k 4500":"c4500",
            "k-4500":"c4500",
            "c5500":"c5500",
            "c 5500":"c5500",
            "c-5500":"c5500",
            "c/k 5500":"c5500",
            "c/5500":"c5500",
            "ck 5500":"c5500",
            "ck5500":"c5500",
            "ck-5500":"c5500",
            "k5500":"c5500",
            "k 5500":"c5500",
            "k-5500":"c5500",
            "c6500":"c6500",
            "c 6500":"c6500",
            "c-6500":"c6500",
            "c/k 6500":"c6500",
            "c/6500":"c6500",
            "ck 6500":"c6500",
            "ck6500":"c6500",
            "ck-6500":"c6500",
            "k6500":"c6500",
            "k 6500":"c6500",
            "k-6500":"c6500",
            "c7500":"c7500",
            "c 7500":"c7500",
            "c-7500":"c7500",
            "c/k 7500":"c7500",
            "c/7500":"c7500",
            "ck 7500":"c7500",
            "ck7500":"c7500",
            "ck-7500":"c7500",
            "k7500":"c7500",
            "k 7500":"c7500",
            "k-7500":"c7500",
            "c8500":"c8500",
            "c 8500":"c8500",
            "c-8500":"c8500",
            "c/k 8500":"c8500",
            "c/8500":"c8500",
            "ck 8500":"c8500",
            "ck8500":"c8500",
            "ck-8500":"c8500",
            "k8500":"c8500",
            "k 8500":"c8500",
            "k-8500":"c8500",
            "c7d042":"c7d042",
            "c7h042":"c7h042",
            "f7b042":"f7b042",
            "210":"210",
            "del ray":"delray",
            "delray":"delray",
            "ss":"ss",
            "3100":"3100",
            "3200":"3200",
            "3600":"3600",
            "4400":"4400",
            "8500":"c8500",
            "7500":"c7500",
            "30":"c30",
            "50":"c50",
            "70":"c70"
        }


class Chrysler(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "200":"200",
            "300m":"300m",
            "300-m":"300m",
            "300":"300",
            "aspen":"aspen",
            "aspin":"aspen",
            "cirrus":"cirrus",
            "concord":"concorde",
            "concorde":"concorde",
            "cordoba":"cordoba",
            "crossfire":"crossfire",
            "crown imperial":"imperial crown",
            "imperial crown":"imperial crown",
            "imperial":"imperial",
            "eagle premier":"eagle premier",
            "fifth avenue":"fifth avenue",
            "5th avenue":"fifth avenue",
            "le baron":"lebaron",
            "lebaron":"lebaron",
            "lhs":"lhs",
            "70":"six",
            "new yorker":"new yorker",
            "newport":"newport",
            "p.t.":"pt cruiser",
            "pt cruiser":"pt cruiser",
            "ptcruiser":"pt cruiser",
            "pacifica":"pacifica",
            "prowler":"prowler",
            "seabring":"sebring",
            "sebring":"sebring",
            "serbing":"sebring",
            "serbring":"sebring",
            "t&c":"town and country",
            "t/c":"town and country",
            "tc":"town and country",
            "tow and country":"town and country",
            "town & country":"town and country",
            "town and country":"town and country",
            "town country":"town and country",
            "town n country":"town and country",
            "town&country":"town and country",
            "town/country":"town and country",
            "valiant charger":"valiant charger",
            "valiant":"valiant",
            "voyager":"voyager",
            "windsor":"windsor"
        }


class Citroen(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "bx":"bx",
            "cx":"cx",
            "ds":"ds",
            "dyane":"dyane",
            "evasion":"evasion",
            "gs":"gs",
            "g.s":"gs",
            "ds":"ds",
            "sm":"sm",
        }


class Coda(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "coda":"coda",
            "electric":"coda",
            "sedan":"coda",
        }


class Corbin(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "sparrow":"sparrow",
            "electric":"sparrow",
            "bike":"sparrow",
        }


class Daewoo(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "espero":"espero",
            "lanos":"lanos",
            "leganza":"leganza",
            "nubira":"nubira",
        }


class Daihatsu(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "charade":"charade",
            "opti":"opti",
            "rocky":"rocky",
            "trimobile":"trimobile",
            "yrv":"yrv",
        }


class Daimler(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models={
            "double six":"double six",
            "sp250":"sp250",
            "saloon":"250",
            "250":"250",
            "2.5":"250",
            "conquest":"conquest",
            "sovereign":"sovereign",
            "db18":"consort",
            "consort":"consort",
            "ds420":"ds420",
        }


class Datsun(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "1600":"1600",
            "1200":"1200",
            "2000":"2000",
            "210":"210",
            "240":"240z",
            "260":"260z",
            "280zx":"280zx",
            "280 zx":"280zx",
            "280-zx":"280zx",
            "280":"280z",
            "300zx":"300zx",
            "300":"300z",
            "510":"510",
            "520":"520",
            "620":"620",
            "710":"710",
            "720":"720",
            "810":"810",
            "b110":"sunny",
            "sunny":"sunny",
            "b120":"sunny",
            "b310":"sunny",
            "f10":"cherry",
            "g90":"g90"
        }


class DeTomaso(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "pantera":"pantera",
        }


class DeLorean(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "dmc":"dmc-12",
        }


class Desoto(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "fireflite":"fireflite",
            "fireflight":"fireflite",
            "firesweep":"firesweep",
            "powermaster":"powermaster",
            "adventurer":"adventurer",
            "firedome":"firedome",
        }


class DiamondT(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "201":"201",
            "203":"203",
            "210":"210",
            "306":"306",
            "704":"704",
        }


class DKW(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "8":"f8",
            "9":"f9",
            "10":"f10",
            "11":"f11",
            "12":"f12",
            "schnellaster":"schnellaster",
        }


class Dodge(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "durango":"durango",
            "durange":"durango",
            "ramcharger":"ramcharger",
            "b2500":"b250",
            "b300":"b300",
            "1500":"ram 1500",
            "2500":"ram 2500",
            "3500":"ram 3500",
            "4500":"ram 4500",
            "5500":"ram 5500",
            "caliber":"caliber",
            "caliper":"caliber",
            "calliper":"caliber",
            "500":"k500",
            "600":"600",
            "a100":"a100",
            "advenger":"avenger",
            "avenger":"avenger",
            "aspen":"aspen",
            "b-3-b":"b3b",
            "b-3b":"b3b",
            "caravan":"caravan",
            "grand can":"caravan",
            "grand carvan":"caravan",
            "cargo":"cargo",
            "charger daytona":"charger daytona",
            "chager daytona":"charger daytona",
            "daytona":"daytona",
            "challanger":"challenger",
            "charger":"charger",
            "chager":"charger",
            "coronet":"coronet",
            "d 150":"d150",
            "d150":"d150",
            "d-150":"d150",
            "d 100":"d100",
            "d100":"d100",
            "d-100":"d100",
            "d 250":"d250",
            "d250":"d250",
            "d-250":"d250",
            "d 200":"d200",
            "d200":"d200",
            "d-200":"d200",
            "d 300":"d300",
            "d300":"d300",
            "d-300":"d300",
            "d 2":"d2",
            "d2":"d2",
            "d-2":"d2",
            "d 5":"d5",
            "d5":"d5",
            "d-5":"d5",
            "d 8":"d8",
            "d8":"d8",
            "d-8":"d8",
            "d50":"ram 50",
            "dakota":"dakota",
            "dokota":"dakota",
            "dart":"dart",
            "dc8":"dc8",
            "demon":"challenger",
            "desoto":"desoto",
            "diplomat":"diplomat",
            "intrepid":"intrepid",
            "journey":"journey",
            "m 37":"m37",
            "m-37":"m37",
            "m37":"m37",
            "m 880":"m880",
            "m-880":"m880",
            "m880":"m880",
            "magnum":"magnum",
            "meadowbrook":"meadowbrook",
            "mirada":"mirada",
            "monaco":"monaco",
            "neon":"neon",
            "nitro":"nitro",
            "polara":"polara",
            "raider":"raider",
            "rampage":"rampage",
            "royal monaco":"royal monaco",
            "monaco":"monaco",
            "shadow":"shadow",
            "stealth":"stealth",
            "stratus":"stratus",
            "super bee":"superbee",
            "superbee":"superbee",
            "viper":"viper",
            "w 100":"w100",
            "w100":"100",
            "w 150":"w150",
            "w150":"w150",
            "w 250":"w250",
            "w250":"w250",
            "w 300":"w300",
            "w300":"w300",
            "w 350":"w350",
            "w350":"w350",
            "wayfarer":"wayfarer",
        }


class Dort(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "10":"model-10"
        }


class Dutton(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "surf":"surf"
        }


class Edsel(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "cortina":"cortina",
            "citation":"citation",
            "corsair":"corsair",
            "pacer":"pacer",
            "ranger":"ranger",
            "ranchero":"ranchero",
            "viking":"viking",
            "village":"villager",
        }


class Excalibur(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "phaeton":"phaeton",
            "roadster":"roadster",
            "series 1":"series 1",
        }


class Exomotive(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "exocet":"exocet",
        }


class FactoryFive(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "818":"818r",
            "gtm":"gtm",
        }


class Ferrari(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "149":"f149",
            "308":"308",
            "328":"328",
            "348":"348",
            "355":"f355",
            "360":"360",
            "365":"365",
            "400":"400",
            "430":"f430",
            "456":"456",
            "458":"458",
            "488":"488",
            "550":"550",
            "575":"575",
            "599":"599",
            "612":"612",
            "california":"f149",
            "berlinetta":"f12",
            "daytona":"365",
            "12":"f12",
            "ff":"ff",
            "mondial":"mondial",
            "testarossa":"testarossa",
        }


class Fiat(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models={
            "1100":"1100",
            "1200":"1200",
            "124":"124",
            "126":"126",
            "127":"127",
            "128":"128",
            "130":"130",
            "131":"131",
            "132":"132",
            "133":"133",
            "500":"500",
            "850":"850",
            "barchetta":"barchetta",
            "brava":"brava",
            "bravo":"bravo",
            "dino":"dino",
            "spider":"124",
            "lombardi":"850",
            "strada":"strada",
            "bertone":"x19",
            "19":"x19",
            "1/9":"x19",
            "campagnola":"campagnola",
            "pininfarina":"coupe",
            "coupe":"coupe",
        }


class Fiberfab(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "avenger":"avenger-gt",
            "gt":"avenger-gt",
            "valkyrie":"valkyrie",
        }


class Fisker(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "karma":"karma",
        }

        
class Ford(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "48":"model-48",
            "ecoline":{
                "150":"e150",
                "250":"e250",
                "350":"e350",
                "450":"e450"
            },
            "transit":{
                "150":"transit 150",
                "250":"transit 250",
                "350":"transit 350"
            }, 
            "econoline":{
                "150":"e150",
                "250":"e250",
                "350":"e350",
                "450":"e450"
            },
            "100":{
                "e100":"e100",
                "e-":"e100",
                "e ":"e100",
                "c100":"c100",
                "c-100":"c100",
                "c 100":"c100",
                "100":"f100"
            },
            "150":{
                "e150":"e150",
                "e-150":"e150",
                "e 150":"e150",
                "c150":"c150",
                "c-150":"c150",
                "c 150":"c150",
                "t 150":"transit 150",
                "t150":"transit 150",
                "t-150":"transit 150",
                "150":"f150"
            },
            "250":{
                "e250":"e250",
                "e-250":"e250",
                "e 250":"e250",
                "t 250":"transit 250",
                "t250":"transit 250",
                "t-250":"transit 250",
                "250":"f250"
            },
            "300":"300",
            "350":{
                "e350":"e350",
                "e-350":"e350",
                "e 350":"e350",
                "c350":"c350",
                "c-350":"c350",
                "c 350":"c350",
                "t 350":"transit 350",
                "t350":"transit 350",
                "t-350":"transit 350",
                "350":"f350"
            },
            "450":{
                "e450":"e450",
                "e-450":"e450",
                "e 450":"e450",
                "450":"f450"
            },
            "500":{
                "f-500":"f500",
                "f 500":"f500",
                "f500":"f500",
                "fairlane":"fairlane",
                "500":"500"
            },
            "550":{
                "550":"f550"
            },
            "6000":{
                "ft":"ft6000",
                "6000":"f6000"
            },
            "600":{
                "n600":"n600",
                "n-600":"n600",
                "n 600":"n600",
                "600":"f600"
            },
            "650":{
                
                "650":"f650"
            },
            "7000":{
                "7000":"f7000"
            },
            "700":{
                "700":"f700"
            },
            "750":{
                
                "750":"f750"
            },
            "8000":{
                "l8000":"l8000",
                "l-8000":"l8000",
                "l 8000":"l8000",
                "ln8000":"ln8000",
                "ln 8000":"ln 8000",
                "ln-8000":"ln-8000",
                "8000":"cf8000"
            },
            "800":{
                "f-800":"f800",
                "f 800":"f800",
                "f800":"f800",

                "800":"c800"
            },
            "9000":{
                "9000":"ln9000"
            },
            "max":{
                "c-":"c-max",
                "c -":"c-max",
                "cmax":"c-max",
                "c max":"c-max",

            },
            "contour":"countour",
            "country":"country squire",
            "crestline":"crestline",
            "crow":"crown victoria",
            "crown":"crown victoria",
            "customline":"customline",
            "deluxe":"deluxe",
            "de luxe":"deluxe",
            "delux":"deluxe",
            "deuce":"deuce",
            "cargo":"cargo",
            "aerostar":"aerostar",
            "beonco ii":"bronco ii",
            "bonco ii":"bronco ii",
            "bronco ii":"bronco ii",
            "beonco 2":"bronco ii",
            "bonco 2":"bronco ii",
            "bronco 2":"bronco ii",
            "beonco":"bronco",
            "bonco":"bronco",
            "bronco":"bronco",
            "escape":"escape",
            "esape":"escape",
            "excape":"escape",
            "escort":"escort",
            "excursion":"excursion",
            "excusrion":"excursion",
            "edge":"edge",
            "elite":"elite",
            "expadition":"expedition",
            "expedetion":"expedition",
            "expedtion":"expedition",
            "expetion":"expedition",
            "espidition":"expedition",
            "explore":"explorer",
            "exploror":"explorer",
            "exployer":"explorer",
            "falcon":"falcon",
            "flacon":"falcon",
            "festiva":"festiva",
            "fiesta":"fiesta",
            "five hundred":"500",
            "fivehundred":"500",
            "flax":"flex",
            "fles":"flex",
            "flex":"flex",
            "focus":"focus",
            "freestar":"freestar",
            "freestyle":"freestyle",
            "fusion":"fusion",
            "fustion":"fusion",
            "galaxie":"galaxy",
            "galazie":"galaxy",
            "galaxy":"galaxy",
            "golden jubilee":"golden jubilee",
            "gran torino":"gran torino",
            "grand torino":"gran torino",
            "torino":"torino",
            "granada":"granada",
            "lcf":"lcf",
            "lt9513":"lt9513",
            "lt-9513":"lt9513",
            "lt 9513":"lt9513",
            "ltd":"ltd",
            "mainline":"mainline",
            "mainliner":"mainline",
            "maverick":"maverick",
            "model":{
                "model-aa":"model-aa",
                " aa":"model-aa",
                "aa ":"model-aa",
                "model-a":"model-a",
                " a":"model-a",
                "a ":"model-a",
                "model-b":"model-b",
                " b":"model-b",
                "b ":"model-b",
                "model-tt":"model-tt",
                " tt":"model-tt",
                "tt ":"model-tt",
                "model-t":"model-t",
                " t":"model-t",
                "t ":"model-t",
                "model-48":"model-48",
                " 48":"model-48",
                "48 ":"model-48",
            },
            "mustan":"mustang",
            "mustang":"mustang",
            "shelby":"mustang",
            "opera":"opera",
            "parklane":"parklane",
            "phaeton":"phaeton",
            "pinto":"pinto",
            "probe":"probe",
            "ranchero":"ranchero",
            "ranger":"ranger",
            "raptor":"raptor",
            "ratrod":"rat rod",
            "rat rod":"rat rod",
            "rat-rod":"rat rod",
            "skyliner":"fairlane",
            "starliner":"starliner",
            "sunliner":"sunliner",
            "t-bird":"thunderbird",
            "tbird":"thunderbird",
            "thunderbird":"thunderbird",
            "tunderbird":"thunderbird",
            "bucket":"t-bucket",
            "taurus":"taurus",
            "tarus":"taurus",
            "turus":"taurus",
            "tuarus":"taurus",
            "tempo":"tempo",
            "vicky":"victoria",
            "victoria":"victoria",
            "windstar":"windstar",
            "winstar":"windstar",
            "f-1":"f1",
            "f 1":"f1",
            "f1":"f1",
            "f-3":"f3",
            "f 3":"f3",
            "f3":"f3",
            "f-4":"f4",
            "f 4":"f4",
            "f4":"f4",
            "f-5":"f5",
            "f 5":"f5",
            "f5":"f5",
            "f-6":"f6",
            "f 6":"f6",
            "f6":"f6",
        }


class Franklin(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "speedster":"speedster",
        }


class Frazer(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "nash":"nash",
            "manhatten":"manhatten",
        }    


class Freightliner(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "fl":{
                "60":"fl60",
                "70":"fl70",
                "80":"fl80",
                "112":"fl112",
            },
            "cascadia":"cascadia",
            "sprinter":"sprinter",
            "m2":"m2",
            "fb":{
                "50":"fb50",
                "60":"fb60",
                "65":"fb65",
                "70":"fb70",
                "80":"fb80",
            },
        }


class Genesis(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "g70":"g70",
            "g80":"g80",
            "g90":"g90",
        }


class Geo(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "metro":"metro",
            "prizm":"prizm",
            "storm":"storm",
            "tracker":"tracker",
            "spectrum":"spectrum",
            "403":"storm",
        }


class GMC(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "100":"100",
            "370":"370",
            "acadia":"acadia",
            "arcadia":"acadia",
            "blazer":"blazer",
            "brigadier":"brigadier",
            "caballero":"caballero",
            "cabellero":"caballero",
            "canyon":"canyon",
            "cayon":"canyon",
            "envoy":"envoy",
            "evoy":"envoy",
            "fc101":"fc101",
            "general":"general",
            "jimmy":"jimmy",
            "safari":"safari",
            "sonoma":"sonoma",
            "1500":{
                "kodiak":"kodiak 1500",
                "topckick":"kodiak 1500",
                "top kick":"kodiak 1500",
                "yukon":"yukon 1500",
                "suburban":"suburban 1500",
                "savana":"savana 1500",
                "savanna":"savana 1500",
                "1500":"sierra 1500"
            },
            "2500":{
                "kodiak":"kodiak 2500",
                "topckick":"kodiak 2500",
                "top kick":"kodiak 2500",
                "yukon":"yukon 2500",
                "savana":"savana 2500",
                "savanna":"savana 2500",
                "suburban":"suburban 2500",
                "2500":"sierra 2500"
            },
            "3500":{
                "kodiak":"kodiak 3500",
                "topckick":"kodiak 3500",
                "top kick":"kodiak 3500",
                "savanna":"savana 3500",
                "savana":"savana 3500",
                "3500":"sierra 3500"
            },
            "4500":{
                "kodiak":"kodiak 4500",
                "topckick":"kodiak 4500",
                "top kick":"kodiak 4500",
                "4500":"sierra 4500"
            },  
            "5500":{
                "kodiak":"kodiak 5500",
                "topckick":"kodiak 5500",
                "top kick":"kodiak 5500",
                "sierra":"sierra 5500",
                "5500":"c5500"
            },
            "6500":{
                "kodiak":"kodiak 6500",
                "topckick":"kodiak 6500",
                "top kick":"kodiak 6500",
                "sierra":"sierra 6500",
                "6500":"c6500"
            },
            "7500":{
                "kodiak":"kodiak 7500",
                "topckick":"kodiak 7500",
                "top kick":"kodiak 7500",
                "t7500":"t7500",
                "t-7500":"t7500",
                "t 7500":"t7500",
                "7500":"c7500"
            },
            "tahoe":"tahoe",
            "terrain":"terrain",
            "terrian":"terrain",
            "c6000":"c6000",
            "c-6000":"c6000",
            "c 6000":"c6000",
            "c7000":"c7000",
            "c-7000":"c7000",
            "c 7000":"c7000",
            "c8500":"c8500",
            "c-8500":"c8500",
            "c 8500":"c8500",
            "c10":"c10",
            "c-10":"c10",
            "c 10":"c10",
            "c35":"c3500",
            "c-35":"c3500",
            "c 35":"c3500",
            "c4e042":"c4e042",
            "sierra":"sierra 1500",
            "savana":"savana 1500",
            "savanna":"savana 1500",
            "sevanna":"savana 1500",
            "suburban":"suburban 1500",
            "yukon":"yukon 1500"
        }


class GrahamPaige(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "612":"612",
            "614":"614",
            "57":"model-57"
        }


class HansGlas(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "250":"goggomobile-t250",
        }


class HarleyDavidson(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "dyna":"dyna",
            "flthc":"flthc",
            "fxcw":"fxcw",
            "fxdl":"fxdl",
            "fxd":"fxd",
            "fxdc":"fxdc",
            "fxdb":"fxdb",
            "fxs":"fxs",
        }


class Henney(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "kilowatt":"kilowatt",
        }


class Hillman(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "imp":"imp",
            "minx":"minx",
            "husky":"husky",
        }


class Honda(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "600":"600",
            "650":"650",
            "750":"750",
            "800":"800",
            "900":"900",
            "1000":"1000",
            "1100":"1100",
            "1200":"1200",
            "1300":"1300",
            "1500":"1500",
            "1600":"1600",
            "1800":"1800",
            "accord":"accord",
            "accrod":"accord",
            "aerodeck":"aerodeck",
            "acty":"acty",
            "beat":"beat",
            "civc":"civic",
            "civic":"civic",
            "civiv":"civic",
            "charity":"clarity",
            "clarity":"clarity",
            "cr v":"cr-v",
            "cr-v":"cr-v",
            "crv":"cr-v",
            "cvr":"cr-v",
            "cr z":"cr-z",
            "cr-z":"cr-z",
            "crz":"cr-z",
            "czr":"cr-z",
            "crosstour":"crosstour",
            "cr x":"cr-x",
            "cr-x":"cr-x",
            "crx":"cr-x",
            "cxr":"cr-x",
            "del sol":"del sol",
            "delsol":"del sol",
            "element":"element",
            "fit":"fit",
            "hr v":"hr-v",
            "hr-v":"hr-v",
            "hrv":"hr-v",
            "hvr":"hr-v",
            "insight":"insight",
            "integra":"integra",
            "life":"life",
            "magna":"magna",
            "oddessy":"odyssey",
            "oddysey":"odyssey",
            "odessey":"odyssey",
            "odessy":"odyssey",
            "odyeesy":"odyssey",
            "odysee":"odyssey",
            "odysey":"odyssey",
            "odyssee":"odyssey",
            "odyssey":"odyssey",
            "oilot":"pilot",
            "pilot":"pilot",
            "passport":"passport",
            "prelude":"prelude",
            "ridge line":"ridgeline" ,
            "ridgeline":"ridgeline",
            "ridgline":"ridgeline",
            "2000":"s2000",
            "passport":"passport",
        }


class Hudson(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "american":"american",
            "commodore":"commodore",
            "jet":"jet",
            "hornet":"hornet",
            "model 20":"model-20",
            "rambler":"rambler",
            "terraplane":"terraplane",
            "wasp":"wasp",
        }


class Hummer(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "h1":"h1",
            "h2":"h2",
            "h3":"h3",
            "h3t":"h3t",
            "m998":"m998",
        }


class Hup(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "model":{
                "32":"model-32",
                " r":"model-r",
                "-r":"model-r",
            }
        }


class Hyundai(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "accent":"accent",
            "azera":"azera",
            "elantra":"elantra",
            "elentra":"elantra",
            "entourage":"entourage",
            "equus":"equus",
            "genesis":"genesis",
            "genisis":"genesis",
            "ioniq":"ioniq",
            "kona":"kona",
            "kauai":"kona",
            "palisade":"palisade",
            "sonata":"sonata",
            "sonota":"sonata",
            "tiburon":"tiburon",
            "tucson":"tucson",
            "tuscan":"tucson",
            "tuscon":"tucson",
            "veloster":"veloster",
            "velostor":"veloster",
            "venue":"venue",
            "veracruz":"veracruz",
            "xg":"grandeur",
            "grandeur":"grandeur",
            " fe":"santa fe"
        }


class Infiniti(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "ex":"qx50",
            "jx":"qx60",
            "fx":"qx70",
            "qx4":"qx70",
            "g ":"q50",
            "g3":"q50",
            "g-":"q50",
            "i-":"q50",
            "i3":"q50",
            "j30":"j30",
            "m3":"q70",
            "m5":"q70",
            "m4":"q70",
            "q40":"q40",
            "q50":"q50",
            "q45":"q70",
            "q60":"q60",
            "q70":"q70",
            "qx50":"qx50",
            "qx 50":"qx50",
            "qx56":"qx50",
            "qx 56":"qx50",
            "qx60":"qx60",
            "qx 60":"qx60",
            "qx70":"qx70",
            "qx 70":"qx70",
            "qx80":"qx80",
            "qx 80":"qx80",
        }


class Isuzu(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "amigo":"amigo",
            "ascender":"ascender",
            "axiom":"axiom",
            "hombre":"hombre",
            "i-280":"i-280",
            "i-290":"i-290",
            "i-350":"i-350",
            "i-370":"i-370",
            "impulse":"impulse",
            "npc":"npc",
            "elf":"elf",
            "npr":"npr",
            "rodeo":"rodeo",
            "trooper":"trooper",
            "wt5500":"wt5500",
        }


class Jaguar(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models={
            "3.8s":"s-type",
            "e type":"e-type",
            "e-type":"e-type",
            "e-pace":"e-pace",
            "e pace":"e pace",
            "etype":"e-type",
            "epace":"e-pace",
            "f type":"f-type",
            "f-type":"f-type",
            "f-pace":"f-pace",
            "f pace":"f pace",
            "ftype":"f-type",
            "fpace":"fpace",
            "i-pace":"i-pace",
            "i pace":"i-pace",
            "ipace":"i-pace",
            "stype":"s-type",
            "s type":"s-type",
            "s-type":"s-type",
            "ss100":"ss100",
            "ss 100":"ss100",
            "ss-100":"ss100",
            "vanden plas":"xj",
            "xj":"xj",
            "x type":"x-type",
            "x-type":"x-type",
            "xtype":"x-type",
            "xe":"xe",
            "xf":"xf",
            "xk":"xk",
        }


class Jeep(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "amc eagle":"amc eagle",
            "gran cherokee":"grand cherokee",
            "grand cherokee":"grand cherokee",
            "gr. cherokee":"grand cherokee",
            "gr cherokee":"grand cherokee",
            "grande cherokee":"grand cherokee",
            "grand wagoneer":"grand wagoneer",
            "gand wagoneer":"grand wagoneer",
            "cherokee":"cherokee",
            "cherokree":"cherokee",
            "cj":"willy",
            "comanche":"comanche",
            "commander":"commander",
            "compass":"compass",
            "dj":"dj",
            "gladiator":"gladiator",
            "j-10":"gladiator",
            "j10":"gladiator",
            "j20":"gladiator",
            "j-20":"gladiator",
            "j30":"gladiator",
            "j-30":"gladiator",
            "j40":"gladiator",
            "j-40":"gladiator",
            "laredo":"laredo",
            "libert":"liberty",
            "m715":"m715",
            "compass":"compass",
            "partiot":"patriot",
            "patriot":"patriot",
            "patroit":"patriot",
            "renegade":"renegade",
            "rubicon":"rubicon",
            "scrambler":"scrambler",
            "wagoneer":"wagoneer",
            "willy":"willys",
            "willeys":"willys",
            "tj":"wrangler",
            "wrang":"wrangler",
            "wanler":"wrangler",
            "xj":"cherokee"
        }


class Jensen(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "interceptor":"interceptor",
        }


class Kaiser(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "frazer":"frazer",
            "henry":"henry-j",
            "virginian":"virginian",
            "jeep":"jeep",
        }


class Kandi(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "coco":"coco",
        }


class Kia(Cadillac):
    def __init__(self):
        super().__init__()
        self.models = {
            "amanti":"opirus",
            "opirus":"opirus",
            "borrego":"borrego",
            "cadenza":"cadenza",
            "corento":"sorento",
            "forte":"forte",
            "k5":"k5",
            "k900":"k900",
            "niro":"niro",
            "optima":"k5",
            "optimia":"k5",
            "optioma":"k5",
            "rio":"rio",
            "rondo":"carens",
            "carens":"carens",
            "sedona":"carnival",
            "carnival":"carnival",
            "sodona":"carnival",
            "seltos":"seltos",
            "sephia":"sephia",
            "sol":"soul",
            "soul":"soul",
            "sorent":"sorento",
            "sorrent":"sorento",
            "spectra":"spectra",
            "sportage":"sportage",
            "sportqage":"sportage",
            "stinger":"stinger",
            "telluride":"telluride",
        }


class Lada(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "21013":"21013",
        }


class LaForza(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "magnum":"magnum",
        }


class Lamborghini(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "aventador":"aventador",
            "countach":"countach",
            "diablo":"diablo",
            "espada":"espada",
            "gallardo":"gallardo",
            "huracan":"huracan",
            "jarama":"jarama",
            "jalpa":"jalpa",
            "joseph":"joseph",
            "lm002":"lm002",
            "murcielago":"murcielago",
            "reventon":"reventon",
            "silhouette":"silhouette",
            "urus":"urus",
            "veneno":"veneno",
            "ventador":"aventador",
            "lp":"aventador",
        }


class Lancia(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "beta":"beta",
            "dedra":"dedra",
            "delta":"delta",
            "flavia":"flavia",
            "fulvia":"fulvia",
            "gamma":"gamma",
            "kappa":"kappa",
            "scorpion":"scorpion",
            "stratos":"stratos",
            "zagato":"zagato",
            "flaminia":"flaminia",
            "appia":"appia",
        }

class LandRover(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "defender":"defender",
            "discovery":"discovery",
            "freelander":"freelander",
            "free lander":"freelander",
            "free-lander":"freelander",
            "lr":"freelander",
            "range":"rangerover",
            "evoque":"rangerover",
            "evoke":"rangerover",
            "velar":"rangerover",
            "hse":"hse",
            "ii":"series-2",
            "iii":"series-3",
            "serie":"series-1"
        }


class Lexus(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "es":"es",
            "ct":"ct",
            "nx":"nx",
            "ls":"ls",
            "gl":"gs",
            "gs":"gs",
            "gx":"gx",
            "hs":"hs",
            "is":"is",
            "lc":"lc",
            "lx":"lx",
            "rc":"rc",
            "rx":"rx",
            "sc":"sc",
            "ux":"ux",
            "200t":"nx",
            "430":"ls"
        }


class Lincoln(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "mercury comet":"mercury comet",
            "comet":"mercury comet",
            "aviator":"aviator",
            "blackwood":"blackwood",
            "capri":"capri",
            "mark":"continental mark",
            "mkc":"mkc",
            "mks":"mks",
            "mkt":"mkt",
            "mkx":"mkx",
            "mkz":"mkz",
            "zephyr":"mkz",
            "mk ":"continental mark",
            "continental":"continental",
            "corsair":"corsair",
            "ls":"ls",
            "mountaineer":"mountaineer",
            "nautilus":"nautilus",
            "navigator":"navigator",
            "town":"town car",
            "versailles":"versailles",
            "cosmopolitan":"cosmopolitan",
        }


class Lotus(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "elise":"elise",
            "eclat":"eclat",
            "elan":"elan",
            "cortina":"cortina",
            "esprit":"esprit",
            "europa":"europa",
            "evora":"evora",
            "excel":"excel",
            "exige":"exige",
            "m100":"m100",
            "seven":"seven",
        }


class Maserati(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "ghibli":"ghibli",
            "gran":"granturismo",
            "levante":"levante",
            "merak":"merak",
            "quattroporte":"quattroporte",
            "spyder":"spyder",
            "tc":"tc",
            "mexico":"mexico",
            "228":"228",
        }


class Maybach(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "57":"57",
            "62":"62",
        }

class Mazda(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models={
            "323":"323",
            "glc":"323",
            "protege":"323",
            "allegro":"323",
            "astina":"323",
            "familia":"323",
            "bongo":"bongo",
            "eunos":"mx",
            "miata":"mx",
            "millenia":"millenia",
            "mallinia":"millenia",
            "mellenia":"millenia",
            "tribute":"tribute",
            "speed":{
                "3":"3",
                "5":"5",
                "6":"6",
            },
            "mazda2":"2",
            "mazda3":"3",
            "mazda5":"5",
            "mazda6":"6",
            "mvp":"mpv",
            "mx":"mx",
            "rx":"rx",
            "cx":"cx",
            "c-x":"cx",
            "b-":"b",
            "b2":"b",
            "b4":"b",
            "2 ":"2",
            "3 ":"3",
            "5 ":"5",
            "6 ":"6",
            "7 ":"7"
        }


class McLaren(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "570":"570",
            "600":"600",
            "650":"650",
            "675":"675",
            "720":"720",
            "mp4":"mp4",
        }


class MercedesBenz(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models={
            "sprinter":"sprinter",
            "ssk":"ssk",
            "amg":{
                " gt":"amg-gt",
                " cls":"amg-cls",
                " gle":"amg-gle",
                " g":"amg-g",
                "g ":"amg-g",
                "g-":"amg-g",
                " sls":"amg-sls",
                " s":"amg-s",
                "s ":"amg-s",
                "s-":"amg-s",
                " c":"amg-c",
                "c ":"amg-c",
                "c-":"amg-c",
            },
            "170":{
                " s":"170s",
                " va":"170va",
            },
            "180":{
                "180b":"180b",
                " b":"180b",
                "180a":"180a",
            },
            "190":{
                "190c":"c190",
                " c":"c190",
                "c ":"c190",
                "c-":"c190",
                "190e":"e109",
                " e":"e109",
                "e ":"e109",
                "e-":"e109",

            },
            "200":{
                "200d":"200d",
                " d":"200d",

            },
            "220":{
                "220se":"220se",
                " se":"220se",
                "220s":"220s",
                " s":"220s",
                "s ":"220s",
                "s-":"220s",
                "220s":"220s",
                " c":"c220",
                "c ":"c220",
                "c-":"c220",
                "c220":"c220",
            },
            "230":{
                "slk":"slk230",
                "ge":"230ge",
                " c":"c230",
                "c ":"c230",
                "c-":"c230",
                "c230":"c230",
            },
            "240":{
                "gd":"240gd",
                "240d":"240d",
                " d":"240d",
                " c":"c240",
                "c ":"c240",
                "c-":"c240",
                "c240":"c240",
            },
            "250":{
                "slk":"slk250",
                "cla":"cla250",
                "gl":"gl250",
                " c":"c250",
                "c ":"c250",
                "c-":"c250",
                "c250":"c250",
            },
            "280":{
                "280e":"e280",
                " e":"e280",
                "e ":"e280",
                "e-":"e280",
                "e280":"e280",
                "slk":"slk280",
                "sl":"sl280",
                "se":"280se",
                "280s":"280s",
                " s":"280s",
                "s ":"280s",
                "s-":"280s",
                " c":"c280",
                "c ":"c280",
                "c-":"c280",
                "c280":"c280",
            },
            "300":{
                "gl":"gl300",
                "sl":"sl300",
                "cd":"300cd",
                " e":"e300",
                "e ":"e300",
                "e-":"e300",
                "e300":"e300",
                "300e":"e300",
                "sdl":"sdl300",
                "sel":"sel300",
                "se":"300se",
                "ce":"300ce",
                " c":"c300",
                "c ":"c300",
                "c-":"c300",
                "c300":"c300",
                "300d":"300d",
                " d":"300d",
                "sd":"300sd",
                "td":"300td",
                "te":"300te",
            },
            "320":{
                "sl":"sl320",
                "clk":"clk320",
                "gl":"gl320",
                "ml":"ml320",
                " e":"e320",
                "e ":"e320",
                "e-":"e320",
                "e320":"e320",
                " c":"c320",
                "c ":"c320",
                "c-":"c320",
                "c320":"c320",
                " s":"s320",
                "s ":"s320",
                "s-":"s320",
                "s320":"s320",
                "r ":"r320",
                "r-":"r320",
                " r":"r320",
                "r320":"r320",
            },
            "350":{
                "clk":"clk350",
                "ml":"ml350",
                "sl":"sl350",
                "e-":"e350",
                "gl":"gl350",
                " e":"e350",
                "e ":"e350",
                "e350":"e350",
                "350e":"e350",
                " c":"c350",
                "c ":"c350",
                "c-":"c350",
                "c350":"c350",
                " r":"r350",
                "r ":"r350",
                "r-":"r350",
                "r350":"r350",
                " s":"s350",
                "s ":"s350",
                "s-":"s350",
                "s350":"s350",
            },
            "380":{
                "sel":"sel380",
                "slc":"slc380",
                "sl":"sl380",
                "sec":"sec380",
                

            },
            "400":{
              " e":"e400",
              "e ":"e400",
              "e-":"e400",
              "e400":"e400",
              "sel":"sel400",  
            },
            "420":{
                " e":"e420",
                "e ":"e420",
                "e-":"e420",
                "e420":"e420",
                "sel":"sel420",
                
            },
            "430":{
                " e":"e430",
                "e ":"e430",
                "e-":"e430",
                "clk":"clk430",
                "e430":"e430",
                "ml":"ml430",
                "s-":"s430",
                "s ":"s430",
                " s":"s430",
                "s430":"s430",
            },
            "450":{
                " e":"e450",
                "e ":"e450",
                "e-":"e450",
                "e450":"e450",
                "se":"se450",
                "slc":"slc450",
                "sl":"sl450",
                "gl":"gl450",
                "ml":"ml450",
                " s":"s450",
                "s ":"s450",
                "s-":"s450",
                "s450":"s450",
            },
            "500":{
                " e":"e500",
                "e ":"e500",
                "e-":"e500",
                "e500":"e500",
                "clk":"clk500",
                "cls":"cls500",
                "sel":"sel500",
                "sl":"sl500",
                "ml":"ml500",
                "cl":"cl500",
                " g":"g500",
                "g ":"g500",
                "g-":"g500",
                "g500":"g500",
                " r":"r500",
                "r ":"r500",
                "r-":"r500",
                "r500":"r500",
                " s":"s500",
                "s ":"s500",
                "s-":"s500",
                "s500":"s500",
            },
            "550":{
                " e":"e550",
                "e ":"e550",
                "e-":"e550",
                "e550":"e550",
                "cls":"cls550",
                "clk":"clk550",
                " s":"s550",
                "s ":"s550",
                "s-":"s550",
                "s550":"s550",
                "sl":"sl550",
                "ml":"ml550",
                "cl":"cl550",
                "gl":"gl550",
                " g":"g550",
                "g ":"g550",
                "g-":"g550",
                "g550":"g550",
            },
            "560":{
                "sl":"sl560",
                "sel":"sel560",
                "sec":"sec560",
            },
            "600":{
                "sel":"sel600",
                "cla":"cla600",
                "cl":"cl600",
                " s":"s600",
                "s ":"s600",
                "s-":"s600",
                "s600":"s600",
            },
            "830":{
                "sl":"sl830",
            },
            "gazelle":"gazelle",
            "unimog":"unimog"
        }


class Mercury(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "capri":"capri",
            "comet":"comet",
            "cougar":"cougar",
            "couger":"cougar",
            "cyclone":"cyclone",
            "eight":"eight",
            "grand marquis":"grand marquis",
            "marauder":"marauder",
            "mariner":"mariner",
            "marineer":"mariner",
            "medalist":"medalist",
            "meteor":"meteor",
            "milan":"milan",
            "monarch":"monarch",
            "montclair":"montclair",
            "montcliar":"montclair",
            "montego":"montego",
            "monterey":"monterey",
            "monterrey":"monterey",
            "mountaineer":"mountaineer",
            "moutaineer":"mountaineer",
            "mystique":"mystique",
            "park":"parklane",
            "topaz":"topaz",
            "tracer":"tracer",
            "turnpike":"turnpike",
            "sable":"sable",
            "villager":"villager",
        }


class Messerschmitt(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "kr200":"kr200",
            "kr201":"kr201",
            "kr202":"kr202",
        }


class MG(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "mg":{
                "mga":"mga",
                " a":"mga",
                "a ":"mga",
                "-a":"mga",
                "mgb":"mgb",
                " b":"mgb",
                "b ":"mgb",
                "-b":"mgb",
                "mgc":"mgc",
                " c":"mgc",
                "c ":"mgc",
                "-c":"mgc",
                "mgt":"mgt",
                " t":"mgt",
                "t ":"mgt",
                "-t":"mgt",
                "1100":"mg-1100",
            },
            "magnette":"magnette",
            "midget":"midget",
            "mv":"mv",
        }


class Midget(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "king":"king midget",
            "midgit":"king midget",
        }


class Mini(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "clubman":"clubman",
            "cooper":"cooper",
            "coooper":"cooper",
            "countryman":"countryman",
            "hardtop":"hardtop",
            "moke":"moke",
            "paceman":"paceman",
            "roadster":"cooper",
            "camper":"campervan",
            "van":"campervan",
        }


class Mitsubishi(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "3000gt":"3000gt",
            "3000":"3000gt",
            "3000 gt":"3000gt",
            "delica":"delica",
            "diamante":"diamante",
            "eclipse":"eclipse",
            "endeavor":"endeavor",
            "fuso":"fuso",
            "galant":"galant",
            "imiev":"imiev",
            "lancer":"lancer",
            "max":"mighty max",
            "mini":"minicab",
            "mirage":"mirage",
            "montero":"montero",
            "monteri":"montero",
            "outlander":"outlander",
            "pajero":"pajero",
            "raider":"raider",
        }


class Morgan(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "aero":"aero",
            "plus":"plus",
            "roadster":"roadster",
            "4/4":"4/4",
        }


class Nash(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "ambassador":"ambassador",
            "american":"american",
            "healey":"healey",
            "metropolitan":"metropolitan",
            "rambler":"rambler",
            "statesman":"statesman",
            "studebaker":"studebaker",
        }



class Nissan(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "200":{
                "sx":"200sx"
            },
            "240":{
                "sx":"240sx",
            },
            "280":{
                "zx":"280zx"
            },
            "300":{
                "zx":"300zx",
            },
            "350":{
                "350z":"350z",
                "z ":"350z",
                " z":"350z",
            },
            "370":{
                "370z":"370z",
                "z ":"370z",
                " z":"370z",
            },
            "720":"720",
            "altima":"altima",
            "sltima ":"altima",
            "atlima":"altima",
            "armada":"armada",
            "armanda":"armada",
            "axxes":"axxess",
            "caravan":"caravan",
            "homy":"caravan",
            "sentra":"sentra",
            "seenra":"sentra",
            "centra":"sentra",
            "cube":"cube",
            "d21":"d21",
            "frontier":"frontier",
            "fromtier":"frontier",
            "gt":"gt-r",
            "juke":"juke",
            "kick":"kicks",
            "leaf":"leaf",
            "maxima":"maxima",
            "marano":"murano",
            "morano":"murano",
            "murano":"murano",
            "murrano":"murano",
            "nv":"nv",
            "nx":"nx",
            "pao":"pao",
            "pathfinder":"pathfinder",
            "pathfider":"pathfinder",
            "pickup":"pickup",
            "quest":"quest",
            "rogue":"rogue",
            "roque":"rogue",
            "rouge":"rogue",
            "safari":"patrol",
            "patrol":"patrol",
            "titan":"titan",
            "silvia":"silvia",
            "skyline":"gt-r",
            "stanza":"stanza",
            "ud":"ud-truck",
            "versa":"versa",
            "exterra":"xterra",
            "xterra":"xterra",
        }


class NSU(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "prinz":"prinz",
            "ro80":"ro80",
        }


class Oldsmobile(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "88":"88",
            "98":"98",
            "442":"442",
            "alero":"alero",
            "aurora":"aurora",
            "bravada":"bravada",
            "calais":"f85",
            "cutlass":"f85",
            "ciera":"f85",
            "delmont":"88",
            "custom":"98",
            "delta":"88",
            "eighty":"88",
            "ninety":"98",
            "85":"f85",
            "holiday":"88",
            "dynamic":"88",
            "intrigue":"intrigue",
            "jetfire":"f85",
            "lss":"88",
            "l36":"88",
            "44":"442",
            "omega":"omega",
            "regency":"98",
            "silhouette":"silhouette",
            "starfire":"starfire",
            "toronado":"toronado",
            "vista":"vista-cruiser",
        }


class Opel(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "adam":"adam",
            "ampera":"ampera",
            "antara":"antara",
            "ascona":"ascona",
            "astra":"astra",
            "calibra":"calibra",
            "campo":"campo",
            "cascada":"cascada",
            "combo":"combo",
            "commodore":"commodore",
            "corsa":"corsa",
            "frontera":"frontera",
            "gt":"gt",
            "insignia":"insignia",
            "kadett":"kadett",
            "manta":"manta",
            "meriva":"meriva",
            "mokka":"mokka",
            "monterey":"monterey",
            "monza":"monza",
            "omega":"omega",
            "olympia":"olympia",
            "rekord":"rekord",
            "senator":"senator",
            "signum":"signum",
            "sintra":"sintra",
            "speedster":"speedster",
            "tigra":"tigra",
            "vectra":"vectra",
            "vivaro":"vivaro",
            "zafira":"zafira",
        }


class Packard(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "clipper":"clipper",
            "caribbean":"caribbean",
            "cavalier":"cavalier",
            "custom":"custom-eight",
            "eight":"custom-eight",
            "four-hundred":"400",
            "hawk":"hawk",
            "patrician":"patrician",
        }


class Peterbilt(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "357":"357",
            "362":"362",
            "377":"377",
            "378":"378",
            "379":"379",
            "387":"387",
            "388":"388",
            "389":"389",
            "567":"567",
        }


class PierceArrow(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "arrow":"arrow",
            "1240":"1240a",
            "1245":"1245",
            "1248":"1248a",
            "1255":"1255",
            "1601":"1601",
            "1602":"1602",
            "1603":"1603",
            "1701":"1701",
            "1702":"1702",
            "1703":"1703",
            "1801":"1801",
            "1802":"1802",
            "1803":"1803",
            "836":"836a",
            "840":"840a",
            "845":"845",
            "1236":"model-1236",
            "1242":"model-1242",
            "1247":"model-1247",
        }


class Polaris(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "slingshot":"slingshot",
        }

class Pontiac(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "aztec":"aztek",
            "aztek":"aztek",
            "acadian":"acadian",
            "beaumont":"beaumont",
            "bonneville":"bonneville",
            "boneville":"bonneville",
            "catalina":"catalina",
            "chieftain":"chieftain",
            "chieften":"chieftain",
            "chiefton":"chieftain",
            "fiero":"fiero",
            "firebird":"firebird",
            "formula":"firebird",
            "g3":"g3",
            "g5":"g5",
            "g6":"g6",
            "g8":"g8",
            "gr prix":"grand prix",
            "grand prix":"grand prix",
            "grand am":"grand am",
            "ville":"grandville",
            "gto":"gto",
            "g t o":"gto",
            "lemans":"lemans", 
            "montana":"montana",
            "montanna":"montana",
            "parisienne":"parisienne",
            "redbird":"firebird",
            "solsstice":"solstice",
            "solistice":"solstice",
            "soltice":"solstice",
            "star chief":"star-chief",
            "super chief":"star-chief",
            "starchief":"star-chief",
            "superchief":"star-chief",
            "streamliner":"streamliner",
            "sunbird":"sunbird",
            "sunfire":"sunfire",
            "tempest":"tempest",
            "torrent":"torrent",
            "tran":"firebird",
            "ventura":"ventura",
            "vibe":"vibe",
        }


class Porsche(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "junior":"junior",
            "356":"356",
            "718":"718",
            "911":"911",
            "912":"912",
            "914":"914",
            "924":"924",
            "928":"928",
            "930":"911",
            "944":"944",
            "964":"911",
            "968":"968",
            "991":"991",
            "997":"911",
            "996":"991",
            "boxster":"718",
            "boxter":"718",
            "carrera":"911",
            "cayenne":"cayenne",
            "caynne":"cayenne",
            "cayman":"718",
            "gt3":"911",
            "macan":"macan",
            "panamera":"panamera",
            "taycan":"taycan",
            "targa":"911",
            "spyder":"718"
        }


class Puma(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "gtc":"gtc",
            "gte":"gte",
        }


class Qvale(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "mangusta":"mangusta",
        }


class Ram(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "1500":"1500",
            "2500":"2500",
            "3500":"3500",
            "4500":"4500",
            "5500":"5500",
            "big horn":"1500",
            "cargo":"cargo",
            "charger":"charger",
            "chassis":"chassis",
            "charger":"charger",
            "dakota":"dakota",
        }


class Renault(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "alliance":"alliance",
            "ambassador":"ambassador",
            "avantime":"avantime",
            "captur":"captur",
            "caravelle":"caravelle",
            "dauphine":"dauphine",
            "fuego":"fuego",
            "gordini":"gordini",
            "kangoo":"kangoo",
            "gta":"gta",
            "lecar":"lecar",
            "medallion":"medallion",
            "r1134":"r1134",
            "r17":"r17",
            "simca":"simca",
        }


class Reo(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "speedwagon":"speedwagon",
            "d19":"speedwagon",
            "22":"gold-comet",
            "63":"v63",
        }


class Riley(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "rm":"rm",
            "elf":"elf",
        }


class RollsRoyce(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "25/30":"25/30",
            "camargue":"camargue",
            "corniche":"corniche",
            "cullinan":"cullinan",
            "dawn":"dawn",
            "ghost":"ghost",
            "spur":"silver",
            "phantom":"phantom",
            "silver":"silver",
            "wraith":"wraith",
        }


class Saab(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "92":"9-2x",
            "9-2":"9-2x",
            "93":"9-3",
            "9-3":"9-3",
            "94":"9-4x",
            "9-4":"9-4x",
            "95":"9-5",
            "9-5":"9-5",
            "97":"9-7x",
            "9-7x":"9-7x",
            "96":"96",
            "99":"99",
            "9000":"9000",
            "900":"900",
            "sonett":"sonett",
        }


class Saturn(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "astra":"astra",
            "aura":"aura",
            "ion":"ion",
            "l ":"l-series",
            "l-":"l-series",
            "l100":"l-series",
            "l200":"l-series",
            "l300":"l-series",
            "l400":"l-series",
            "ls":"l-series",
            "lw":"l-series",
            "outlook":"outlook",
            "relay":"relay",
            "sky":"sky",
            "solstice":"sky",
            "sl":"sl",
            "sc":"sc",
            "sw":"sw",
            "vue":"vue",
        }


class Scion(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "fr-s":"frs",
            "frs":"frs",
            "iq":"iq",
            "tc":"tc",
            "xa":"xa",
            "xb":"xb",
            "xd":"xd",
        }


class Shelby(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "cobra":"cobra",
            "daytona":"daytona",
            "gt":"gt",
            "mustang":"mustang",
            "911":"911",
        }


class Siata(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "daina":"daina",
            "spider":"spider",
            "spring":"spring",
        }


class Smart(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "fortwo":"fortwo",
            "forfour":"forfour",
            "city":"fortwo",
            "451":"fortwo",
            "cabrio":"fortwo",
        }


class Sterling(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "825":"825",
            "827":"827",
            "aceterra":"aceterra",
        }


class Studebaker(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "champion":"champion",
            "avanti":"avanti",
            "commander":"commander",
            "eagle":"golden-hawk",
            "golden":"golden-hawk",
            "hawk":"golden-hawk",
        }


class Stutz(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "hawk":"blackhawk",
            "victoria":"victoria",
        }


class Subaru(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "ascent":"ascent",
            "cross":"crosstrek",
            "baja":"baja",
            "brat":"brat",
            "brz":"brz",
            "crosstrek":"crosstrek",
            "foreser":"forester",
            "forester":"forester",
            "foreter":"forester",
            "forreseter":"forester",
            "forster":"forester",
            "impreza":"impreza",
            "imprezza":"impreza",
            "imprza":"impreza",
            "inpreza":"impreza",
            "justy":"justy",
            "legacy":"legacy",
            "legay":"legacy",
            "loyale":"leone",
            "leone":"leone",
            "sambar":"sambar",
            "outback":"outback",
            "putback":"outback",
            "tribeca":"tribeca",
            "tribecca":"tribeca",
            "gl":"leone",
            "svx":"svx",
            "wrx":"wrx",
            "xt":"xt",
            "xv":"xv",
            "360":"360",
        }


class Suzuki(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "aerio":"aerio",
            "capuccino":"capuccino",
            "carry":"carry",
            "equator":"equator",
            "forenza":"forenza",
            "grand":"grand-vitara",
            "vitara":"grand-vitara",
            "kizashi":"kizashi",
            "samurai":"jimny",
            "jimny":"jimny",
            "sidekick":"sidekick",
            "swift":"swift",
            "sx4":"sx4",
            "verona":"verona",
            "lj":"lj",
            "reno":"reno",
            "xl7":"xl-7",
            "x90":"x-90",
        }
            


class Tesla(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "model 3":"model 3",
            "model s":"model s",
            "model x":"model x",
            "model y":"model y",
            "s":"model s",
            "3":"model 3",
            "x":"model x",
            "y":"model y",
        }


class Toyota(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "runner":"4runner",
            "runne":"4runner",
            "86":"86",
            "avalon":"avalon",
            "bj":"bj",
            "chr":"c-hr",
            "c-hr":"c-hr",
            "c-hr":"c-hr",
            "camry":"camry",
            "camery":"camry",
            "camrey":"camry",
            "carolla":"corolla",
            "corolla":"corolla",
            "celica":"celica",
            "celsior":"celsior",
            "coaster":"coaster",
            "corona":"corona",
            "corrola":"corolla",
            "corrolla":"corolla",
            "cressida":"cressida",
            "crown":"crown",
            "echo":"yaris",
            "platz":"yaris",
            "yari":"yaris",
            "fj":"fj",
            "estima":"previa",
            "previa":"previa",
            "supra":"supra",
            "hiace":"hiace",
            "highlander":"highlander",
            "hilander":"highlander",
            "highlnader":"highlander",
            "hylander":"highlander",
            "highlandr":"highlander",
            "hilux":"hilux",
            "cruise":"land-cruiser",
            "liteace":"liteace",
            "townace":"liteace",
            "martrix":"matrix",
            "matrix":"matrix",
            "ace":"masterace",
            "max":"mighty max",
            "mirai":"mirai",
            "mr":"mr2",
            "omgea":"omega",
            "omega":"omega",
            "paseo":"paseo",
            "pilot":"pilot",
            "prius":"prius",
            "rav":"rav4",
            "salara":"solara",
            "solara":"solara",
            "scion":"scion",
            "seinna":"sienna",
            "sieana":"sienna",
            "sequioa":"sequoia",
            "sequoia":"sequoia",
            "sera":"sera",
            "soarer":"soarer",
            "t-100":"t100",
            "t100":"t100",
            "t 100":"t100",
            "tacoma":"tacoma",
            "tacom":"tacoma",
            "tandra":"tundra",
            "tundra":"tundra",
            "tercel":"tercel",
            "turcel":"tercel",
            "venza":"venza",
            "auris":"auris",
            "dolphin":"dolphin",
        }


class Triumph(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "2000":"2000",
            "gt6":"gt6",
            "herald":"herald",
            "renown":"renown",
            "spitfire":"spitfire",
            "stag":"stag",
            "tr":{
                "250":"tr-5",
                "2":"tr-2",
                "3":"tr-3",
                "4":"tr-4",
                "5":"tr-5",
                "6":"tr-6",
                "7":"tr-7",
                "8":"tr-8",
            }
        }


class Tvr(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "cerbera":"cerbera",
            "chimaera":"chimaera",
            "griffith":"griffith",
            "sagaris":"sagaris",
            "speed":"speed",
            "tamora":"tamora",
            "tuscan":"tuscan",
            "taimar":"m-series",
            "vixen":"vixen",
            "s3":"s-series",
            "2500m":"m-series",
        }


class Volkswagen(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "arteon":"arteon",
            "atlas":"atlas",
            "beelte":"beetle",
            "beetle":"beetle",
            "bug":"beetle",
            "beettle":"beetle",
            "beetel":"beetle",
            "cabrio":"cabriolet",
            "cc":"cc",
            "corrado":"corrado",
            "eos":"eos",
            "eurovan":"eurovan",
            "ghia":"karmann-ghia",
            "karmann":"karmann-ghia",
            "golf":"golf",
            "gti":"golf",
            "jeeta":"jetta",
            "jetta":"jetta",
            "gli":"jetta",
            "mg tc":"mg-tc",
            "mk":"mk",
            "passat":"passat",
            "phideon":"phideon",
            "phaeton":"phaeton",
            "rabbit":"rabbit",
            "lupo":"lupo",
            "routan":"routan",
            "t2":"type-2",
            "type 2":"type-2",
            "vanagon":"type-2",
            "westfalia":"type-2",
            "t1":"type-1",
            "type 1":"type-1",
            "iii":"type-3",
            "thing":"thing",
            "tiguan":"tiguan",
            "touareg":"touareg",
            "toureg":"touareg",
            "411":"type-4",
            "412":"type-4",
            "dashar":"passat",
            "atlas":"atlas",
            "scirocco":"scirocco",
        }


class Volvo(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "122":"122",
            "1800":"p1800",
            "240":"240",
            "245":"245",
            "265":"265",
            "340":"340",
            "360":"360",
            "440":"440",
            "460":"460",
            "480":"480",
            "444":"pv444",
            "544":"pv544",
            "670":"670",
            "740":"740",
            "760":"760",
            "780":"780",
            "850":"850",
            "940":"940",
            "960":"960",
            "amazon":"amazon",
            "c30":"c30",
            "c 30":"c30",
            "c-30":"c30",
            "c70":"c70",
            "c 70":"c70",
            "c-70":"c70",
            "country":"cross-country",
            "s40":"s40",
            "s 40":"s40",
            "s-40":"s40",
            "s60":"s60",
            "s 60":"s60",
            "s-60":"s60",
            "s70":"s70",
            "s 70":"s70",
            "s-70":"s70",
            "s80":"s80",
            "s 80":"s80",
            "s-80":"s80",
            "s90":"s90",
            "s 90":"s90",
            "s-90":"s90",
            "v40":"v40",
            "v 40":"v40",
            "v-40":"v40",
            "v50":"v50",
            "v 50":"v50",
            "v-50":"v50",
            "v60":"v60",
            "v 60":"v60",
            "v-60":"v60",
            "v70":"v70",
            "v 70":"v70",
            "v-70":"v70",
            "v90":"v90",
            "v 90":"v90",
            "v-90":"v90",
            "xc":{
                "60":"xc60",
                "70":"xc70",
                "90":"xc90"
            },
        }


class Yugo(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "gv":"gv",
        }


class Zimmer(CarModelParser):
    def __init__(self):
        super().__init__()
        self.models = {
            "gold":"golden-spirit",
        }


############################################################################




#                   Help functions to clean data                           #





############################################################################

def filter_manufacturers(manufacturer: str) -> str:
    manufacturer_filter = {
        "acura":"acura",
        "alfa":"alfa-romeo",
        "alpine":"alpine",
        "am":"am-general",
        "amc":"amc",
        "american lafrance":"american-lafrance",
        "american motors":"amc",
        "amphicar":"amphicar",
        "aprilia":"aprilia",
        "ariel":"ariel",
        "arnolt":"arnolt",
        "martin":"aston-martin",
        "auburn":"auburn",
        "cord":"auburn",
        "audi":"audi",
        "austin":"austin-healey",
        "avanti":"studebaker",
        "baw":"baw",
        "bentley":"bentley",
        "bertone":"bertone",
        "bmw":"bmw",
        "bricklin":"bricklin",
        "bugatti":"bugatti",
        "buick":"buick",
        "cadillac":"cadillac",
        "cagiva":"cagiva",
        "cami":"cami",
        "checker":"checker",
        "chevrolet":"chevrolet",
        "chevy":"chevrolet",
        "chrysler":"chrysler",
        "eagle":"chrysler",
        "citroen":"citroen",
        "citroën":"citroen",
        "coda":"coda",
        "corbin":"corbin",
        "daewoo":"daewoo",
        "daihatsu":"daihatsu",
        "daimler":"daimler",
        "datsun":"datsun",
        "de tomaso":"de-tomaso",
        "delorean":"delorean",
        "desoto":"desoto",
        "diamond":"diamond-t",
        "dkw":"dkw",
        "dodge":"dodge",
        "dort":"dort",
        "ducati":"ducati",
        "dutton":"dutton",
        "edsel":"edsel",
        "excalibur":"excalibur",
        "exomotive":"exomotive",
        "factory five":"factory-five",
        "federal motors":"federal motor",
        "ferrari":"ferrari",
        "fiat":"fiat",
        "fiberfab":"fiberfab",
        "fisker":"fisker",
        "ford":"ford",
        "franklin":"franklin",
        "frazer":"frazer",
        "frazier":"frazer",
        "freightliner":"freightliner",
        "freightlnr":"freightliner",
        "frt-thomas bus":"thomas",
        "fuji heavy industries":"subaru",
        "fwd corp.":"four-wheel-drive",
        "gac trumpchi":"trumpchi",
        "general motors":"gmc",
        "genesis":"genesis",
        "geo":"geo",
        "goggomobil":"hans-glas",
        "gmc":"gmc",
        "graham":"graham-paige",
        "olson":"morgan-olson",
        "harley":"harley-davidson",
        "healey":"austin-healey",
        "henney":"henney",
        "hillman":"hillman",
        "hino":"hino",
        "honda":"honda",
        "aerodeck":"honda",
        "hudson":"hudson",
        "hummer":"hummer",
        "hupmobile":"hupp",
        "hyundai":"hyundai",
        "ikarus":"ikarus",
        "infiniti":"infiniti",
        "infinity":"infiniti",
        "isuzu":"isuzu",
        "iveco":"iveco",
        "jaguar":"jaguar",
        "jeep":"jeep",
        "jensen":"jensen",
        "kaiser":"kaiser",
        "kandi":"kandi",
        "kawasaki":"kawasaki",
        "kenworth":"kenworth",
        "kia":"kia",
        "king midget":"midget",
        "krm":"krm",
        "lada":"lada",
        "laforza":"laforza",
        "lamborghini":"lamborghini",
        "lancia":"lancia",
        "rover":"land-rover",
        "lexus":"lexus",
        "lincoln":"lincoln",
        "lotus":"lotus",
        "mack":"mack",
        "maserati":"maserati",
        "maybach":"maybach",
        "mazda":"mazda",
        "mclaren":"mclaren",
        "mercedes":"mercedes-benz",
        "mercury":"mercury",
        "messerschmitt":"messerschmitt",
        "mg":"mg",
        "mini":"mini",
        "mitsubishi":"mitsubishi",
        "morgan":"morgan",
        "morris":"morris",
        "nash":"nash",
        "nissan":"nissan",
        "nummi":"nummi",
        "nsu":"nsu",
        "oldsmobile":"oldsmobile",
        "opel":"opel",
        "packard":"packard",
        "peterbilt":"peterbilt",
        "peugeot":"peugeot",
        "piaggio":"piaggio",
        "pierce":"pierce-arrow",
        "plymouth":"plymouth",
        "polaris":"polaris",
        "pontiac":"pontiac",
        "pontlac":"pontiac",
        "porsche":"porsche",
        "puma":"puma",
        "qvale":"qvale",
        "ram":"ram",
        "rambler":"rambler",
        "renault":"renault",
        "reo":"reo",
        "riley":"riley",
        "royce":"rolls-royce",
        "ruf":"ruf",
        "saab":"saab",
        "saturn":"saturn",
        "scion":"scion",
        "shelby":"shelby",
        "siata":"siata",
        "smart":"smart",
        "sterling":"sterling",
        "studabaker":"studebaker",
        "studabeker":"studebaker",
        "stutz":"stutz",
        "subaru":"subaru",
        "suburu":"subaru",
        "sunbeam":"alpine",
        "suzuki":"suzuki",
        "tesla":"tesla",
        "toyota":"toyota",
        "triumph":"triumph",
        "tvr":"tvr",
        "volkswagen":"volkswagen",
        "vw":"volkswagen",
        "volvo":"volvo",
        "wester":"wester-star",
        "yamaha":"yamaha",
        "yugo":"yugo",
        "zimmer":"zimmer"
    }


    for filter_ in manufacturer_filter:
        if filter_ in manufacturer:
            return manufacturer_filter[filter_]
    return np.nan