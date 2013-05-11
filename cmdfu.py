__kupfer_name__ = _('CmdFu')
__kupfer_actions__ = ('Search', )
__description__ = _('Search shell command through online repositories')
__version__ = "0.1"
__author__ = "Francesco Brundu <francesco.brundu@gmail.com>"


from kupfer.objects import Action, TextLeaf, Source
import json
import urllib2
import operator


SEARCH_HOSTS = [['http://www.commandlinefu.com/commands/using/'],
    ['http://www.commandlinefu.com/commands/matching/', 'CMD_BASE64']]


class Search (Action):

    def __init__(self):

        Action.__init__(self, _("Command search"))

    def is_factory(self):

        return True

    def activate(self, leaf):

        return SearchResults(leaf.object)

    def item_types(self):

        yield TextLeaf

    def get_description(self):

        return __description__

class SearchResults (Source):

    def __init__(self, query):

        Source.__init__(self, _('Results for "%s"') % query)
        print query
        self.query = query

    def repr_key(self):

        return self.query

    def get_items(self):

        results = []
        query_formatted = '-'.join(self.query.split(' '))
        for host in SEARCH_HOSTS:
            url = host[0] + query_formatted
            if len(host) > 1:
                for parameter in host[1:]:
                    if parameter == 'CMD_BASE64':
                        _encode_handler = urllib2.base64.encodestring
                        query_encoded_tmp = _encode_handler(query_formatted)
                        query_encoded = query_encoded_tmp.strip('\n')
                        url += '/' + query_encoded
            url += '/sort-by-votes/json'
            print(url)
            response = urllib2.urlopen(url)
            results += json.load(response)

        results.sort(reverse=True, key=operator.itemgetter('votes'))
        for result in results:
            summary = (result['summary'][:40] +
                (result['summary'][40:41] and ".."))
            yield TextLeaf(result['command'], summary)

    def provides(self):

        yield TextLeaf
