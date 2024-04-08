import anthropic
import sys
import json
import tinydb
import dotenv
from collections.abc import Mapping, Sequence
from termcolor import cprint

dotenv.load_dotenv()
def run(words: Sequence[str]):
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
    )

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0.0,
        system="Respond only in Yoda-speak.",
        messages=[
            {"role": "user", "content": "User: You are a bot that replies in JSON format. input (word[]) --> output (output: {sentence, senetenceInJapanese}[]) // sentence is a sample text for learning English. So you must return in **valid** JSON format from now. input(" + ','.join(words) + ") // if the word does not exist, **return the nearest word in the dictionary** but output format is the same"}
        ])

    for item in json.loads(message.content[0].text)["output"]:
        prettyPrint(item)
        # save to tiny db
        db = tinydb.TinyDB('db.json')
        db.insert(item)

def prettyPrint(db_item):
    cprint(db_item["sentence"], 'green')
    cprint(db_item["sentenceInJapanese"], 'white')

# if command --show is given, show the db
if __name__ == "__main__":
    db = tinydb.TinyDB('db.json')
    if len(sys.argv) > 1 and sys.argv[1] == "--show":
        for db_item in db.all():
            # colorize the output
            prettyPrint(db_item)

    # run() if --text is given
    elif len(sys.argv) > 1 and sys.argv[1] == "--text":

        run(sys.argv[2:])

