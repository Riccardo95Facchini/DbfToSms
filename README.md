<!--
*** Many thanks for README template to Othneil Drew: https://github.com/othneildrew
*** Taken from: https://github.com/othneildrew/Best-README-Template
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Riccardo95Facchini/DbfToSms)

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a>
    <img src="./Android.py.png" alt="Logo" width="100" height="100">
  </a>

  <h3 align="center">DBF to SMS</h3>

  <p align="center">
    A mostly automated system to send SMS from data in DBF files.
    <br />
  </p>
</p>

<!-- ABOUT THE PROJECT -->
## About The Project

An individual project made to automate sending SMS messages to customers of a shop.<br/>
This also served as a learning experience being my first Python project.

The project is composed by two sub-projects: a [Python script](https://github.com/Riccardo95Facchini/DbfToSms/tree/master/Python_Script) in charge of the SQLite database parsed by reading the DBF files, it then formats the information and delivers it via sockets to an [Android application](https://github.com/Riccardo95Facchini/DbfToSms/tree/master/Android_App) that will send the SMS messages to the customers. The Python script also manages a small SQLite database.

### Built With
* [PyCharm](https://www.jetbrains.com/pycharm/)
* [Android Studio](https://developer.android.com/studio)
* [SQLite](https://www.sqlite.org/index.html)

<!-- CONTACT -->
## Contact

Riccardo Facchini - [LinkedIn](https://www.linkedin.com/in/riccardo-facchini-1a8206194/) - riccardo95facchini@gmail.com

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Riccardo95Facchini/DbfToSms
[contributors-url]: https://github.com/Riccardo95Facchini/DbfToSms/graphs/contributors
[license-shield]: https://img.shields.io/github/license/Riccardo95Facchini/DbfToSms
[license-url]: https://github.com/Riccardo95Facchini/DbfToSms/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=2867B2
[linkedin-url]: https://linkedin.com/in/riccardo-facchini-1a8206194
