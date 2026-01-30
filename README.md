# AI Prompt Consultant 🤖✨

**AI Prompt Consultant** è un potente strumento CLI (Command Line Interface) scritto in Python che agisce come un **Senior Prompt Engineer**. Utilizza l'intelligenza artificiale di Google Gemini per aiutarti a raffinare, strutturare e ottimizzare i tuoi prompt tramite un processo di intervista interattiva.

## 🚀 Funzionalità Principali

- **Prompt Engineering Assistito**: Un'AI esperta che ti pone domande mirate per migliorare la tua idea iniziale.
- **Multilingua**: Supporto completo per **Italiano** (default) e **Inglese**. L'interfaccia e l'AI si adattano alla lingua scelta.
- **Zero-Config Setup**: Niente file `.env` complessi. Al primo avvio, il tool ti guida nella configurazione di API Key e preferenze.
- **Persistenza**: Salva automaticamente la tua API Key, il modello preferito e la lingua in `config.json`.
- **Supporto Modelli Next-Gen**: Compatibile con gli ultimi modelli Google (`gemini-2.5-flash`, `gemini-2.5-pro` e altri).
- **Slash Commands**: Comandi rapidi per modificare le impostazioni al volo durante la conversazione.

## 🛠️ Installazione

### Prerequisiti

- Python 3.10 o superiore.
- Una API Key di Google AI Studio (ottenibile [qui](https://aistudio.google.com/)).

### Setup

1.  Clona la repository (o scarica i file).
2.  Installa le dipendenze:
    ```bash
    pip3 install -r requirements.txt
    ```

## 💻 Utilizzo

Esegui il programma dal terminale:

```bash
python3 main.py
```

### Primo Avvio

Se è la prima volta che lo esegui, il tool ti chiederà:

1.  La lingua preferita (IT/EN).
2.  La tua Google Gemini API Key.
3.  Il modello da utilizzare (es. `gemini-2.5-flash`).

Queste informazioni verranno salvate per i futuri utilizzi.

### Flusso di Lavoro

1.  **Idea Iniziale**: Descrivi brevemente cosa vuoi ottenere (es. "Voglio un prompt per scrivere un articolo SEO").
2.  **Intervista**: L'AI ti farà 1-3 domande alla volta per chiarire il contesto, il target, il tono e i vincoli.
3.  **Generazione**: Una volta raccolti abbastanza dettagli, l'AI genererà un **Prompt Ottimizzato** pronto per essere copiato e incollato.

## ⚡ Comandi Disponibili (Slash Commands)

Durante la conversazione, puoi usare i seguenti comandi speciali:

| Comando         | Descrizione                                                                                    |
| :-------------- | :--------------------------------------------------------------------------------------------- |
| `/set-model`    | Cambia il modello AI utilizzato (es. da Flash a Pro).                                          |
| `/set-apikey`   | Aggiorna la tua API Key salvata.                                                               |
| `/set-language` | Cambia la lingua dell'interfaccia e dell'AI (IT 🇮🇹 / EN 🇬🇧).                                   |
| `/reset`        | Cancella **tutte** le impostazioni salvate e chiude il programma. Utile per ripartire da zero. |
| `/exit`         | Termina la sessione e chiude il programma.                                                     |

## ⚙️ Configurazione Avanzata

Tutte le preferenze sono salvate nel file local `config.json`.
Non è necessario modificarlo manualmente, ma ecco come appare:

```json
{
	"model": "gemini-2.5-flash",
	"api_key": "AIzaSy...",
	"language": "it"
}
```

Per lanciare il programma ignorando le preferenze salvate (senza cancellarle):

```bash
python3 main.py --reset
```

_(Nota: Il flag `--reset` agisce solo per la sessione corrente. Per cancellare definitivamente, usa il comando `/reset` dentro l'app)._

## 🐞 Risoluzione Problemi

- **Errore 404 (Modello non trovato)**: Assicurati di usare un nome modello valido (es. `gemini-1.5-flash`, `gemini-2.5-flash`). Usa `/set-model` per cambiarlo.
- **Comando non riconosciuto**: Assicurati di scrivere il comando correttamente (es. `/exit` e non `exit` o `/esci`).
- **Problemi API Key**: Se la chiave è scaduta, usa `/set-apikey` per inserirne una nuova.

---

_Creato con ❤️ e 🤖_
