# Birthday-reminder
Kursinis darbas: Birthday reminder

# Birthday Reminder – OOP Kursinis Darbas

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

## Kaip paleisti?

Reikalavimai: Python 3.10 arba naujesnė versija.

```bash
python main.py
```

## Funkcionalumas

* Pridėti gimtadienį
* Ištrinti gimtadienį
* Rodyti artėjančius gimtadienius
* Gauti priminimus
* Išsaugoti į failą
* Užkrauti iš failo

---

# 3. Analizė

## Projekto struktūra

Projektas suskirstytas į atskirus failus:

```
birthday_reminder/
│
├── main.py              (pagrindinis paleidimo failas)
├── manager.py           (ReminderManager klasė – Singleton)
├── user.py              (User klasė)
├── reminder_book.py     (Birthday sąrašas)
├── birthday_entry.py    (vienas gimtadienis)
├── notification.py      (pranešimų sistema)
└── birthdays.json       (duomenų saugojimas)
```

---

## OOP principai

### Abstrakcija

Programa slepia sudėtingą logiką ir vartotojui pateikia paprastas funkcijas (pvz. pridėti gimtadienį).

---

### Inkapsuliacija

Duomenys saugomi klasėse ir pasiekiami per metodus (pvz. `user.get_upcoming_birthdays()`).

---

### Paveldėjimas

Naudojamas, jei klasės išplečia kitas (pvz. notification sistemoje).

---

### Polimorfizmas

Skirtingi objektai gali naudoti tuos pačius metodus, bet veikti skirtingai.

---

## Design Pattern – Singleton

Naudojamas **ReminderManager** klasėje.

Tikslas: turėti tik vieną objektą visoje programoje.

```python
manager1 = ReminderManager()
manager2 = ReminderManager()

print(manager1 is manager2)  # True
```

Tai reiškia, kad visi vartotojai naudoja tą patį managerį.

---

## Kompozicija ir agregacija

### Kompozicija

User turi savo gimtadienių sąrašą.

Jei user ištrinamas – jo duomenys dingsta.

---

### Agregacija

ReminderManager saugo visus vartotojus.

Vartotojai gali egzistuoti atskirai.

---

## Darbas su failais

Programa saugo duomenis į JSON failą:

```python
save_to_file()
load_from_file()
```

---

# 4. Rezultatai ir išvados

## Rezultatai

* Sukurta veikianti gimtadienių priminimo sistema
* Palaikomi keli vartotojai
* Įgyvendinti visi OOP principai
* Duomenys išsaugomi ir užkraunami iš failo
* Veikia priminimų sistema

---

## Išvados

Šio darbo metu buvo sukurtas pilnai veikiantis projektas, kuriame pritaikyti objektinio programavimo principai.
Kiekviena klasė atlieka savo funkciją, o visa sistema veikia kaip vienas vienetas.




