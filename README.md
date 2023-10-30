# Reservations app

## Sisällysluettelo
- [Sovelluksen idea](#sovelluksen-idea)
- [Tarkastajalle](#tarkastajalle)
- [Käyttäjäryhmät ja niiden toiminnot](#käyttäjäryhmät-ja-niiden-toiminnot)
    * [Asiakas (kirjautumaton)](#asiakas-kirjautumaton)
    * [Työntekijä (kirjautunut)](#työntekijä-kirjautunut)
    * [Pääkäyttäjä (kirjautunut)](#pääkäyttäjä-kirjautunut)

<a name="sovelluksen-idea"></a>
## Sovelluksen idea
Kampaamon varausjärjestelmä, jossa asiakkaat voivat varata ajan haluamaansa palveluun, haluamaansa toimipisteeseen ja haluamalleen kampaajalle. Kampaamon työntekijät voivat katsella varauksia ja merkitä niitä tehdyiksi.

<a name="tarkastajalle"></a>
## Tarkastajalle
Sovelluksessa on jo tehtynä käyttöliittymä, mutta mitään palvelinpuolen logiikkaa ei ole olemassa. Kyseistä käyttöliittymää voi kuitenkin käyttää ja siitä saa hyvän kuvan miltä sovellus visuaalisesti tulee näyttämään sekä sen toiminnalisuuksista. Koodi löytyy kansioista `/templates` ja `/static`

<a name="käyttäjäryhmät-ja-niiden-toiminnot"></a>
## Käyttäjäryhmät ja niiden toiminnot
Käyttäjäryhmät ovat järjestyksessä pienemmistä oikeuksista suurimpiin oikeuksiin. Suuremman oikeuden käyttäjäryhmä saa kaikkien alempien käyttäjäryhmien oikeudet myös käyttöönsä.

<a name="asiakas-kirjautumaton"></a>
### Asiakas (kirjautumaton)
- Luoda varaus
  - Valitsee toimipisteen, palvelun ja kampaajan
  - Syöttää omat tiedot ja mahdollisesti viestin kampaajalle
- Muokata tekemäänsä varausta
  - Oman varauksen löytää varauksen tunnisteella ja sen luonnin yhteydessä saadulla pin-koodilla.
  - Varauksen omia tietoja voi muokata ja sen voi perua
- Tarkastella verkkosivuilla toimipisteitä

<a name="työntekijä-kirjautunut"></a>
### Työntekijä (kirjautunut)
- Muokata omia käyttäjätietojaan
  - Nimi, sähköpostiosoite
- Tarkastella tulevia varauksia
- Tarkastella yhtä varausta
  - Näkee asiakkaan tarkemmat tiedot ja viestin
  - Voi poistaa tai merkitä varauksen suoritetuksi

<a name="pääkäyttäjä-kirjautunut"></a>
### Pääkäyttäjä (kirjautunut)
- Muokata varattavia aikoja (timeslots)
  - Luo siis vapaat ajat, joita asiakas voi varata sekä määrittelee niille palvelun ja työntekijän
  - Poistaa varattavissa olevia aikoja, joita ei ole vielä varattu
- Muokata käyttäjiä
  - Hyväksyä rekisteröityneet käyttäjät (eli päästää heidät järjestelmään)
  - Muokata käyttäjien käyttäjäroolia (työntekijä/pääkäyttäjä)
  - Poistaa käyttäjiä käytöstä (tiedot jää, mutta käyttäjä ei pääse järjestelmään käsiksi eikä se näy varaussivulla)
- Muokata varattavia palveluita
  - Luoda ja poistaa palveluita (palvelulla on nimi ja hinta)
- Muokata toimipisteitä
  - Luoda, muokata ja poistaa toimipisteitä
    - Toimipisteellä on nimi, osoite ja kuva (URL)