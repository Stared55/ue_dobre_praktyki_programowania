# 🚗 Automatic License Plate Recognition (ALPR)

Projekt realizujący detekcję oraz rozpoznawanie tekstu (OCR) na polskich tablicach rejestracyjnych. Rozwiązanie opiera się na bibliotece **EasyOCR** i zawiera wbudowany moduł automatycznej oceny jakości algorytmu (dokładność vs czas przetwarzania).

---

## 📋 Opis projektu

Głównym celem projektu jest stworzenie systemu, który:
1. **Lokalizuje** tablicę rejestracyjną na zdjęciu (Detekcja).
2. **Odczytuje** numer rejestracyjny (OCR).
3. **Weryfikuje** wyniki względem bazy danych (Ground Truth z plików XML).
4. **Ocenia** działanie algorytmu na podstawie wzoru uwzględniającego dokładność i czas działania.

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

### 1. IoU (Intersection over Union)
Mierzy precyzję detekcji ramki tablicy.

$$IoU = \frac{\text{Obszar Wspólny}}{\text{Całkowity Obszar Ramek}}$$

* **Wynik > 0.5** uznawany jest za poprawną detekcję.

## 👥 Autorzy
* Radosław Staroszyński
* Piotr Stefański (Właściciel datasetu)