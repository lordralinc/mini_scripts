import enum
import typing


class QuoteSymbol:
    SINGLE = "'"
    DOUBLE = '"'
    TREE = "«»"


def quote(text: str, mode: str = QuoteSymbol.TREE) -> str:
    if len(mode) == 0:
        raise ValueError("At least 1 character is required")
    if len(mode) == 1:
        mode = mode + mode
    return mode[0] + text + mode[1]


def b2s(value: bool, on_yes: str = "✅", on_no: str = "❌") -> str:
    return on_yes if value else on_no


def f2i(value: float, force: bool = False) -> typing.Union[int, float]:
    if force:
        return int(value)
    return int(value) if value == int(value) else value


def join(data: typing.Union[str, typing.Iterable], separator: str = ",") -> str:
    if isinstance(data, str):
        data = [data]
    if not data:
        return ''
    return separator.join([str(obj) for obj in data])


def get_reversed_word(text: str) -> str:
    lines = [list(s) for s in text.split('\n')]
    reversed_lines = [reversed(line) for line in lines]
    return "\n".join("".join(line) for line in reversed_lines)


class Case(enum.Enum):
    """Обьект описывает падежи

    - **NOMN** --   именительный падеж
        `Кто? Что? Хомяк ест`
    - **GENT** --   родительный падеж
        `Кого? Чего? У нас нет хомяка`
    - **DATV** --   дательный падеж
        `Кому? Чему? сказать хомяку спасибо`
    - **ACCS** --   винительный падеж
        `Кого? Что? хомяк читает книгу`
    - **ABLT** --   творительный падеж
        `Кем? Чем? Зерно съедено хомяком`
    - **LOCT** --   предложный падеж
        `О ком? О чём? и т.п. хомяка несут в корзинке`
    - **VOCT** --   звательный падеж
        `Его формы используются при обращении к человеку. Саш, пойдем в кино.`
    - **GEN2** --   второй родительный (частичный) падеж
        - ложка сахару (*gent* - производство сахара)
        - стакан яду (*gent* - нет яда)`
    - **ACC2** --   второй винительный падеж
        `записался в солдаты`
    - **LOC2** --   второй предложный (местный) падеж
        - я у него в долгу (*loct* - напоминать о долге)
        - висит в шкафу (*loct* - монолог о шкафе)
        - весь в снегу (*loct* - писать о снеге)

    """
    NOMN = 'nomn'
    GENT = 'gent'
    DATV = 'datv'
    ACCS = 'accs'
    ABLT = 'ablt'
    LOCT = 'loct'
    VOCT = 'voct'
    GEN2 = 'gen2'
    ACC2 = 'acc2'
    LOC2 = 'loc2'


def get_case(
        morph_analyzer: "MorphAnalyzer",
        num: typing.Union[float, str],
        word: str,
        case: typing.Union[Case, str] = Case.NOMN,
        without_num=False
) -> str:
    case = case.value if isinstance(case, Case) else case
    inflected = morph_analyzer.parse(word)[0].inflect({case})[0]
    p = morph_analyzer.parse(inflected)[0]
    if without_num:
        return p.make_agree_with_number(int(num)).word
    return "{} {}".format(
        num, p.make_agree_with_number(int(num)).word
    )


def split_by_limit(text: str, limit: int, sep=" ") -> typing.List[str]:
    words = text.split(' ')
    if max(map(len, words)) > limit:
        raise ValueError("limit is too small")
    res, part, others = [], words[0], words[1:]
    for word in others:
        if len(sep) + len(word) > limit - len(part):
            res.append(part)
            part = word
        else:
            part += sep + word
    if part:
        res.append(part)
    return res
