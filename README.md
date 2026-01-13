# 🚀 Mikroserwisy z RabbitMQ: Instrukcja Uruchomienia

Ten projekt demonstruje komunikację między mikroserwisami przy użyciu **RabbitMQ**.

Składa się z trzech głównych elementów:
1.  **Service A (Producer):** API (FastAPI), które przyjmuje żądania HTTP i wysyła zadania do kolejki.
2.  **RabbitMQ:** Broker wiadomości (pośrednik).
3.  **Service B (Consumer/Worker):** Serwis przetwarzający zadania w tle (odbiera wiadomości z kolejki).

---

## 📋 Wymagania

* Zainstalowany **Docker**
* Zainstalowany **Docker Compose**

---

## 🛠️ Krok 1: Uruchomienie (Clean Start)

Jeśli masz już uruchomione kontenery lub chcesz mieć pewność, że wszystko jest aktualne, wykonaj poniższe kroki.

1.  Otwórz terminal w głównym folderze projektu.
2.  Zatrzymaj stare kontenery i usuń je:
    ```bash
    docker-compose down
    ```
3.  Zbuduj i uruchom system (flaga `--build` wymusza aktualizację obrazów):
    ```bash
    docker-compose up --build
    ```

**Oczekiwanie:**
Po uruchomieniu poczekaj około 15-30 sekund, aż RabbitMQ w pełni wystartuje. W logach powinieneś zobaczyć:
* `Application startup complete` (dla Service A)
* `Server startup complete` (dla RabbitMQ)

---

## 🧪 Krok 2: Testowanie

1.  Wejdź na adres: **http://localhost:8001/docs**
2.  Wejdź na adres: **http://localhost:8002/docs**
