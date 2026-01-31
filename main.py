"""
This script provides a command-line interface (CLI) for an AI Prompt Consultant.

It allows users to interact with a Gemini-powered AI model to refine their prompts,
manage API keys, select models, set language preferences, and reset configurations.
The CLI is built using `typer` and `rich` for a rich interactive experience.
"""
import typer
from rich.console import Console
from rich.prompt import Prompt
import os
import sys
from src.agent import PromptConsultant
from src.config import ConfigManager
from src.translation import TranslationManager

app = typer.Typer(
    name="prompt-consultant",
    help="AI Consultant to help you craft the best prompts.",
    add_completion=False
)
console = Console()

@app.command()
def start(
    model: str = typer.Option(None, help="The Gemini model to use. Overrides saved preference."),
    debug: bool = typer.Option(False, help="Enable debug mode."),
    reset: bool = typer.Option(False, help="Reset saved model preference.")
):
    """
    Starts a consultation session with the AI Prompt Consultant.

    Allows the user to interact with the AI to refine prompts.
    Handles initial setup like language selection, API key management,
    and generative model selection. Supports various commands for session control.

    Args:
        model: The Gemini model to use for the session. Overrides saved preference.
        debug: If True, enables debug mode for the consultant.
        reset: If True, resets saved model preference, API key, and language.
    """
    config_manager = ConfigManager()
    
    # --- LANGUAGE SELECTION ---
    if reset:
         config_manager.set_language(None)
    
    language = config_manager.get_language()
    if not language:
        language_choice = Prompt.ask(
            "[bold cyan]Choose your language / Scegli la tua lingua[/bold cyan]", 
            choices=["it", "en"], 
            default="it"
        )
        config_manager.set_language(language_choice)
        language = language_choice
    
    t = TranslationManager(language)

    # --- API KEY MANAGEMENT ---
    if reset:
        config_manager.set_api_key(None)
    
    api_key = config_manager.get_api_key()
    
    # Fallback/Check: API Key MUST be in config.
    if not api_key:
        console.print(t.get("api_key_missing_config"))
        api_key = Prompt.ask(t.get("api_key_prompt"), password=True)
        if not api_key:
            console.print(t.get("api_key_required"))
            raise typer.Exit(code=1)
        config_manager.set_api_key(api_key)
        console.print(t.get("api_key_saved"))

    # --- MODEL SELECTION ---
    if reset:
        console.print(t.get("model_reset"))
        model = None
    
    if not model:
        saved_model = config_manager.get_model()
        if saved_model and not reset:
            model = saved_model
            console.print(t.get("model_in_use", model=model))
        else:
            console.print(t.get("choose_model"))
            # Updated Model List
            models = [
                "gemini-2.5-flash",
                "gemini-2.5-pro",
                "gemini-2.5-flash-lite",
                "gemini-2.0-flash", 
                "gemini-3-flash-preview",
                "gemma-3-27b-it"
            ]
            for idx, m in enumerate(models, 1):
                clean_name = m.split()[0] 
                console.print(f"{idx}. {m}")
            
            console.print(f"{len(models)+1}. {t.get('manual_entry')}")

            choice = Prompt.ask(t.get("enter_number"), choices=[str(i) for i in range(1, len(models)+2)], default="1")
            
            if int(choice) <= len(models):
                model = models[int(choice)-1].split()[0]
            else:
                model = Prompt.ask(t.get("enter_model_name"))
            
            config_manager.set_model(model)
            console.print(t.get("model_saved", model=model))

    console.print(t.get("welcome"))
    console.print(t.get("intro"))
    console.print(t.get("commands_help"))

    # Pass TranslationManager to Consultant
    consultant = PromptConsultant(api_key=api_key, model_name=model, debug=debug, translation_manager=t)
    
    first_turn = True

    # Unified Interaction Loop
    while True:
        if first_turn:
            user_input = Prompt.ask(t.get("initial_idea")).strip()
        else:
            user_input = Prompt.ask(t.get("user_label")).strip()
        
        # --- COMMAND HANDLING ---
        
        # Exit
        if user_input.lower() in ["exit", "quit", "basta", "esci", "/exit"]:
            console.print(t.get("goodbye"))
            break
            
        # Set API Key
        if user_input.lower().startswith("/set-apikey"):
            new_key = Prompt.ask(t.get("api_key_prompt_new"), password=True)
            if new_key:
                config_manager.set_api_key(new_key)
                # Re-init client
                from google import genai
                consultant.api_key = new_key
                consultant.client = genai.Client(api_key=new_key)
                console.print(t.get("api_key_updated"))
            continue

        # Set Model
        if user_input.lower().startswith("/set-model"):
            console.print(t.get("available_models"))
            models = [
                "gemini-2.5-flash",
                "gemini-2.5-pro",
                "gemini-2.5-flash-lite",
                "gemini-2.0-flash", 
                "gemini-3-flash-preview",
                "gemma-3-27b-it"
            ]
            for idx, m in enumerate(models, 1):
                console.print(f"{idx}. {m}")
            console.print(f"{len(models)+1}. {t.get('manual_selection')}")
            
            c = Prompt.ask(t.get("choice"), choices=[str(i) for i in range(1, len(models)+2)])
            if int(c) <= len(models):
                new_model = models[int(c)-1]
            else:
                new_model = Prompt.ask(t.get("enter_model_name"))
            
            config_manager.set_model(new_model)
            # Update running instance
            consultant.update_model(new_model)
            console.print(t.get("model_updated", model=new_model))
            continue
        
        # Set Language
        if user_input.lower().startswith("/set-language"):
            console.print("[cyan]Languages / Lingue:[/cyan]")
            console.print("1. Italiano (it)")
            console.print("2. English (en)")
            
            lang_choice = Prompt.ask("Scelta / Choice", choices=["1", "2"], default="1")
            new_lang = "it" if lang_choice == "1" else "en"
            
            config_manager.set_language(new_lang)
            t.load_translations(new_lang)
            consultant.translation_manager = t 
            consultant.start_new_session() 
            
            if new_lang == "it":
                 console.print("[green]Lingua impostata su Italiano![/green]")
            else:
                 console.print("[green]Language set to English![/green]")
            continue
            
        # Reset
        if user_input.lower().startswith("/reset"):
            confirm = Prompt.ask(t.get("reset_confirm"), choices=["y", "n", "s"], default="n")
            if confirm.lower() in ["y", "s"]:
                config_manager.clear_config()
                console.print(t.get("reset_done"))
                raise typer.Exit()
            else:
                console.print(t.get("reset_cancel"))
            continue

        # Catch-all for unknown slash commands
        if user_input.startswith("/"):
            console.print(t.get("unknown_command", command=user_input))
            console.print(t.get("available_commands"))
            continue

        # --- AI INTERACTION ---
        with console.status(t.get("thinking"), spinner="dots"):
             if first_turn:
                 response = consultant.start_consultation(user_input)
                 first_turn = False
             else:
                 response = consultant.chat(user_input)
        
        console.print(f"{t.get('consultant_label')}{response}")

if __name__ == "__main__":
    """
    Entry point for the Typer CLI application.

    Initializes and runs the main application, enabling command-line interactions.
    """
    app()
