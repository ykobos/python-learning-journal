# code works

import csv

class Country:
    def __init__(self, name, capital, population, language, continent):
        self.name = name
        self.capital = capital
        self.population = population
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
        if results:
            for country in results:
                print(country)
        else:
            print("No countries found for this language.")

    def search_by_continent(self, continent):
        results = [country for country in self.countries if country.continent.lower() == continent.lower()]
        if results:
            for country in results:
                print(country)
        else:
            print("No countries found for this continent.")

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
