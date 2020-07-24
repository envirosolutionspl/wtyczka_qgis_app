initialValues = {
    # "lokalnyId" : "RYS1",
    # "przestrzenNazw" : "PL.ZIPPZP.9999/14-PZPW"
}
placeholders = {
    "RysunekAktuPlanowniaPrzestrzenegoType:lokalnyId" : "RYS1",
    "RysunekAktuPlanowniaPrzestrzenegoType:przestrzenNazw" : "PL.ZIPPZP.9999/14-PZPW",
    "RysunekAktuPlanowniaPrzestrzenegoType:wersjaId" : "20200525",
    "RysunekAktuPlanowniaPrzestrzenegoType:tytul" : "Plan zagospodarowania przestrzennego województwa mazowieckiego Stan zagospodarowania",
    "RysunekAktuPlanowniaPrzestrzenegoType:lacze" : "http://www.przykladowa.domena/zagospodarowanie.tif",
    "RysunekAktuPlanowniaPrzestrzenegoType:legenda" : "http://www.przykladowa.domena/legenda.png",
    "RysunekAktuPlanowniaPrzestrzenegoType:rozdzielczoscPrzestrzenna" : "250000",
    "RysunekAktuPlanowniaPrzestrzenegoType:opis" : "Zał. 2 stan zagospodarowania",
    "AktPlanowaniaPrzestrzennegoType:lokalnyId" : "P1",
    "AktPlanowaniaPrzestrzennegoType:przestrzenNazw" : "PL.ZIPPZP.9999/14-PZPW",
    "AktPlanowaniaPrzestrzennegoType:wersjaId" : "20200525",
    "AktPlanowaniaPrzestrzennegoType:tytul" : "Plan zagospodarowania przestrzennego województwa mazowieckiego",
    "AktPlanowaniaPrzestrzennegoType:zmiana" : "0",
    "AktPlanowaniaPrzestrzennegoType:referencja" : "Plan zagospodarowania przestrzennego województwa mazowieckiego został sporządzony na podkładzie Bazy Danych Obiektów Ogólnogeograficznych (BDOO).",
    "AktPlanowaniaPrzestrzennegoType:lacze" : "http://mapy.geoportal.gov.pl/wss/service/ATOM/httpauth/atom/CODGIK_BDOO",
    "DokumentFormalnyType:lokalnyId" : "DOC1",
    "DokumentFormalnyType:przestrzenNazw" : "PL.ZIPPZP.9999/14-PZPW",
    "DokumentFormalnyType:wersjaId" : "20200525",
    "DokumentFormalnyType:tytul" : "Uchwała nr 22/18 Sejmiku Wojewodztwa Mazowieckiego z dnia 19 grudnia 2018r. w sprawie Planu zagospodarowania przestrzennego województwa mazowieckiego",
    "DokumentFormalnyType:nazwaSkrocona" : "Plan zagospodarowania przestrzennego województwa mazowieckiego",
    "DokumentFormalnyType:numerIdentyfikacyjny" : "DZ. URZ. WOJ. 2018.13180",
    "DokumentFormalnyType:organUstanawiajacy" : "Sejmik Wojewodztwa Mazowieckiego",
    "DokumentFormalnyType:lacze" : "http://www.przykladowa.domena/akt.pdf"
}

# listy rozwijalne combobox

nilReasons = {
        "inapplicable": "inapplicable",
        "missing": "missing",
        "template": "template",
        "unknown": "unknown",
        "withheld": "withheld"}
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
# słownik definiujący relacje między "typPlanu", a "poziomHierarchii"
typyPlanuPoziomyHierarchii = dict(zip(typyPlanu.keys(),[
    [list(poziomyHierarchii.keys())[2] ,list(poziomyHierarchii.keys())[1]],
    [list(poziomyHierarchii.keys())[0]],
    [list(poziomyHierarchii.keys())[1]],
    [list(poziomyHierarchii.keys())[2]],
    [list(poziomyHierarchii.keys())[2]]
]))
statusListaKodowa = {
    "nieaktualny" : "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/obsolete",
    "prawnie wiążący lub realizowany" : "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/legalForce",
    "w opracowaniu" : "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/elaboration",
    "w trakcie przyjmowania" : "http://inspire.ec.europa.eu/codelist/ProcessStepGeneralValue/adoption"
}
dziennikUrzedowyKod = {
    "Dziennik Ustaw" : "dziennikUstaw",
    "Monitor Polski" : "monitorPolski",
    "Dziennik urzędowy organu władzy państwowej" : "dziennikResortowy",
    "Dziennik Urzędowy Unii Europejskiej" : "dziennikUrzedowyUniiEuropejskiej",
    "Dziennik Urzędowy Woj. Dolnośląskiego" : "dziennikUrzedowyWojDolnoslaskiego",
    "Dziennik Urzędowy Woj. Kujawsko-Pomorskiego" : "dziennikUrzedowyWojKujawskoPomorskiego",
    "Dziennik Urzędowy Woj. Lubelskiego" : "dziennikUrzedowyWojLubelskiego",
    "Dziennik Urzędowy Woj. Lubuskiego" : "dziennikUrzedowyWojLubuskiego",
    "Dziennik Urzędowy Woj. Łódzkiego" : "dziennikUrzedowyWojLodzkiego",
    "Dziennik Urzędowy Woj. Małopolskiego" : "dziennikUrzedowyWojMalopolskiego",
    "Dziennik Urzędowy Woj. Mazowieckiego" : "dziennikUrzedowyWojMazowieckiego",
    "Dziennik Urzędowy Woj. Opolskiego" : "dziennikUrzedowyWojOpolskiego",
    "Dziennik Urzędowy Woj. Podkarpackiego" : "dziennikUrzedowyWojPodkarpackiego",
    "Dziennik Urzędowy Woj. Podlaskiego" : "dziennikUrzedowyWojPodlaskiego",
    "Dziennik Urzędowy Woj. Pomorskiego" : "dziennikUrzedowyWojPomorskiego",
    "Dziennik Urzędowy Woj. Śląskiego" : " dziennikUrzedowyWojSlaskiego",
    "Dziennik Urzędowy Woj. Świętokrzyskiego" : "dziennikUrzedowyWojSwietokrzyskiego",
    "Dziennik Urzędowy Woj. Warmińsko-Mazurskiego" : "dziennikUrzedowyWojWarminskoMazurskiego",
    "Dziennik Urzędowy Woj. Wielkopolskiego" : "dziennikUrzedowyWojWielkopolskiego",
    "Dziennik Urzędowy Woj. Zachodniopomorskiego" : "dziennikUrzedowyWojZachodniopomorskiego"
}
cI_DateTypeCode = {
    "utworzenie": "creation",
    "publikacja": "publication",
    "rewizja": "revision"
}