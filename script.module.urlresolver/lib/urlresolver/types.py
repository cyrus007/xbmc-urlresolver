#    urlresolver XBMC Addon
#    Copyright (C) 2011 t0mm0
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urlresolver
from plugnplay.interfaces import NewUrlResolver

class HostedMediaFile:

    def __init__(self, url='', host='', media_id='', title=''):
        if not url and not (host and media_id) or (url and (host or media_id)):
            raise ValueError('Set either url, or host AND media_id. ' +
                             'No other combinations are valid.')
        if url:
            self._url = url
            self._host = ''
            self._media_id = ''
        else:
            self._url = ''
            self._host = host
            self._media_id = media_id
        
        self._resolvers = self._find_resolvers()
        print self._resolvers
        if url and self._resolvers:
            self._host, self._media_id = self._resolvers[0].get_host_and_id(url)
        elif self._resolvers:
            self._url = self._resolvers[0].get_url(host, media_id)
            
        
        if title:
            self.title = title
        else:
            self.title = self._host

    def get_url(self):
        return self._url    
    
    def get_host(self):
        return self._host
        
    def get_media_id(self):
        return self._media_id
          
    def resolve(self):
        print self
        if self._resolvers:
            return self._resolvers[0].get_media_url(self._host, self._media_id)
        else:
            return False
        
    def valid_url(self):
        if self._resolvers:
            return True
        return False
        
    def _find_resolvers(self):
        imps = []
        for imp in NewUrlResolver.implementors():
            if imp.valid_url(self):
                imps.append(imp)
        return imps

        
    def __nonzero__(self):
        return self.valid_url() 
        
    def __str__(self):
        return '{\'url\': \'%s\', \'host\': \'%s\', \'media_id\': \'%s\'}' % (
                    self._url, self._host, self._media_id)

    def __repr__(self):
        return self.__str__()
