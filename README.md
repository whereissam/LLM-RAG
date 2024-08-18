# LLM-RAG

## Pre-request

1. Go to [Ollama](https://ollama.com/), install it.
2. Run `ollama run llama3.1`
3. Run `ollama serve`

## Install

```bash
pip install -r requirements.txt
```

## Create Database

```bash
python3 fill_db.py
```

## Run Query

```bash
python3 ask.py
```

## Test

### Not related

```bash
Who is sam?

---------------------

I don't have enough information to answer that question accurately.

Related questions you might want to ask:
1. Who is the Sam in relation to crypto or payFi?
2. Is there a notable figure named Sam in finance or technology?
3. Are you referring to a specific project or initiative led by someone named Sam?
```

### Related

```bash
What is payFi?

---------------------

Answer: PayFi is a concept or technology that the user finds useful and believes aligns with what cryptocurrency (specifically, Bitcoin) set out to enable.

Related questions you might want to ask:
1. How does PayFi differ from other financial technologies?
2. What role do you think PayFi plays in enabling seamless cross-border transactions?
3. Can PayFi be used as a standalone payment system, or is it primarily a tool for enhancing existing financial infrastructure?
```
