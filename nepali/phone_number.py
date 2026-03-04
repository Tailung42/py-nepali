import re
from enum import Enum

_mobile_number_re = re.compile(r"^(?:\+977|977)?(?:-)?(?:98|97|96)\d{8}$")
_landline_number_re = re.compile(
    r"^(?:\+977|977)?(?:-)?(?:0)?(?:[01][1-9]|2[13-9]|[3-9]\d)\d{6,7}$"
)


class Operator(Enum):
    NEPAL_TELECOM = "Nepal Telecom"
    NCELL = "Ncell"
    SMART_CELL = "Smart Cell"
    UTL = "UTL"
    HELLO_MOBILE = "Hello Mobile"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"<Operator: {self.value}>" 

from enum import Enum

class AreaCode(Enum):
    ACHHAM = ("Achham", "097")
    BAITADI = ("Baitadi", "095")
    BANKE = ("Banke", "081")
    BARA = ("Bara", "053")
    BARDIA = ("Bardia", "084")
    BHAKTAPUR = ("Bhaktapur", "01")
    BHERI = ("Bheri", "083")
    BHOJPUR = ("Bhojpur", "029")
    BIRGUNJ = ("Birgunj", "051")
    CHITWAN = ("Chitwan", "056")
    DADELDHURA = ("Dadeldhura", "096")
    DAILEKH = ("Dailekh", "089")
    DARCHULA = ("Darchula", "093")
    DHADING = ("Dhading", "010")
    DHANKUTA = ("Dhankuta", "026")
    DHANUSHA = ("Dhanusha", "041")
    DHAWALAGIRI = ("Dhawalagiri", "068")
    DOLKHA = ("Dolkha", "049")
    DOTI = ("Doti", "094")
    GANDAKI = ("Gandaki", "064")
    GORKHA = ("Gorkha", "064")
    GULMI = ("Gulmi", "079")
    ILAM = ("Ilam", "027")
    JANAKPUR = ("Janakpur", "046")
    JUMLA = ("Jumla", "087")
    KAILALI = ("Kailali", "091")
    KAPILVASTU = ("Kapilvastu", "076")
    KASKI = ("Kaski", "061")
    KATHMANDU = ("Kathmandu", "01")
    KHOTANG = ("Khotang", "036")
    KOSHI = ("Koshi", "025")
    LAMJUNG = ("Lamjung", "066")
    LUMBINI = ("Lumbini", "071")
    MAHAKALI = ("Mahakali", "099")
    MAHOTTARI = ("Mahottari", "044")
    MAKWANPUR = ("Makwanpur", "057")
    MECHI = ("Mechi", "023")
    MORANG = ("Morang", "021")
    MYAGDI = ("Myagdi", "069")
    N_PARASI = ("N. Parasi", "078")
    NARAYANI = ("Narayani", "055")
    OKHALDHUNGA = ("Okhaldhunga", "037")
    PALPA = ("Palpa", "075")
    PANCHTHAR = ("Panchthar", "024")
    PARBAT = ("Parbat", "067")
    PARSA = ("Parsa", "051")
    PATAN = ("Patan", "01")
    POKHARA = ("Pokhara", "061")
    PYUTHAN = ("Pyuthan", "086")
    RAPTI = ("Rapti", "082")
    RUPANDEHI = ("Rupandehi", "071")
    S_PALCHOK = ("S. Palchok", "011")
    SAGARMATHA = ("Sagarmatha", "033")
    SAPTARI = ("Saptari", "031")
    SETI = ("Seti", "092")
    SINDHULI = ("Sindhuli", "047")
    SOLUKHUMBU = ("Solukhumbu", "038")
    SYANGIA = ("Syangia", "063")
    UDAYPUR = ("Udaypur", "035")

    def __init__(self, district: str, area_code: str):
        self.district= district
        self.area_code = area_code

    def __str__(self):
        return f"{self.district}: {self.area_code}"

    @classmethod
    def get_by_area_code(cls, area_code:str):
        for area in cls:
            if area.value[1] == area_code:
                return area
        return None


def is_mobile_number(number: str) -> bool:
    """
    Returns True is the input number is mobile number.

    >>> is_mobile = is_mobile_number(number)
    >>> if is_mobile:
    >>>     ...
    """
    try:
        return bool(_mobile_number_re.match(number))
    except Exception:
        return False


def is_landline_number(number: str) -> bool:
    """
    Returns True is the input number is landline number.

    >>> is_landline = is_landline_number(number)
    >>> if is_landline:
    >>>     ...
    """
    try:
        return bool(_landline_number_re.match(number))
    except Exception:
        return False


def is_valid(number: str) -> bool:
    return is_mobile_number(number) or is_landline_number(number)


def get_exact_number(number: str) -> str:
    # replacing start 977
    if number.startswith("977"):
        number = number.replace("977", "")
    # replacing +977 and all -
    return number.replace("+977", "").replace("-", "")


def parse(number: str):
    """
    Parse and returns the details of the phone number: `dict`.
    The return data may vary between mobile and landline numbers.
    If the number is invalid it returns `None`.

    If you want to make sure you get a valid response, please use
    `is_valid`, `is_mobile_number`, and `is_landline_number`.

    :return:
    {
        "type": "Mobile" | "Landline",
        "number": "XXXXXXX",
        ...
    }
    """
    if not number and type(number) != str:
        return None

    number = number.replace("-", "")

    # checking if mobile number
    if is_mobile_number(number):
        return _parse_mobile_number(number)

    if is_landline_number(number):
        return _parse_landline_number(number)

    return None


def _get_operator(number: str) -> Operator | None:
    """
    Returns operator from the number.
    NOTE: The number should be 10digit mobile number.
    """
    starting_number = number[:3]

    # NTC
    if starting_number in ["984", "985", "986", "974", "975"]:
        return Operator.NEPAL_TELECOM

    # NCELL
    if starting_number in ["980", "981", "982"]:
        return Operator.NCELL

    # Smart Cell
    if starting_number in ["961", "962", "988"]:
        return Operator.SMART_CELL

    # UTL
    if starting_number == "972":
        return Operator.UTL

    # Hello Mobile
    if starting_number == "963":
        return Operator.HELLO_MOBILE

    return None


def _parse_mobile_number(number: str):
    """
    Parse and returns mobile number details.
    :return:
    {
        "type": "Mobile",
        "number": "98XXXXXXXX",
        "operator": <Operator>
    }
    """
    number = get_exact_number(number)
    operator = _get_operator(number)

    if not operator:
        return None

    detail = {
        "type": "Mobile",
        "number": number,
        "operator": operator,
    }
    return detail


def _get_area_code(number) -> str:
    """
    Returns area code of the number.
    NOTE: The number should be landline number without +977/977.
    """
    code = number[:3]

    # Kathmandu, Lalitpur, and Bhaktapur => 01
    if number.startswith("01") and code not in ["010", "011", "019"]:
        return "01"

    return code


def _parse_landline_number(number) -> dict:
    """
    Parse and returns landline number details.
    :return:
    {
        "type": "Landline",
        "number": "98XXXXXXXX",
        "area_code": <AreaCode>
    }
    """
    
    # adding zero
    if number[0] != "0":
        number = f"0{number}"
        
    number = get_exact_number(number)
    area_code = _get_area_code(number)
    district = _get_district(area_code)
    
    if not district:
        return None
     

    return {
        "type": "Landline",
        "number": number,
        "area_code": _get_area_code(number),
        "district": district,
    }


def _get_district(area_code: str) -> AreaCode | None:
    """
    Returns the details of the area code. 
    """
    return AreaCode.get_by_area_code(area_code).district
    