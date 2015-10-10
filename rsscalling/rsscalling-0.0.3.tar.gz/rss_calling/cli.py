import click
import feedparser
import html

@click.command()
@click.option("--htmld",is_flag=True,default=False)
@click.argument("feedraw")
def leggi(htmld,feedraw):
	feed = feedparser.parse(feedraw)
	click.secho("Ci sono " + str(len(feed["entries"])) + " notizie,premi un tasto per leggerle...",bg='yellow',fg="black")
	click.pause()
	if htmld == False:
		click.secho("Inizio della stampa notizie",bg='green',fg="black")
		for entry in feed['entries']:
			click.secho(entry["title"],bg='white',fg="black")
		click.secho("Stampa delle notizie finita",bg='green',fg="black")
	elif htmld == True:
		pag = html.HTML()
		ul = pag.ul
		for entry in feed['entries']:
			ul.li.link(entry["title"],href=entry["link"])
		nomefile = "HtmlDump-" + feedraw + "-" + feed["updated"] + ".html"
		f = open("htmldump.html","w")
		pags = unicode(pag)
		uni = pags.encode('utf-8')
		f.write(uni)
		f.flush()
		f.close()




if __name__ == "__main__":
	leggi()