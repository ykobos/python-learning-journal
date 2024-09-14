# code works, but will continue testing

import csv

class Country:
    def __init__(self, name, capital, population, language, continent):
        self.name = name
        self.capital = capital
        self.population = int(population)
        self.languages = language.split('/')  # Assume languages are separated by '/'
        self.continent = continent

    def __str__(self):
        return (f"Country: {self.name}\n"
                f"Capital: {self.capital}\n"
                f"Population: {self.population}\n"
                f"Languages: {', '.join(self.languages)}\n"
                f"Continent: {self.continent}\n")

class CountryDatabase:
    def __init__(self, csv_file):
        self.countries = []
        self.load_data(csv_file)

    def load_data(self, csv_file):
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 5:
                    country = Country(*row)
                    self.countries.append(country)
        self.countries.sort(key=lambda x: x.name)

    def binary_search(self, country_name):
        """ Binary search to find country by name """
        low, high = 0, len(self.countries) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.countries[mid].name.lower() == country_name.lower():
                return self.countries[mid]
            elif self.countries[mid].name.lower() < country_name.lower():
                low = mid + 1
            else:
                high = mid - 1
        return None

    def search_by_country(self, country_name):
        result = self.binary_search(country_name)
        if result:
            return [result]
        return []

    def search_by_language(self, language):
        # Enhanced to check all languages for a match
        return [country for country in self.countries 
                if any(lang.lower() == language.lower() for lang in country.languages)]

    def search_by_continent(self, continent):
        return [country for country in self.countries if continent.lower() == country.continent.lower()]

    def sort_by_language(self, countries):
        return sorted(countries, key=lambda x: x.languages[0].lower())

    def sort_by_continent(self, countries):
        return sorted(countries, key=lambda x: x.continent.lower())

def display_countries(countries):
    if not countries:
        print("No results found.")
    else:
        for country in countries:
            print(country)
            print()

def main():
    db = CountryDatabase('countries.csv')
    last_search_results = None

    while True:
        print("\nCountry Search Options:")
        print("1. Search by country name")
        print("2. Search by language")
        print("3. Search by continent")
        if last_search_results is not None:
            print("4. Sort last search results by language")
            print("5. Sort last search results by continent")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            country_name = input("Enter country name: ")
            last_search_results = db.search_by_country(country_name)
            display_countries(last_search_results)
        elif choice == '2':
            language = input("Enter language: ")
            last_search_results = db.search_by_language(language)
            display_countries(last_search_results)
        elif choice == '3':
            continent = input("Enter continent: ")
            last_search_results = db.search_by_continent(continent)
            display_countries(last_search_results)
        elif choice == '4' and last_search_results is not None:
            sorted_countries = db.sort_by_language(last_search_results)
            display_countries(sorted_countries)
        elif choice == '5' and last_search_results is not None:
            sorted_countries = db.sort_by_continent(last_search_results)
            display_countries(sorted_countries)
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice or no search results to sort. Please try again.")

if __name__ == '__main__':
    main()
