"""
Example usage of the search engine components.
This demonstrates how the search parser and engine work.
"""
from src.parsers.search_parser import SearchParser
from src.search import SearchEngine, ResultsFormatter


def main():
    """Run example searches."""
    print("=" * 60)
    print("Telegram Data Breach Search Bot - Example Usage")
    print("=" * 60)
    
    # Example queries
    queries = [
        "Muhammad Sobri Maulana",
        "example@gmail.com",
        "+79024196473",
        "127.0.0.1",
        "XTA21150053965897",
        "Sergio 79024196473"
    ]
    
    for query in queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print("=" * 60)
        
        # Parse the query
        parsed = SearchParser.parse_query(query)
        print(f"\nQuery Type: {parsed['type'].value}")
        print(f"Query Value: {parsed['value']}")
        
        # Perform search
        results = SearchEngine.search(parsed)
        
        print(f"\nFound in {results['total_platforms']} platforms:")
        for platform_data in results['platforms'][:5]:  # Show first 5
            print(f"  - {platform_data['platform']}: {platform_data['data_count']} data points")
        
        if len(results['platforms']) > 5:
            print(f"  ... and {len(results['platforms']) - 5} more platforms")
        
        print(f"\nTotal Data Points: {results['total_data_points']}")
    
    # Multi-query example
    print(f"\n{'=' * 60}")
    print("Multi-Query Example")
    print("=" * 60)
    
    multi_text = """Muhammad Sobri Maulana
example@gmail.com
+79024196473"""
    
    queries = SearchParser.parse_multi_query(multi_text)
    print(f"\nParsed {len(queries)} queries:")
    for i, q in enumerate(queries, 1):
        print(f"  {i}. {q['value']} ({q['type'].value})")


if __name__ == "__main__":
    main()
