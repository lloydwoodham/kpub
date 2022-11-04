"""Categorize publications into fine-grained categories
"""

from pprint import pprint
import pandas as pd
import kpub

FILENAME = "k2-categories.csv"

CATEGORIES = {
              'as': 'Asteroseismology',
              'ga': 'Galactic Archaeology',
              'wd': 'White Dwarfs',
              'cv': 'Cataclysmic Variables',
              'eb': 'Eclipsing Binaries',
              'ac': 'Stellar Activity',
              'ro': 'Stellar Rotation',
              'yo': 'Young Stars',
              'cl': 'Clusters',
              'ss': 'Solar System Science',
              'ca': 'Catalogs',
              'da': 'Data Analysis',
              'ed': 'Exoplanet Discovery',
              'ec': 'Exoplanet Characterization',
              'ml': 'Microlensing',
              'sn': 'Supernovae',
              'ag': 'AGN',
              'va': 'Classical Pulsators',
              'ot': 'Other Topics'
              }


if __name__ == "__main__":
    # Read in existing db
    try:
        catdb = pd.read_csv(FILENAME, names=["bibcode", "cat"])
        classified_bibcodes = catdb.bibcode.values
    except FileNotFoundError:
        classified_bibcodes = []

    with open(FILENAME, 'a') as out:
        db = kpub.PublicationDB()
        pubs = db.get_all(mission="k2")
        for idx, pub in enumerate(pubs):
            # Skip articles already categorizes
            if pub['bibcode'] in classified_bibcodes:
                continue

                    # Clear screen and show the article
            print(f"{chr(27)}[2J")
            print(f"Article {idx + 1} out of {len(pubs)}")
            kpub.display_abstract(pub)

            # Prompt the user to classify the paper
            print("Categories:")
            pprint(CATEGORIES)
            while True:
                print("=> Enter code: ", end="")
                prompt = input()
                if prompt in CATEGORIES:
                    out.write(f"{pub['bibcode']},{prompt}\n")
                    out.flush()
                    break

                else:
                    print("Error: invalid category")
