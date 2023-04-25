"""
Tähän tiedostoon on erotettu Shakkilauta-luokka, joka vastaa pelin 
teoreettisesta toiminnasta. Tehtävänä on vielä kommentointia sekä
shakkikoneen toiminnan parantamista.
"""

from copy import deepcopy

KIRJAIMET = ["a", "b", "c", "d", "e", "f", "g", "h"]


class Shakkilauta:
    def __init__(self, vs=None, vt=None, vr=None, vl=None, vq=None, vk=None,
                 ms=None, mt=None, mr=None, ml=None, mq=None, mk=None):
        """
        Teorialauta rakentuu annettujen asemien pohjalta.
        Jos parametreja ei ole annettu, aloitetaan lähtöasetelmasta.
        """

        # Jos parametreja ei ole annettu, aloitetaan lähtöasetelmasta
        if not (vs or vt or vr or vl or vq or vk or ms or mt or mr or ml or
                mq or mk):
            vs = ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"]
            vt = ["a1", "h1"]
            vr = ["b1", "g1"]
            vl = ["c1", "f1"]
            vq = ["d1"]
            vk = ["e1"]

            ms = ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]
            mt = ["a8", "h8"]
            mr = ["b8", "g8"]
            ml = ["c8", "f8"]
            mq = ["d8"]
            mk = ["e8"]
        
        # Asetetaan asemat Shakkilaudan attribuuteille

        # Valkoiselle
        self.__valkoisen_sotilaat = vs
        self.__valkoisen_tornit = vt
        self.__valkoisen_ratsut = vr
        self.__valkoisen_lahetit = vl
        self.__valkoisen_kuningatar = vq
        self.__valkoisen_kuningas = vk
        
        # Mustalle
        self.__mustan_sotilaat = ms
        self.__mustan_tornit = mt
        self.__mustan_ratsut = mr
        self.__mustan_lahetit = ml
        self.__mustan_kuningatar = mq
        self.__mustan_kuningas = mk

        # Lisätiedot metodien toiminnan mahdollistamiseksi
        
        # Linnoittamiseen tarvittavat tiedot
        self.__valkoisen_vasen_torni_liikkunut = False
        self.__valkoisen_oikea_torni_liikkunut = False
        self.__valkoisen_kuningas_liikkunut = False
        self.__mustan_vasen_torni_liikkunut = False
        self.__mustan_oikea_torni_liikkunut = False
        self.__mustan_kuningas_liikkunut = False
        self.__linnoittaminen = False

    # Metodit, jotka muuttavat tietorakenteita ("setter")

    def tee_siirto(self, asema, siirto):

        # Poistetaan tiedoista nappulan sijaintiruutu ja
        # lisätään sen paikalle annettu siirtoruutu

        for asemalista in self.asemat_erikseen():

            # Nappulan syöminen
            if siirto in asemalista:
                asemalista.remove(siirto)

            # Nappulan siirtäminen
            if asema in asemalista:
                asemalista.remove(asema)
                asemalista.append(siirto)

        # Tarkkaillaan seuraavien nappuloiden liikkeitä linnoittamista varten:
        if asema == "a1":
            self.__valkoisen_vasen_torni_liikkunut = True
        if asema == "a8":
            self.__mustan_vasen_torni_liikkunut = True
        if asema == "h1":
            self.__valkoisen_oikea_torni_liikkunut = True
        if asema == "h8":
            self.__mustan_oikea_torni_liikkunut = True
        if asema == "e1":
            self.__valkoisen_kuningas_liikkunut = True
        if asema == "e8":
            self.__mustan_kuningas_liikkunut = True

        # Jos linnoittaminen tapahtuu, myös tornit siirtyvät
        if self.__linnoittaminen:
            if siirto == "c1":
                self.__valkoisen_tornit.remove("a1")
                self.__valkoisen_tornit.append("d1")
            if siirto == "g1":
                self.__valkoisen_tornit.remove("h1")
                self.__valkoisen_tornit.append("f1")

            if siirto == "c8":
                self.__mustan_tornit.remove("a8")
                self.__mustan_tornit.append("d8")
            if siirto == "g8":
                self.__mustan_tornit.remove("h8")
                self.__mustan_tornit.append("f8")

        # Kuningattareksi nousu sotilaalle laudan päädyssä
        if siirto in self.__valkoisen_sotilaat and siirto in \
                ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
            self.__valkoisen_sotilaat.remove(siirto)
            self.__valkoisen_kuningatar.append(siirto)
        if siirto in self.__mustan_sotilaat and siirto in \
                ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
            self.__mustan_sotilaat.remove(siirto)
            self.__mustan_kuningatar.append(siirto)

    def tietokoneen_siirto(self, puoli):

        paras_valkoiselle = -39
        paras_mustalle = 39
        paras_siirto = []

        siirrot = self.puolen_kaikki_siirrot(puoli)
        for sijainti in siirrot:
            for siirto in siirrot[sijainti]:

                uusi_lauta = deepcopy(self)
                uusi_lauta.tee_siirto(sijainti, siirto)

                valkoisen_materiaali, mustan_materiaali = \
                    uusi_lauta.puolten_kokonaismateriaali()
                suhde = valkoisen_materiaali + mustan_materiaali

                if puoli == "valkoinen" and suhde > paras_valkoiselle:
                    paras_valkoiselle = suhde
                    paras_siirto = [sijainti, siirto]

                if puoli == "musta" and suhde < paras_mustalle:
                    paras_mustalle = suhde
                    paras_siirto = [sijainti, siirto]

        return paras_siirto

    # Metodit, jotka palauttavat tietoja laudasta ("getter")

    def asemat_erikseen(self):
        return self.__valkoisen_sotilaat, self.__valkoisen_tornit, \
            self.__valkoisen_ratsut, self.__valkoisen_lahetit, \
            self.__valkoisen_kuningatar, self.__valkoisen_kuningas, \
            self.__mustan_sotilaat, self.__mustan_tornit, \
            self.__mustan_ratsut, self.__mustan_lahetit, \
            self.__mustan_kuningatar, self.__mustan_kuningas

    def asemat_yhdessa(self):

        valkoisen_asemat = self.__valkoisen_sotilaat \
            + self.__valkoisen_tornit + self.__valkoisen_ratsut \
            + self.__valkoisen_lahetit + self.__valkoisen_kuningatar \
            + self.__valkoisen_kuningas

        mustan_asemat = self.__mustan_sotilaat \
            + self.__mustan_tornit + self.__mustan_ratsut \
            + self.__mustan_lahetit + self.__mustan_kuningatar \
            + self.__mustan_kuningas

        return valkoisen_asemat, mustan_asemat

    def tarkista_shakitus(self):

        # Oletetaan, että kuninkaat eivät ole shakissa
        valkoinen_shakitettu_kuningas = None
        musta_shakitettu_kuningas = None

        for sijainti in self.puolen_kaikki_siirrot("valkoinen"):
            if self.__mustan_kuningas[0] in \
                    self.puolen_kaikki_siirrot("valkoinen")[sijainti]:
                musta_shakitettu_kuningas = self.__mustan_kuningas[0]

        for sijainti in self.puolen_kaikki_siirrot("musta"):
            if self.__valkoisen_kuningas[0] in \
                    self.puolen_kaikki_siirrot("musta")[sijainti]:
                valkoinen_shakitettu_kuningas = self.__valkoisen_kuningas[0]

        return valkoinen_shakitettu_kuningas, musta_shakitettu_kuningas
    
    def tarkista_matitus(self):
        valkoinen_shakissa, musta_shakissa = self.tarkista_shakitus()
        
        if valkoinen_shakissa:
            siirrot = self.puolen_kaikki_siirrot("valkoinen")
            
            for sijainti in siirrot:
                for siirto in siirrot[sijainti]:
                    uusi_lauta = deepcopy(self)
                    uusi_lauta.tee_siirto(sijainti, siirto)
                    valkoinen_shakissa, musta_shakissa = \
                        uusi_lauta.tarkista_shakitus()
            
                    if not valkoinen_shakissa:
                        return False, False

            return True, False

        if musta_shakissa:
            siirrot = self.puolen_kaikki_siirrot("musta")

            for sijainti in siirrot:
                for siirto in siirrot[sijainti]:
                    uusi_lauta = deepcopy(self)
                    uusi_lauta.tee_siirto(sijainti, siirto)
                    valkoinen_shakissa, musta_shakissa = \
                        uusi_lauta.tarkista_shakitus()

                    if not musta_shakissa:
                        return False, False

                    del uusi_lauta
            return False, True

        # Jos tämä koodi saavutetaan, kumpikaan kuningas ei ollut shakissa
        return False, False

    def puolten_kokonaismateriaali(self):
        """
        Määritetään puolten materiaalin arvo yleisesti käytetyllä taulukolla:
        Sotilas = 1 piste
        Ratsu = 3 pistettä
        Lähetti = 3 pistettä
        Torni = 5 pistettä
        Kuningatar = 9 pistettä

        :return: int, int; materiaalin arvo kokonaislukuna
        """

        valkoisen_materiaali = \
            len(self.__valkoisen_sotilaat) \
            + len(self.__valkoisen_lahetit) * 3 \
            + len(self.__valkoisen_ratsut) * 3 \
            + len(self.__valkoisen_tornit) * 5 \
            + len(self.__valkoisen_kuningatar) * 9

        mustan_materiaali = \
            - len(self.__mustan_sotilaat) \
            - len(self.__mustan_lahetit) * 3 \
            - len(self.__mustan_ratsut) * 3 \
            - len(self.__mustan_tornit) * 5 \
            - len(self.__mustan_kuningatar) * 9

        return valkoisen_materiaali, mustan_materiaali

    def nappulan_kaikki_siirrot(self, sijainti):

        if sijainti in self.__valkoisen_sotilaat:
            return self.valkoisen_sotilaan_liike(sijainti)

        if sijainti in self.__mustan_sotilaat:
            return self.mustan_sotilaan_liike(sijainti)

        if sijainti in self.__valkoisen_tornit or \
                sijainti in self.__mustan_tornit:
            return self.tornin_liike(sijainti)

        if sijainti in self.__valkoisen_ratsut or \
                sijainti in self.__mustan_ratsut:
            return self.ratsun_liike(sijainti)

        if sijainti in self.__valkoisen_lahetit or \
                sijainti in self.__mustan_lahetit:
            return self.lahetin_liike(sijainti)

        if sijainti in self.__valkoisen_kuningatar or \
                sijainti in self.__mustan_kuningatar:
            return self.tornin_liike(sijainti) + self.lahetin_liike(sijainti)

        if sijainti in self.__valkoisen_kuningas or \
                sijainti in self.__mustan_kuningas:
            return self.kuninkaan_liike(sijainti)

    def puolen_kaikki_siirrot(self, puoli):
        
        siirrot = {}
        valkoisen_asemat, mustan_asemat = self.asemat_yhdessa()

        if puoli == "valkoinen":
            asemalista = valkoisen_asemat
        else:
            asemalista = mustan_asemat

        for asema in asemalista:
            if self.nappulan_kaikki_siirrot(asema):
                siirrot.update({asema: self.nappulan_kaikki_siirrot(asema)})

        return siirrot

    def valkoisen_sotilaan_liike(self, asema):
        """
        Apufunktio, joka tutkii valkoisen sotilaan liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Sotilaat voivat liikkua kaksi askelta eteen
        ensimmäisellä siirrollaan, sen jälkeen vain yhden. Sotilas voi myös
        syödä vastustajan pelinappulan yhden askeleen päästä viistottain.
        Koska nappulat siirtyvät eri väreillä eri suuntaan, ne on eroteltu
        omiksi metodeikseen.

        :param asema: str, ruudun koordinaatit, josta sotilas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]

        valkoisen_asemat, mustan_asemat = self.asemat_yhdessa()

        # syömismahdollisuudet
        for kirjain in viereiset_kirjaimet(aseman_kirjain):
            if (kirjain + str(int(aseman_numero) + 1)) in mustan_asemat:
                siirrot.append(kirjain + str(int(aseman_numero) + 1))

        # ei ole blokkausta
        if (aseman_kirjain + str(int(aseman_numero) + 1)) not in \
                (valkoisen_asemat + mustan_asemat):
            siirrot.append(aseman_kirjain + str(int(aseman_numero) + 1))
            # lähtöasemassa ja kahden askeleen päässä ei ole blokkausta
            if aseman_numero == "2" and (aseman_kirjain + "4") not in \
                    (valkoisen_asemat + mustan_asemat):
                # kahden askeleen siirto on mahdollinen
                siirrot.append(aseman_kirjain + str(int(aseman_numero) + 2))
        return siirrot

    def mustan_sotilaan_liike(self, asema):
        """
        Apufunktio, joka tutkii mustan sotilaan liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Sotilaat voivat liikkua kaksi askelta eteen
        ensimmäisellä siirrollaan, sen jälkeen vain yhden. Sotilas voi myös
        syödä vastustajan pelinappulan yhden askeleen päästä viistottain.

        :param asema: str, ruudun koordinaatit, josta sotilas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]

        valkoisen_asemat, mustan_asemat = self.asemat_yhdessa()

        # syömismahdollisuudet
        for kirjain in viereiset_kirjaimet(aseman_kirjain):
            if (kirjain + str(int(aseman_numero) - 1)) in valkoisen_asemat:
                siirrot.append(kirjain + str(int(aseman_numero) - 1))
        # ei ole blokkausta
        if (aseman_kirjain + str(int(aseman_numero) - 1)) not in \
                (valkoisen_asemat + mustan_asemat):
            siirrot.append(aseman_kirjain + str(int(aseman_numero) - 1))
        # lähtöasemassa ja kahden askeleen päässä ei ole blokkausta
            if aseman_numero == "7" and (aseman_kirjain + "5") not in \
                    (valkoisen_asemat + mustan_asemat):
                # kahden askeleen siirto on mahdollinen
                siirrot.append(aseman_kirjain + str(int(aseman_numero) - 2))
        return siirrot

    def tornin_liike(self, asema):
        """
        Apufunktio, joka tutkii tornin liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Torni voi liikkua suorasti niin pitkälle kuin
        vain mahdollista. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta torni lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]
        indeksi = KIRJAIMET.index(aseman_kirjain)

        valkoisen_asemat, mustan_asemat = self.asemat_yhdessa()

        if asema in valkoisen_asemat:
            oma_puoli, vast_puoli = valkoisen_asemat, mustan_asemat
        else:
            oma_puoli, vast_puoli = mustan_asemat, valkoisen_asemat

        # Torni voi liikkua neljään suuntaan
        # ylös pääsee, alas pääsee, vasemmalle pääsee, oikealle pääsee
        paasylista = [True, True, True, True]
        for kerroin in range(1, 9):
            # tallennetaan kierroksen käsiteltävät ruudut listaan
            kasiteltavat_ruudut = []
            # ylöspäin, jos ei olla ylälaidassa tai blokattuna
            if int(aseman_numero) + kerroin <= 8 and paasylista[0]:
                kasiteltavat_ruudut.append(aseman_kirjain + str(int(
                    aseman_numero) + kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # alaspäin, jos ei olla alalaidassa
            if int(aseman_numero) - kerroin >= 1 and paasylista[1]:
                kasiteltavat_ruudut.append(aseman_kirjain + str(int(
                    aseman_numero) - kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # oikealle, jos ei olla oikeassa laidassa tai blokattuna
            if indeksi + kerroin <= 7 and paasylista[2]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi + kerroin] +
                                           aseman_numero)
            else:
                kasiteltavat_ruudut.append("")
            # vasemmalle, jos ei olla vasemmassa laidassa tai blokattuna
            if indeksi - kerroin >= 0 and paasylista[3]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi - kerroin] +
                                           aseman_numero)
            else:
                kasiteltavat_ruudut.append("")
            # käsitellään ruudut
            for ruutu in kasiteltavat_ruudut:
                ruudun_indeksi = kasiteltavat_ruudut.index(ruutu)
                if not ruutu or ruutu in oma_puoli:
                    paasylista[ruudun_indeksi] = False
                elif ruutu in vast_puoli:
                    paasylista[ruudun_indeksi] = False
                    siirrot.append(ruutu)
                else:
                    siirrot.append(ruutu)
        return siirrot

    def ratsun_liike(self, asema):
        """
        Apufunktio, joka tutkii ratsun liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Ratsu voi liikkua L-kirjaimen mukaisesti eli
        kaksi eteen, yhden sivulle. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta ratsu lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]
        indeksi = KIRJAIMET.index(aseman_kirjain)

        valkoisen_asemat, mustan_asemat = self.asemat_yhdessa()

        if asema in valkoisen_asemat:
            oma_puoli, vast_puoli = valkoisen_asemat, mustan_asemat
        else:
            oma_puoli, vast_puoli = mustan_asemat, valkoisen_asemat

        # hevonen saattaa liikkua enintään kahdeksaan ruutuun
        # kaksi ruutua ylös
        if int(aseman_numero) <= 6:
            # ruutu vasempaan
            if indeksi >= 1:
                ruutu = KIRJAIMET[indeksi - 1] + str(int(aseman_numero) + 2)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
            # ruutu oikeaan
            if indeksi <= 6:
                ruutu = KIRJAIMET[indeksi + 1] + str(int(aseman_numero) + 2)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
        # kaksi ruutua alas
        if int(aseman_numero) >= 3:
            # ruutu vasempaan
            if indeksi >= 1:
                ruutu = KIRJAIMET[indeksi - 1] + str(int(aseman_numero) - 2)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
            # ruutu oikeaan
            if indeksi <= 6:
                ruutu = KIRJAIMET[indeksi + 1] + str(int(aseman_numero) - 2)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
        # kaksi ruutua vasempaan
        if indeksi >= 2:
            # ruutu ylös
            if int(aseman_numero) <= 7:
                ruutu = KIRJAIMET[indeksi - 2] + str(int(aseman_numero) + 1)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
            # ruutu alas
            if int(aseman_numero) >= 2:
                ruutu = KIRJAIMET[indeksi - 2] + str(int(aseman_numero) - 1)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
        # kaksi ruutua oikeaan
        if indeksi <= 5:
            # ruutu ylös
            if int(aseman_numero) <= 7:
                ruutu = KIRJAIMET[indeksi + 2] + str(int(aseman_numero) + 1)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
            # ruutu alas
            if int(aseman_numero) >= 2:
                ruutu = KIRJAIMET[indeksi + 2] + str(int(aseman_numero) - 1)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
        return siirrot

    def lahetin_liike(self, asema):
        """
        Apufunktio, joka tutkii lähetin liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Lähetti voi liikkua viistottain niin pitkälle
        kuin vain mahdollista. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta lähetti lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]

        valkoisen_asemat, mustan_asemat = self.asemat_yhdessa()

        if asema in valkoisen_asemat:
            oma_puoli, vast_puoli = valkoisen_asemat, mustan_asemat
        else:
            oma_puoli, vast_puoli = mustan_asemat, valkoisen_asemat

        indeksi = KIRJAIMET.index(aseman_kirjain)
        # Lähetti saattaa liikkua enintään neljään suuntaan
        # ylös vasemmalle, ylös oikealle, alas vasemmalle, alas oikealle
        paasylista = [True, True, True, True]
        for kerroin in range(1, 9):
            # tallennetaan kierroksen käsiteltävät ruudut listaan
            kasiteltavat_ruudut = []
            # ylös ja vasemmalle, jos ei olla ylä- tai vasemmassa laidassa
            if indeksi - kerroin >= 0 and int(aseman_numero) + kerroin <= 8 \
                    and paasylista[0]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi - kerroin]
                                           + str(int(aseman_numero) + kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # ylös ja oikealle, jos ei olla ylä- tai oikeassa laidassa
            if indeksi + kerroin <= 7 and int(aseman_numero) + kerroin <= 8 \
                    and paasylista[1]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi + kerroin]
                                           + str(int(aseman_numero) + kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # alas ja vasemmalle, jos ei olla ala- tai vasemmassa laidassa
            if indeksi - kerroin >= 0 and int(aseman_numero) - kerroin >= 1 \
                    and paasylista[2]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi - kerroin]
                                           + str(int(aseman_numero) - kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # alas ja oikealle, jos ei olla ala- tai oikeassa laidassa
            if indeksi + kerroin <= 7 and int(aseman_numero) - kerroin >= 1 \
                    and paasylista[3]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi + kerroin]
                                           + str(int(aseman_numero) - kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # käsitellään ruudut
            for ruutu in kasiteltavat_ruudut:
                ruudun_indeksi = kasiteltavat_ruudut.index(ruutu)
                if not ruutu or ruutu in oma_puoli:
                    paasylista[ruudun_indeksi] = False
                elif ruutu in vast_puoli:
                    paasylista[ruudun_indeksi] = False
                    siirrot.append(ruutu)
                else:
                    siirrot.append(ruutu)
        return siirrot

    def kuninkaan_liike(self, asema):
        """
        Apufunktio, joka tutkii kuninkaan liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Kuningas voi liikkua yhden askeleen joka
        suuntaan laudalla. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta kuningas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]

        valkoisen_asemat, mustan_asemat = self.asemat_yhdessa()

        if asema in valkoisen_asemat:
            oma_puoli, vast_puoli = valkoisen_asemat, mustan_asemat
        else:
            oma_puoli, vast_puoli = mustan_asemat, valkoisen_asemat

        indeksi = KIRJAIMET.index(aseman_kirjain)
        # ylöspäin
        # jos ei olla jo ylälaidassa
        if int(aseman_numero) <= 7:
            # ruutu vasempaan
            if indeksi >= 1:
                ruutu = KIRJAIMET[indeksi - 1] + str(int(aseman_numero) + 1)
                siirrot.append(ruutu)
            # ruutu oikeaan
            if indeksi <= 6:
                ruutu = KIRJAIMET[indeksi + 1] + str(int(aseman_numero) + 1)
                siirrot.append(ruutu)
            # keskelle voi liikkua ilman lisärajoituksia
            ruutu = aseman_kirjain + str(int(aseman_numero) + 1)
            siirrot.append(ruutu)
        # alaspäin
        if int(aseman_numero) >= 2:
            # ruutu vasempaan
            if indeksi >= 1:
                ruutu = KIRJAIMET[indeksi - 1] + str(int(aseman_numero) - 1)
                siirrot.append(ruutu)
            # ruutu oikeaan
            if indeksi <= 6:
                ruutu = KIRJAIMET[indeksi + 1] + str(int(aseman_numero) - 1)
                siirrot.append(ruutu)
            ruutu = aseman_kirjain + str(int(aseman_numero) - 1)
            siirrot.append(ruutu)
        # vasemmalle tarvitsee lisätä vain yksi askel suoraan vasemmalle
        if indeksi >= 1:
            ruutu = KIRJAIMET[indeksi - 1] + aseman_numero
            siirrot.append(ruutu)
        # oikealle
        if indeksi <= 6:
            ruutu = KIRJAIMET[indeksi + 1] + aseman_numero
            siirrot.append(ruutu)
        # poistetaan vielä siirroista sellaiset ruudut,
        # jotka ovat varattuina omille nappuloille
        for ruutu in oma_puoli:
            if ruutu in siirrot:
                siirrot.remove(ruutu)

        # Linnoittaminen
        # Valkoiselle
        self.__linnoittaminen = False
        if not self.__valkoisen_kuningas_liikkunut and asema == "e1":
            if self.__valkoisen_vasen_torni_liikkunut:
                pass
            elif "b1" in oma_puoli + vast_puoli \
                    or "c1" in oma_puoli + vast_puoli \
                    or "d1" in oma_puoli + vast_puoli:
                pass
            else:
                siirrot.append("c1")
                self.__linnoittaminen = True
            if self.__valkoisen_oikea_torni_liikkunut:
                pass
            elif "f1" in oma_puoli + vast_puoli \
                    or "g1" in oma_puoli + vast_puoli:
                pass
            else:
                siirrot.append("g1")
                self.__linnoittaminen = True
        # Mustalle
        if not self.__mustan_kuningas_liikkunut and asema == "e8":
            if self.__mustan_vasen_torni_liikkunut:
                pass
            elif "b8" in oma_puoli + vast_puoli \
                    or "c8" not in oma_puoli + vast_puoli \
                    or "d8" not in oma_puoli + vast_puoli:
                pass
            else:
                siirrot.append("c8")
                self.__linnoittaminen = True
            if self.__mustan_oikea_torni_liikkunut:
                pass
            elif "f8" in oma_puoli + vast_puoli \
                    or "g8" in oma_puoli + vast_puoli:
                pass
            else:
                siirrot.append("g8")
                self.__linnoittaminen = True
        return siirrot


def viereiset_kirjaimet(kirjain):
    """
    Apufunktio nappuloiden siirtomahdollisuuksien tutkimiseen. Palauttaa
    laudan koordinaattikirjaimen viereiset kirjaimet tai viereisen kirjaimen.

    :param kirjain: str, koordinaattikirjain.
    :return: str / str, str; viereiset koordinaattikirjaimet.
    """

    indeksi = KIRJAIMET.index(kirjain)
    if indeksi == 0:
        return KIRJAIMET[1]
    if indeksi == 7:
        return KIRJAIMET[6]
    return KIRJAIMET[indeksi-1], KIRJAIMET[indeksi+1]