from ._abstract import AbstractScraper
from ._utils import get_minutes, get_yields, normalize_string


class Matprat(AbstractScraper):
    @classmethod
    def host(cls):
        return "matprat.no"

    def title(self):
        return self.soup.find("h1").get_text().strip()

    def total_time(self):
        total_time = 0
        if tt := self.soup.find("span", {"data-epi-property-name": "RecipeTime"}):
            tt1 = normalize_string(tt.get_text())
            tt2 = get_minutes(tt1)
            total_time = tt1 if tt1 and (tt2 == 0) else tt2
        return total_time

    def yields(self):
        if recipe_yield := self.soup.find("input", {"id": "portionsInput"}):
            return str(recipe_yield["value"]) + " serving(s)"
        else:
            return get_yields(
                self.soup.find(
                    "div", {"class": "recipe-adjust-servings__original-serving"}
                ).get_text()
            )

    def image(self):
        image = self.soup.find("div", {"class": "responsive-image"})
        if image:
            tag = image.find("img")
            src = tag.get("src", None)
        return src if image else None

    def ingredients(self):
        details = self.soup.find("div", {"class": "ingredients-list"})
        sections = details.findAll("h3", {"class": "ingredient-section-title"})
        ingredients = details.findAll("ul", {"class": "ingredientsList"})

        ilist = []
        for cntr, ingpart in enumerate(ingredients):
            ingreditem = ingpart.findAll("li")
            ilist.extend(normalize_string(i.get_text()) for i in ingreditem)
            if cntr <= (len(sections) - 1) and len(sections[cntr].text) > 0:
                # txt = f'--- {sections[cntr].text} ---'
                txt = "--- {0} ---".format(sections[cntr].text)
                ilist.append(txt)
        return ilist

    def instructions(self):
        instructions = self.soup.find("div", {"class": "rich-text"})
        ins = instructions.findAll("li")

        return "\n".join([normalize_string(inst.text) for inst in ins])

    def ratings(self):
        r = self.soup.find("span", {"data-bind": "text: numberOfVotes"})
        return int(normalize_string(r.get_text()))

    def description(self):
        return normalize_string(self.soup.find("div", {"class": "article-intro"}).text)
