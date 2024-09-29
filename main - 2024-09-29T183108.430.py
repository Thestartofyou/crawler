import asyncio
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def extract_product_listings():
    # Define the schema to extract products from the e-commerce page
    schema = {
        "name": "Product Listing Extractor",
        "baseSelector": ".product-listing",
        "fields": [
            {
                "name": "name",
                "selector": ".product-title",
                "type": "text",
            },
            {
                "name": "price",
                "selector": ".product-price",
                "type": "text",
            },
            {
                "name": "rating",
                "selector": ".product-rating span",
                "type": "text",
            },
            {
                "name": "image",
                "type": "nested",
                "selector": ".product-image img",
                "fields": [
                    {"name": "src", "type": "attribute", "attribute": "src"},
                    {"name": "alt", "type": "attribute", "attribute": "alt"},
                ],
            },
            {
                "name": "link",
                "selector": ".product-title a[href]",
                "type": "attribute",
                "attribute": "href",
            },
        ],
    }

    # Create an extraction strategy using the schema
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    async with AsyncWebCrawler(verbose=True) as crawler:
        # Target a hypothetical e-commerce website's product page
        result = await crawler.arun(
            url="https://www.example.com/products",
            extraction_strategy=extraction_strategy,
            bypass_cache=True,
        )

        # Check if the extraction was successful
        assert result.success, "Failed to crawl the page"

        # Parse the extracted content and print it
        product_listings = json.loads(result.extracted_content)
        print(f"Successfully extracted {len(product_listings)} product listings")
        print(json.dumps(product_listings[0], indent=2))  # Print first product for demo

if __name__ == "__main__":
    asyncio.run(extract_product_listings())
