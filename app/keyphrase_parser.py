from difflib import SequenceMatcher

import wikipediaapi
import pke

wikipedia = wikipediaapi.Wikipedia("en")


def get_keyphrases(text):
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(input=text, language="en")
    extractor.candidate_selection()
    extractor.candidate_filtering(maximum_word_number=3)
    extractor.candidate_weighting()

    keyphrases = []

    for keyphrase in extractor.get_n_best(n=15):
        keyphrase = keyphrase[0]
        keyphrase_dict = {"keyphrase": keyphrase}

        page = wikipedia.page(keyphrase)

        if page.exists() and SequenceMatcher(None, page.title, keyphrase).ratio() > 0.6:
            dis_page = wikipedia.page(f"{page.title}_(disambiguation)")

            if dis_page.exists():
                keyphrase_dict["url"] = dis_page.fullurl
                keyphrase_dict["disambiguation"] = True
            else:
                keyphrase_dict["url"] = page.fullurl

        keyphrases.append(keyphrase_dict)

    return keyphrases
