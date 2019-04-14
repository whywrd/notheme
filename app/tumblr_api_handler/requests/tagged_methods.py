from tumblr_api_handler.requests import requests
import tumblr_api_handler.params.tagged_method_params as ps


class TaggedQuery(requests.GETRequest):

    def __init__(self, params: ps.TaggedParams):
        super().__init__('api.tumblr.com/v2/tagged', params)
