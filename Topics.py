import spacy


# Loading model
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


def topics_sa(dataset):
    # Lemmatization with stopwords removal
    dataset['lemmatized'] = dataset['statuses_text'].apply(
        lambda x: ' '.join([token.lemma_ for token in list(nlp(x)) if (token.is_stop == False)]))
    normal_words_sa = ' '.join([text for text in dataset['lemmatized'][dataset['tweets_location'] == 'local']])
    return normal_words_sa

def topics_global(dataset):
    dataset['lemmatized'] = dataset['statuses_text'].apply(
        lambda x: ' '.join([token.lemma_ for token in list(nlp(x)) if (token.is_stop == False)]))
    normal_words_global = ' '.join([text for text in dataset['lemmatized'][dataset['tweets_location'] == 'global']])
    return normal_words_global

