def sentiment_file(gcs_uri):
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types

    client = language.LanguageServiceClient()

    document = types.Document(
        gcs_content_uri = gcs_uri,
        type = enums.Document.Type.PLAIN_TEXT)

    sentiment = client.analyze_sentiment(document).document_sentiment

    return sentiment.score

def classify_file(gcs_uri):
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types

    client = language.LanguageServiceClient()

    document = types.Document(
        gcs_content_uri=gcs_uri,
        type=enums.Document.Type.PLAIN_TEXT
    )
    
    categories = client.classify_text(document).categories

    holder = []
    cat = ""
    conf = ""
    
    once = False

    for category in categories:
        if once == False:
            cat += category.name
            conf += str(category.confidence)
            once==True
        else:
            cat += ";" + category.name
            conf += ";" + str(category.confidence)
    
    return[cat, conf]


# Sentiment and Intent Analysis using Cloud Natural Language API

from google.cloud import storage
import pandas as pd

filename = []
score = []
category = []
confidence = []

client = storage.Client()
bucket = client.bucket('bucket_name')
path = 'gcs_uri'

for blob in bucket.list_blobs():
    filename.append(blob.name)
    score.append(sentiment_file(str(path) + blob.name))
    t = classify_file(str(path) + blob.name)
    cat = t[0]
    conf = t[1]
    category.append(cat)
    confidence.append(conf)

# Write the output to pandas dataframe 
final_output = pd.DataFrame({'filename': filename, 'sentiment_score': score, 'category': category, 'confidence': confidence})
final_output = final_output[['filename', 'sentiment_score', 'category', 'confidence']]

# Save as csv into Cloud Storage
final_output.to_csv(r'gcs_uri/filename.csv', index=False)

