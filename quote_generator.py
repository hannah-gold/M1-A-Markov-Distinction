import random
import sys
import re

SEED_QUOTES = [
    "The only way to do great work is to love what you do.",
    "Whether you think you can or you think you can’t, you’re right.",
    "It always seems impossible until it’s done.",
    "Start where you are. Use what you have. Do what you can.",
    "Success is not final; failure is not fatal: it is the courage to continue that counts.",
    "The future depends on what you do today.",
    "Dream big and dare to fail.",
    "Small steps every day lead to big results.",
    "Do one thing every day that scares you.",
    "What we think, we become.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Act as if what you do makes a difference. It does.",
    "You are never too old to set another goal or to dream a new dream.",
    "Everything you can imagine is real.",
    "The best way out is always through."
]

ANSI_COLORS = [
    "\033[31m", # red
    "\033[32m", # green
    "\033[33m", # yellow
    "\033[34m", # blue
    "\033[35m", # magenta
    "\033[36m", # cyan
]

RESET = "\033[0m"

def tokenize(text):
    # Simple word + punctuation tokenizer
    # Keep punctuation tokens so the model learns comma/period placement
    tokens = re.findall(r"[A-Za-z’']+|[.,;:!?]", text)
    return tokens

def build_markov_model(quotes, order=2):
    """ Markov model as dict: state(tuple)->list of next tokens."""
    model = {}
    starts = []  # starting states for sentences
    for q in quotes:
        tokens = tokenize(q)
        if len(tokens) < order + 1:
            continue
        # record starting state
        starts.append(tuple(tokens[:order]))
        for i in range(len(tokens) - order):
            state = tuple(tokens[i:i+order])
            nxt = tokens[i+order]
            model.setdefault(state, []).append(nxt)
    return model, starts

def generate_sentence(model, starts, max_len=30):
    if not model or not starts:
        return "Keep going."
    state = random.choice(starts)
    out = list(state)
    for _ in range(max_len):
        options = model.get(state, None)
        if not options:
            break
        nxt = random.choice(options)
        out.append(nxt)
        state = tuple(out[-len(state):])
        # early stop if we ended with a sentence terminator after at least ~8 tokens
        if len(out) >= 8 and out[-1] in (".", "!", "?"):
            break

    # Join tokens while handling punctuation spacing
    s = []
    for i, tok in enumerate(out):
        if tok in ".,;:!?":
            if s:
                s[-1] = s[-1].rstrip()  # ensure no trailing space before punctuation
            s.append(tok + " ")
        else:
            s.append(tok + " ")
    s = "".join(s).strip()
    s = re.sub(r"\s+([.,;:!?])", r"\1", s)  # final cleanup

    # Capitalize first letter and ensure terminal punctuation
    if s and s[0].islower():
        s = s[0].upper() + s[1:]
    if s and s[-1] not in ".!?":
        s += "."
    return s

def main():
    model, starts = build_markov_model(SEED_QUOTES, order=2)
    quote = generate_sentence(model, starts, max_len=28)

    # Pick a random color each time
    color = random.choice(ANSI_COLORS)

    print(color + "Inspirational Quote:" + RESET)
    print(color + quote + RESET)

if __name__ == "__main__":
    main()