from models import db, Camapign
from app import app

kampanie = {
    "Wiosenny_Rabat":["sell", "kred",True,"Piotr"],
    "Zimowa_Promocja":["act", "dep", False,"Andrzej"],
    "Black_Friday_2024":["ret", "dep",True],
    "Cyber_Monday_Sale":["ret", "kred", False],
    "Letnia_Wyprzedaż":["act", "kred",True,"Piotr"],
    "Noworoczna_Oferta":["sell", "kred",True,"Krzysiek"],
    "Dni_Otwarte":["act", "dep",True],
    "Świąteczne_Rabaty":["ret", "kred", False],
    "Powrót_do_Szkoły":["act", "dep",True,"Asia"],
    "Długi_Weekend_Promocja":["ret", "kred",True],
    "Tydzień_Super_Ofert":["act", "kred",True],
    "Happy_Hour_Rabaty":["act", "kred",True],
    "Urodziny_Sklepu":["act", "dep", False],
    "Wielkanocne_Rabaty":["sell", "kred",True],
    "Jesienna_Wyprzedaż":["ret", "kred",True],
    "Ekspresowe_Promocje":["sell", "kred",True],
    "Prezent_na_Walentynki":["act", "dep", False],
    "Promocja_Majowa":["act", "kred",True],
    "Mikołajkowe_Oferty":["ret", "kred",True],
    "Zakupy_na_Weekend":["ret", "kred",True],
    "Wakacyjne_Rabaty":["act", "dep",True],
    "Oferta_Bez_VAT":["act", "dep", False],
    "Bestseller_Tygodnia":["act", "dep", False],
    "Taniej_z_Kodem":["act", "kred",True],
    "Promocja_Lojalnościowa":["act", "kred", False],
    "Darmowa_Dostawa":["act", "dep",True],
    "24h_Super_Oferty":["act", "kred",True],
    "Specjalna_Oferta_Dla_Ciebie":["act", "dep", False],
    "Tydzień_Markowych_Produktów":["act", "dep", False],
    "Mega_Rabat_Dni":["act", "dep",True],
    # "1Wiosenny_Rabat":["sell", "kred","Piotr"],
    # "1Zimowa_Promocja":["act", "dep","Andrzej"],
    # "1Black_Friday_2024":["ret", "dep"],
    # "1Cyber_Monday_Sale":["ret", "kred"],
    # "1Letnia_Wyprzedaż":["act", "kred","Piotr"],
    # "1Noworoczna_Oferta":["sell", "kred","Krzysiek"],
    # "1Dni_Otwarte":["act", "dep"],
    # "1Świąteczne_Rabaty":["ret", "kred"],
    # "1Powrót_do_Szkoły":["act", "dep","Asia"],
    # "1Długi_Weekend_Promocja":["ret", "kred"],
    # "1Tydzień_Super_Ofert":["act", "kred"],
    # "1Happy_Hour_Rabaty":["act", "kred"],
    # "1Urodziny_Sklepu":["act", "dep"],
    # "1Wielkanocne_Rabaty":["sell", "kred"],
    # "1Jesienna_Wyprzedaż":["ret", "kred"],
    # "1Ekspresowe_Promocje":["sell", "kred"],
    # "1Prezent_na_Walentynki":["act", "dep"],
    # "1Promocja_Majowa":["act", "kred"],
    # "1Mikołajkowe_Oferty":["ret", "kred"],
    # "1Zakupy_na_Weekend":["ret", "kred"],
    # "1Wakacyjne_Rabaty":["act", "dep"],
    # "1Oferta_Bez_VAT":["act", "dep"],
    # "1Bestseller_Tygodnia":["act", "dep"],
    # "1Taniej_z_Kodem":["act", "kred"],
    # "1Promocja_Lojalnościowa":["act", "kred"],
    # "1Darmowa_Dostawa":["act", "dep"],
    # "124h_Super_Oferty":["act", "kred"],
    # "1Specjalna_Oferta_Dla_Ciebie":["act", "dep"],
    # "1Tydzień_Markowych_Produktów":["act", "dep"],
    # "1Mega_Rabat_Dni":["act", "dep"]
}


with app.app_context():
    camps = []
    for i in kampanie:
        if len(kampanie[i]) == 3:
            camps.append(Camapign(name=i, lv1=kampanie[i][0], lv2=kampanie[i][1], rt=kampanie[i][2]))
        else:
            camps.append(Camapign(name = i, lv1 = kampanie[i][0], lv2 = kampanie[i][1], rt=kampanie[i][2], person=kampanie[i][-1]))
    db.session.add_all(camps)
    db.session.commit()
    print("Dodano użytkowników!")
