from models import db, Camapign
from app import app

kampanie = {
    "Wiosenny_Rabat":["Sprzedaż", "Aplikacja",True,"Piotr Beczka"],
    "Zimowa_Promocja":["Informacja", "Email", False,"Andrzej Ciemny"],
    "Black_Friday_2024":["Sprzedaż", "WWW",True],
    "Cyber_Monday_Sale":["Sprzedaż", "Aplikacja", False],
    "Letnia_Wyprzedaż":["Informacja", "Aplikacja",True,"Piotr Krzyżanowski"],
    "Noworoczna_Oferta":["Sprzedaż", "Aplikacja",True,"Krzysiek Kudłaty"],
    "Dni_Otwarte":["Informacja", "Email",True],
    "Świąteczne_Rabaty":["Sprzedaż", "Aplikacja", False],
    "Powrót_do_Szkoły":["Informacja", "Email",True,"Asia Rycz"],
    "Długi_Weekend_Promocja":["Sprzedaż", "WWW",True],
    "Tydzień_Super_Ofert":["Informacja", "SMS",True],
    "Happy_Hour_Rabaty":["Informacja", "SMS",True],
    "Urodziny_Sklepu":["Informacja", "Email", False],
    "Wielkanocne_Rabaty":["Sprzedaż", "SMS",True],
    "Jesienna_Wyprzedaż":["Informacja", "SMS",True],
    "Ekspresowe_Promocje":["Sprzedaż", "Aplikacja",True],
    "Prezent_na_Walentynki":["Informacja", "SMS", False],
    "Promocja_Majowa":["Informacja", "SMS",True],
    "Mikołajkowe_Oferty":["Sprzedaż", "SMS",True],
    "Zakupy_na_Weekend":["Sprzedaż", "Aplikacja",True],
    "Wakacyjne_Rabaty":["Informacja", "Aplikacja",True],
    "Oferta_Bez_VAT":["Informacja", "WWW", False],
    "Bestseller_Tygodnia":["Informacja", "WWW", False],
    "Taniej_z_Kodem":["Informacja", "Aplikacja",True],
    "Promocja_Lojalnościowa":["Informacja", "WWW", False],
    "Darmowa_Dostawa":["Informacja", "Aplikacja",True],
    "24h_Super_Oferty":["Informacja", "Aplikacja",True],
    "Specjalna_Oferta_Dla_Ciebie":["Informacja", "WWW", False],
    "Tydzień_Markowych_Produktów":["Informacja", "WWW", False],
    "Mega_Rabat_Dni":["Informacja", "WWW",True],
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
