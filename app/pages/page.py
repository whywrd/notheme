class Page:

    def __init__(self, json, **kwargs):
        self._json = json
        self.kwargs = kwargs
        self.meta_info = self.build_meta_info(json)
        self.content = self.build_content(json)

    def build_content(self, json):
        raise NotImplementedError

    def build_meta_info(self, json):
        raise NotImplementedError
