import json
import re
from urllib import response
import requests
import html_to_json

class semrush:

    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Referer" : "https://www.google.com/"
    }

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

        balance = self.checkBalance()
        print(balance)

    def sendRequest(self, url):
        response = requests.get(url, headers=self.headers)
        status = response.status_code

        if status != 200:
            print("Error")
            return response.text

        print(response)

        #dataform = str(response.json()).strip("'<>() ").replace('\'', '\"')

        #with open("r.json", 'w') as f: f.write(struct)
        
        return html_to_json.convert(response.text)

    def checkBalance(self):
        requestURL = f"http://www.semrush.com/users/countapiunits.html?key={self.API_KEY}"
        response = self.sendRequest(requestURL)

        return response

    """
    Code for requesting information about backlinks. Check this link for documentation:
    https://developer.semrush.com/api/v3/analytics/backlinks/#backlinks-overview/
    """

    def getBacklinksOverview(self, target:str, targetType:str, exportColumns:list=["ascore", "total", "domains_num", "urls_num", "ips_num", "ipclassc_num", "follows_num"]) -> dict:
        """
        This report provides a summary of backlinks, including their type, referring domains and 
        IP addresses for a domain, root domain, or URL. Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#backlinks-overview/

        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

        # Create the request URl
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_overview&target={target}"
                      f"&target_type={targetType}&export_columns={exportColumnsStr}")

        response = self.sendRequest(requestURL)  # Send the request
        return response  # Return the response

    def getBacklinks(self, target:str, targetType:str, exportColumns:list=["page_ascore", "response_code", "source_size"], displaySort:str="page_ascore_asc", displayLimit:int=20, displayOffset:int=None, displayFilter:str=None) -> dict:
        """
        This report lists backlinks for a domain, root domain, or URL. Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#backlinks/

        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displaySort : str
            How you want to sort the list. You can find the sort options using the link above

        displayLimit : int
            Set a limit to how many items you want to display

        displayOffset : int
            How many entries you want to skip until it start to count

        displayFilter : str
            The filter you want to put on the display

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displaySort != None: requestURL += f"&display_sort={displaySort}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit + displayOffset if displayOffset != None else displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if displayFilter != None: requestURL += f"&display_filter={displayFilter}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getReferringDomains(self, target:str, targetType:str, exportColumns:list=["domain_ascore", "domain", "backlinks_num"], displaySort:str=None, displayLimit:int=20, displayOffset:int=0, displayFilter:str="") -> dict:
        """
        This report lists domains pointing to the queried domain, root domain, or URL. Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#referring-domains/

        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displaySort : str
            How you want to sort the list. You can find the sort options using the link above

        displayLimit : int
            Set a limit to how many items you want to display

        displayOffset : int
            How many entries you want to skip until it start to count

        displayFilter : str
            The filter you want to put on the display

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_refdomains"
                      f"&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displaySort != None: requestURL += f"&display_sort={displaySort}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit + displayOffset if displayOffset != None else displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if displayFilter != None: requestURL += f"&display_filter={displayFilter}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getReferringIps(self, target:str, targetType:str, exportColumns:list=["ip", "country", "backlinks_num"], displaySort:str=None, displayLimit:int=None, displayOffset:int=0) -> dict:
        """
        This report lists IP addresses where backlinks to a domain, root domain, or URL
        are coming from. Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#referring-ips/

        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displaySort : str
            How you want to sort the list. You can find the sort options using the link above

        displayLimit : int
            Set a limit to how many items you want to display

        displayOffset : int
            How many entries you want to skip until it start to count

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_refips"
                      f"&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displaySort != None: requestURL += f"&display_sort={displaySort}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit + displayOffset if displayOffset != None else displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getBacklinksTLD(self, target:str, targetType:str, exportColumns:list=["zone", "domains_num", "backlinks_num"], displaySort:str="page_ascore_asc", displayLimit:int=20, displayOffset:int=0) -> dict:
        """
        This report shows referring domain distributions depending on their top-level domain type.
        Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#TLD_distribution/
        
        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displaySort : str
            How you want to sort the list. You can find the sort options using the link above

        displayLimit : int
            Set a limit to how many items you want to display

        displayOffset : int
            How many entries you want to skip until it start to count

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_tld"
                      f"&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displaySort != None: requestURL += f"&display_sort={displaySort}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit + displayOffset if displayOffset != None else displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getReferringDomainsByCountry(self, target:str, targetType:str, exportColumns:list=["country", "domains_num", "backlinks_num"], displaySort:str="page_ascore_asc", displayLimit:int=20, displayOffset:int=0) -> dict:
        """
        This report shows referring domain distributions by country (an IP address defines a country).
        Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#reffering_domains_by_country/
        
        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displaySort : str
            How you want to sort the list. You can find the sort options using the link above

        displayLimit : int
            Set a limit to how many items you want to display

        displayOffset : int
            How many entries you want to skip until it start to count

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_geo"
                      f"&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displaySort != None: requestURL += f"&display_sort={displaySort}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit + displayOffset if displayOffset != None else displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getAnchors(self, target:str, targetType:str, exportColumns:list=["anchor", "domains_num", "backlinks_num"], displaySort:str="page_ascore_asc", displayLimit:int=20, displayOffset:int=0) -> dict:
        """
        This report lists anchor texts used in backlinks leading to the queried domain, root domain, or URL. It also
        includes the number of backlinks and referring domains per anchor. Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#anchors/
        
        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displaySort : str
            How you want to sort the list. You can find the sort options using the link above

        displayLimit : int
            Set a limit to how many items you want to display

        displayOffset : int
            How many entries you want to skip until it start to count

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_anchors"
                      f"&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displaySort != None: requestURL += f"&display_sort={displaySort}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit + displayOffset if displayOffset != None else displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getIndexedPages(self, target:str, targetType:str, exportColumns:list=["source_url", "source_title", "response_code", "backlinks_num"], displaySort:str="page_ascore_asc", displayLimit:int=20, displayOffset:int=0) -> dict:
        """
        This report shows indexed pages of the queried domain Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#indexed_pages/
        
        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displaySort : str
            How you want to sort the list. You can find the sort options using the link above

        displayLimit : int
            Set a limit to how many items you want to display

        displayOffset : int
            How many entries you want to skip until it start to count

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_pages"
                      f"&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displaySort != None: requestURL += f"&display_sort={displaySort}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit + displayOffset if displayOffset != None else displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getCompetitors(self, target:str, targetType:str, exportColumns:list=["ascore", "neighbour", "similarity"], displayLimit:int=20, displayOffset:int=0) -> dict:
        """
        A list of domains with a similar backlink profile to the analyzed domain.
        Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#competitors/
        
        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displaySort : str
            How you want to sort the list. You can find the sort options using the link above

        displayLimit : int
            Set a limit to how many items you want to display

        displayOffset : int
            How many entries you want to skip until it start to count

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_competitors"
                      f"&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displayLimit != None: requestURL += f"&display_limit={displayLimit + displayOffset if displayOffset != None else displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getBacklinksAscore(self, target:str, targetType:str) -> dict:
        """
        This report returns distribution of referring domains by Authority Score. When you run a query for a domain, 
        in return, for each Authority Score value [from 0 to 100], you receive a number of domains that have at least 
        one link, pointing to queried domain. Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#authority_score_profile/

        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Create the request URl
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_ascore_profile&target={target}"
                      f"&target_type={targetType}")

        response = self.sendRequest(requestURL)  # Send the request
        return response  # Return the response
   
    def getCategories(self, target:str, targetType:str, exportColumns:list=["category_name", "rating"]) -> dict:
        """
        This report returns the list of categories queried domain belong to. When you run a query for 
        a domain, in return, in each line, you receive a category and a rating. Rating is a level of
        confidence that this domain belongs to this category (ranged from 0 to 1). Results are sorted
        by the rating. Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#categories/

        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

        # Create the request URl
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_categories&target={target}"
                      f"&target_type={targetType}&export_columns={exportColumnsStr}")

        response = self.sendRequest(requestURL)  # Send the request
        return response  # Return the response

    def getHistoricalData(self, target:str, targetType:str, exportColumns:list=["source_url", "source_title", "response_code", "backlinks_num"], displayLimit:int=20) -> dict:
        """
        This report returns only monthly historical trends of number of backlinks and referring domains 
        for queried domain. When you run a query for a domain, in return, in each line, you receive a 
        date and a number of backlinks and referring domains queried domain had on this date. Results are 
        sorted by date in descending order (from most recent to oldest). Find more information here:
        https://developer.semrush.com/api/v3/analytics/backlinks/#indexed_pages/
        
        Parameters:
        ===========
        target : str
            The url, root domain or domain you want to get the backlink overview for
        
        targetType : str
            The type of requested target. Your options are root_domain, domain or url

        exportColumns : list
            The columns you want to be shown as a list.

        displayLimit : int
            Set a limit to how many items you want to display

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}"
                      f"&type=backlinks_pages"
                      f"&target={target}&"
                      f"target_type={targetType}&"
                      f"export_columns={exportColumnsStr}")

        # Put in any optional paramaters needed
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getAuthorityScoreProfile(self, target:str, targetType:str):
        """
        Find more info here: https://developer.semrush.com/api/v3/analytics/backlinks/#authority_score_profile/
        """

        # Get the request URL with all required parameters
        requestURL = f"https://api.semrush.com/analytics/v1/?key={self.API_KEY}&type=backlinks_ascore_profile&target={target}&target_type={targetType}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

        

    """
    Code for requesting information about domain reports
    """

    def getDomainOrganicSearchKeywords(self, domain:str, database:str, displayLimit:int=None, displayOffset:int=None, exportEscape:int=None, displayDate:str=None, displayDaily:int=None, exportColumns:list=None, displaySort:str=None, displayPositions:str="new", displayFilter:str=None) -> dict:
        """
        This report lists keywords that bring users to a domain via Google's top 100 organic search results.
        Find more information here: https://developer.semrush.com/api/v3/analytics/domain-reports/#domain-organic-search-keywords/

        Parameters:
        ==========
        domain : str
            The domain of the website you want to get info for. (www.example.com)

        database : str
            The database you want to use. Find databases here: https://developer.semrush.com/api/v3/analytics/basic-docs/#databases/

        displayLimit : int
            The number of results returned to a request. The default is 10,000

        displayOffset : int
            How many results you want to skip before sending a report

        exportEscape : int
            If set to 1, the report's columns will be wrapped in quotation marks

        displayDate : str
            A date formatted as YYYYMMDD

        displayDaily : int
            This parameter allows you to get daily updates on position changes that occurred in the last 30 days or more.

        exportColumns : list
            A list of the columns you want in the report

        displaySort : str
            How you want to sort the list

        displayPositions : str
            Which positions you want to see

        displayFilter : str
            Filter the results

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/",
                        f"?type=domain_organic"
                        f"&key={self.API_KEY}",
                        f"&domain={domain}",
                        f"&database={database}")

        # Put in any optional paramaters needed
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if exportEscape != None: requestURL += f"&export_escape={exportEscape}"
        if displayDate != None: requestURL += f"&display_date={displayDate}"
        if exportColumns != None: requestURL += f"export_columns={exportColumns}"
        if displaySort != None: requestURL += f"display_sort={displaySort}"
        if displayPositions != None: requestURL += f"display_positions={displayPositions}"
        if displayFilter != None: requestURL += f"display_filter={displayFilter}"

        # Send response
        response = self.sendRequest(requestURL)
        return response
        
    def getDomainPaidSearchKeywords(self, domain:str, database:str, displayLimit:int=None, displayOffset:int=None, exportEscape:int=1, exportDecode:int=None, displayDate:str=None, displayDaily:int=None, exportColumns:list=None, displaySort:str=None, displayPositions:str="new", displayFilter:str=None) -> dict:
        """
        This report lists keywords that bring users to a domain via Google's paid search results.
        Find more information here: https://developer.semrush.com/api/v3/analytics/domain-reports/#domain-paid-search-keywords/

        Parameters:
        ==========
        domain : str
            The domain of the website you want to get info for. (www.example.com)

        database : str
            The database you want to use. Find databases here: https://developer.semrush.com/api/v3/analytics/basic-docs/#databases/

        displayLimit : int
            The number of results returned to a request. The default is 10,000

        displayOffset : int
            How many results you want to skip before sending a report

        exportEscape : int
            If set to 1, the report's columns will be wrapped in quotation marks

        exportDecode : int
            If this parameter uses the value "0", the response will be sent as a URL-encoded string; if "1", the response will not be converted.

        displayDate : str
            A date formatted as YYYYMMDD

        displayDaily : int
            This parameter allows you to get daily updates on position changes that occurred in the last 30 days or more.

        exportColumns : list
            A list of the columns you want in the report

        displaySort : str
            How you want to sort the list

        displayPositions : str
            Which positions you want to see

        displayFilter : str
            Filter the results

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

             # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/",
                        f"?type=domain_adwords"
                        f"&key={self.API_KEY}",
                        f"&domain={domain}",
                        f"&database={database}")

        # Put in any optional paramaters needed
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if exportEscape != None: requestURL += f"&export_escape={exportEscape}"
        if exportDecode != None: requestURL += f"export_decode={exportDecode}"
        if displayDate != None: requestURL += f"&display_date={displayDate}"
        if exportColumns != None: requestURL += f"export_columns={exportColumns}"
        if displaySort != None: requestURL += f"display_sort={displaySort}"
        if displayPositions != None: requestURL += f"display_positions={displayPositions}"
        if displayFilter != None: requestURL += f"display_filter={displayFilter}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getAdsCopies(self, domain:str, database:str, displayLimit:int=None, displayOffset:int=None, exportEscape:int=1, exportDecode:int=None, displayDate:str=None, displayDaily:int=None, exportColumns:list=None, displaySort:str=None, displayFilter:str=None) -> dict:
        """
        This report shows unique ad copies Semrush noticed when the domain ranked in Google's paid search 
        results for keywords from our databases. Find more information here: 
        https://developer.semrush.com/api/v3/analytics/domain-reports/#ads-copies/

        Parameters:
        ==========
        domain : str
            The domain of the website you want to get info for. (www.example.com)

        database : str
            The database you want to use. Find databases here: https://developer.semrush.com/api/v3/analytics/basic-docs/#databases/

        displayLimit : int
            The number of results returned to a request. The default is 10,000

        displayOffset : int
            How many results you want to skip before sending a report

        exportEscape : int
            If set to 1, the report's columns will be wrapped in quotation marks

        exportDecode : int
            If this parameter uses the value "0", the response will be sent as a URL-encoded string; if "1", the response will not be converted.

        displayDate : str
            A date formatted as YYYYMMDD

        displayDaily : int
            This parameter allows you to get daily updates on position changes that occurred in the last 30 days or more.

        exportColumns : list
            A list of the columns you want in the report

        displaySort : str
            How you want to sort the list

        displayPositions : str
            Which positions you want to see

        displayFilter : str
            Filter the results

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

             # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/",
                        f"?type=domain_adwords_unique"
                        f"&key={self.API_KEY}",
                        f"&domain={domain}",
                        f"&database={database}")

        # Put in any optional paramaters needed
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if exportEscape != None: requestURL += f"&export_escape={exportEscape}"
        if exportDecode != None: requestURL += f"export_decode={exportDecode}"
        if displayDate != None: requestURL += f"&display_date={displayDate}"
        if exportColumns != None: requestURL += f"export_columns={exportColumns}"
        if displaySort != None: requestURL += f"display_sort={displaySort}"
        if displayFilter != None: requestURL += f"display_filter={displayFilter}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getCompetitorsInOrganicSearch(self, domain:str, database:str, displayLimit:int=None, displayOffset:int=None, exportEscape:int=1, exportDecode:int=None, displayDate:str=None, displayDaily:int=None, exportColumns:list=None, displaySort:str=None) -> dict:
        """
        This report lists a domain’s competitors in organic search results. 
        Find more information here: 
        https://developer.semrush.com/api/v3/analytics/domain-reports/#competitors-in-organic-search/

        Parameters:
        ==========
        domain : str
            The domain of the website you want to get info for. (www.example.com)

        database : str
            The database you want to use. Find databases here: https://developer.semrush.com/api/v3/analytics/basic-docs/#databases/

        displayLimit : int
            The number of results returned to a request. The default is 10,000

        displayOffset : int
            How many results you want to skip before sending a report

        exportEscape : int
            If set to 1, the report's columns will be wrapped in quotation marks

        exportDecode : int
            If this parameter uses the value "0", the response will be sent as a URL-encoded string; if "1", the response will not be converted.

        displayDate : str
            A date formatted as YYYYMMDD

        displayDaily : int
            This parameter allows you to get daily updates on position changes that occurred in the last 30 days or more.

        exportColumns : list
            A list of the columns you want in the report

        displaySort : str
            How you want to sort the list

        displayPositions : str
            Which positions you want to see

        displayFilter : str
            Filter the results

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

             # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/",
                        f"?type=domain_organic_organic"
                        f"&key={self.API_KEY}",
                        f"&domain={domain}",
                        f"&database={database}")

        # Put in any optional paramaters needed
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if exportEscape != None: requestURL += f"&export_escape={exportEscape}"
        if exportDecode != None: requestURL += f"export_decode={exportDecode}"
        if displayDate != None: requestURL += f"&display_date={displayDate}"
        if exportColumns != None: requestURL += f"export_columns={exportColumns}"
        if displaySort != None: requestURL += f"display_sort={displaySort}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getCompetitorsInPaidSearch(self, domain:str, database:str, displayLimit:int=None, displayOffset:int=None, exportEscape:int=1, exportDecode:int=None, displayDate:str=None, displayDaily:int=None, exportColumns:list=None, displaySort:str=None) -> dict:
        """
        This report lists a domain’s competitors in paid search results. 
        Find more information here: 
        https://developer.semrush.com/api/v3/analytics/domain-reports/#competitors-in-paid-search/

        Parameters:
        ==========
        domain : str
            The domain of the website you want to get info for. (www.example.com)

        database : str
            The database you want to use. Find databases here: https://developer.semrush.com/api/v3/analytics/basic-docs/#databases/

        displayLimit : int
            The number of results returned to a request. The default is 10,000

        displayOffset : int
            How many results you want to skip before sending a report

        exportEscape : int
            If set to 1, the report's columns will be wrapped in quotation marks

        exportDecode : int
            If this parameter uses the value "0", the response will be sent as a URL-encoded string; if "1", the response will not be converted.

        displayDate : str
            A date formatted as YYYYMMDD

        displayDaily : int
            This parameter allows you to get daily updates on position changes that occurred in the last 30 days or more.

        exportColumns : list
            A list of the columns you want in the report

        displaySort : str
            How you want to sort the list

        displayPositions : str
            Which positions you want to see

        displayFilter : str
            Filter the results

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

             # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/",
                        f"?type=domain_adwords_adwords"
                        f"&key={self.API_KEY}",
                        f"&domain={domain}",
                        f"&database={database}")

        # Put in any optional paramaters needed
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if exportEscape != None: requestURL += f"&export_escape={exportEscape}"
        if exportDecode != None: requestURL += f"export_decode={exportDecode}"
        if displayDate != None: requestURL += f"&display_date={displayDate}"
        if exportColumns != None: requestURL += f"export_columns={exportColumns}"
        if displaySort != None: requestURL += f"display_sort={displaySort}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getDomainAdHistory(self, domain:str, database:str, displayLimit:int=None, displayOffset:int=None, exportEscape:int=1, exportDecode:int=None, exportColumns:list=None) -> dict:
        """
        This report shows keywords a domain has bid on in the last 12 months and its positions in paid search results. 
        Find more information here: 
        https://developer.semrush.com/api/v3/analytics/domain-reports/#domain-ad-history/

        Parameters:
        ==========
        domain : str
            The domain of the website you want to get info for. (www.example.com)

        database : str
            The database you want to use. Find databases here: https://developer.semrush.com/api/v3/analytics/basic-docs/#databases/

        displayLimit : int
            The number of results returned to a request. The default is 10,000

        displayOffset : int
            How many results you want to skip before sending a report

        exportEscape : int
            If set to 1, the report's columns will be wrapped in quotation marks

        exportDecode : int
            If this parameter uses the value "0", the response will be sent as a URL-encoded string; if "1", the response will not be converted.

        exportColumns : list
            A list of the columns you want in the report

        displayFilter : str
            Filter the results

        Returns:
        ========
        response : dict
            The response of the request
        """

        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/",
                        f"?type=domain_adwords_historical"
                        f"&key={self.API_KEY}",
                        f"&domain={domain}",
                        f"&database={database}")

        # Put in any optional paramaters needed
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if exportEscape != None: requestURL += f"&export_escape={exportEscape}"
        if exportDecode != None: requestURL += f"export_decode={exportDecode}"
        if exportColumns != None: requestURL += f"export_columns={exportColumns}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getKeywordOverview(self, phrase:str, database:str=None, exportEscape:int=None, exportDecode:int=None, exportColumns:list=None):
        # Turn the export columns list into a string
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        
        # Get the request URL with all required parameters
        requestURL = (f"https://api.semrush.com/",
                        f"?type=phrase_all",
                        f"&key={self.API_KEY}",
                        f"&phrase={phrase}")

        if database != None: requestURL += f"&database={database}"
        if exportEscape != None: requestURL += f"&export_escape={exportEscape}"
        if exportDecode != None: requestURL += f"&export_decode={exportDecode}"
        if exportColumns != None: requestURL += f"&export_columnw={exportColumns}"

        # Send response
        response = self.sendRequest(requestURL)
        return response


    def getTrafficSummary(self, targets:list, displayData:str, deviceType:str, country:str, exportColumns:list):
        
        try:
            exportColumnsStr = "" 
            for i in exportColumns:
                exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i
        except:
            pass
        
        try:
            targetsStr = "" 
            for i in targets:
                targetsStr += f"{i}," if targets.index(i) != len(targets)-1 else i
        except:
            pass

        #requestURL = (f"https://api.semrush.com/analytics/ta/api/v3/summary?targets={targetsStr}&display_date={displayData}&device_type={deviceType}&country={country}&export_columns={exportColumnsStr}")
        requestURL = f"https://api.semrush.com/analytics/ta/api/v3/summary?targets=golang.org,blog.golang.org,tour.golang.org/welcome/&export_columns=target,visits,users&key={self.API_KEY}"

        # Send response
        response = self.sendRequest(requestURL)
        return response;
    
    def getDomainRankings(self, displayDate:str=None, deviceType:str=None, displayLimit:int=None, displayOffset:int=None, country:str=None, exportColumns:list=None):
        """
        
        """
        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

        requestURL = ("https://api.semrush.com/analytics/ta/api/v3/rank?&key=YOUR_API_KEY")

        if displayDate != None: requestURL += f"&display_date={displayDate}"
        if deviceType != None: requestURL += f"&device_type={deviceType}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if country != None: requestURL += f"&country={country}"
        if exportColumns != None: requestURL += f"&export_columns={exportColumnsStr}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getSemrushRank(self, database, displayLimit=None, displayOffset=None, exportEscape=None, exportDecode=None, displayDate=None, exportColumns=None):
        """
        Find more information here: https://developer.semrush.com/api/v3/analytics/overview-reports/#semrush-rank/
        """

        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

        requestURL = f"https://api.semrush.com/?key={self.API_KEY}&database={database}"

        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displayOffset != None: requestURL += f"&display_offset={displayOffset}"
        if exportEscape != None: requestURL += f"&export_columns={exportEscape}"
        if exportDecode != None: requestURL += f"&export_columns={exportDecode}"
        if displayDate != None: requestURL += f"&export_columns={displayDate}"
        if exportColumns != None: requestURL += f"&export_columns={exportColumnsStr}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getDomainOverview(self, domain:str, database:str=None, displayLimit:int=None, displatOffset:int=None, exportEscape:int=None, displayDate:str=None, exportColumns:list=None, displaySort:str=None):
        """
        Find more information here: https://developer.semrush.com/api/v3/analytics/overview-reports/#domain-overview-all-databases/
        """


        exportColumnsStr = "" 
        for i in exportColumns:
            exportColumnsStr += f"{i}," if exportColumns.index(i) != len(exportColumns)-1 else i

        requestURL = f"https://api.semrush.com/?key={self.API_KEY}&type=domain_ranks&domain={domain}"
        
        if database != None: requestURL += f"&database={database}"
        if displayLimit != None: requestURL += f"&display_limit={displayLimit}"
        if displatOffset != None: requestURL += f"&display_offset={displatOffset}"
        if exportEscape != None: requestURL += f"&export_escape={exportEscape}"
        if displayDate != None: requestURL += f"&displayDate={displayDate}"
        if exportColumns != None: requestURL += f"&export_columns={exportColumnsStr}"
        if displaySort != None: requestURL += f"&display_sort={displaySort}"

        # Send response
        response = self.sendRequest(requestURL)
        return response

    def getContent(self, URL):
        backlinks = self.getBacklinksOverview(URL, "domain", exportColumns=["total", "ascore"])
        b = backlinks["_value"].split("\r\n")[1].split(";")
        
        return [b[0].strip(), b[1].strip()]


if __name__ == "__main__":
    site = semrush("e472db72a04560d630bc4d2866f62cbf")
    #t = site.getTrafficSummary(["astoundz.com"], 1, 1, 1, 1)
    #t = site.getTrafficSummary(1, 1, 1, 1, 1)
    
    c = site.getContent("astoundz.com")
    #authorityScore = site.getAuthorityScoreProfile("astoundz.com", "domain")
    #traffic = site.getTrafficSummary(1, 1, 1, 1, 1)
    #domainOverview = site.getDomainOverview("astoundz.com", database='us', exportColumns="Rk, Or, Ot")

    print(c)

    # For refferingips
    # for i in v: 
    #     try:
    #         n = int(i.split(";")[len(i.split(";"))-1].strip())
    #         print(n)
    #         num += n
    #     except:
    #         pass

    #print(backlinks)