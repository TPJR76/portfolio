"""
Tämä ohjelma perustuu ohjelmoinnin peruskurssilla Tkinter-kirjastolla 
toteuttamaani graafisen käyttöliitymän shakkipeliin. Kurssilla palauttamani 
versio oli toteutettu yhtenä luokkana, mutta kerättyäni lisäoppeja
modulaarisuudesta, päädyin erottamaan luokat ja tiedostot toisistaan. 
Graafinen käyttöliittymä käyttää siis Shakkilauta-luokan metodeja pelin 
teoreettiseen pyörittämiseen ja ShakkiGUI-luokan metodeja käyttöliittymän
pyörittämiseen.

Projekti on vielä kesken, sen graafiset elementit ovat alkeellisia eivätkä
toimi täysin toivotulla ja tavoitteena on implementoida jokin koneoppimisen
metodi.

Versiohistoria:
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.1 GUI yhdistettynä teorialautaan (palautettu ohjelmoinnin peruskurssille).
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.2 Alkuperäisen GUI-luokan attribuutit ja metodit erotettuina kahteen
    luokkaan, joilla omat tiedostot (ShakkiGUI ja Shakkilauta).
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.3 Lisätty, muokattu ja poistettu metodeja Shakkilaudalta vastaamaan uutta
    suunnitelmaa. Mahdollistettu matin tarkistelua varten rekursiivinen
    ohjelmointi, jossa Shakkilauta voi muodostaa uusia Shakkilautoja
    (saattaa olla myöhemmin hyötyä shakkikoneen toteuttamisessa).
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.4 Lisätty, muokattu ja poistettu metodeja ShakkiGUI:lta vastaamaan uutta
    suunnitelmaa sekä Shakkilaudan uutta toimintaa.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
0.5 Lisätty yksinpeli: Hyvin alkeellinen shakkikone, joka harkitsee tulevan
    siirron arvoa materiaalieron perusteella
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(0.6?) Paranneltu shakkikone
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(0.7?) Koneoppimisen implementaatio
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(1.0?) Lisätty nappuloille grafiikat ja hiottu lopullinen versio graafisesta
       käyttöliittymästä
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
"""

from tkinter import *
from shakkilauta import Shakkilauta

# Globaalit vakiot

# Ulkoasu
IKKUNAN_TAUSTAVARI = "#424242"
IKKUNAN_FONTTI = "Kozuka Gothic Pro B", 18, "bold"
IKKUNAN_FONTIN_VARI = "#ffffff"
PELILAUDAN_FONTTI = "Kozuka Gothic Pro B", 12
# Shakkilaudan ruudut
TUMMA_RUUTU = "#66452d"
VAALEA_RUUTU = "#c9a565"

# Lista shakkilaudan koordinaattikirjaimista
KIRJAIMET = ["a", "b", "c", "d", "e", "f", "g", "h"]


class ShakkiGUI:
    def __init__(self):
        """
        Keskittyy käyttöliittymän rakentamiseen.
        """
        
        # Otetaan käyttöön pelin teoreettinen toteutus Shakkilauta
        self.__peli = Shakkilauta()
        
        # Määritetään pääikkunä
        self.__paaikkuna = Tk()
        self.__paaikkuna.overrideredirect(True)
        self.__paaikkuna.configure(bg=IKKUNAN_TAUSTAVARI, relief="solid")
        self.__paaikkuna.resizable(width=False, height=False)
        self.__paaikkuna.title("Shakki")

        # Ideana asettaa ikkuna hieman koko näyttöä pienemmäksi
        # ja keskelle näyttöä
        self.__ruudun_koko = self.__paaikkuna.winfo_screenheight() // 10
        self.__maksimileveys_tekstille = self.__ruudun_koko // 8
        ikkunan_leveys = str(self.__ruudun_koko * 8)
        ikkunan_korkeus = str(self.__ruudun_koko * 9)
        leveyden_keskikohta = str(self.__paaikkuna.winfo_screenwidth()//2
                                  - int(ikkunan_leveys)//2)
        self.__paaikkuna.geometry(ikkunan_leveys+"x"+ikkunan_korkeus
                                  + "+"+leveyden_keskikohta+"+"+"0")

        # Ennen shakkinäkymää muodostetaan päävalikko, jossa valitaan pelitila
        # (1 = moninpeli, 2 = yksinpeli valkoisilla, 3 = yksinpeli mustilla)
        self.__pelimuoto = 0
        moninpeli = Button(self.__paaikkuna, bg=IKKUNAN_TAUSTAVARI,
                           relief="flat", overrelief="flat",
                           text="Moninpeli", font=IKKUNAN_FONTTI,
                           fg=IKKUNAN_FONTIN_VARI, command=lambda tieto=1:
                           self.aloita_peli(tieto))

        yksinpeli_v = Button(self.__paaikkuna, bg=IKKUNAN_TAUSTAVARI,
                             relief="flat", overrelief="flat",
                             text="Yksinpeli valkoisella",
                             font=IKKUNAN_FONTTI, fg=IKKUNAN_FONTIN_VARI,
                             command=lambda tieto=2: self.aloita_peli(tieto))

        yksinpeli_m = Button(self.__paaikkuna, bg=IKKUNAN_TAUSTAVARI,
                             relief="flat", overrelief="flat",
                             text="Yksinpeli mustalla",
                             font=IKKUNAN_FONTTI, fg=IKKUNAN_FONTIN_VARI,
                             command=lambda tieto=3: self.aloita_peli(tieto))

        moninpeli.grid(row=2, column=3, columnspan=2, sticky="nsew",
                       ipadx=0, ipady=0, padx=0, pady=0)
        yksinpeli_v.grid(row=3, column=3, columnspan=2, sticky="nsew",
                         ipadx=0, ipady=3, padx=0, pady=0)
        yksinpeli_m.grid(row=4, column=3, columnspan=2, sticky="nsew",
                         ipadx=0, ipady=0, padx=0, pady=0)

        # Luodaan käyttöliittymään pelin lisäksi muutama muu toiminto
        # Koko näytölle asettaminen
        self.__koko_naytto = Button(self.__paaikkuna,
                                    bg=IKKUNAN_TAUSTAVARI,
                                    relief="flat", overrelief="flat",
                                    text="Koko näyttö",
                                    font=IKKUNAN_FONTTI,
                                    fg=IKKUNAN_FONTIN_VARI,
                                    command=self.koko_naytto)
        self.__koko_naytto.grid(row=0, column=6, columnspan=2, sticky="nsew",
                                ipadx=0, ipady=0, padx=0, pady=0)
        
        # Sulkeminen
        sulje = Button(self.__paaikkuna, bg=IKKUNAN_TAUSTAVARI,
                       relief="flat", overrelief="flat",
                       text="Sulje pelilauta", font=IKKUNAN_FONTTI,
                       fg=IKKUNAN_FONTIN_VARI,
                       command=self.__paaikkuna.destroy)
        sulje.grid(row=0, column=0, columnspan=2, sticky="nsew", ipadx=0,
                   ipady=0, padx=0, pady=0)
        
        # Päivitettävä tilanneteksti
        self.__siirtonro = 1
        self.__tilanneteksti = Label(self.__paaikkuna,
                                     bg=IKKUNAN_TAUSTAVARI,
                                     text="Pelimuodon valitseminen",
                                     font=IKKUNAN_FONTTI,
                                     fg=IKKUNAN_FONTIN_VARI)
        self.__tilanneteksti.grid(row=0, column=2, columnspan=4, sticky="nsew",
                                  ipadx=0, ipady=0, padx=0, pady=0)

        # Tässä muotoillaan taulukkoa lisää
        for sarake in range(0, 8):
            self.__paaikkuna.grid_columnconfigure(index=sarake, pad=0,
                                                  minsize=self.__ruudun_koko)
        for rivi in range(0, 9):
            self.__paaikkuna.grid_rowconfigure(index=rivi, pad=0,
                                               minsize=self.__ruudun_koko)
        self.__paaikkuna.grid_anchor("n")

        # Luodaan laudan jokaista ruutua varten nappi ja lisätään listaan
        self.__ruudut_nappeina = []
        for numero in range(64):
            self.__ruudut_nappeina.append(Button(self.__paaikkuna,
                                                 relief="flat",
                                                 overrelief="flat"))

    def aloita_peli(self, pelimuoto):

        # Asetetaan pelimuoto
        self.__pelimuoto = pelimuoto
        # Lisätään shakkilauta ikkunaan eli laudan jokaisen ruudun nappi
        # taulukkoon

        # Haluan ensimmäisen napin vastaavan shakkilaudan koordinaateissa
        # a1, toisen a2 jne.

        # Napit täytetään alhaalta ylöspäin (taulukon riveille 1-8) ja
        # vasemmalta oikealle (sarakkeisiin 0-7).
        indeksi = 0
        for sarake in range(0, 8):
            for rivi in range(8, 0, -1):
                self.__ruudut_nappeina[indeksi].grid(row=rivi, column=sarake,
                                                     sticky="nsew",
                                                     columnspan=1,
                                                     ipadx=0, ipady=0,
                                                     padx=0, pady=0)
                indeksi += 1

        self.__tilanneteksti.configure(text="Siirto " + str(self.__siirtonro))

        # Aloita pelin ensimmäinen vuoro
        self.uusi_vuoro()

    def laudan_pohja(self):
        """
        Tyhjentää laudalla olevat napit sekä asettaa ruuduille alkuperäiset
        taustavärinsä.
        """

        # Konfiguroidaan napit silmukkana
        ehto = 0
        for ruutu in self.__ruudut_nappeina:
            # Aloitetaan tyhjistä napeista
            ruutu.configure(text="", command=NONE, state=DISABLED)

            # Joka toinen ruutu on tumma ja joka toinen vaalea
            if ehto % 2 == 0:
                taustavari = TUMMA_RUUTU
            else:
                taustavari = VAALEA_RUUTU

            ruutu.configure(bg=taustavari, activebackground=taustavari)
            ehto += 1
            # 8. ja 9. ruutu halutaan samanvärisiksi, sitten 16. ja 17. jne.
            if ehto in range(8, 64, 9):
                ehto += 1

    def aseta_nappulat(self):
        """
        Lisää nappulat pelilaudalle siirtomahdollisuudet näyttävinä nappeina.
        Merkkaa myös shakitetun kuninkaan punaisella.
        """

        valkoisen_sotilaat, valkoisen_tornit, valkoisen_ratsut, \
            valkoisen_lahetit, valkoisen_kuningatar, valkoisen_kuningas, \
            mustan_sotilaat, mustan_tornit, mustan_ratsut, \
            mustan_lahetit, mustan_kuningatar, mustan_kuningas = \
            self.__peli.asemat_erikseen()

        valkoisen_asemat, mustan_asemat = self.__peli.asemat_yhdessa()

        for asema in valkoisen_asemat + mustan_asemat:

            if asema in valkoisen_asemat:
                oikea_vari = "White"
            else:
                oikea_vari = "Black"

            if asema in valkoisen_sotilaat:
                oikea_teksti = "Sotilas"
                siirrot = self.__peli.valkoisen_sotilaan_liike(asema)

            if asema in mustan_sotilaat:
                oikea_teksti = "Sotilas"
                siirrot = self.__peli.mustan_sotilaan_liike(asema)

            if asema in valkoisen_tornit or asema in mustan_tornit:
                oikea_teksti = "Torni"
                siirrot = self.__peli.tornin_liike(asema)

            if asema in valkoisen_ratsut or asema in mustan_ratsut:
                oikea_teksti = "Ratsu"
                siirrot = self.__peli.ratsun_liike(asema)

            if asema in valkoisen_lahetit or asema in mustan_lahetit:
                oikea_teksti = "Lähetti"
                siirrot = self.__peli.lahetin_liike(asema)

            if asema in valkoisen_kuningatar or asema in mustan_kuningatar:
                oikea_teksti = "Kuningatar"
                siirrot = self.__peli.tornin_liike(asema) \
                    + self.__peli.lahetin_liike(asema)

            if asema in valkoisen_kuningas or asema in mustan_kuningas:
                oikea_teksti = "Kuningas"
                siirrot = self.__peli.kuninkaan_liike(asema)

            self.nappi_koordinaatille(asema).configure(
                state=DISABLED, font=PELILAUDAN_FONTTI, text=oikea_teksti,
                fg=oikea_vari, disabledforeground=oikea_vari,
                activeforeground=oikea_vari,
                command=lambda tieto1=asema, tieto2=siirrot:
                self.nayta_siirrot(tieto1, tieto2))

        # Tarkistetaan ja merkataan mahdolliset shakit
        valkoinen_shakissa, musta_shakissa = self.__peli.tarkista_shakitus()

        if valkoinen_shakissa:
            self.nappi_koordinaatille(
                valkoisen_kuningas[0]).configure(bg="Red",
                                                 activebackground="Red")

        if musta_shakissa:
            self.nappi_koordinaatille(
                mustan_kuningas[0]).configure(bg="Red", activebackground="Red")

    def uusi_vuoro(self):
        """
        Tarkistaa ensin, onko toinen voittanut. Jos ei, jakaa vuoron oikealle
        puolelle yksinkertaisesti laskurin parillisuuteen perustuen.
        """

        # Uuden vuoron alussa rakennetaan pelilauta uudelleen
        self.laudan_pohja()
        self.aseta_nappulat()

        # Päivitetään tilateksti
        self.__tilanneteksti.configure(text="Siirto "+str(self.__siirtonro))

        valkoisen_asemat, mustan_asemat = self.__peli.asemat_yhdessa()

        # Shakkimatti tarkoittaa pelin voittoa
        valkoinen_matissa, musta_matissa = self.__peli.tarkista_matitus()
        if valkoinen_matissa:
            self.__tilanneteksti.configure(text="Peli on päättynyt, "
                                                "musta voitti!")
            return

        if musta_matissa:
            self.__tilanneteksti.configure(text="Peli on päättynyt, valkoinen "
                                                "voitti!")
            return

        # Tarkistetaan shakit
        valkoinen_shakissa, musta_shakissa = self.__peli.tarkista_shakitus()

        # Päätellään kumpi on vuorossa vuoronumeron perusteella
        if self.__siirtonro % 2 == 1:

            # Vastapuolen kuningas shakissa vuoron alussa tarkoittaa voittoa
            if musta_shakissa:
                self.__tilanneteksti.configure(
                    text="Peli on päättynyt, valkoinen voitti!")
                return

            # Pelaajan nappulat aktivoidaan tai annetaan tietokoneen tehdä
            # siirto
            if self.__pelimuoto == 1 or self.__pelimuoto == 2:
                self.aktivoi_merkkijonolistan_napit(valkoisen_asemat)
            else:
                tietokoneen_siirto = \
                    self.__peli.tietokoneen_siirto("valkoinen")
                self.tee_siirto(tietokoneen_siirto[0], tietokoneen_siirto[1])

        else:

            if valkoinen_shakissa:
                self.__tilanneteksti.configure(
                    text="Peli on päättynyt, musta voitti!")

            if self.__pelimuoto == 1 or self.__pelimuoto == 3:
                self.aktivoi_merkkijonolistan_napit(mustan_asemat)
            else:
                tietokoneen_siirto = \
                    self.__peli.tietokoneen_siirto("musta")
                self.laudan_pohja()
                self.tee_siirto(tietokoneen_siirto[0], tietokoneen_siirto[1])

    def nayta_siirrot(self, asema, siirrot):
        """
        Tämä komento ajetaan pelilaudan nappulaa vastaavaa nappia painettaessa.
        Tyhjentää laudan vanhentuneista siirtonapeista ja lisää laudalle
        nappulan siirtämisen mahdollistavat siirtonapit.

        :param asema: str, painetun napin lähtökoordinaatit merkkijonona.
        :param siirrot: [str, ...]; lista nappulan mahdollisista siirroista
                        koordinaattien merkkijoina.
        """

        oma_puoli, vast_puoli = self.kummat_puolet(asema)

        # Helpoin tapa poistaa vanhentuneet siirtonapit on ladata lauta
        # uudelleen
        self.laudan_pohja()
        self.aseta_nappulat()
        self.aktivoi_merkkijonolistan_napit(oma_puoli)

        for ruutu in siirrot:
            self.nappi_koordinaatille(ruutu).configure(
                state=NORMAL, text="Siirto", fg="grey",
                font=PELILAUDAN_FONTTI,
                activeforeground="grey",
                command=lambda tieto1=asema, tieto2=ruutu:
                self.tee_siirto(tieto1, tieto2))

    def tee_siirto(self, asema, siirto):
        """
        Tämä komento ajetaan siirtonappia painettaessa. Se poistaa ensin
        siirtonapit laudalta. Sitten se siirtää nappulan valittuun paikkaan
        päivittämällä tietolistat ja laudan.

        :param asema: str, siirrettävän nappulan koordinaatit merkkijonona.
        :param siirto: str, siirryttävän ruudun koordinaatit merkkijonona.
        """

        # Tehdään siirto Shakkilaudalla
        self.__peli.tee_siirto(asema, siirto)

        # Siirretään siirtonumeroaa eteenpäin
        self.__siirtonro += 1

        # Vuoro siirtyy vastustajalle
        self.uusi_vuoro()

    def aktivoi_merkkijonolistan_napit(self, merkkijonolista):
        """
        Apufunktio, joka pistää annetun merkkijonolistan koordinaattien
        mukaiset napit päälle.

        :param merkkijonolista: [str, ...]; lista ruutujen koordinaateista
                                merkkijonoina
        """

        for ruutu in merkkijonolista:
            self.nappi_koordinaatille(ruutu).configure(state=NORMAL)

    def deaktivoi_merkkijonolistan_napit(self, merkkijonolista):
        """
        Apufunktio, joka pistää annetun merkkijonolistan koordinaattien
        mukaiset napit pois päältä.

        :param merkkijonolista: [str, ...]; lista ruutujen koordinaateista
               merkkijonoina
        """

        for ruutu in merkkijonolista:
            self.nappi_koordinaatille(ruutu).configure(state=DISABLED)

    def nappi_koordinaatille(self, merkkijono):
        """
        Kenties tärkein apufunktio, joka parittaa ruudun koordinaattiin
        käyttöliittymässä koordinaattia vastaavassa paikassa sijaitsevan napin.

        :param merkkijono: str, ruudun koordinaatti merkkijonona
        :return: Button-tyyppinen attribuutti
        """

        ruudut_merkkijonoina = shakkilaudan_koordinaatit()
        # Luodaan lista laudan ruuduista merkkijonoina, samaan järjestykseen
        # kuin self.__ruudut_nappeina eli a1, a2, ..., a8, b1 jne.
        # otetaan etsityn merkkijonon indeksi
        indeksi = ruudut_merkkijonoina.index(merkkijono)
        # palautetaan indeksiä vastaava attribuutti
        return self.__ruudut_nappeina[indeksi]

    def kummat_puolet(self, asema):
        """
        Apufunktio, joka palauttaa asemien listat järjestyksessä omat asemat,
        vastustajan asemat.

        :param asema: str, ruudun koordinaatit, jossa on pelinappula.
        :return: [str, ...], [str, ...]; lista omista asemista ja
                 vastustajan asemista.
        """

        valkoisen_asemat, mustan_asemat = self.__peli.asemat_yhdessa()

        if asema in valkoisen_asemat:
            return valkoisen_asemat, mustan_asemat
        return mustan_asemat, valkoisen_asemat

    def koko_naytto(self):
        """
        Asettaa ikkunan koko näytölle sekä muuttaa napin toiminnoksi palaamaan
        alkuperäiseen ikkunaan.
        """
        self.__paaikkuna.overrideredirect(False)
        self.__paaikkuna.attributes('-fullscreen', True)
        self.__koko_naytto.configure(text="Ikkunaksi",
                                     command=self.pois_koko_naytosta)

    def pois_koko_naytosta(self):
        """
        Asettaa ikkunan koko näytöltä takaisin alkuperäiseen kokoon sekä
        muuttaa napin toiminnoksi palaamaan koko näytölle.
        """
        self.__paaikkuna.overrideredirect(True)
        self.__paaikkuna.attributes('-fullscreen', False)
        self.__koko_naytto.configure(text="Koko näyttö",
                                     command=self.koko_naytto)

    def aloita(self):
        """
        Käynnistää pääikkunan silmukan, ts. käynnistää käyttöliittymän ikkunan.
        """

        self.__paaikkuna.mainloop()


def shakkilaudan_koordinaatit():
    """
    Apufunktio, joka palauttaa shakkilaudan ruudut listana a1, a2, ..., b1 jne.

    :return: [str, ...]; shakkilaudan ruudut.
    """

    ruudut = []
    for kirjain in KIRJAIMET:
        for numero in range(1, 9):
            ruudut.append(kirjain + str(numero))
    return ruudut


def main():
    # otetaan graafinen käyttöliittymä käyttöön
    peli = ShakkiGUI()
    # käynnistetään ikkuna
    peli.aloita()


if __name__ == "__main__":
    main()
