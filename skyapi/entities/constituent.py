from skyapi.baseapi import BaseApi


class Constituent(BaseApi):

    def __init__(self, *args, **kwargs):
        super(Constituent, self).__init__(*args, **kwargs)
        self.entity = 'constituent'
        self.endpoint = 'constituents'

    def get(self, constituent_id):
        self.constituent_id = constituent_id
        return self._sky_client._get(url=self._build_path(constituent_id))
