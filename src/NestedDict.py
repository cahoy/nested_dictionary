from collections.abc import MutableMapping


class NestedDict(MutableMapping):

    def __init__(self, root=True):
        super().__init__()
        self._val = {}
        self._found = False
        self._root = root

    def __getitem__(self, item):

        if item in self._val:
            return self._val.__getitem__(item)
        else:
            n = NestedDict(root=False)
            result = None
            for k, v in self._val.items():
                if isinstance(v, dict):
                    n._val = self._val[k]
                    if item in n:
                        result = n[item]
                        n._found = True
                    self._found = self._found or n._found

            if self._root:
                if self._found:
                    self._found = False
                else:
                    raise KeyError

            return result

    def __setitem__(self, branch_key, value):
        if isinstance(branch_key, tuple):
            branch, key = branch_key
            n = NestedDict(root=False)
            for k, v in self._val.items():
                if v and isinstance(v, dict):
                    n._val = self._val[k]
                    n[branch_key] = value
                    self._found = self._found or n._found

                if k == branch:
                    self._found = True
                    if not isinstance(self._val[branch], dict):
                        if self._val[branch]:
                            raise ValueError('value of this key is not a logical False')
                        else:
                            self._val[branch] = {}  # replace None, [], 0 and False to {}
                    self._val[branch][key] = value

            if self._root:
                if self._found:
                    self._found = False
                else:
                    raise KeyError

        elif branch_key in self._val:
            self._found = True
            self._val.__setitem__(branch_key, value)

        else:
            n = NestedDict(root=False)
            for k, v in self._val.items():
                if v and isinstance(v, dict):
                    n._val = self._val[k]
                    n[branch_key] = value
                    self._found = self._found or n._found

            if self._root:
                if self._found:
                    self._found = False
                else:
                    self._val.__setitem__(branch_key, value)

    def __delitem__(self, key):
        self._val.__delitem__(key)

    def __iter__(self):
        return self._val.__iter__()

    def __len__(self):
        return self._val.__len__()

    def __repr__(self):
        return str(self._val)