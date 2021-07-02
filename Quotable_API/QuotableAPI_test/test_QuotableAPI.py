import unittest
from QuotableAPI import QuotableAPI

class TestQuotableAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.quotableAPI = QuotableAPI()
        self.author_name = "Confucius"
        self.non_existing_author = "Santhosh"
        self.non_existing_tag = "welcome"
        self.non_existing_tag1 = "inspire"
        self.tag1 = "inspirational"
        self.tag2 = "love"
        self.total_pages, self.total_quotes, self.total_quotes_per_page = self.getTotalPages(self)

    def getTotalPages(self):
        params = { "page": 1 }
        result = self.quotableAPI.getQuotes(params)
        return result["totalPages"], result["totalCount"], result["count"]

    def generateExpectedResponse(self, count=None, totalCount=None, page=None, 
                                                totalPages=None, lastItemIndex=None, results=None):
        expected_response= locals()
        expected_response.pop("self")
        if expected_response["count"]==None:
            expected_response["count"] = self.total_quotes_per_page
        if expected_response["totalCount"]==None:
            expected_response["totalCount"] = self.total_quotes
        if expected_response["page"] == None:
            expected_response["page"] = 1
        if expected_response["totalPages"] == None:
            expected_response["totalPages"] = self.total_pages
        if expected_response["lastItemIndex"] != None:
            expected_response["lastItemIndex"] = self.total_quotes_per_page * expected_response["page"]
        if results == None:
            expected_response["results"] = []
        return expected_response
    
    def testResponseForMaxPageNumber(self):
        """ 
        Check Empty quotes are shown for any page number greater than totalPages
        """
        params = { "page": self.total_pages + 1 }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], page=params["page"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForNonExistAuthor(self):
        """
        Check Empty quotes are shown for a non existing author
        """
        params = { "author": self.non_existing_author }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForNonExistTag(self):
        """
        Check Empty quotes are shown for a non exisitng tags
        """
        params = { "tags": self.non_existing_tag }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForBothTagsNotPresent(self):
        """
        Check Empty quotes are shown because no quotes doesn't have both the tags - AND Operation
        """
        params = { "tags": self.tag1 + "," + self.tag2 }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForNonExistTagWithExistTag(self):
        """
        Check Empty quotes are shown because no quotes doesn't have one of the non existing tag - AND Operation
        """
        params = { "tags": self.tag1 + "," + self.non_existing_tag }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForBothNonExistTags(self):
        """
        Check empty quotes are shown for neither of the tags are not present - OR Operation
        """
        params = { "tags": self.non_existing_tag1 + "," + self.non_existing_tag }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForMaxPageNumberWithExistAuthor(self):
        """
        Check Empty quotes are shown for any page number greater than totalPages on author
        """
        params = { "page": self.total_pages + 1, "author": self.author_name }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], page=params["page"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForNonExistAuthorWithExistPage(self):
        """
        Check Empty quotes are shown for a non existing author on valid page number 
        """
        params = { "author": self.non_existing_author, "page": self.total_pages }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], page=params["page"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForNonExistAuthorWithMaxPageNumber(self):
        """
        Check Empty quotes are shown for a non existing author on page number greater than totalPages on author
        """
        params = { "author": self.non_existing_author, "page": self.total_pages + 1 }
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], page=params["page"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)

    def testResponseForNegativePageNumberWithNonExistAuthor(self):
        """
        Check Empty quotes are shown for a non existing author on page number greater than totalPages on author
        """
        params = { "author": self.non_existing_author, "page": - self.total_pages}
        result = self.quotableAPI.getQuotes(params)
        expected_response = self.generateExpectedResponse(count=result["count"], totalCount=result["totalCount"], totalPages=result["totalPages"], lastItemIndex=None)
        self.assertDictEqual(result, expected_response)
    

if __name__ == "__main__":
    suite = unittest.makeSuite(TestQuotableAPI)
    runner = unittest.TextTestRunner()
    runner.run(suite)





