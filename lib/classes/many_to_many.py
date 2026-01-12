class Article:
    all = []

    def __init__(self, author, magazine, title):
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise Exception("Invalid title")

        if not isinstance(author, Author):
            raise Exception("Author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be a Magazine instance")

        self._title = title  # immutable
        self.author = author  # mutable
        self.magazine = magazine  # mutable

        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Ignore assignment to keep immutable
        pass

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("Author must be an Author instance")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise Exception("Magazine must be a Magazine instance")
        self._magazine = value


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise Exception("Invalid name")
        self._name = name  # immutable

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Ignore assignment to keep immutable
        pass

    def articles(self):
        return [a for a in Article.all if a.author == self]

    def magazines(self):
        return list({a.magazine for a in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        arts = self.articles()
        if not arts:
            return None
        return list({a.magazine.category for a in arts})


class Magazine:
    all = []

    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Only assign if valid (2–16 characters), otherwise ignore
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # Only assign if valid (length > 0), otherwise ignore
        if isinstance(value, str) and len(value.strip()) > 0:
            self._category = value

    def articles(self):
        return [a for a in Article.all if a.magazine == self]

    def contributors(self):
        return list({a.author for a in self.articles()})

    def article_titles(self):
        arts = self.articles()
        if not arts:
            return None
        return [a.title for a in arts]

    def contributing_authors(self):
        result = [
            author for author in self.contributors()
            if len([a for a in self.articles() if a.author == author]) > 2
        ]
        return result if result else None

    @classmethod
    def top_publisher(cls):
        if not cls.all:
            return None
        top = max(cls.all, key=lambda m: len(m.articles()))
        return top if len(top.articles()) > 0 else None
