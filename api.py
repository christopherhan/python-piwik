# -*- coding: utf-8 -*-
import urllib
import httplib
import urlparse
import simplejson

class PiwikApi:
    def __init__(self, url, token_auth):
        self.url = url
        self.token_auth = token_auth

        (scheme, netloc, path, query, fragment) = urlparse.urlsplit(self.url)
        self.host = netloc

    def call(self, method, params = {}, format = 'json'):
        args = {'module' : 'API',
                'method' : method,
                'format' : format,
                'token_auth' : self.token_auth}
        args.update(params)
        
        conn = httplib.HTTPConnection(self.host)
        
        conn.request('GET', u"%s?%s" % (self.url, urllib.urlencode(args)), 
                headers={'User-Agent' : 'Django Piwik'})
        result = conn.getresponse()
        data = None
        if result.status == 200:
            data = result.read()
        conn.close()
        if data is not None and format == 'json':
            return simplejson.loads(data)
        return data
    
    """
    Actions
    """
    def getPageTitles(self, id, period, date, segment='', expanded='', id_subtable=''):
        return self.call('Actions.getPageTitles', params = {'idSite':id, 'period':period,
                'date':date, 'segment':segment, 'expanded':expanded,
                'idSubtable':id_subtable})
        
        
    """
    SiteManager
    """
    def getAllSites(self):
        return self.call('SitesManager.getSitesWithAtLeastViewAccess')

    def getSiteFromId(self, id):
        return self.call('SitesManager.getSiteFromId', params = {'idSite' : id})

    def getJavascriptTag(self, id, piwikUrl = '', actionName = ''):
        result = self.call('SitesManager.getJavascriptTag', params = {'idSite' : id})
        if result:
            return result['value']
        return None
        
    def addSite(self, sitename, urls, excluded_ips='', excluded_query_params='', 
                timezone='', currency='', group='', start_date=''):
        return self.call('SitesManager.addSite', params = {'siteName': sitename,
                'urls': urls, 'excludedIps': excluded_ips, 
                'excludedQueryParameters':excluded_query_params, 'timezone':timezone,
                'currency':currency, 'group':group, 'startdate':start_date})
    
    def getSitesIdFromSiteUrl(self, url):
        return self.call('SitesManager.getSitesIdFromSiteUrl', params = {'url':url})
    
    """
    UsersManager
    """
    def addUser(self, username, password, email, alias  = ''):
        return self.call('UsersManager.addUser', params = {'userLogin': username,
                'password': password, 'email': email, 'alias': alias})
                
    def getUser(self, username):
        return self.call('UsersManager.getUser', params = {'userLogin': username})

    def getUsersSiteFromAccess(self, access):
        return self.call('UsersManager.getUsersSitesFromAccess', params = {'access':access})
    
    def setUserAccess(self, login, access, ids):
        return self.call('UsersManager.setUserAccess', params = {'userLogin':login,
                'access':access, 'idSites':ids})
                
    def deleteUser(self, login):
        return self.call('UsersManager.deleteUser', params={'userLogin':login})
        
    """
    User Country
    """
    def getCountry(self, id, period, date, segment=''):
        return self.call('UserCountry.getCountry', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    
    def getContinent(self, id, period, date, segment=''):
        return self.call('UserCountry.getContinent', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    def getNumberOfDistinctCountries(self, id, period, date, segment=''):
        return self.call('UserCountry.getNumberOfDistinctCountries', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    """
    UserSettings
    """
    def getResolution(self, id, period, date, segment=''):
        return self.call('UserSettings.getResolution', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    
    def getOS(self, id, period, date, segment=''):
        return self.call('UserSettings.getOS', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    
    def getBrowser(self, id, period, date, segment=''):
        return self.call('UserSettings.getBrowser', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})

    def getBrowserType(self, id, period, date, segment=''):
        return self.call('UserSettings.getBrowserType', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    
    def getWideScreen(self, id, period, date, segment=''):
        return self.call('UserSettings.getWideScreen', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    
    def getGetPlugin(self, id, period, date, segment=''):
        return self.call('UserSettings.getPlugin', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
                
    """
    VisitFrequency
    """
    def getVisitsReturning(self, id, period, date):
        return self.call('VisitFrequency.getVisitsReturning', 
                params = {'idSite': id, 'period':period, 'date':date})
    
    
    """
    VisitorInterest
    """
    def getNumberOfVisitsPerPage(self, id, period, date, segment=''):
        return self.call('VisitorInterest.getNumberOfVisitsPerPage', 
                params = {'idSite': id, 'period':period, 'date':date, 'segment':segment})
    
    def getNumberOfVisitsPerVisitDuration(self, id, period, date, segment=''):
        return self.call('VisitorInterest.getNumberOfVisitsPerVisitDuration', 
                params = {'idSite': id, 'period':period, 'date':date, 'segment':segment})
    
    """
    VisitsSummary
    """
    def get(self, id, period, date, segment='', columns=''):
        return self.call('VisitsSummary.get', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment, 'columns':columns})
    
    def getVisits(self, id, period, date, segment=''):
        return self.call('VisitsSummary.getVisits', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
                
    def getUniqueVisitors(self, id, period, date, segment=''):
        return self.call('VisitsSummary.getUniqueVisitors', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    
    def getSumVisitsLengthPretty(self, id, period, date, segment=''):
        return self.call('VisitsSummary.getSumVisitsLengthPretty', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment})
    
    """
    Referrers
    """
    def getSearchEngines(self, id, period, date, segment='', expanded=''):
        return self.call('Referers,getSearchEngines', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment, 'expanded':expanded})
    
    def getRefererType(self, id, period, date, segment='', type_referer=''):
        return self.call('Referers.getRefererType', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment, 'typeReferer':type_referer})

    def getKeywords(self, id, period, date, segment='', expanded=''):
        return self.call('Referers,getKeywords', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment, 'expanded':expanded})

    def getWebsites(self, id, period, date, segment='', expanded=''):
        return self.call('Referers,getWebsites', params = {'idSite': id, 
                'period':period, 'date':date, 'segment':segment, 'expanded':expanded})
