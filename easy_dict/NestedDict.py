from collections.abc import MutableMapping
import logging


class NestedDict(MutableMapping):

    def __init__(self, initial_value=None, root=True):
        super().__init__()
        self._val = {}
        if initial_value is not None:
            self._val.update(initial_value)
        self._found = False
        self._root = root

    def __getitem__(self, item):
        self._found = False

        def _look_deeper():
            result = []
            for k, v in self._val.items():
                if isinstance(v, dict):
                    n = NestedDict(self[k], root=False)
                    if n[item]:
                        result.append(n[item])
                    self._found = self._found or n._found

            if self._root:
                if self._found:
                    self._found = False
                else:
                    # result = self[item] = type(self)()
                    raise KeyError

            result = result[0] if len(result) == 1 else result

            return result

        def _process_list():
            if len(item) == 1:
                return self[item[0]]

            trunk, *branches = item
            nd = NestedDict(self[trunk], root=False)
            result = nd[branches] if len(branches) > 1 else nd[branches[0]]

            return result

        if isinstance(item, list):
            return _process_list()

        elif self.__isstring_containing_char(item, '/'):
            item = item.split('/')
            return _process_list()

        elif item in self._val:
            self._found = True
            return self._val.__getitem__(item)

        else:
            return _look_deeper()

    def __setitem__(self, branch_key, value):
        self._found = False

        def _process_short_tuple():
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

        def _process_list():
            first_branch, *branches = branch_key

            # self._val.setdefault(first_branch, {})
            if self._val[first_branch]:
                pass
            else:
                self._val[first_branch] = {}

            if first_branch in self:
                self[first_branch] = value

            nd = NestedDict(self[first_branch], root=False)
            if len(branches) > 1:
                nd[branches] = value
            elif len(branches) == 1:
                nd._val[branches[0]] = value
            else:
                raise KeyError

        def _process_set_default():
            first_branch, *branches = branch_key

            # nd = NestedDict(root=False)
            self._val.setdefault(first_branch, {})
            if self._val[first_branch]:
                pass
            else:
                self._val[first_branch] = {}

            # nd._val = self._val[first_branch]
            nd = NestedDict(self[first_branch], root=False)
            if len(branches) > 1:
                nd[branches] = value
            elif len(branches) == 1:
                nd._val[branches[0]] = value
            else:
                raise KeyError

        def _look_deeper():
            nd = NestedDict(root=False)
            for k, v in self._val.items():
                if v and (isinstance(v, dict) or isinstance(v, NestedDict)):
                    nd._val = self._val[k]
                    nd[branch_key] = value
                    self._found = self._found or nd._found

            if self._root:
                if self._found:
                    self._found = False
                else:
                    self._val.__setitem__(branch_key, value)

        if isinstance(branch_key, tuple):
            # branch_key = list(branch_key)
            # _process_list()
            _process_short_tuple()

        elif isinstance(branch_key, list):
            _process_list()

        elif self.__isstring_containing_char(branch_key, '/'):
            branch_key = branch_key.split('/')
            _process_list()

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

    def __call__(self):
        return self._val

    @staticmethod
    def __isstring_containing_char(obj, char):
        if isinstance(obj, str):
            if char in obj:
                return True
        return False
