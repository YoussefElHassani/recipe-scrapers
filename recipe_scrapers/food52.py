from recipe_scrapers._abstract import AbstractScraper
from recipe_scrapers._utils import get_minutes, normalize_string


class Food52(AbstractScraper):
    @classmethod
    def host(cls):
        return "food52.com"

    def title(self):
        return self.schema.title()

    def total_time(self):
        ul = self.soup.find("ul", {"class": "recipe__details"})
        return sum(
            get_minutes(list(li.children)[2].strip())
            for li in ul.find_all("li")
            if li.span.get_text().lower() in ["prep time", "cook time"]
        )

    def yields(self):
        return self.schema.yields()

    def image(self):
        return self.schema.image()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        instructions = self.soup.findAll("li", {"class": "recipe__list-step"})

        return "\n".join(
            [
                normalize_string(instruction.span.get_text())
                for instruction in instructions
            ]
        )

    def ratings(self):
        return self.schema.ratings()
