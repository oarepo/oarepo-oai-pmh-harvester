import json

from oarepo_oaipmh_harvester.transformer import OAITransformer, OAIRecord, matches, make_dict, make_array

from ..nr_theses_metadata.proxies import current_service as theses_service
from ..nr_theses_metadata.records.api import NrThesesMetadataRecord
import pycountry


def get_alpha2_lang(lang):
    py_lang = pycountry.languages.get(alpha_3=lang) or pycountry.languages.get(
        bibliographic=lang)
    if not py_lang:
        raise LookupError()
    return py_lang.alpha_2


def deduplicate(md, what):
    contribs = [json.dumps(x, sort_keys=True) for x in md.get(what, [])]
    for idx in range(len(contribs) - 1, -1, -1):
        for pidx in range(0, idx):
            if contribs[idx] == contribs[pidx]:
                del contribs[idx]
                del md[what][idx]
                break


class NuslTransformer(OAITransformer):
    oaiidentifier_search_property = 'metadata_systemIdentifiers_identifier'
    oaiidentifier_search_path = ('metadata', 'systemIdentifiers', 'identifier')
    record_service = theses_service
    record_model = NrThesesMetadataRecord

    def transform_single(self, rec: OAIRecord):
        md = rec.transformed.setdefault('metadata', {})

        # rec.service = theses_service
        # rec.model = NrThesesMetadataRecord

        transform_001_control_number(md, rec)
        transform_020_isbn(md, rec)
        transform_022_issn(md, rec)
        transform_035_original_record_oai(md, rec)
        transform_046_date_modified(md, rec)
        transform_046_date_issued(md, rec)
        transform_245_title(md, rec)
        transform_245_translated_title(md, rec)
        transform_246_title_alternate(md, rec)
        transform_24633a_subtitle(md, rec)
        transform_24633b_subtitle(md, rec)
        transform_260_publisher(md, rec)
        transform_300_extent(md, rec)
        transform_490_series(md, rec)
        transform_520_abstract(md, rec)
        transform_598_note(md, rec)
        transform_65007_subject(md, rec)
        transform_65017_subject(md, rec)
        transform_650_7_subject(md, rec)
        transform_6530_en_keywords(md, rec)
        transform_653_cs_keywords(md, rec)
        transform_7112_event(md, rec)
        transform_720_creator(md, rec)
        transform_720_contributor(md, rec)
        transform_7731_related_item(md, rec)
        transform_85640_original_record_url(md, rec)
        transform_85642_external_location(md, rec)
        transform_970_catalogue_sysno(md, rec)
        transform_980_resource_type(md, rec)
        transform_996_accessibility(md, rec)
        transform_999C1_funding_reference(md, rec)

        transform_04107_language(md, rec)
        transform_336_certifikovana_metodika(md, rec)

        transform_540_rights(md, rec)

        transform_oai_identifier(md, rec)

        transform_502_degree_grantor(md, rec)
        transform_7102_degree_grantor(md, rec)  # a a 9='cze'

        transform_502_date_defended(md, rec)

        transform_586_defended(md, rec)  # obhajeno == true
        transform_656_study_field(md, rec)

        transform_998_collection(md, rec)

        deduplicate(md, 'languages')
        deduplicate(md, 'contributors')
        deduplicate(md, 'subjects')
        deduplicate(md, 'additionalTitles')
        deduplicate(md, 'degreeGrantor')

        rec.ignore('909COq')  # "licensed", "openaire", ...
        rec.ignore('909COp')  # oai set
        rec.ignore('909COo')  # oai identifier taken from elsewhere
        rec.ignore('005')     # modification time
        rec.ignore('502__b')  # titul
        rec.ignore('502__g')  # treba "Magisterský studijní program"
        rec.ignore('008')     # podivnost
        rec.ignore('0248_a')  # nusl identifikator

        # # asi prilogy
        rec.ignore('340__a')  # "text/pdf"
        rec.ignore('506__a')  # "public"
        rec.ignore("655_72")  # "NUŠL typ dokumentu"
        rec.ignore("655_7a")  # "Disertační práce"
        rec.ignore("8564_u")  # odkaz na soubor
        rec.ignore("8564_z")  # nazev/typ souboru "plny text"
        rec.ignore("8564_x")  # "icon"
        rec.ignore("996__9")  # "0"
        rec.ignore("656_72")  # "AKVO"
        rec.ignore("500__a")  # "BÍLEK, Martin. Hospodářská etika jako etika rámcového řádu. Kritická reflexe hospodářsko-etické koncepce Karla Homanna. Č. Budějovice, 2011. disertační práce (Th.D.). JIHOČESKÁ UNIVERZITA V ČESKÝCH BUDĚJOVICÍCH. Teologická fakulta",
        rec.ignore("85642z")  # "Elektronické umístění souboru",
        rec.ignore("502__d")  # "2007"
        rec.ignore("586__b")  # "successfully defended",


        # rec.ignore("720__e")  # "advisor", "referee"

        # rec.ignore("6557_2")  # "NUŠL typ dokumentu"
        # rec.ignore("6557_a")  # "Výzkumné zprávy",
        # rec.ignore("999C1b")  # "GA AV ČR"
        # rec.ignore("7731_x")  # "ISSN 1804–2406",
        # rec.ignore("4900_v")  # "V-1110"
        # rec.ignore("7112_c")  # "Praha (CZ)",
        # rec.ignore("7112_d")  # "2010-12-08",
        # rec.ignore("7731_z")  # "978-80-7375-514-0",
        # rec.ignore("7112_d")  # "2008-08-24 / 2008-08-28",
        #
        # rec.ignore("720__6")  # "https://orcid.org/0000-0002-8255-348X",
        # rec.ignore("8564_y")  # "česká verze",
        # rec.ignore("7731_g")  # "Česká národní banka",
        # rec.ignore("FFT_0a")  # "http://pro.inflow.cz/projekt-informacniho-vzdelavani-pedagogu-na-stredni-technicke-skole"
        # rec.ignore("246__n")  # "Podprojekt A",
        # rec.ignore("7201_i")  # "Univerzita Karlova, Lékařská fakulta v Plzni",
        # rec.ignore("24500 ")  # "12 zák. č. 144/1992/ Sb. o ochraně přírody a krajiny) na území v
        #
        # rec.ignore("650_72")  # "PSH",
        # rec.ignore("650_77")  # "nlk20040147082",
        # rec.ignore("999c1a")  # "WP2-98"
        # rec.ignore("999c1a")  # "WP2-98"
        # rec.ignore("999c1b")  # "Ministerstvo zemědělství ČR",
        # rec.ignore("4900_b")  # "4/2012",
        # rec.ignore("7731_g")  # "Roč. 22, č. 2 (2011)",
        # rec.ignore("999C19")  # "MŠMT ČR"
        # rec.ignore("8564_y")  # "česká verze", "English version"
        # rec.ignore("999C2a")  # "UK", "GA ČR"
        #
        #
        # rec.ignore("24630a")  # "ročník 8, číslo 1",


        return True


@matches('001')
def transform_001_control_number(md, rec, value):
    md.setdefault('systemIdentifiers', []).append({
        'identifier': 'http://www.nusl.cz/ntk/nusl-' + value,
        'scheme': 'nusl'
    })


@matches('020__a')
def transform_020_isbn(md, rec, value):
    md.setdefault('objectIdentifiers', []).append({
        'identifier': value,
        'scheme': 'ISBN'
    })


@matches('022__a')
def transform_022_issn(md, rec, value):
    md.setdefault('objectIdentifiers', []).append({
        'identifier': value,
        'scheme': 'ISSN'
    })


@matches('035__a')
def transform_035_original_record_oai(md, rec, value):
    md.setdefault('systemIdentifiers', []).append({
        'identifier': value,
        'scheme': 'originalRecordOAI'
    })


@matches('046__j')
def transform_046_date_modified(md, rec, value):
    md['dateModified'] = value


@matches('046__k')
def transform_046_date_issued(md, rec, value):
    md['dateIssued'] = value


@matches('24500a')
def transform_245_title(md, rec, value):
    md['title'] = value


@matches('24500b')
def transform_245_translated_title(md, rec, value):
    md.setdefault('additionalTitles', []).append({
        'title': [
            {'lang': 'en', 'value': value}
        ],
        'titleType': 'translatedTitle'
    })


@matches('24630n', '24630p')
def transform_246_title_alternate(md, rec, val):
    _transform_title(md, rec, 'alternativeTitle', val)


def _transform_title(md, rec, titleType, val):
    try:
        lang = get_alpha2_lang(rec.get("04107a"))
        md.setdefault('additionalTitles', []).append({
            'title': [
                {'lang': lang, 'value': val}
            ],
            'titleType': titleType
        })
    except LookupError:
        # append it with the original language, marshmallow will take care of that
        md.setdefault('additionalTitles', []).append({
            'title': [
                {'lang': rec.get("04107a"), 'value': val}
            ],
            'titleType': titleType
        })


@matches('24633a')
def transform_24633a_subtitle(md, rec, val):
    _transform_title(md, rec, 'subtitle', val)


@matches('24633b')
def transform_24633b_subtitle(md, rec, val):
    md.setdefault('additionalTitles', []).append({
        'title': [
            {'lang': 'en', 'value': val}
        ],
        'titleType': 'subtitle'
    })


@matches('260__b')
def transform_260_publisher(md, rec, val):
    md.setdefault('publishers', []).append(val)


@matches('300__a')
def transform_300_extent(md, rec, val):
    md['extent'] = val


@matches('4900_a', '4900_v', paired=True)
def transform_490_series(md, rec, value):
    md.setdefault('series', []).append(make_dict(
        'seriesTitle', value[0],
        'seriesVolume', value[1]
    ))


@matches('520__a', '520__9', paired=True)
def transform_520_abstract(md, rec, value):
    try:
        md.setdefault('abstract', []).append({
            'lang': get_alpha2_lang(value[1]),
            'value': value[0]
        })
    except LookupError:
        md.setdefault('abstract', []).append({
            'lang': value[1],  # marshmallow will take care of that
            'value': value[0]
        })


@matches('598__a')
def transform_598_note(md, rec, value):
    md.setdefault('notes', []).append(value)


@matches('65007a', '65007j', '650072', '650070', paired=True)
def transform_65007_subject(md, rec, value):
    transform_subject(md, value)


@matches('65017a', '65017j', '650172', '650170', paired=True)
def transform_65017_subject(md, rec, value):
    transform_subject(md, value)


@matches('650_7a', '650_7j', '650_72', '650_70', '650_77', paired=True)
def transform_650_7_subject(md, rec, value):
    transform_subject(md, value)


def transform_subject(md, value):
    purl = value[3] or ''
    val_url = purl if purl.startswith('http://') or purl.startswith('https://') else None
    class_code = value[4] if len(value) > 4 else None
    if not class_code and not (purl.startswith('http://') or purl.startswith('https://')):
        class_code = purl

    md.setdefault('subjects', []).append(
        make_dict(
            'subjectScheme', value[2],
            'classificationCode', class_code,
            'valueURI', val_url,
            'subject', make_array(
                value[0], lambda: {'lang': 'cs', 'value': value[0]},
                value[1], lambda: {'lang': 'en', 'value': value[1]},
            )
        ))


@matches('6530_a')
def transform_6530_en_keywords(md, rec, value):
    # splitnout take na carce
    for v in value.split('|'):
        v = v.strip()
        if not v:
            continue
        md.setdefault('subjects', []).append(
            {
                'subjectScheme': 'keyword',
                'subject': [
                    {'lang': 'en', 'value': v}
                ]
            }
        )


@matches('653__a')
def transform_653_cs_keywords(md, rec, value):
    # splitnout take na carce
    for v in value.split('|'):
        v = v.strip()
        if not v:
            continue
        md.setdefault('subjects', []).append(
            {
                'subjectScheme': 'keyword',
                'subject': [
                    {'lang': 'cs', 'value': v}
                ]
            }
        )


@matches('7112_a', '7112_c', '7112_d', '7112_g', paired=True)
def transform_7112_event(md, rec, value):
    event = {
        'eventNameOriginal': value[0]
    }

    alternate_name = value[3]
    if alternate_name:
        event["eventNameAlternate"] = [alternate_name]

    date = value[2]
    if date:
        event['eventDate'] = date

    place = value[1]
    if place:
        place = parse_place(place)
        if place:
            event["eventLocation"] = place

    return event


def parse_place(place):
    res = {}
    place_array = place.strip().rsplit("(", 1)
    country = place_array[-1].replace(")", "").strip().lower()
    place = place_array[0].strip()
    if place:
        res["place"] = place
        res["country"] = country  # TODO: taxonomy
    return res


@matches('720__a', unique=True)
def transform_720_creator(md, rec, value):
    if value:
        md.setdefault('creators', []).append({
            'fullName': value,
            'nameType': 'Personal'
        })


# TODO: check this if the value match correctly (array aligning in parser)
@matches('720__i', '720__e', paired=True, unique=True)
def transform_720_contributor(md, rec, value):
    if value[0]:
        md.setdefault('contributors', []).append(
            make_dict(
                'fullName', value[0],
                'nameType', 'Personal',
                'role', value[1]  # TODO: taxonomy
            ))


@matches('7731_t', '7731_z', '7731_x', '7731_g', paired=True)
def transform_7731_related_item(md, rec, value):
    # TODO: pokud je na zacatku stringu "ISBN " nebo "ISSN ", stripnout
    item_volume_issue = value[3]
    if item_volume_issue:
        item_volume_issue_parsed = parse_item_issue(item_volume_issue)
        if not item_volume_issue_parsed:
            item_volume_issue_parsed = {"itemIssue": item_volume_issue, "error": "Bad format"}
    else:
        item_volume_issue_parsed = {}

    md.setdefault('relatedItems', []).append(make_dict(
        'itemTitle', value[0],
        'itemPIDs', make_array(
            value[1], {'identifier': value[1], 'scheme': 'ISBN'},
            value[2], {'identifier': value[2], 'scheme': 'ISSN'},
        ),
    ) + item_volume_issue_parsed)


def parse_item_issue(text: str):
    dict_ = {
        "Roč. 22, č. 2 (2011)": {"itemVolume": "22", "itemIssue": "2", "itemYear": "2011"},
        "2008": {"itemYear": "2008"},
        "Roč. 19 (2013)": {"itemVolume": "19", "itemYear": "2013"},
        "Roč. 2016": {"itemYear": "2016"},
        "roč. 2, č. 2, s. 76-86": {
            "itemVolume": "2", "itemIssue": "2", "itemStartPage": "76", "itemEndPage": "86"
        }
    }
    return dict_.get(text)


@matches('85640u', '85640z', paired=True)
def transform_85640_original_record_url(md, rec, value):
    if value[1] == "Odkaz na původní záznam":
        md['originalRecord'] = value[0]
        # TODO: pokud je to handle (tzn. hdl.handle.net substring), tak dat i do objectIdentifiers se scheme Handle


@matches('85642u')
def transform_85642_external_location(md, rec, value):
    md['externalLocation'] = {
        'externalLocationURL': value
    }


@matches('970__a')
def transform_970_catalogue_sysno(md, rec, value):
    md.setdefault('systemIdentifiers', []).append({
        'identifier': value,
        'scheme': 'catalogueSysNo'
    })


@matches('980__a')
def transform_980_resource_type(md, rec, value):
    # TODO: taxonomie
    if value == "metodiky":
        if "336__" not in rec:
            value = 'methodologies-without-certification'

    md["resourceType"] = {
        "bakalarske_prace": "Bakalářská práce",
        "diplomove_prace": "Diplomová práce",
        "disertacni_prace": "Rigorózní práce",
        "rigorozni_prace": "Disertační práce",
        "habilitacni_prace": "Habilitační práce"
    }.get(value, value)


@matches('996__a', '996__b', '996__9', paired=True)
def transform_996_accessibility(md, rec, value):
    md['accessibility'] = make_array(
        value[0], {'lang': 'cs', 'value': value[0]},
        value[1], {'lang': 'en', 'value': value[1]},
    )
    if value[0]:
        md['accessRights'] = get_access_rights(text=value[0])
    else:
        md['accessRights'] = get_access_rights(slug=value[2] or "c_abf2")


access_right_dict = {
    "0": "c_14cb",  # pouze metadata
    "1": "c_abf2",  # open
    "2": "c_16ec"  # omezeny
}


def get_access_rights(text=None, slug=None):
    if not slug:
        sentence_dict = {
            "Dokument je dostupný v repozitáři Akademie věd.": "1",
            "Dokumenty jsou dostupné v systému NK ČR.": "1",
            "Plný text je dostupný v Digitální knihovně VUT.": "1",
            "Dostupné v digitálním repozitáři VŠE.": "1",
            "Plný text je dostupný v digitálním repozitáři JČU.": "1",
            "Dostupné v digitálním repozitáři UK.": "1",
            "Dostupné v digitálním repozitáři Mendelovy univerzity.": "1",
            "Dostupné v repozitáři ČZU.": "1",
            "Dostupné registrovaným uživatelům v digitálním repozitáři AMU.": "2",
            "Dokument je dostupný v NLK. Dokument je dostupný též v digitální formě v Digitální "
            "knihovně NLK. Přístup může být vázán na prohlížení z počítačů NLK.": "2",
            "Dostupné v digitálním repozitáři UK (pouze z IP adres univerzity).": "2",
            "Text práce je neveřejný, pro více informací kontaktujte osobu uvedenou v repozitáři "
            "Mendelovy univerzity.": "2",
            "Dokument je dostupný na vyžádání prostřednictvím repozitáře Akademie věd.": "2",
            "Dokument je dostupný v příslušném ústavu Akademie věd ČR.": "0",
            "Dokument je po domluvě dostupný v budově Ministerstva životního prostředí.": "0",
            "Plný text není k dispozici.": "0",
            "Dokument je dostupný v NLK.": "0",
            'Dokument je po domluvě dostupný v budově <a '
            'href=\"http://www.mzp.cz/__C125717D00521D29.nsf/index.html\" '
            'target=\"_blank\">Ministerstva životního prostředí</a>.': "0",
            "Dostupné registrovaným uživatelům v knihovně Mendelovy univerzity v Brně.": "2",
            'Dostupné registrovaným uživatelům v repozitáři ČZU.': "2",
            'Dokument je dostupný na externích webových stránkách.': "0",
        }

        slug = access_right_dict.get(sentence_dict.get(text, "0"))

    return {
        'c_abf2': 'otevřený přístup',
        'c_f1cf': 'odložené zpřístupnění',
        'c_16ec': 'omezený přístup',
        'c_14cb': 'pouze metadata'
    }.get(slug, slug)  # TODO: taxonomy


@matches('999C1a')
def transform_999C1_funding_reference(md, rec, val):
    md.setdefault('fundingReferences', []).append(make_dict(
        "projectID", val,
        "funder", get_funder_from_id(val)
    ))


def get_funder_from_id(funder_id: str):
    # TODO: prohnat jeste "taxonomii funderu, aby tady byl nazev v cestine, ne slug
    dict_ = {
        "1A": "MZ0",
        "1B": "MZE",
        "1C": "MZP",
        "1D": "MZP",
        "1E": "AV0",
        "1F": "MD0",
        "1G": "MZE",
        "1H": "MPO",
        "1I": "MZP",
        "1J": "MPS",
        "1K": "MSM",
        "1L": "MSM",
        "1M": "MSM",
        "1N": "MSM",
        "1P": "MSM",
        "1Q": "AV0",
        "1R": "MZE",
        "2A": "MPO",
        "2B": "MSM",
        "2C": "MSM",
        "2D": "MSM",
        "2E": "MSM",
        "2F": "MSM",
        "2G": "MSM",
        "7A": "MSM",
        "7B": "MSM",
        "7C": "MSM",
        "7D": "MSM",
        "7E": "MSM",
        "7F": "MSM",
        "7G": "MSM",
        "7H": "MSM",
        "8A": "MSM",
        "8B": "MSM",
        "8C": "MSM",
        "8D": "MSM",
        "8E": "MSM",
        "8F": "MSM",
        "8G": "MSM",
        "8H": "MSM",
        "8I": "MSM",
        "8J": "MSM",
        "8X": "MSM",
        "AA": "CBU",
        "AB": "CBU",
        "BI": "BIS",
        "CA": "MD0",
        "CB": "MD0",
        "CC": "MD0",
        "CD": "MI0",
        "CE": "MD0",
        "CF": "MI0",
        "CG": "MD0",
        "CI": "MD0",
        "CK": "TA0",
        "DA": "MK0",
        "DB": "MK0",
        "DC": "MK0",
        "DD": "MK0",
        "DE": "MK0",
        "DF": "MK0",
        "DG": "MK0",
        "DH": "MK0",
        "DM": "MK0",
        "EA": "MPO",
        "EB": "MPO",
        "EC": "MPO",
        "ED": "MSM",
        "EE": "MSM",
        "EF": "MSM",
        "EG": "MPO",
        "EP": "MZE",
        "FA": "MPO",
        "FB": "MPO",
        "FC": "MPO",
        "FD": "MPO",
        "FE": "MPO",
        "FF": "MPO",
        "FI": "MPO",
        "FR": "MPO",
        "FT": "MPO",
        "FV": "MPO",
        "FW": "TA0",
        "FX": "MPO",
        "GA": "GA0",
        "GB": "GA0",
        "GC": "GA0",
        "GD": "GA0",
        "GE": "GA0",
        "GF": "GA0",
        "GH": "GA0",
        "GJ": "GA0",
        "GK": "MK0",
        "GM": "GA0",
        "GP": "GA0",
        "GS": "GA0",
        "GV": "GA0",
        "GX": "GA0",
        "HA": "MPS",
        "HB": "MPS",
        "HC": "MPS",
        "HR": "MPS",
        "HS": "MPS",
        "IA": "AV0",
        "IB": "AV0",
        "IC": "AV0",
        "ID": "MSM",
        "IE": "MZE",
        "IN": "MSM",
        "IP": "AV0",
        "IS": "MSM",
        "IZ": "MZ0",
        "JA": "SUJ",
        "JB": "SUJ",
        "JC": "SUJ",
        "KA": "AV0",
        "KJ": "AV0",
        "KK": "MK0",
        "KS": "AV0",
        "KZ": "MK0",
        "LA": "MSM",
        "LB": "MSM",
        "LC": "MSM",
        "LD": "MSM",
        "LE": "MSM",
        "LF": "MSM",
        "LG": "MSM",
        "LH": "MSM",
        "LI": "MSM",
        "LJ": "MSM",
        "LK": "MSM",
        "LL": "MSM",
        "LM": "MSM",
        "LN": "MSM",
        "LO": "MSM",
        "LP": "MSM",
        "LQ": "MSM",
        "LR": "MSM",
        "LS": "MSM",
        "LT": "MSM",
        "LZ": "MSM",
        "ME": "MSM",
        "MH": "MH0",
        "MI": "URV",
        "MJ": "URV",
        "MO": "MO0",
        "MP": "MPO",
        "MR": "MZP",
        "NA": "MZ0",
        "NB": "MZ0",
        "NC": "MZ0",
        "ND": "MZ0",
        "NE": "MZ0",
        "NF": "MZ0",
        "NG": "MZ0",
        "NH": "MZ0",
        "NI": "MZ0",
        "NJ": "MZ0",
        "NK": "MZ0",
        "NL": "MZ0",
        "NM": "MZ0",
        "NN": "MZ0",
        "NO": "MZ0",
        "NR": "MZ0",
        "NS": "MZ0",
        "NT": "MZ0",
        "NU": "MZ0",
        "NV": "MZ0",
        "OB": "MO0",
        "OC": "MSM",
        "OD": "MO0",
        "OE": "MSM",
        "OF": "MO0",
        "OK": "MSM",
        "ON": "MO0",
        "OP": "MO0",
        "OR": "MO0",
        "OS": "MO0",
        "OT": "MO0",
        "OU": "MSM",
        "OV": "MO0",
        "OW": "MO0",
        "OY": "MO0",
        "PD": "MD0",
        "PE": "MH0",
        "PG": "MSM",
        "PI": "MH0",
        "PK": "MK0",
        "PL": "MZ0",
        "PO": "MH0",
        "PR": "MPO",
        "PT": "MH0",
        "PV": "MSM",
        "PZ": "MH0",
        "QA": "MZE",
        "QB": "MZE",
        "QC": "MZE",
        "QD": "MZE",
        "QE": "MZE",
        "QF": "MZE",
        "QG": "MZE",
        "QH": "MZE",
        "QI": "MZE",
        "QJ": "MZE",
        "QK": "MZE",
        "RB": "MZV",
        "RC": "MS0",
        "RD": "MS0",
        "RE": "MZE",
        "RH": "MH0",
        "RK": "MK0",
        "RM": "MZV",
        "RN": "MV0",
        "RO": "MO0",
        "RP": "MPO",
        "RR": "MZP",
        "RS": "MSM",
        "RV": "MPS",
        "RZ": "MZ0",
        "SA": "MZP",
        "SB": "MZP",
        "SC": "MZP",
        "SD": "MZP",
        "SE": "MZP",
        "SF": "MZP",
        "SG": "MZP",
        "SH": "MZP",
        "SI": "MZP",
        "SJ": "MZP",
        "SK": "MZP",
        "SL": "MZP",
        "SM": "MZP",
        "SN": "MZP",
        "SP": "MZP",
        "SS": "TA0",
        "ST": "NBU",
        "SU": "NBU",
        "SZ": "MZP",
        "TA": "TA0",
        "TB": "TA0",
        "TC": "MPO",
        "TD": "TA0",
        "TE": "TA0",
        "TF": "TA0",
        "TG": "TA0",
        "TH": "TA0",
        "TI": "TA0",
        "TJ": "TA0",
        "TK": "TA0",
        "TL": "TA0",
        "TM": "TA0",
        "TN": "TA0",
        "TO": "TA0",
        "TP": "TA0",
        "TR": "MPO",
        "UA": "KUL",
        "UB": "KHK",
        "UC": "KHK",
        "UD": "KLI",
        "UE": "KKV",
        "UF": "KHP",
        "UH": "KHP",
        "US": "MV0",
        "VA": "MV0",
        "VD": "MV0",
        "VE": "MV0",
        "VF": "MV0",
        "VG": "MV0",
        "VH": "MV0",
        "VI": "MV0",
        "VJ": "MV0",
        "VS": "MSM",
        "VV": "MSM",
        "VZ": "MSM",
        "WA": "MMR",
        "WB": "MMR",
        "WD": "MMR",
        "WE": "MMR",
        "YA": "MI0",
        "ZK": "CUZ",
        "ZO": "MZP",
        "ZZ": "MZP",
        "GN": "GA0",
        "LU": "MSM",
        "LX": "MSM",
        "MC": "MSM",
        "MS": "MSM",
        "VB": "MV0",
        "VC": "MV0",
    }
    if not funder_id:
        return None

    id_prefix = funder_id[:2]
    slug = dict_.get(id_prefix)
    return slug  # TODO: taxonomyalp


@matches('04107a', '04107b')
def transform_04107_language(md, rec, value):
    # TODO: taxonomy
    try:
        md.setdefault('languages', []).append(get_alpha2_lang(value))
    except LookupError:
        raise Exception(f'Bad language {value} - no alpha2 equivalent')

@matches('336__a')
def transform_336_certifikovana_metodika(md, rec, value):
    # TODO: taxonomy
    md["resourceType"] = 'certified-methodologies'


@matches('540__a', '540__9', paired=True)
def transform_540_rights(md, rec, value):
    if value[1] != 'cze':
        return
    rights = value[0]
    # TODO: pozdeji rights = parse_rights(value[0])
    if rights:
        md.setdefault('rights', []).append(rights)


rights_dict = {
    # 'Dílo je chráněno podle autorského zákona č. 121/2000 Sb.': 'copyright', # vyhozeno, protoze uz neni ve slovniku
    # 'Text je chráněný podle autorského zákona č. 121/2000 Sb.': 'copyright', # vyhozeno, protoze uz neni ve slovniku
    'Licence Creative Commons Uveďte autora 3.0 Česko': '3-BY-CZ',
    'Licence Creative Commons Uveďte autora-Neužívejte dílo komerčně 3.0 Česko': '3-BY-NC-CZ',
    'Licence Creative Commons Uveďte autora-Neužívejte dílo komerčně-Nezasahujte do díla 3.0 '
    'Česko': '3-BY-NC-ND-CZ',
    'Licence Creative Commons Uveďte autora-Neužívejte dílo komerčně-Zachovejte licenci 3.0 '
    'Česko': '3-BY-NC-SA-CZ',
    'Licence Creative Commons Uveďte autora-Nezasahujte do díla 3.0 Česko': '3-BY-ND-CZ',
    'Licence Creative Commons Uveďte autora-Zachovejte licenci 3.0 Česko': '3-BY-SA-CZ',
    'Licence Creative Commons Uveďte původ 4.0': '4-BY',
    'Licence Creative Commons Uveďte původ-Neužívejte komerčně-Nezpracovávejte 4.0':
        '4-BY-NC-ND',
    'Licence Creative Commons Uveďte původ-Neužívejte komerčně-Zachovejte licenci 4.0':
        '4-BY-NC-SA',
    'Licence Creative Commons Uveďte původ-Zachovejte licenci 4.0': '4-BY-SA',
}


def parse_rights(text):
    license = rights_dict.get(text)
    if not license:
        return
    return license.replace("-", "_").lower()  # TODO: taxonomy


def transform_oai_identifier(md, rec):
    md.setdefault('systemIdentifiers', []).append({
        'identifier': rec.identifier,
        'scheme': 'nuslOAI'  # TODO: pridat to do modelu !!!
    })


@matches('502__c')
def transform_502_degree_grantor(md, rec, value):
    md.setdefault('degreeGrantor', []).append(value)


@matches('7102_a', '7102_b', '7102_g', '7102_9', paired=True)
def transform_7102_degree_grantor(md, rec, value):
    if value[3] != 'cze':
        return
    if value[1] and value[1].startswith('Program '):
        md.setdefault('studyFields', []).extend(value[1][len('Program '):])

    md.setdefault('degreeGrantor', []).extend(
        make_array(
            value[0], value[0],
            value[1] and not value[1].startswith('Program '), value[1],
            value[2], value[2]
        )
    )


@matches('586__a')
def transform_586_defended(md, rec, value):
    if value == 'obhájeno':
        md['defended'] = True


@matches('656_7a')
def transform_656_study_field(md, rec, value):
    value = [x.strip() for x in value.split('/')]
    value = [x for x in value if x]
    md.setdefault('studyFields', []).extend(value)


@matches('998__a')
def transform_998_collection(md, rec, value):
    md['collection'] = {
        "univerzita_karlova_v_praze": "Univerzita Karlova",
        "vutbr": "Vysoké učení technické v Brně",
        "vysoka_skola_ekonomicka_v_praze": "Vysoká škola ekonomická v Praze",
        "jihoceska_univerzita_v_ceskych_budejovicich": "Jihočeská univerzita v Českých Budějovicích",
        "mendelova_univerzita_v_brne": "Mendelova univerzita v Brně",
        "ceska_zemedelska_univerzita": "Česká zemědělská univerzita v Praze",
        "akademie_muzickych_umeni_v_praze": "Akademie múzických umění v Praze"
    }.get(value, value)


@matches('502__a')
def transform_502_date_defended(md, rec, value):
    md['dateDefended'] = value
