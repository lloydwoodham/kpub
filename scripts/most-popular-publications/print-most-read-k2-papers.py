import datetime
import kpub

def print_articles(articles):
    for idx, art in enumerate(articles):
        print(
            f"""{idx + 1}. {art["title"][0].upper()}\n{art['first_author_norm']} ({art['bibcode']})\n{art['read_count']} reads\n"""
        )


if __name__ == "__main__":
    db = kpub.PublicationDB()
    articles = db.get_most_read(mission="k2", top=25)
    print(
        f'THE 25 MOST READ K2 PAPERS IN THE LAST 90 DAYS\n==============================================\nLast update: {datetime.datetime.now().strftime("%Y-%m-%d")}\n'
    )

    print_articles(articles)

