# 🌐 Web Data Crawler – Projekt semestralny PRiR
Zofia Głowacka, 21234

Aplikacja rozproszona do automatycznego pobierania, selekcji i zapisu danych z witryn internetowych, stworzona w ramach przedmiotu **Przetwarzanie równoległe i rozproszone (PRiR)**.

---

## 📌 Opis projektu

Projekt opiera się na architekturze mikroserwisowej i pozwala użytkownikowi:

- podać adresy URL do przeszukania,
- wybrać **profil danych** do ekstrakcji,
- uruchomić **asynchroniczny i wieloprocesowy crawler**,
- obejrzeć wyniki w graficznym interfejsie webowym (Flask),
- dane są zapisywane w bazie danych **MongoDB**.

---

## 🔍 Profile danych (do wyboru)

- 📧 Adresy e-mail
- ☎️ Numery telefonów
- 🏠 Adresy pocztowe
- 🌐 Linki do mediów społecznościowych

---

## 🧱 Architektura

Projekt składa się z trzech głównych modułów, każdy uruchamiany w osobnym kontenerze Docker:

---

## ⚙️ Technologie

- **Python 3.11**
- **Flask** – frontend (UI)
- **FastAPI** – backend API
- **MongoDB** – baza danych
- **BeautifulSoup** – parsowanie HTML
- **aiohttp** – pobieranie asynchroniczne
- **multiprocessing** – równoległe przetwarzanie
- **Docker + docker-compose** – konteneryzacja

---

## 🚀 Jak uruchomić

   git clone https://github.com/LaRitaait/PRIR_Projekt.git
   cd prir
   docker-compose up --build

