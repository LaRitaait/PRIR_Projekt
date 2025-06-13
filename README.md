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

- Frontend (Flask)
Odpowiada za interfejs użytkownika. Umożliwia wprowadzanie adresów URL, wybór profilu danych oraz przeglądanie wyników.

- Silnik (FastAPI + multiprocessing + asyncio)
Odpowiada za pobieranie i przetwarzanie danych z podanych stron internetowych. Wykorzystuje asynchroniczność (aiohttp, asyncio) oraz przetwarzanie wieloprocesowe (multiprocessing) do równoległego scrapowania.

- Baza danych (MongoDB)
Przechowuje zebrane dane z podziałem na adresy e-mail, numery telefonów, adresy pocztowe i linki społecznościowe.
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

## Wykonanie

- Interfejs użytkownika
  
![image](https://github.com/user-attachments/assets/b25b1585-1873-4e06-9113-aed28d9316eb)

- Wyniki po kliknięciu "Rozpocznij"
  
![image](https://github.com/user-attachments/assets/bc6f63e5-b241-4045-8488-5e9f26ad8383)

---

## 🚀 Jak uruchomić

- git clone https://github.com/LaRitaait/PRIR_Projekt.git
- cd PRIR_Projekt
- docker-compose up --build

