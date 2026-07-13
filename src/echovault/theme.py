from textual.theme import Theme

echovault_purple = Theme(
    name="echovault_purple",
    primary="#8e44ad",
    secondary="#9b59b6",
    accent="#6c5ce7",
    foreground="#e5e5e5",
    background="#121212",
    panel="#181818",
    surface="#1c1c1c",
    success="#27ae60",
    warning="#e67e22",
    error="#c0392b",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#9b59b6",
        "input-selection-background": "#8e44ad 35%",
        "border": "#282828",
        "text-muted": "#a0a0a0",
    },
)

dracula_theme = Theme(
    name="dracula",
    primary="#BD93F9",
    secondary="#6272A4",
    accent="#FF79C6",
    foreground="#F8F8F2",
    background="#282A36",
    panel="#1E1F29",
    surface="#3A3C4E",
    success="#50FA7B",
    warning="#F1FA8C",
    error="#FF5555",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)

arctic_theme = Theme(
    name="arctic",
    primary="#88C0D0",
    secondary="#81A1C1",
    accent="#B48EAD",
    foreground="#D8DEE9",
    background="#2E3440",
    success="#A3BE8C",
    warning="#EBCB8B",
    error="#BF616A",
    surface="#3B4252",
    panel="#434C5E",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)
