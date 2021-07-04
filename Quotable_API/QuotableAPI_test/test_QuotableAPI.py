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
        self.quote_keys = ["tags", "_id", "author", "content", "authorSlug", "length", "dateAdded", "dateModified"]

    def getTotalPages(self):
        params = { "page": 1 }
        response = self.quotableAPI.getQuotes(params)
        return response["totalPages"], response["totalCount"], response["count"]

    def validateResults(self, results):
        flag=0
        if results:
            for each_result in results:
                for each_key in self.quote_keys:
                    if each_key not in each_result:
                        flag=1
                        break
        if(flag==0):
            return True
        else:
            return False

    def generateExpectedResponse(self, count=None, totalCount=None, page=None, 
                                                totalPages=None, lastItemIndex=None):
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
        return expected_response
    
    def testResponseForMaxPageNumber(self):
        """ 
        Check Empty quotes are shown for any page number greater than totalPages
        """
        params = { "page": self.total_pages + 1 }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], page=params["page"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForNonExistAuthor(self):
        """
        Check Empty quotes are shown for a non existing author
        """
        params = { "author": self.non_existing_author }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForNonExistTag(self):
        """
        Check Empty quotes are shown for a non exisitng tags
        """
        params = { "tags": self.non_existing_tag }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForBothTagsNotPresent(self):
        """
        Check Empty quotes are shown because no quotes doesn't have both the tags - AND Operation
        """
        params = { "tags": self.tag1 + "," + self.tag2 }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForNonExistTagWithExistTag(self):
        """
        Check Empty quotes are shown because no quotes doesn't have one of the non existing tag - AND Operation
        """
        params = { "tags": self.tag1 + "," + self.non_existing_tag }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForBothNonExistTags(self):
        """
        Check empty quotes are shown for neither of the tags are not present - OR Operation
        """
        params = { "tags": self.non_existing_tag1 + "," + self.non_existing_tag }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForMaxPageNumberWithExistAuthor(self):
        """
        Check Empty quotes are shown for any page number greater than totalPages on author
        """
        params = { "page": self.total_pages + 1, "author": self.author_name }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], page=params["page"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForNonExistAuthorWithExistPage(self):
        """
        Check Empty quotes are shown for a non existing author on valid page number 
        """
        params = { "author": self.non_existing_author, "page": self.total_pages }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], page=params["page"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForNonExistAuthorWithMaxPageNumber(self):
        """
        Check Empty quotes are shown for a non existing author on page number greater than totalPages on author
        """
        params = { "author": self.non_existing_author, "page": self.total_pages + 1 }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], page=params["page"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForNegativePageNumberWithNonExistAuthor(self):
        """
        Check Empty quotes are shown for a non existing author on page number greater than totalPages on author
        """
        params = { "author": self.non_existing_author, "page": - self.total_pages}
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(count=response["count"], totalCount=response["totalCount"], totalPages=response["totalPages"], lastItemIndex=None)
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))
    
    def testResponseForValidPageNumber(self):
        """
        Check 20 quotes are shown for any page number lesser than totalPages and validate the response
        """
        params = { "page": 1 }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(lastItemIndex=response["lastItemIndex"])
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

    def testResponseForNegativePageNumber(self):
        """
        Check first 20 quotes are shown for any negative page number
        """
        params = { "page": -1 }
        response = self.quotableAPI.getQuotes(params)
        results = response.pop("results")
        expected_response = self.generateExpectedResponse(lastItemIndex=response["lastItemIndex"])
        self.assertDictEqual(response, expected_response)
        self.assertTrue(self.validateResults(results))

if __name__ == "__main__":
    suite = unittest.makeSuite(TestQuotableAPI)
    runner = unittest.TextTestRunner()
    runner.run(suite)





