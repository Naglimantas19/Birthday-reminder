# Birthday-reminder
Kursinis darbas: Birthday reminder

# 🎂 Birthday Reminder – OOP Kursinis Darbas

---

## Turinys
1. Įvadas  
2. Programos naudojimas  
3. Analizė  
4. Rezultatai ir išvados  

---

# 1. Įvadas

## Kas yra ši programa?

Tai Python programa, skirta priminti apie artėjančius gimtadienius.  
Vartotojas gali pridėti, pašalinti gimtadienius, peržiūrėti artėjančius įvykius ir gauti priminimus.

Programa palaiko kelis vartotojus.

---

# 2. Programos naudojimas

## Kaip paleisti programą?

Reikalavimai: Python 3.10 arba naujesnė versija.

---

## Funkcionalumas

- Pridėti gimtadienį  
- Ištrinti gimtadienį  
- Rodyti artėjančius gimtadienius  
- Gauti priminimus  
- Išsaugoti į failą  
- Užkrauti iš failo  

---

# 3. Analizė

## OOP principai

### Encapsulation (Inkapsuliacija)
Naudojami privatūs atributai (`_name`, `_birthday`).

---

### Inheritance (Paveldėjimas)
`ConsoleNotificationSender` paveldi iš `NotificationSender`.

---

### Polymorphism (Polimorfizmas)
Tas pats metodas `send()` veikia skirtingai.

---

### Abstraction (Abstrakcija)
Naudojama bazinė klasė `NotificationSender`.

---

## Design Pattern

Naudojamas **Singleton pattern**.

`ReminderManager` klasė turi tik vieną instanciją visoje programoje.

---

## Kompozicija ir agregacija

- `User` turi `ReminderBook` → kompozicija  
- `ReminderBook` turi `BirthdayEntry` → agregacija  

---

## Failų naudojimas

Duomenys saugomi faile:

---

# 4. Rezultatai ir išvados

## Rezultatai

- Programa veikia stabiliai  
- Gimtadieniai skaičiuojami teisingai  
- Veikia keli vartotojai  
- Failų saugojimas veikia  

---

## Išvados

Šio darbo metu išmokau:
- OOP principus praktikoje  
- Darbą su klasėmis  
- Failų skaitymą ir rašymą  
- Design pattern (Singleton)  

---

## Ateities patobulinimai

- GUI sąsaja  
- Email/SMS priminimai  
- Duomenų bazė vietoj JSON  
