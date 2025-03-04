import termcolor as t
import string
import requests
from textblob import TextBlob


def correct_spelling(sentence):
  sentence = TextBlob(sentence)
  result = sentence.correct()
  return result


def get_synonyms_antonyms(word):
  url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    if isinstance(data, list) and data:
      meanings = data[0].get('meanings')
      synonyms = []
      antonyms = []
      for meaning in meanings:
        definitions = meaning.get('definitions')
        for definition in definitions:
          synonyms.extend(definition.get('synonyms', []))
          antonyms.extend(definition.get('antonyms', []))
      return synonyms, antonyms
  return [], []


def check_word(word):
  url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    if isinstance(response.json(), list) and response.json():
      # The word is in the dictionary
      return True
  # The word is not in the dictionary
  return False


def check_sentence(sentence):
  ready = sentence.strip()
  correct_words = []

  if " " in ready:
    # If sentence then
    print("\n\nSentence detected. Commencing grammar check...")
    nopunc = ready.translate(str.maketrans('', '', string.punctuation))
    sent_words = ([i for i in nopunc.split()])

    for word in sent_words:
      if check_word(word):
        correct_words.append(word)
      else:
        t.cprint(f"\nPossibly misspelled word: {word}",
                 "yellow",
                 attrs=["bold"])
        synonyms, antonyms = get_synonyms_antonyms(word)
        if synonyms:
          t.cprint(f"Synonyms for {word}: {', '.join(synonyms)}",
                   "blue",
                   attrs=["bold"])
        if antonyms:
          t.cprint(f"Antonyms for {word}: {', '.join(antonyms)}",
                   "magenta",
                   attrs=["bold"])

    if ready.endswith("."):
      t.cprint("\nSentence punctuation correct, period detected.",
               "green",
               attrs=['bold'])
    elif ready.endswith("?"):
      t.cprint("\nSentence punctuation correct, question mark detected.",
               "green",
               attrs=['bold'])
    elif ready.endswith("!"):
      t.cprint("\nSentence punctuation correct, exclamation point detected.",
               "green",
               attrs=['bold'])
    else:
      t.cprint(
          "\nPunctuation not detected, check your punctuation at the end of your sentence.",
          "red",
          attrs=['bold'])

    if ready[0].isupper():
      t.cprint(
          "\nFirst letter of sentence capitalized, capitalization correct.",
          "green",
          attrs=['bold'])
    else:
      t.cprint(
          "\nNo capitalization detected at the beginning of the sentence, check your capitalization.",
          "red",
          attrs=["bold"])

    if len(correct_words) == len(sent_words):
      t.cprint("\nAll words are spelled correctly.", "green", attrs=["bold"])

  else:
    print("\n\nWord detected. Commencing dictionary check...")
    if check_word(ready):
      t.cprint(f"\nYour word, \"{ready}\", is in the English Dictionary!",
               "green",
               attrs=["bold"])
      synonyms, antonyms = get_synonyms_antonyms(ready)
      if synonyms:
        t.cprint(f"\nSynonyms for {ready}: {', '.join(synonyms)}",
                 "blue",
                 attrs=["bold"])
      if antonyms:
        t.cprint(f"Antonyms for {ready}: {', '.join(antonyms)}",
                 "magenta",
                 attrs=["bold"])
    else:
      t.cprint(
          f"\nYour word, \"{ready}\", is not in the dictionary. Try checking your spelling.",
          "red",
          attrs=["bold"])


def main():
  print(
      "Welcome to SpellCheck, by Zain Keshwani! With this spell checker, you can either insert a sentence to check its grammar, capitalization, or punctuation, or you can insert a word to check if it is in the English Dictionary and get some synonyms and antonyms for the word as well (if there are any on the free API being used).\n\n"
  )
  while True:
    text = input("\n\nEnter your word/sentence (or 'q' to quit): ")
    if text.lower() == 'q':
      print("Thank you for using SpellCheck, by Zain Keshwani!")
      break
    check_sentence(text)
    print("\nA corrected version of your text may look something like this: " +
          str(correct_spelling(text)))


main()
