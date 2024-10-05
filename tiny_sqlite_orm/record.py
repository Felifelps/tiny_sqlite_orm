class Record:

    def __init__(self, table, **kwargs):
        self.table = table
        self.__attrs = kwargs
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.__define_pk()

    def __define_pk(self):
        value = self.__attrs.get(self.table.pk._name)
        if value is None:
            value = self.table.pk.default
        self.pk = value

    @property
    def attrs(self):
        for name in self.__attrs:
            self.__attrs[name] = getattr(self, name)
        return self.__attrs

    def delete(self):
        return self.table.objects.delete(
            **self.__get_self_where()
        )

    def save(self):
        result = self.__check_if_exists()

        if result:
            self._update()
        else:
            self._create()

        return self

    def _create(self):
        self.table.objects.insert(self.attrs)

    def _update(self):
        self.table.objects.update(
            self.attrs,
            **self.__get_self_where()
        )

    def __check_if_exists(self):
        return self.table.objects.select(
            **self.__get_self_where()
        ).first()

    def __get_self_where(self):
        return {self.table.pk._name: self.pk}

    def __repr__(self):
        return 'Record(table={}, pk={})'.format(
            self.table.table_name,
            self.pk
        )
