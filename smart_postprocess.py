import re

def smart_postprocess(text):
    """
    Zaawansowana naprawa polskich tablic na podstawie Twoich logów.
    """
    # 1. Podstawowe czyszczenie
    text = re.sub(r'[^A-Z0-9]', '', text.upper())
    
    # 2. Usuwanie "doklejonych" prefiksów (bazując na logach: ISW..., USJ..., EKOS...)
    # Jeśli tekst jest za długi (Polska tablica max 8 znaków, rzadko 9 z błędami), 
    # a zaczyna się od typowych śmieci OCR.
    while len(text) > 7:
        if text[0] in ['I', 'E', 'U', 'L', 'F', '1']: 
            # Uwaga: F usuwamy tylko jeśli to nadmiarowy znak. 
            # Jeśli F zamieniło S (np FTA zamiast STA), obsłużymy to niżej.
            # Sprawdzamy czy po usunięciu zostanie sensowna długość (min 4)
            text = text[1:]
        else:
            break

    # Jeśli po czyszczeniu pusto, zwróć cokolwiek
    if len(text) < 3: return text 

    chars = list(text)

    # 3. Słowniki naprawcze (bazując na Twoich błędach 5->S, F->S)
    
    # Zamienniki dla POZYCJI 0 i 1 (gdzie muszą być litery)
    first_two_chars_map = {
        '0': 'O', 
        '1': 'I', 
        '2': 'Z', 
        '4': 'A', 
        '5': 'S', # Kluczowe: 5H -> SH
        '8': 'B', 
        'F': 'S', # Kluczowe: FTA -> STA, FBL -> SBL
        'D': 'O'
    }

    # Zamienniki dla RESZTY (gdzie preferujemy cyfry, ale mogą być litery)
    rest_chars_map = {
        'O': '0', # Częsty błąd: SG058O1 -> SG05801
        'Q': '0',
        'L': '1', # Czasem myli L z 1
        'Z': '2', # SR881ZP -> SR8817P (ryzykowne, ale Z często jest mylone z 7 lub 2)
        'B': '8'
    }

    # --- REGUŁA 1: PIERWSZE 2 ZNAKI TO LITERY ---
    for i in range(min(2, len(chars))):
        if chars[i] in first_two_chars_map:
            chars[i] = first_two_chars_map[chars[i]]

    # --- REGUŁA 2: OSTATNI ZNAK ---
    # Jeśli ostatni znak to 'O', to prawie na pewno '0' (chyba że krótka tablica)
    # Ale w Twoim logu 'SG058O1' -> O było przedostatnie.
    
    # --- REGUŁA 3: CZYSZCZENIE ŚRODKA (Cyfryzacja) ---
    # Przechodzimy od 3 znaku do końca
    for i in range(2, len(chars)):
        c = chars[i]
        # Jeśli to Q, to zawsze 0
        if c == 'Q': chars[i] = '0'
        # Jeśli to O, a nie jest na końcu (gdzie może być np. wyróżnik), zamień na 0
        if c == 'O' and i < len(chars) - 1: chars[i] = '0'

    return "".join(chars)