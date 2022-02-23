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
  <h3 align="center">Monitoring Biomassa</h3>

  <p align="center">
    Aplicació per llegir les variables necessàries per monitoritzar la biomassa i extreure els valors de consum per aconseguir els informes necessaris.
    
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

Aquest projecte es basa el la lectura de les variables necessàries del bus BACnet per mostrar-les a el grafana
o enviar notificacions per Telegram:
* Monitorització de l'estat de la màquina
* Control de les alarmes per fer la notificació per telegram
* Adquisició dels consums i energia generada per la planta.



<p align="right">(<a href="#top">back to top</a>)</p>



### Build With

Per fer funcionar la aplicació són necessaris tots aquets paquets i llibraries:
* [Python 3.9.2](https://www.python.org/downloads/)
* [datetime](https://docs.python.org/3/library/datetime.html)
* [BAC0](https://pypi.org/project/BAC0/)
* [mysql.connector](https://pypi.org/project/mysql-connector/)
* [json](https://docs.python.org/3/library/json.html)
* [os](https://docs.python.org/3/library/os.html)


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

La aplicació es basa en un programa lecturaBacnet.py, per llegir les dades del bus i guardar-les a la base de dades.
A part també hi ha tres fitxers de configuració per tal de definir les variables necessàries del bus:
* alarmes.json
* consum.json
* estat.json


### Prerequisites

Per fer funcionar l'aplicació és necessari:
* Python 3.8 o superior.
* Tots els paquets necessaris de python esmentats anteriorment.
* Accés a les base de dades dels sistemes de manteniment i producció.
* Comunicació amb els bus BACnet i amb les ip's i identificadors definits com:
  - El dispositiu 100 està confiugrat amb la ip 192.100.101.89/23
  - El dispositiu 101 està confiugrat amb la ip 192.100.101.90/23
  - El dispositiu 102 està confiugrat amb la ip 192.100.101.91/23
  - El dispositiu 103 està confiugrat amb la ip 192.100.101.92/23
  - El dispositiu 104 està confiugrat amb la ip 192.100.101.93/23
  - El dispositiu 105 està confiugrat amb la ip 192.100.101.94/23
    
### Incorporar noves variables
Hi ha una classe per cada fitxer json; Alarmes, Estats i Consums. Per entrar una nova variable s'ha de crear el camp a la base de dades :
* Biomassa
  - alarmes
    - timestamp
    - alarmName
    - missatge
    - alarmValue
    
El programa va comprovant les variables que hi han actives al sistema i les de la base de dades i les va actaulitzant
  - consums 
    - timestamp
    - TCTR_103_CT_01_ME_ENERGIA
    - TCTR_103_CT_02_ME_ENERGIA
    - TCTR_103_CT_05_ME_ENERGIA
    - TCTR_103_CT_03_ME_ENERGIA
    - TCTR_103_CT_01_ME_KG_SEG_PCI
    - TCTR_103_CT_04_ME_ENERGIA
    - TCTR_100_ME_CONTA_GAS
    - TCTR_100_ME_CONTA_AIGUA
    - TCTR_103_CT_01_ME_KGH_SEG_PCI
    - TCTR_103_CT_01_ME_POTENCIA
    - TCTR_103_CT_02_ME_POTENCIA
    - TCTR_103_CT_05_ME_POTENCIA
    - TCTR_103_CT_03_ME_POTENCIA
    - TCTR_103_CT_04_ME_POTENCIA
  - estatTemp
    - timestamp
    - TCTR_106_INT_MCB1_ME_TSOR_AIGUA
    - TCTR_106_INT_MCB2_ME_TSOR_AIGUA
    - TCTR_100_ME_TIMP_ST17_CAS1
    - TCTR_100_ME_TIMP_ST16_CAS2
    - TCTR_100_ME_TDEP_90_ALT
    - TCTR_100_ME_TDEP_80_ALT
    - TCTR_100_XS_TEMP_CALOR_DIPOSIT
    - TCTR_100_XS_DIP_CALOR_SEC
    - TCTR_101_ME_TDEP_7_ALT
    - TCTR_106_INT_MCB1_ME_TCOM_CAMBRE
    - TCTR_106_INT_MCB2_ME_TCOM_CAMBRE
    - TCTR_106_INT_MABS_ME_XSREFEDA
    - TCTR_100_OR_CALD_BIOMASA_CAB01
    - TCTR_100_OR_CALD_BIOMASA_CAB02
    - TCTR_106_INT_MCB1_ES_VENT_COMB
    - TCTR_106_INT_MCB2_ES_VENT_COMB
    - TCTR_100_OR_CALD_GAS_CAG1_1
    - TCTR_100_OR_CALD_GAS_CAG2_1
    - TCTR_100_ME_TEMP_EXT
    - TCTR_100_ME_HUM_EXT
    - TCTR_100_ES_ANTIGEL_PRODUCCIO
    - TCTR_101_OR_REF_ABS
    - TCTR_101_ES_ENF_ABS01
    - TCTR_100_XS_TANTIGEL_PRODUCCIO

<p align="right">(<a href="#top">back to top</a>)</p>



[comment]: <> (<!-- USAGE EXAMPLES -->)

[comment]: <> (## Usage)

[comment]: <> ([comment]: <> &#40;TODO&#41;)

