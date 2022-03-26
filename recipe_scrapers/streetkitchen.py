from ._abstract import AbstractScraper
from ._utils import get_yields, normalize_string


class StreetKitchen(AbstractScraper):
    @classmethod
    def host(cls):
        return "streetkitchen.hu"

    def title(self):
        return self.soup.find("h1", {"class": "entry-title"}).get_text()

    def total_time(self):
        return None

    def image(self):
        return (
            self.soup.find("div", {"class": "article-featured-image-bg"})
            .find("noscript")
            .find("img")["src"]
        )

    def ingredients(self):
        ingredient_group = self.soup.find("div", {"class": "ingredient-group"}).findAll(
            "dd"
        )

        return [
            normalize_string(ingredient.get_text()).strip()
            for ingredient in ingredient_group
        ]

    def instructions(self):
        instructions = self.soup.find("div", {"class": "the-content-div"}).findAll("p")[
            :-1
        ]  # the last paragraph is advertisement, not instructions
        instructions_arr = [instruction.get_text() for instruction in instructions]
        return "\n".join(instructions_arr)

    def yields(self):
        return get_yields(
            self.soup.find("span", {"class": "quantity-number"}).get_text()
        )
