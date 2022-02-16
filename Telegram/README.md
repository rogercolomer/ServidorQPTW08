[comment]: <> (<div id="top"></div>)
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Telegram Quadpack Wood Aplication</h3>

  <p align="center">
    Aplicació per la notificació de averies, canvis d'estat i control de la producció i manteniment de la planta de Torelló
    
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">Sobre el projecte</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Sobre el projecte

Aquest projecte es basa en un bot de telegram:
* Notificacions de canvis d'estat de la OTR, sistema d'aspiració i compressors.
* Sistema d'alarmes dels sistemes anteriors i la biomassa.
* Consulta de l'estat dels sistemes bàsiscs de la planta de Torelló.
* Notificació de les OF's posades en marxa i parades del sistema de mesbook.
* Notificació dels excessos de producció > del 105% del total de la OF.


<p align="right">(<a href="#top">back to top</a>)</p>



### Build With

Per fer funcionar la aplicació són necessaris tots aquets paquets i llibraries:
* [Python 3.9.2](https://www.python.org/downloads/)
* [datetime](https://docs.python.org/3/library/datetime.html)
* [telebot](https://github.com/eternnoir/pyTelegramBotAPI)
* [mysql.connector](https://pypi.org/project/mysql-connector/)
* [json](https://docs.python.org/3/library/json.html)
* [os](https://docs.python.org/3/library/os.html)
* [subprocess](https://docs.python.org/3/library/subprocess.html)
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
* [threading](https://docs.python.org/3/library/threading.html)


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

La aplicació es basa en tres programes de python:
* alarmesProduccio.py
* alarmesTelegram.py
* botTelegram.py


### Prerequisites

Per fer funcionar l'aplicació és necessari:
* Python 3.8 o superior.
* Tots els paquets necessaris de python asmentats anteriorment.
* Accés a les base de dades dels sistemes de manteniment i producció.
* Bot de Telegram actiu i funcionant.
### Installation
* Token:  '867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs'
* Per entrar un usuari d'ha d'afegir a l'arxiu json de cada aplicatiu (alarmes, producció i/o Bot)
* Mitjançant el següent enllaç es pot extreure els missatges enviats [https://api.telegram.org/bot867573955:AAEJUO1URD6ICiinQ-sr_kEPnmuJ2dCMgNs/getUpdates](getUpdates)
* Perquè es mostri el teclat del BOT ens els nous contactes d'executar la següent línea de codi del programa botTelegram.py:
````python
    tb.send_message(chatID, missatge, reply_markup=markup)
````


<p align="right">(<a href="#top">back to top</a>)</p>



[comment]: <> (<!-- USAGE EXAMPLES -->)

[comment]: <> (## Usage)

[comment]: <> ([comment]: <> &#40;TODO&#41;)

