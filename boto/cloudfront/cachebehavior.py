# Copyright (c) 2006-2009 Mitch Garnaat http://garnaat.org/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from boto.cloudfront.signers import TrustedSigners

class CacheBehavior(object):

    def __init__(self, path_pattern=None, target_origin_id='', forwarded_values=None,
                 trusted_signers=None, viewer_protocol_policy=None,
                 min_ttl=None,allowed_methods=None,smooth_streaming=None):
        """

        :param path_pattern: The pattern for which this cache behavior applies to.
        :type path_pattern: string

        :param target_origin_id: ID of the origin
        :type origin: string

        :param forwarded_values:
        :type forwarded_values: :class`boto.cloudfront.cachebehavior.ForwardedValues`

        :param trusted_signers: list of trusted signers AWS Account IDs or self
        :type trusted_signers: list of string

        :param viewer_protocol_policy: redirect-to-https or allow-all
        :type viewer_protocol_policy: string

        :param min_ttl: TTL for the distribution
        :type min_ttl: int

        :param allowed_methods: list of HTTP verbs to allow for cache. Ex: ["GET", "HEAD"]
        :type trusted_signers: list of string

        :param smooth_streaming: Indicates whether to distribute media files in the Microsoft Smooth Streaming format by using the origin that is associated with this cache behavior. If you specify true, you can still use this cache behavior to distribute other content if the content matches the PathPattern value.
        :type smooth_streaming: bool
        """

        self.path_pattern = path_pattern
        self.target_origin_id = target_origin_id
        self.forwarded_values = forwarded_values
        self.trusted_signers = trusted_signers
        self.viewer_protocol_policy = viewer_protocol_policy
        self.min_ttl = min_ttl
        self.allowed_methods = allowed_methods
        self.smooth_streaming = smooth_streaming

    def __repr__(self):
        return '<{}: {} {} {} {}>'.format( type(self).__name__, self.target_origin_id, self.path_pattern, self.forwarded_values, self.trusted_signers, self.min_ttl)

    def startElement(self, name, attrs, connection):
        if name == 'ForwardedValues':
            self.forwarded_values = ForwardedValues()
            return self.forwarded_values
        if name == 'TrustedSigners':
            self.trusted_signers = TrustedSigners()
            return self.trusted_signers
        if name == 'AllowedMethods':
            self.allowed_methods = AllowedMethods()
            return self.allowed_methods
        return None

    def endElement(self, name, value, connection):
        if name == 'PathPattern':
            self.path_pattern = value
        elif name == 'TargetOriginId':
            self.target_origin_id = value
        elif name == 'ForwardedValues':
            self.forwarded_values = value
        elif name == 'TrustedSigners':
            self.trusted_signers = value
        elif name == 'ViewerProtocolPolicy':
            self.viewer_protocol_policy = value
        elif name == 'MinTTL':
            try:
                self.min_ttl = int(value)
            except ValueError:
                self.min_ttl = value
        elif name == 'AllowedMethods':
            self.allowed_methods = value
        elif name == 'SmoothStreaming':
            if value.lower() == 'true':
                self.smooth_streaming = True
            else:
                self.smooth_streaming = False
        else:
            setattr(self, name, value)

    def to_xml(self):
        classname = type(self).__name__
        s = '  <%s>\n' % classname
        if self.path_pattern:
            s += '    <PathPattern>%s</PathPattern>\n' % self.path_pattern
        if self.target_origin_id:
            s += '    <TargetOriginId>%s</TargetOriginId>\n' % self.target_origin_id
        if self.forwarded_values:
            s += self.forwarded_values.to_xml()
        if self.trusted_signers:
            s += '    <TrustedSigners>\n'
            s += '      <Enabled>true</Enabled>\n'
            s += '      <Quantity>%s</Quantity>\n' % len(self.trusted_signers)
            s += '      <Items>\n'
            for signer in self.trusted_signers:
                s += '        <AwsAccountNumber>%s</AwsAccountNumber>\n' % signer
            s += '      </Items>\n'
            s += '    </TrustedSigners>\n'
        if self.viewer_protocol_policy:
            s += '    <ViewerProtocolPolicy>%s</ViewerProtocolPolicy>\n' % self.viewer_protocol_policy
        if self.min_ttl:
            s += '    <MinTTL>%s</MinTTL>\n' % self.min_ttl
        if self.allowed_methods:
            s += '    <AllowedMethods>\n'
            if self.allowed_methods.items:
                s += '      <Quantity>%s</Quantity>\n' % len(self.allowed_methods.items)
                s += '      <Items>\n'
                for name in self.allowed_methods.items:
                    s += '        <Method>%s</Method>\n' % name
                s += '      </Items>\n'
            if self.allowed_methods.cached_methods:
                s += '      <CachedMethods>\n'
                s += '        <Quantity>%s</Quantity>\n' % len(self.allowed_methods.cached_methods)
                s += '        <Items>\n'
                for name in self.allowed_methods.cached_methods:
                    s += '          <Method>%s</Method>\n' % name
                s += '        </Items>\n'
                s += '      </CachedMethods>\n'
            s += '    </AllowedMethods>\n'
        s += '    <SmoothStreaming>'
        if self.smooth_streaming:
            s += 'true'
        else:
            s += 'false'
        s += '</SmoothStreaming>\n'
        s += '  </%s>\n' % classname
        return s

class ForwardedValues(object):
    def __init__(self, querystring=None, cookies=None, headers=None):
        """
        :param querystring: True to forward querystring values
        :type querystring: bool

        :param cookies: list of Cookies to forward
        :type cookies: list of :class`boto.cloudfront.cachebehavior.Cookies`

        """
        self.querystring = querystring
        self.cookies = cookies
        self.headers = headers

    def __repr__(self):
        return '<ForwardedValues: %s>' % self.querystring

    def startElement(self, name, attrs, connection):
        if name == 'Cookies':
            self.cookies = Cookies()
            return self.cookies
        return None

    def endElement(self, name, value, connection):
        if name == 'QueryString':
            self.querystring = value
        else:
            setattr(self, name, value)

    def to_xml(self):
        s = '    <ForwardedValues>\n'
        s += '      <QueryString>'
        if self.querystring:
            s += 'true'
        else:
            s += 'false'
        s += '</QueryString>\n'
        if self.cookies:
            s += self.cookies.to_xml()
        s += '    </ForwardedValues>\n'
        return s

class Cookies(object):
    def __init__(self,forward=None,whitelisted_names=None):
        """
        :param forward: all or whitelist
        :type forward: string

        :param whitelisted_names: if whitelist, the list of cookie names to forward
        :type whitelisted_names: list of string

        """
        self.forward = forward
        self.whitelisted_names = whitelisted_names

    def __repr__(self):
        return '<Cookies: %s>' % self.forward

    def startElement(self, name, attrs, connection):
        if name == 'WhitelistedNames':
            self.whitelisted_names = WhitelistedNames()
            return self.whitelisted_names
        return None

    def endElement(self, name, value, connection):
        if name == 'Forward':
            self.forward = value
        elif name == 'WhitelistedNames':
            self.whitelisted_names = values
        else:
            setattr(self, name, value)

    def to_xml(self):
        s = '      <Cookies>\n'
        if self.forward:
            s += '        <Forward>%s</Forward>\n' % self.forward
        if self.forward == 'whitelist' and self.whitelisted_names:
            s += '        <WhitelistedNames>\n'
            s += '          <Quantity>%s</Quantity>\n' % len(self.whitelisted_names)
            s += '          <Items>\n'
            for name in self.whitelisted_names:
                s += '            <Name>%s</Name>\n' % name
            s += '          </Items>\n'
            s += '        </WhitelistedNames>\n'
        s += '      </Cookies>\n'
        return s

class WhitelistedNames(object):
    def __init__(self, items=None):
        self.items = items

    def startElement(self, name, attrs, connection):
        if name == 'Items':
            self.items = Names()
            return self.items
        return None

    def endElement(self, name, value, connection):
        if name == 'Items':
            self.items = value
        else:
            setattr(self, name, value)

class Names(list):
    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == 'Name':
            self.append(value)

class AllowedMethods(object):
    def __init__(self, items=None,cached_methods=None):
        self.items = items
        self.cached_methods = cached_methods

    def startElement(self, name, attrs, connection):
        if name == 'Items':
            self.items = Methods()
            return self.items
        if name == 'CachedMethods':
            self.cached_methods = Methods()
            return self.cached_methods
        return None

    def endElement(self, name, value, connection):
        if name == 'Items':
            self.items = value
        elif name == 'CachedMethods':
            self.cached_methods = value
        else:
            setattr(self, name, value)

class Methods(list):
    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == 'Method':
            self.append(value)

class DefaultCacheBehavior(CacheBehavior):
    pass

class CacheBehaviors(object):
    def __init__(self,items=None):
        self.items = items

    def startElement(self, name, attrs, connection):
        if name == 'Items':
            self.items = CacheBehaviorList()
            return self.items
        return None

    def endElement(self, name, value, connection):
        setattr(self, name, value)

    def to_xml(self):
        length = len(self.items)
        s = '  <CacheBehaviors>\n'
        s += '    <Quantity>%s</Quantity>\n' % length
        if length > 0:
            s += '    <Items>\n'
            for cache_behavior in self.items:
                s += cache_behavior.to_xml()
            s += '    </Items>\n'
        s += '  </CacheBehaviors>\n'
        return s

class CacheBehaviorList(list):
    def startElement(self, name, attrs, connection):
        return None

    def endElement(self, name, value, connection):
        if name == 'CacheBehaviors':
            self.append(value)