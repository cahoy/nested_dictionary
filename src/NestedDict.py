from collections.abc import MutableMapping


class NestedDict(MutableMapping):

    def __init__(self, root=True):
        super().__init__()
        self._val = {}
        self._found = False
        self._root = root

    def __getitem__(self, item):
        self._found = False

        def _look_deeper():
            n = NestedDict(root=False)
            result = None
            for k, v in self._val.items():
                if isinstance(v, dict):
                    n._val = self._val[k]
                    if item in n:
                        result = n[item]
                    self._found = self._found or n._found

            if self._root:
                if self._found:
                    self._found = False
                else:
                    raise KeyError

            return result

        def _process_slash():
            first_branch, *branches = item.split('/')

            nd = NestedDict(root=False)

            nd._val = self._val[first_branch]
            result = nd['/'.join(branches)]

            return result

        if self.__isstring_containing_char(item, '/'):
            return _process_slash()

        elif item in self._val:
            self._found = True
            return self._val.__getitem__(item)
        else:
            return _look_deeper()

    def __setitem__(self, branch_key, value):
        self._found = False

        def _process_tuple():
            branch, key = branch_key
            nd = NestedDict(root=False)
            for k, v in self._val.items():
                if v and isinstance(v, dict):
                    nd._val = self._val[k]
                    nd[branch_key] = value
                    self._found = self._found or nd._found

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

        def _process_slash():
            first_branch, *branches = branch_key.split('/')

            nd = NestedDict(root=False)
            self._val.setdefault(first_branch, {})

            if self._val[first_branch]:
                pass
            else:
                self._val[first_branch] = {}

            nd._val = self._val[first_branch]
            if len(branches) > 1:
                nd['/'.join(branches)] = value
            elif len(branches) == 1:
                nd._val[branches[0]] = value
            else:
                raise KeyError

        def _look_deeper():
            nd = NestedDict(root=False)
            for k, v in self._val.items():
                if v and isinstance(v, dict):
                    nd._val = self._val[k]
                    nd[branch_key] = value
                    self._found = self._found or nd._found

            if self._root:
                if self._found:
                    self._found = False
                else:
                    self._val.__setitem__(branch_key, value)

        if isinstance(branch_key, tuple):
            _process_tuple()

        elif self.__isstring_containing_char(branch_key, '/'):
            _process_slash()

        elif branch_key in self._val:
            self._found = True
            self._val.__setitem__(branch_key, value)

        else:
            _look_deeper()

    def __delitem__(self, key):
        self._val.__delitem__(key)

    def __iter__(self):
        return self._val.__iter__()

    def __len__(self):
        return self._val.__len__()

    def __repr__(self):
        return str(self._val)

    @staticmethod
    def __isstring_containing_char(obj, char):
        if isinstance(obj, str):
            if char in obj:
                return True
        return False