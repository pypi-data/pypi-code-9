import os
import sys
import json
from random import randint

from bst.pygasus.core import ext

from bst.pygasus.wsgi.interfaces import IRequest
from bst.pygasus.wsgi.events import IApplicationStartupEvent
from bst.pygasus.wsgi.interfaces import IApplicationSettings

from bst.pygasus.demo import model
from bst.pygasus.demo.model import Card

from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.index import EmptyIndexError

from whoosh.fields import TEXT
from whoosh.fields import NUMERIC
from whoosh.fields import STORED
from whoosh.fields import KEYWORD
from whoosh.fields import Schema
from whoosh.fields import SchemaClass

from whoosh.qparser import QueryParser


cardIndexer = None


class CardHandler(ext.AbstractModelHandler):
    ext.adapts(model.Card, IRequest)

    def get(self, model, batch):
        start, limit = self.slice()
        property, direction = self.sort()

        return cardIndexer.search_index(start, limit, property, direction)

    def create(self, model, batch):
        model.id = cardIndexer.get_next_id()
        cardIndexer.extend_index(model)

        return [model], 1

    def update(self, model, batch):
        cardIndexer.update_index(model)

        return [model], 1

    def delete(self, model, batch):
        cardIndexer.reduce_index(model)

        return [model], 1


@ext.subscribe(IApplicationSettings, IApplicationStartupEvent)
def initalize_card_index(settings, event):
    global cardIndexer
    cardIndexer = CardIndexer()
    cardIndexer.create_index()


class CardIndexSchema(SchemaClass):
    id = NUMERIC(unique=True)
    name = KEYWORD()
    type = KEYWORD()
    layout = TEXT()
    text = TEXT
    colors = KEYWORD(commas=True)
    costs = NUMERIC()
    power = TEXT()
    toughness = TEXT()
    availability = NUMERIC()
    card = STORED


class CardIndexer(object):

    ix = None

    def create_index(self):
        data = list()
        storage_path = self.get_storage_path()
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        try:
            self.ix = open_dir(storage_path)
            self.ix.schema.clean()
        except EmptyIndexError:

            self.ix = create_in(storage_path, CardIndexSchema())
            writer = self.ix.writer()

            file_path = os.path.join(os.path.dirname(__file__),
                                     'app/resources/AllCards.json')
            data = self.read_json(file_path)
            id = 1
            for key in data.keys():
                model = Card()
                model.id = id
                id += 1
                model.type = data[key]['type']
                model.layout = data[key]['layout']
                model.name = data[key]['name']
                model.availability = randint(0, 5)
                if 'text' in data[key].keys():
                    model.text = data[key]['text'].replace('\n', '')
                if 'cmc' in data[key].keys():
                    model.costs = int(data[key]['cmc'])
                if 'power' in data[key].keys():
                    model.power = data[key]['power']
                if 'toughness' in data[key].keys():
                    model.toughness = data[key]['toughness']
                if 'colors' in data[key].keys():
                    model.colors = ', '.join(data[key]['colors'])

                writer.add_document(id=model.id,
                                    name=model.name,
                                    type=model.type,
                                    layout=model.layout,
                                    text=model.text,
                                    colors=model.colors,
                                    costs=model.costs,
                                    power=model.power,
                                    toughness=model.toughness,
                                    availability=model.availability,
                                    card=model)

            writer.commit()
            data.clear()

    def search_index(self, start, limit, property, direction):
        cards = list()

        total_results = 0

        with self.ix.searcher() as searcher:
            cards.clear()
            query = QueryParser('', self.ix.schema).parse('*')
            page = int(start / limit) + 1
            if direction == 'ASC':
                direction = False
            else:
                direction = True

            results = searcher.search_page(query,
                                           page,
                                           limit,
                                           sortedby=property,
                                           reverse=direction)

            total_results = results.total

            for result in results:
                cards.append(result['card'])

        return cards, total_results

    def extend_index(self, model):
        writer = self.ix.writer()

        writer.add_document(id=model.id,
                            name=model.name,
                            type=model.type,
                            layout=model.layout,
                            text=model.text,
                            colors=model.colors,
                            costs=model.costs,
                            power=model.power,
                            toughness=model.toughness,
                            availability=model.availability,
                            card=model)

        writer.commit()

    def update_index(self, model):
        with self.ix.searcher() as searcher:
            query = QueryParser('id', self.ix.schema).parse(str(model.id))
            result = searcher.search(query)
            if len(result):
                writer = self.ix.writer()

                writer.update_document(id=model.id,
                                       name=model.name,
                                       type=model.type,
                                       layout=model.layout,
                                       text=model.text,
                                       colors=model.colors,
                                       costs=model.costs,
                                       power=model.power,
                                       toughness=model.toughness,
                                       availability=model.availability,
                                       card=model)

                writer.commit()

    def reduce_index(self, model):
        writer = self.ix.writer()

        query = QueryParser('id', self.ix.schema).parse(str(model.id))
        writer.delete_by_query(query)
        writer.commit()

    def get_next_id(self):
        id = 1
        with self.ix.searcher() as searcher:
            query = QueryParser('', self.ix.schema).parse('*')
            results = searcher.search_page(query,
                                           pagenum=1,
                                           pagelen=1,
                                           sortedby='id',
                                           reverse=True)

            if len(results):
                id = results[0]['card'].id + 1
        return id

    def read_json(self, path):
        with open(path) as data_file:
            return json.load(data_file)

    def get_storage_path(self):
        return os.path.abspath(os.path.join(sys.argv[0],
                                            os.pardir,
                                            os.pardir,
                                            'index'))
