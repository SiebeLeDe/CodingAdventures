import requests
from bs4 import BeautifulSoup
import csv


def fetch_search_results(search_url: str) -> str:
    """
    Fetch the search results for hummus products.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch search results. Status code: {response.status_code}")
        return None


def parse_search_results(html: str, base_url: str) -> list[str]:
    """
    Parse the search results page to extract product links.
    """
    soup = BeautifulSoup(html, "html.parser")
    product_links = []

    # Find product containers (adjust the class based on the website structure)
    products = soup.find_all("a", class_="product-card-container_link")  # Example class
    for product in products:
        link = product.get("href", "")
        if link:
            product_links.append(base_url + link)

    return product_links


def fetch_product_details(product_url: str):
    """
    Fetch and parse product details from a product page.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(product_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract product name
        name = soup.find("h1", class_="product-title").text.strip()

        # Extract nutritional information (adjust based on the website structure)
        nutrition_table = soup.find("table", class_="nutrition-table")
        nutrition_data = {}
        if nutrition_table:
            rows = nutrition_table.find_all("tr")
            for row in rows:
                columns = row.find_all("td")
                if len(columns) == 2:
                    key = columns[0].text.strip()
                    value = columns[1].text.strip()
                    nutrition_data[key] = value

        return {"name": name, "nutrition": nutrition_data, "url": product_url}
    else:
        print(f"Failed to fetch product details for {product_url}. Status code: {response.status_code}")
        return None


def save_to_csv(products, filename="hummus_products.csv"):
    """
    Save the product details to a CSV file.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "URL", "Nutrition"])
        for product in products:
            writer.writerow([product["name"], product["url"], product["nutrition"]])


def main():
    # Base URL of Albert Heijn
    BASE_URL = "https://www.ah.nl"

    # Search query for hummus
    SEARCH_URL = f"{BASE_URL}/zoeken?query=hummus"

    # Step 1: Fetch search results
    html = fetch_search_results(SEARCH_URL)
    if not html:
        return

    # Step 2: Parse search results
    product_links = parse_search_results(html, BASE_URL)
    print(f"Found {len(product_links)} products.")

    # Step 3: Fetch product details
    products = []
    for link in product_links:
        print(f"Fetching details for {link}...")
        product_details = fetch_product_details(link)
        if product_details:
            products.append(product_details)

    # Step 4: Save to CSV
    save_to_csv(products)
    print(f"Saved {len(products)} products to hummus_products.csv")


if __name__ == "__main__":
    main()
