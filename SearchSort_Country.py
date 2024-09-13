import csv

class Country:
    def __init__(self, name, capital, population, language, continent):
        self.name = name
        self.capital = capital
        self.population = int(population)
        self.language = language
        self.continent = continent

    def __str__(self):
        return f"Country: {self.name}, Capital: {self.capital}, Population: {self.population}, Language: {self.language}, Continent: {self.continent}"


class CountrySearch:
    def __init__(self, csv_file):
        self.countries = self.load_countries(csv_file)

    def load_countries(self, csv_file):
        countries = []
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                country = Country(row['Country'], row['Capital'], row['Population'], row['Language'], row['Continent'])
                countries.append(country)
        return countries

    def search_by_country(self, country_name):
        results = [country for country in self.countries if country.name.lower() == country_name.lower()]
        if results:
            for country in results:
                print(country)
        else:
            print("Country not found.")

    def search_by_language(self, language):
        results = [country for country in self.countries if country.language.lower() == language.lower()]
        self.display_results(results)

    def search_by_continent(self, continent):
        results = [country for country in self.countries if country.continent.lower() == continent.lower()]
        self.display_results(results)

    def display_results(self, results):
        if results:
            print("\nDo you want to sort the results?")
            print("1. No sorting")
            print("2. Sort by language")
            print("3. Sort by continent")
            sort_choice = input("Enter your choice (1-3): ")

            if sort_choice == '2':
                results.sort(key=lambda x: x.language)
            elif sort_choice == '3':
                results.sort(key=lambda x: x.continent)

            for country in results:
                print(country)
        else:
            print("No countries found for this search.")

    def user_interface(self):
        while True:
            print("\nSearch Options:")
            print("1. Search by Country Name")
            print("2. Search by Language")
            print("3. Search by Continent")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                country_name = input("Enter country name: ")
                self.search_by_country(country_name)
            elif choice == '2':
                language = input("Enter language: ")
                self.search_by_language(language)
            elif choice == '3':
                continent = input("Enter continent: ")
                self.search_by_continent(continent)
            elif choice == '4':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

# Usage
if __name__ == "__main__":
    searcher = CountrySearch('countries.csv')
    searcher.user_interface()
