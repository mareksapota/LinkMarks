import urllib.request
import urllib.parse
import json
import threading

app_id = None
rest_key = None

def init(parse_app_id, parse_rest_key):
    global app_id, rest_key
    app_id = parse_app_id
    rest_key = parse_rest_key

class ParsePromise(threading.Thread):
    def __init__(self, fun, *args, **kwargs):
        threading.Thread.__init__(self)
        self.__fun = fun
        self.__args = args
        self.__kwargs = kwargs
        self.__ret = None
        self.start()

    def run(self):
        self.__ret = self.__fun(*self.__args, **self.__kwargs)

    def prep(self):
        self.join()
        return self.__ret

    def then(self, fun):
        return ParsePromise(lambda: fun(self.prep()))

class ParseBase():
    api_url = "https://api.parse.com/1/classes/"

    @staticmethod
    def make_request(url, method, data = None):
        global app_id, rest_key
        headers = {
            "X-Parse-Application-Id": app_id,
            "X-Parse-REST-API-Key": rest_key,
        }
        if data is not None:
            if method != 'GET':
                data = json.dumps(data).encode("utf-8")
                headers["Content-Type"] = "application/json"
            else:
                url += "?" + urllib.parse.urlencode(data)
                data = None
        req = urllib.request.Request(
            url,
            headers = headers,
            data = data,
        )
        req.get_method = lambda: method
        ret = urllib.request.urlopen(req)
        data = ret.read().decode("utf-8")
        ret.close()
        return data

class ParseQuery(ParseBase):
    def __init__(self, cls):
        self.__cls = cls
        self.__where = {}
        self.__limit = None
        self.__skip = None
        self.__order = []

    def __make_prop(self, prop, name, value):
        if prop in self.__where and type(self.__where[prop]) != dict:
            raise Exception(prop + " already has an equal to constraint")
        if prop not in self.__where:
            self.__where[prop] = {}
        self.__where[prop][name] = value

    def equal_to(self, prop, value):
        self.__where[prop] = value
        return self

    def not_equal_to(self, prop, value):
        self.__make_prop(prop, "$ne", value)
        return self

    def greater_than(self, prop, value):
        self.__make_prop(prop, "$gt", value)
        return self

    def greater_than_or_equal_to(self, prop, value):
        self.__make_prop(prop, "$gte", value)
        return self

    def less_than(self, prop, value):
        self.__make_prop(prop, "$lt", value)
        return self

    def less_than_or_equal_to(self, prop, value):
        self.__make_prop(prop, "$lte", value)
        return self

    def matches(self, prop, value):
        self.__make_prop(prop, "$regex", value)
        return self

    def limit(self, value):
        self.__limit = value
        return self

    def skip(self, value):
        self.__skip = value
        return self

    def ascending(self, prop):
        self.__order.append(prop)
        return self

    def descending(self, prop):
        self.__order.append("-" + prop)
        return self

    def gen_find(self):
        return ParsePromise(self.find)

    def find(self):
        data = {}
        if self.__where:
            data["where"] = json.dumps(self.__where)
        if self.__limit is not None:
            data["limit"] = self.__limit
        if self.__skip is not None:
            data["skip"] = self.__skip
        if self.__order:
            data["order"] = ",".join(self.__order)
        ret = self.make_request(
            self.api_url + self.__cls.__name__,
            "GET",
            data = data,
        )
        results = json.loads(ret)["results"]
        return [self.__cls(**data) for data in results]

    @staticmethod
    def or_(*queries):
        cls = queries[0].__cls
        for query in queries:
            if query.__cls != cls:
                raise Exception(
                    "All classes have to be the same, got {} and {}".format(
                        query.__cls.__name__,
                        cls.__name__,
                    )
                )
        query = ParseQuery(cls)
        query.__where["$or"] = [q.__where for q in queries]
        return query

class ParseObj(ParseBase):
    def __init__(self, properties, values):
        self.__cls = self.__class__
        self.__cls_name = self.__cls.__name__
        for prop in properties:
            if properties[prop].get("type") is None:
                raise AttributeError(
                    "Property type not specified: {}.{}".format(
                        self.__cls_name,
                        prop,
                    )
                )
        for prop in values:
            if prop in properties and values[prop] is not None:
                # Parse stores both int and float as number type, converting
                # here prevents type errors when save() is called.
                t = properties[prop]["type"]
                setattr(self, prop, t(values[prop]))
            else:
                setattr(self, prop, values[prop])
        self.__properties = properties
        self.__base_url = self.api_url + self.__cls_name

    @classmethod
    def query(cls):
        return ParseQuery(cls)

    def save(self):
        data = {}
        for prop in self.__properties:
            val = getattr(self, prop, None)
            if val is None:
                if not self.__properties[prop].get("nullable", False):
                    raise AttributeError(prop + " should not be empty")
            elif type(val) != self.__properties[prop]["type"]:
                raise AttributeError(
                    "{}.{} expected type {} but got {} instead".format(
                        self.__cls_name,
                        prop,
                        self.__properties[prop]["type"].__name__,
                        type(val).__name__,
                    )
                )
            data[prop] = val

        url = self.__base_url
        method = "POST"
        if hasattr(self, "objectId"):
            # update request
            url += "/" + getattr(self, "objectId")
            method = "PUT"
        ret = self.make_request(url, method, data = data)
        if not hasattr(self, "objectId"):
            # create request
            self.objectId = json.loads(ret)["objectId"]

    def destroy(self):
        if not hasattr(self, "objectId"):
            raise Exception("Can not destroy object that has not been saved")
        self.make_request(
            self.__base_url + "/" + getattr(self, "objectId"),
            "DELETE",
        )
        delattr(self, "objectId")

    @classmethod
    def get(cls, objectId):
        cls_name = cls.__name__
        url = "{}{}/{}".format(ParseObj.api_url, cls_name, objectId)
        ret = ParseObj.make_request(url, "get")
        data = json.loads(ret)
        return cls(**data)