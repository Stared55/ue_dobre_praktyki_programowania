# 🚗 Automatic License Plate Recognition (ALPR)

Projekt realizujący detekcję oraz rozpoznawanie tekstu (OCR) na polskich tablicach rejestracyjnych. Rozwiązanie opiera się na bibliotece **EasyOCR** i zawiera wbudowany moduł automatycznej oceny jakości algorytmu (dokładność vs czas przetwarzania).

---

## 📋 Opis projektu

Głównym celem projektu jest stworzenie systemu, który:
1. **Lokalizuje** tablicę rejestracyjną na zdjęciu (Detekcja).
2. **Odczytuje** numer rejestracyjny (OCR).
3. **Weryfikuje** wyniki względem bazy danych (Ground Truth z plików XML).
4. **Ocenia** działanie algorytmu na podstawie wzoru uwzględniającego dokładność (70%) i czas działania (30%).

## 🛠️ Technologie

* **Python 3.13**
* **EasyOCR** (Silnik OCR oparty na Deep Learningu)
* **OpenCV** (Przetwarzanie obrazu)
* **XML ElementTree** (Parsowanie adnotacji)

## 📂 Struktura katalogów

Aby projekt działał poprawnie, pliki muszą być ułożone w następujący sposób:

```text
├── main.py                # Główny skrypt uruchamiający testy
├── README.md              # Dokumentacja projektu
└── raw_data/              # Folder z danymi
    └── annotations/   
        ├── annotations.xml    # Plik z adnotacjami (Ground Truth)
    └── photos/
        ├── 1.jpg              # Zdjęcia pojazdów...
        ├── 2.jpg
        └── ...
```

## 🚀 Instalacja i Uruchomienie

1. **Sklonuj repozytorium** (lub pobierz pliki).
2. **Zainstaluj wymagane biblioteki**:

```bash
pip install easyocr opencv-python-headless numpy lxml
```

*(Uwaga dla użytkowników macOS: Jeśli wystąpi błąd SSL, uruchom skrypt `Install Certificates.command` w folderze instalacyjnym Pythona).*

3. **Uruchom projekt**:

```bash
python3 main.py
```

## 📊 Metodyka Oceny

Skrypt automatycznie dzieli zbiór danych (losowe 30% do testów) i wylicza następujące miary:

### 1. IoU (Intersection over Union)
Mierzy precyzję detekcji ramki tablicy.

$$IoU = \frac{\text{Obszar Wspólny}}{\text{Całkowity Obszar Ramek}}$$

* **Wynik > 0.5** uznawany jest za poprawną detekcję.

### 2. Algorytm Oceny Końcowej
Ocena (2.0 - 5.0) wyliczana jest na podstawie funkcji wagowej:

* **Waga Dokładności (Accuracy):** 0.7 (wymagane min. 60%)
* **Waga Czasu (Time):** 0.3 (wymagane max. 60s na 100 zdjęć)

$$Score = 0.7 \cdot Norm(Accuracy) + 0.3 \cdot Norm(Time)$$
$$Grade = 2.0 + 3.0 \cdot Score$$

## 📈 Przykładowy Wynik (Log)

```text
Liczba zdjęć w bazie: 195
Liczba zdjęć do testu (30%): 58
--------------------------------------------------
[1/58] Plik: 117.jpg | Prawda: SK8843W | Wykryto: SK8843W | IoU: 0.79 | OK
[2/58] Plik: 92.jpg  | Prawda: SK192TF | Wykryto: SK1P2TF | IoU: 0.78 | X
...
--------------------------------------------------
WYNIKI KOŃCOWE:
Dokładność (Accuracy): 85.00%
Średnie IoU (Detection): 0.81
Czas testu: 14.50s
Przewidywany czas dla 100 zdjęć: 25.00s

OCENA PROJEKTU: 4.5
```

## 👥 Autorzy
* Radosław Staroszyński
* Piotr Stefański (Właściciel datasetu)