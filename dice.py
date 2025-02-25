# Importiere benötigte Module
import tkinter as tk                               # Tkinter für die GUI
from tkinter import Frame, Label, Button, Entry, messagebox, colorchooser  # Wichtige Tkinter-Widgets und -Funktionen
import random                                      # Zufallszahlengenerator für das Würfeln
import math                                        # Mathematische Funktionen (z.B. ceil)
import matplotlib.pyplot as plt                    # Plotting-Bibliothek für die grafische Darstellung der Würfel
import numpy as np                                 # Numpy wird hier eventuell benötigt (z.B. für Berechnungen)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Integration von Matplotlib in Tkinter

# Versuche, das Modul number_entry zu importieren, das benutzerdefinierte Eingabefelder (IntEntry) bereitstellt.
try:
    from number_entry import IntEntry
except ImportError:
    # Zeige eine Fehlermeldung an und beende das Programm, wenn das Modul nicht gefunden wird.
    messagebox.showerror("Error", "number_entry module is missing.")
    exit()

# Globale Variablen, die später für die Berechnung der Zellenmaße im Ergebnisbereich verwendet werden
cell_width = 0
cell_height = 0
# Faktoren, die angeben, welcher Anteil der Zellenbreite bzw. -höhe für die Würfelzeichnung genutzt wird.
dice_area_width_factor = 0.9   # 90% der Zellenbreite wird verwendet
dice_area_height_factor = 0.5  # 50% der Zellenhöhe wird verwendet

def draw_dice_face(ax, number, dice_color, text_color, use_dots=False):
    """
    Zeichnet die Darstellung eines einzelnen Würfels auf der gegebenen Matplotlib-Achse (ax).

    Parameter:
      ax         - Matplotlib-Achse, auf der gezeichnet wird
      number     - Die gewürfelte Zahl
      dice_color - Hintergrundfarbe des Würfels
      text_color - Farbe für die Zahl oder die Punkte
      use_dots   - Wenn True, wird statt der Zahl ein Punktmuster (typische Würfelaugen) gezeichnet
    """
    # Lösche den aktuellen Inhalt der Achse
    ax.clear()
    # Entferne Achsenticks, damit die Darstellung sauber bleibt
    ax.set_xticks([])
    ax.set_yticks([])
    # Setze die Grenzen der Achse (hier als feste Werte gewählt)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 0.5)
    # Setze die Hintergrundfarbe der Achse auf die gewählte Würfelfarbe
    ax.set_facecolor(dice_color)

    # Wenn use_dots aktiviert ist und somit Würfelpunkte statt einer Zahl gezeichnet werden sollen:
    if use_dots:
        # Definiere die Positionen (Pip-Positionen) für die typischen Würfelaugen
        pip_positions = {
            1: [(0.25, 0.25)],  # Ein einzelner Punkt in der Mitte
            2: [(0.1, 0.4), (0.4, 0.1)],  # Zwei Punkte diagonal zueinander
            3: [(0.1, 0.4), (0.25, 0.25), (0.4, 0.1)],  # Drei Punkte (diagonal mit einem in der Mitte)
            4: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.1), (0.4, 0.1)],  # Vier Punkte an den Ecken
            5: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.1), (0.4, 0.1), (0.25, 0.25)],  # Vier Ecken plus ein mittlerer Punkt
            6: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.25), (0.4, 0.25), (0.1, 0.1), (0.4, 0.1)]  # Sechs Punkte in zwei Reihen
        }
        # Hole die Punktpositionen für die gewürfelte Zahl; falls die Zahl nicht definiert ist, verwende einen einzelnen Punkt
        dots = pip_positions.get(number, [(0.25, 0.25)])
        # Zeichne jeden Punkt als kleinen Kreis auf der Achse
        for (x, y) in dots:
            circle = plt.Circle((x, y), 0.04, color=text_color)
            ax.add_artist(circle)
    else:
        # Wenn use_dots False ist, zeige einfach die Zahl in der Mitte des Würfels an.
        ax.text(0.25, 0.25, str(number), fontsize=16, ha='center', va='center',
                fontweight='bold', color=text_color)

def roll_single_set(result_frame, dice_count, dice_sides, set_name, dice_color, number_color):
    """
    Würfelt einen einzelnen Set und zeigt die Ergebnisse grafisch an.

    Parameter:
      result_frame - Das Tkinter-Frame, in dem das Ergebnis (die Würfelbilder) dargestellt wird
      dice_count   - Eingabefeld für die Anzahl der zu würfelnden Würfel
      dice_sides   - Eingabefeld für die Anzahl der Seiten des Würfels
      set_name     - Name des Sets (wird zur Beschriftung verwendet)
      dice_color   - Hintergrundfarbe des Würfels
      number_color - Farbe der angezeigten Zahl bzw. der Würfelpunkte
    """
    # Entferne alle bisherigen Widgets im Ergebnisbereich, um einen sauberen Start zu haben
    for widget in result_frame.winfo_children():
        widget.destroy()
    
    try:
        # Lese die Werte für Seitenzahl und Anzahl der Würfel aus den Eingabefeldern aus
        sides_val = dice_sides.get()
        count_val = dice_count.get()
        # Überprüfe, ob die Eingaben im erlaubten Bereich liegen (Seiten: 2-50, Würfelanzahl: 1-12)
        if not (2 <= sides_val <= 50) or not (1 <= count_val <= 12):
            raise ValueError
        # Erzeuge eine Liste von Zufallszahlen, die die Ergebnisse des Würfelwurfs darstellen
        rolls = [random.randint(1, sides_val) for _ in range(count_val)]
    except ValueError:
        # Falls ein Fehler bei der Eingabe auftritt, zeige eine Fehlermeldung an
        messagebox.showerror("Input Error", "Bitte gültige Werte für Seiten (2-50) und Anzahl der Würfel (1-12) eingeben.")
        return

    # Bestimme, wie viele Würfel pro Zeile gezeichnet werden sollen.
    # Hier werden maximal 6 Würfel pro Zeile dargestellt.
    dice_cols = min(6, count_val)
    # Berechne die benötigte Zeilenanzahl basierend auf der Gesamtzahl der Würfel
    dice_rows = math.ceil(count_val / 6)

    # Berechne die Größe eines einzelnen Würfels in Pixeln basierend auf der aktuellen Fenstergröße und den definierten Faktoren
    die_size_pixels = min((cell_width * dice_area_width_factor) / dice_cols,
                          (cell_height * dice_area_height_factor) / dice_rows)
    # Konvertiere die Pixel in Inches, da Matplotlib mit Inches arbeitet (bei 100 dpi entspricht 1 inch 100 Pixel)
    fig_width = (die_size_pixels * dice_cols) / 100
    fig_height = (die_size_pixels * dice_rows) / 100

    # Erzeuge eine Matplotlib-Figur mit einem Raster (Subplots), das die Anordnung der Würfel definiert
    fig, axes = plt.subplots(dice_rows, dice_cols, figsize=(fig_width, fig_height), dpi=100)
    # Passe die Achsen in eine Liste um, egal ob es sich um einen einzelnen Plot oder mehrere handelt
    if dice_rows * dice_cols == 1:
        axes = [axes]
    elif dice_rows == 1 or dice_cols == 1:
        axes = list(axes)
    else:
        # Wenn es mehrere Zeilen und Spalten gibt, flache die 2D-Liste in eine eindimensionale Liste ab
        axes = [ax for row in axes for ax in row]

    # Entscheide, ob das Punktmuster (Würfelaugen) verwendet wird.
    # Wenn die Anzahl der Seiten kleiner oder gleich 6 ist, wird use_dots True gesetzt.
    use_dots = (sides_val <= 6)
    # Zeichne jeden Würfel auf einer separaten Achse
    for ax, roll in zip(axes, rolls):
        draw_dice_face(ax, roll, dice_color, number_color, use_dots=use_dots)
    # Blende überzählige Achsen (falls vorhanden) aus, falls nicht alle Subplots benötigt werden
    for ax in axes[len(rolls):]:
        ax.set_visible(False)
    
    # Binde die Matplotlib-Figur in das Tkinter-Frame ein
    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.get_tk_widget().pack(pady=5)
    canvas.draw()
    
    # Wenn mehr als ein Würfel geworfen wurde, zeige zusätzlich das Gesamtergebnis an
    if count_val > 1:
        total = sum(rolls)
        Label(result_frame, text=f"Gesamtergebnis: {total}", font=("Arial", 12, "bold")).pack(pady=5)

def confirm_sets():
    """
    Liest die vom Benutzer eingegebene Anzahl an Sets aus, validiert diese,
    erstellt für jedes Set ein eigenes Konfigurationsfeld und speichert die Sets global.
    """
    try:
        # Lese die Anzahl der Sets aus dem entsprechenden Eingabefeld
        num_sets = enter_set.get()
        # Überprüfe, ob die Anzahl der Sets im erlaubten Bereich liegt (zwischen 1 und 12)
        if not (1 <= num_sets <= 12):
            raise ValueError
    except:
        # Zeige eine Fehlermeldung, wenn die Eingabe ungültig ist
        messagebox.showerror("Fehler", "Bitte eine gültige Anzahl von Sets (1-12) eingeben.")
        return

    # Definiere die globale Variable "sets" neu
    global sets
    sets = []
    # Lösche alle bisherigen Konfigurationen aus dem Grid-Frame
    for widget in grid_frame.winfo_children():
        widget.destroy()
    
    # Erstelle für jedes Set ein eigenes Frame mit Eingabefeldern
    # Die Sets werden in einem Grid angeordnet, wobei maximal 4 Zeilen pro Spalte angezeigt werden
    for i in range(num_sets):
        # Erstelle ein Frame für das Set mit Rahmen und Padding
        set_frame = Frame(grid_frame, bd=1, relief="groove", padx=5, pady=5)
        # Positioniere das Frame im Grid (Reihen- und Spaltenindex werden dynamisch berechnet)
        set_frame.grid(row=i % 4, column=i // 4, padx=10, pady=10, sticky="nsew")
        
        # Eingabefeld für den Namen des Sets
        Label(set_frame, text=f"Set {i+1} Name:").grid(row=0, column=0, sticky="w")
        set_name = Entry(set_frame, width=15)
        set_name.grid(row=0, column=1, padx=5, pady=2)
        
        # Eingabefeld für die Anzahl der Würfel in diesem Set
        Label(set_frame, text="Anzahl Würfel (max. 12):").grid(row=1, column=0, sticky="w")
        dice_count = IntEntry(set_frame, width=5, lower_bound=1, upper_bound=12)
        dice_count.grid(row=1, column=1, padx=5, pady=2)
        
        # Eingabefeld für die Anzahl der Seiten pro Würfel
        Label(set_frame, text="Anzahl Seiten (max. 50):").grid(row=2, column=0, sticky="w")
        dice_sides = IntEntry(set_frame, width=5, lower_bound=2, upper_bound=50)
        dice_sides.grid(row=2, column=1, padx=5, pady=2)
        
        # Farbauswahl für die Würfelfarbe:
        Label(set_frame, text="Würfelfarbe:").grid(row=3, column=0, sticky="w")
        dice_color_label = Label(set_frame, text=" ", width=8, relief="solid", bg="white")
        dice_color_label.grid(row=3, column=1, padx=5, pady=2)
        # Button, der einen Farbdialog öffnet, um die Würfelfarbe auszuwählen
        Button(set_frame, text="Wählen", 
               command=lambda lbl=dice_color_label: lbl.config(bg=colorchooser.askcolor()[1] or "white")
        ).grid(row=3, column=2, padx=5, pady=2)
        
        # Farbauswahl für die Farbe der angezeigten Zahl bzw. Punkte:
        Label(set_frame, text="Zahlenfarbe:").grid(row=4, column=0, sticky="w")
        text_color_label = Label(set_frame, text=" ", width=8, relief="solid", bg="black")
        text_color_label.grid(row=4, column=1, padx=5, pady=2)
        Button(set_frame, text="Wählen", 
               command=lambda lbl=text_color_label: lbl.config(bg=colorchooser.askcolor()[1] or "black")
        ).grid(row=4, column=2, padx=5, pady=2)
        
        # Füge die Konfiguration dieses Sets zur globalen Liste hinzu
        sets.append((set_name, dice_count, dice_sides, dice_color_label, text_color_label))

def show_dice_results():
    """
    Zeigt die Ergebnisse des Würfelns an, indem die Einstellungen ausgeblendet
    und die Ergebnis-Frames für jedes Set im Hauptfenster angezeigt werden.
    """
    # Blende das Einstellungs-Frame aus
    settings_frame.pack_forget()
    # Lösche vorherige Ergebnisanzeigen
    for widget in results_menu.winfo_children():
        widget.destroy()
    
    # Passe die Fenstergröße automatisch an die Bildschirmgröße und die Anzahl der Sets an
    n_sets = len(sets)
    # Bestimme die Anzahl der Zeilen: wenn mindestens 3 Sets vorhanden sind, werden 3 Zeilen verwendet, sonst so viele Sets wie vorhanden
    n_rows = 3 if n_sets >= 3 else n_sets
    # Bestimme die Anzahl der Spalten, sodass alle Sets untergebracht werden (Aufrunden)
    n_columns = math.ceil(n_sets / 3)
    # Lese die Bildschirmgröße aus
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Definiere die gewünschte Fenstergröße mit etwas Rand (50 bzw. 100 Pixel abgezogen)
    desired_width = screen_width - 50
    desired_height = screen_height - 100
    # Berechne die Zellengröße für jeden Set-Bereich
    global cell_width, cell_height
    cell_width = desired_width / n_columns
    cell_height = desired_height / n_rows
    # Setze die Fenstergröße
    root.geometry(f"{desired_width}x{desired_height}")
    
    # Erstelle einen Header-Bereich mit einem Button, um zurück zu den Einstellungen zu wechseln
    header_frame = Frame(results_menu)
    header_frame.pack(side="top", fill="x", pady=5)
    Button(header_frame, text="Zurück zu den Einstellungen", command=show_settings).pack(padx=5, pady=5)
    
    # Erstelle einen Inhaltsbereich, in dem die einzelnen Set-Ergebnisse dargestellt werden
    content_frame = Frame(results_menu)
    content_frame.pack(fill="both", expand=True)
    
    # Für jedes Set wird ein eigenes Frame erstellt und die Würfel werden darin dargestellt
    for i, (set_name, dice_count, dice_sides, dice_color_label, text_color_label) in enumerate(sets):
        # Erstelle ein Frame mit fester Größe für das Set
        set_frame = Frame(content_frame, bd=1, relief="groove", width=int(cell_width), height=int(cell_height))
        set_frame.grid_propagate(False)  # Verhindere, dass sich das Frame automatisch an den Inhalt anpasst
        set_frame.grid(row=i % 3, column=i // 3, padx=10, pady=10, sticky="nsew")
        
        # Innerhalb des Set-Frames wird ein Ergebnis-Frame erstellt, in dem die Würfel gezeichnet werden
        result_frame = Frame(set_frame)
        result_frame.pack(fill="both", expand=True)
        # Erstelle einen Button, der das Würfeln für dieses Set auslöst
        Button(set_frame, text=f"{set_name.get()} - Würfeln", 
               command=lambda rf=result_frame, dc=dice_count, ds=dice_sides, sn=set_name, 
                              dc_lbl=dice_color_label, tc_lbl=text_color_label: roll_single_set(
                                  rf, dc, ds, sn.get(), dc_lbl["bg"], tc_lbl["bg"])
        ).pack(side="bottom", pady=2)
    
    # Zeige das Ergebnis-Frame an
    results_menu.pack(fill="both", expand=True)

def show_settings():
    """
    Zeigt die Einstellungsansicht wieder an, indem das Ergebnis-Frame ausgeblendet wird.
    """
    results_menu.pack_forget()
    settings_frame.pack(fill="both", expand=True)

# Erstelle das Hauptfenster der Anwendung
root = tk.Tk()
# Setze eine Standard-Schriftart für alle Widgets
root.option_add("*Font", "Arial 12")
# Setze den Fenstertitel
root.title("Dice Roller mit adaptiven Größen")

# Globale Liste, in der die einzelnen Set-Konfigurationen gespeichert werden
sets = []

# Erstelle das Einstellungs-Frame, in dem der Benutzer die Anzahl der Sets und deren Parameter eingeben kann
settings_frame = Frame(root)
settings_frame.pack(fill="both", expand=True)

# Oberer Bereich des Einstellungs-Frames: Eingabe, wie viele Sets gewürfelt werden sollen
top_frame = Frame(settings_frame)
top_frame.pack(side="top", fill="x", pady=5)

# Label und Eingabefeld für die Anzahl der Sets (zwischen 1 und 12)
Label(top_frame, text="Wie viele Sets möchtest du würfeln? (1-12)").grid(row=0, column=0, padx=5)
enter_set = IntEntry(top_frame, width=5, lower_bound=1, upper_bound=12)
enter_set.grid(row=0, column=1, padx=5)
# Button, der den nächsten Schritt (Set-Konfiguration) einleitet
Button(top_frame, text="Weiter", command=confirm_sets).grid(row=0, column=2, padx=5)
# Button, der direkt zur Ergebnisanzeige wechselt (nachdem alle Sets konfiguriert wurden)
Button(top_frame, text="Einstellungen bestätigen", command=show_dice_results).grid(row=0, column=3, padx=5)

# Frame, in dem die einzelnen Set-Konfigurationen (Name, Würfelanzahl, Seitenzahl, Farben) angeordnet werden
grid_frame = Frame(settings_frame)
grid_frame.pack(fill="both", expand=True)

# Frame, das später die Ergebnisse (Würfelgrafiken) anzeigt
results_menu = Frame(root)

# Starte die Tkinter-Hauptschleife, um das GUI am Laufen zu halten
root.mainloop()
