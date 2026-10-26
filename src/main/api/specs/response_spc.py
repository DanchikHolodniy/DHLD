from http import HTTPStatus




class ResponseSpc:
    @staticmethod
    def response_ok():
        def confirm(response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm


    @staticmethod
    def response_create():
        def confirm(response):
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm


    @staticmethod
    def response_bad():
        def confirm(response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm


    @staticmethod
    def response_conflict():
        def confirm(response):
            assert response.status_code == HTTPStatus.CONFLICT, response.text
        return confirm


    @staticmethod
    def response_422():
        def confirm(response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT, response.text
        return confirm
