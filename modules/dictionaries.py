# -*- coding: utf-8 -*-
from PyQt5.QtCore import QDateTime
initialValues = {
    "lokalnyId": "RYS1",
    "przestrzenNazw": "PL.ZIPPZP.9999/14-PZPW"
}
placeholders = {
    "RysunekAktuPlanowaniaPrzestrzennegoType:lokalnyId": "121_Rys1 LUB np. XXVI.49.2010_Rys1",
    "RysunekAktuPlanowaniaPrzestrzennegoType:przestrzenNazw": "PL.ZIPPZP.2481/206101-MPZP",
    "RysunekAktuPlanowaniaPrzestrzennegoType:wersjaId": "20200630T223418",
    "RysunekAktuPlanowaniaPrzestrzennegoType:tytul": "Plan zagospodarowania przestrzennego województwa mazowieckiego Stan zagospodarowania",
    "RysunekAktuPlanowaniaPrzestrzennegoType:lacze": "http://www.przykladowa.domena/zagospodarowanie.tif",
    "RysunekAktuPlanowaniaPrzestrzennegoType:legenda": "http://www.przykladowa.domena/legenda.png",
    "RysunekAktuPlanowaniaPrzestrzennegoType:rozdzielczoscPrzestrzenna": "2000",
    "RysunekAktuPlanowaniaPrzestrzennegoType:opis": "Zał. 2 stan zagospodarowania",
    "AktPlanowaniaPrzestrzennegoType:lokalnyId": "121_P1 LUB np. XXVI.49.2010_P1",
    "AktPlanowaniaPrzestrzennegoType:przestrzenNazw": "PL.ZIPPZP.2481/206101-MPZP",
    "AktPlanowaniaPrzestrzennegoType:wersjaId": "20200630T223418",
    "AktPlanowaniaPrzestrzennegoType:tytul": "Plan zagospodarowania przestrzennego województwa mazowieckiego",
    "AktPlanowaniaPrzestrzennegoType:zmiana": "0",
    "AktPlanowaniaPrzestrzennegoType:referencja": "Plan zagospodarowania przestrzennego województwa mazowieckiego został sporządzony na podkładzie Bazy Danych Obiektów Ogólnogeograficznych (BDOO).",
    "AktPlanowaniaPrzestrzennegoType:lacze": "http://mapy.geoportal.gov.pl/wss/service/ATOM/httpauth/atom/CODGIK_BDOO",
    "DokumentFormalnyType:lokalnyId": "121_Doc1 LUB np. XXVI.49.2010_Doc1",
    "DokumentFormalnyType:przestrzenNazw": "PL.ZIPPZP.2481/206101-MPZP",
    # "DokumentFormalnyType:wersjaId": "20200630T223418",
    "DokumentFormalnyType:tytul": "Uchwała nr 22/18 Sejmiku Województwa Mazowieckiego z dnia 19 grudnia 2018r. w sprawie Planu zagospodarowania przestrzennego województwa mazowieckiego",
    "DokumentFormalnyType:nazwaSkrocona": "Plan zagospodarowania przestrzennego województwa mazowieckiego",
    "DokumentFormalnyType:numerIdentyfikacyjny": "DZ. URZ. WOJ. 2018.13180",
    "DokumentFormalnyType:organUstanawiajacy": "Sejmik Województwa Mazowieckiego",
    "DokumentFormalnyType:lacze": "http://www.przykladowa.domena/akt.pdf"
}

# listy rozwijalne combobox

nilReasons = {
    "inapplicable": "inapplicable",
    "missing": "missing",
    "template": "template",
    "unknown": "unknown",
    "withheld": "withheld"
}
ukladyOdniesieniaPrzestrzennego = {
    "PL-1992": "http://www.opengis.net/def/crs/EPSG/0/2180",
    "PL-2000(5)": "http://www.opengis.net/def/crs/EPSG/0/2176",
    "PL-2000(6)": "http://www.opengis.net/def/crs/EPSG/0/2177",
    "PL-2000(7)": "http://www.opengis.net/def/crs/EPSG/0/2178",
    "PL-2000(8)": "http://www.opengis.net/def/crs/EPSG/0/2179"
}
typyPlanu = {
    "miejscowy plan zagospodarowania przestrzennego": "miejscowyPlanZagospodarowaniaPrzestrzennego",
    "plan zagospodarowania przestrzennego województwa": "planZagospodarowaniaPrzestrzennegoWojewodztwa",
    "studium uwarunkowań i kier. zagosp. przestrz. gminy": "studiumUwarunkowanIKierunkowZagospodarowaniaPrzestrzennegoGminy",
    "miejscowy plan odbudowy": "miejscowyPlanOdbudowy",
    "miejscowy plan rewitalizacji": "miejscowyPlanRewitalizacji"
}

poziomyHierarchii = {
    "regionalny": "http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue/regional",
    "lokalny": "http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue/local",
    "sublokalny": "http://inspire.ec.europa.eu/codelist/LevelOfSpatialPlanValue/infraLocal"
}
metadataKeywordAnchors = {
    'regionalnym': "https://inspire.ec.europa.eu/metadata-codelist/SpatialScope/regional",
    'lokalne': "https://inspire.ec.europa.eu/metadata-codelist/SpatialScope/local",
    'zagospodarowanie przestrzenne': "http://inspire.ec.europa.eu/theme/lu",
    'Brak warunków dostępu i użytkowania': "http://inspire.ec.europa.eu/metadata-codelist/ConditionsApplyingToAccessAndUse/noConditionsApply"
}
zgodnoscAnchors = {
    'Zgodny (conformant)': 'http://inspire.ec.europa.eu/metadata-codelist/DegreeOfConformity/conformant',
    'Niezgodny (notConformant)': 'http://inspire.ec.europa.eu/metadata-codelist/DegreeOfConformity/notConformant',
    'Brak oceny zgodności (notEvaluated)': 'http://inspire.ec.europa.eu/metadata-codelist/DegreeOfConformity/notEvaluated'
}

# słownik definiujący relacje między "typPlanu", a "poziomHierarchii"
typyPlanuPoziomyHierarchii = dict(zip(typyPlanu.keys(), [
    [list(poziomyHierarchii.keys())[2], list(poziomyHierarchii.keys())[1]],
    [list(poziomyHierarchii.keys())[0]],
    [list(poziomyHierarchii.keys())[1]],
    [list(poziomyHierarchii.keys())[2]],
    [list(poziomyHierarchii.keys())[2]]
]))
statusListaKodowa = {
    "nieaktualny": "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/obsolete",
    "prawnie wiążący lub realizowany": "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/legalForce",
    "w opracowaniu": "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/elaboration",
    "w trakcie przyjmowania": "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/adoption"
}
dziennikUrzedowyKod = {
    "Dziennik Ustaw": "dziennikUstaw",
    "Monitor Polski": "monitorPolski",
    "Dziennik urzędowy organu władzy państwowej": "dziennikResortowy",
    "Dziennik Urzędowy Unii Europejskiej": "dziennikUrzedowyUniiEuropejskiej",
    "Dziennik Urzędowy Woj. Dolnośląskiego": "dziennikUrzedowyWojDolnoslaskiego",
    "Dziennik Urzędowy Woj. Kujawsko-Pomorskiego": "dziennikUrzedowyWojKujawskoPomorskiego",
    "Dziennik Urzędowy Woj. Lubelskiego": "dziennikUrzedowyWojLubelskiego",
    "Dziennik Urzędowy Woj. Lubuskiego": "dziennikUrzedowyWojLubuskiego",
    "Dziennik Urzędowy Woj. Łódzkiego": "dziennikUrzedowyWojLodzkiego",
    "Dziennik Urzędowy Woj. Małopolskiego": "dziennikUrzedowyWojMalopolskiego",
    "Dziennik Urzędowy Woj. Mazowieckiego": "dziennikUrzedowyWojMazowieckiego",
    "Dziennik Urzędowy Woj. Opolskiego": "dziennikUrzedowyWojOpolskiego",
    "Dziennik Urzędowy Woj. Podkarpackiego": "dziennikUrzedowyWojPodkarpackiego",
    "Dziennik Urzędowy Woj. Podlaskiego": "dziennikUrzedowyWojPodlaskiego",
    "Dziennik Urzędowy Woj. Pomorskiego": "dziennikUrzedowyWojPomorskiego",
    "Dziennik Urzędowy Woj. Śląskiego": " dziennikUrzedowyWojSlaskiego",
    "Dziennik Urzędowy Woj. Świętokrzyskiego": "dziennikUrzedowyWojSwietokrzyskiego",
    "Dziennik Urzędowy Woj. Warmińsko-Mazurskiego": "dziennikUrzedowyWojWarminskoMazurskiego",
    "Dziennik Urzędowy Woj. Wielkopolskiego": "dziennikUrzedowyWojWielkopolskiego",
    "Dziennik Urzędowy Woj. Zachodniopomorskiego": "dziennikUrzedowyWojZachodniopomorskiego"
}
cI_DateTypeCode = {
    "utworzenie": "creation",
    "publikacja": "publication",
    "przegląd": "revision"
}
languages = {
    "polski": "pol",
    "angielski": "eng"
}
licznoscMetadataFields = {
    "e1": '1',
    "e2": '1',
    "e3": '1',
    "e4": '1+',
    "e5": '1+',
    "e6": '1+',
    "e7": '0+',
    "e8": '1',
    "e9": '4+',
    "e10": '01',
    "e11": '1+',
    "e12": '1+',
    "e13": '1',
    "e14": '01',
    "e15": '1',
    "e16": '1+',
    "e17": '2',
    "e18": '4+',
    "e19": '1',
    "e20": '1+',
    "e21": '1',
    "e22": '1+',
    "e23": '1',
    "e24": '1+',
    "e25": '1',
    "e26": '1',
    "e27": '1+',
    "e28": '1',
    "e29": '1+',
    "e30": '1',
    "e31": '1',
    "e32": '1',
    "e33": '1',
    "e34": '1'
}

nazwyMetadataFields = {
    "e1": 'Tytuł zbioru danych przestrzennych',
    "e2": 'Streszczenie',
    "e3": 'Typ zbioru danych przestrzennych',
    "e4": 'Adres zbioru danych przestrzennych',
    "e5": 'Unikalny identyfikator zbioru danych przestrzennych',
    "e6": 'Język zbioru danych przestrzennych',
    "e7": 'Kodowanie znaków',
    "e8": 'Kategoria tematyczna',
    "e9": 'Wartość słowa kluczowego',
    "e10": 'Standardowy słownik źródłowy',
    "e11": 'Geograficzny prostokąt ograniczający',
    "e12": 'System odniesienia za pomocą współrzędnych',
    "e13": 'Data utworzenia',
    "e14": 'Data opublikowania',
    "e15": 'Pochodzenie',
    "e16": 'Rozdzielczość przestrzenna',
    "e17": 'Typ reprezentacji przestrzennej',
    "e18": 'Specyfikacja',
    "e19": 'Stopień',
    "e20": 'Warunki dotyczące dostępu i użytkowania',
    "e21": 'Ograniczenia w publicznym dostępie',
    "e22": 'Jednostka odpowiedzialna',
    "e23": 'Rola jednostki odpowiedzialnej',
    "e24": 'Nazwa formatu',
    "e25": 'Wersja formatu',
    "e26": 'Częstotliwość aktualizacji',
    "e27": 'Informacja o szczegółowych wymaganiach dotyczących utrzymania',
    "e28": 'Zakres danych',
    "e29": 'Punkt kontaktowy metadanych',
    "e30": 'Data metadanych',
    "e31": 'Język metadanych',
    "e32": 'Unikalny identyfikator rekordu (pliku) metadanych',
    "e33": 'Standard metadanych',
    "e34": 'Standard metadanych'
}
# domyślne zmienne wartości dla pól wielokrotnych
metadataListWidgetsDefaultItems = {
    'e6': [{'e6_cmbbx': 'polski'}],
    'e9': [
        {
            'e9_lineEdit': 'Zagospodarowanie przestrzenne',
            'e10_cmbbx': 'Data opublikowania',
            'e10_dateTimeEdit': QDateTime(2008, 6, 1, 0, 0),
            'e10_lineEdit': 'GEMET - INSPIRE themes, version 1.0',
            'xlink': "http://www.eionet.europa.eu/gemet/inspire_themes"
        },
        {
            'e9_lineEdit': 'PlannedLandUse',
            'e10_cmbbx': None,
            'e10_dateTimeEdit': None,
            'e10_lineEdit': '',
            'xlink': None
        }
    ],
    'e17': [{'e17_lineEdit': 'wektor'}, {'e17_lineEdit': 'raster'}],
    'e20': [{'e20_lineEdit': 'Brak warunków dostępu i użytkowania'}],
}

relacjeDokumentu = {
    'przystąpienie': 'przystapienie',
    'uchwala': 'uchwala',
    'zmienia': 'zmienia',
    'uchyla': 'uchyla',
    'unieważnia': 'uniewaznia',
    'inna': ''
}

relacjeDokumentuZApp = {
    'przystapienie': 'dokumentPrzystepujacy',
    'uchwala': 'dokumentUchwalajacy',
    'zmienia': 'dokumentZmieniajacy',
    'uchyla': 'dokumentUchylajacy',
    'uniewaznia': 'dokumentUniewazniajacy',
    '': 'dokument'
}

rodzajeZbiorow = {
    '': '',
    'PZPW': 'PZPW',
    'SUIKZP': 'SUIKZP',
    'MPZP': 'MPZP'
}

nameSpaces = {
    'xsi': "http://www.w3.org/2001/XMLSchema",
    'app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0",
    'gmd': "http://www.isotc211.org/2005/gmd",
    'gco': 'http://www.isotc211.org/2005/gco',
    'xlink': 'http://www.w3.org/1999/xlink',
    'gml': "http://www.opengis.net/gml/3.2",
    'wfs': 'http://www.opengis.net/wfs/2.0',
    'gmlexr': "http://www.opengis.net/gml/3.3/exr"
}

xmlNameSpaces = {
    'xmlns:gco': "http://www.isotc211.org/2005/gco",
    'xmlns:gmd': "http://www.isotc211.org/2005/gmd",
    'xmlns:gml': "http://www.opengis.net/gml/3.2",
    'xmlns:wfs': "http://www.opengis.net/wfs/2.0",
    'xmlns:xlink': "http://www.w3.org/1999/xlink",
    'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'xmlns:app': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0",
    'xsi:schemaLocation': "https://www.gov.pl/static/zagospodarowanieprzestrzenne/schemas/app/1.0/planowaniePrzestrzenne.xsd http://www.opengis.net/gml/3.2 http://schemas.opengis.net/gml/3.2.1/gml.xsd http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
}
