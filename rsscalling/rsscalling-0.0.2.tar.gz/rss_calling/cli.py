import click
import feedparser

@click.command()
@click.argument("feed")
def leggi(feed):
	feed = feedparser.parse(feed)
	click.secho("Ci sono " + str(len(feed["entries"])) + " notizie,premi un tasto per leggerle...",bg='yellow',fg="black")
	click.pause()
	click.secho("Inizio della stampa notizie",bg='green',fg="black")
	for entry in feed['entries']:
		click.secho(entry["title"],bg='white',fg="black")
	click.secho("Stampa delle notizie finita",bg='green',fg="black")


if __name__ == "__main__":
	leggi()