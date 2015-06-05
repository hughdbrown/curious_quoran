import pandas as pd


def gutenberg_cat(path):
    '''
    INPUT: filepath to csv from Gutenberg SQL dump
    OUTPUT: dataframe with Title, Author, subject tags and pre-vectorized descriptions

    '''
    ebook = pd.read_csv(path)

    # Filter for only English books 
    english_only = ebook[ebook['flanguage']=='{en}']
    df = english_only[['ftitle', 'fsubjectname', 'ffriendlytitle']]

    # Rename columns
    df.columns = ['title', 'tags', 'title_auth']
    df = df.dropna()

    # Clean up cols
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.replace('{', ' ')).apply(lambda x: x.replace('}', ' ')).apply(lambda x: x.replace('"', ' '))

    df.subj_tags = df.tags.apply(lambda x: x.replace('--',' '))

    # Make a composite description with tags and title
    df['desc_tot'] = df['tags']+' '+ df['title']
    return df

if __name__=="__main__":
    gutenberg_cat('ebooks.csv')