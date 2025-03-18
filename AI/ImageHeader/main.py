import sys
import os
from image import ds, process_images
import json
from dotenv import load_dotenv

def check_venv():
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        print("Warning: Not running in a virtual environment!")
        print("Please run:")
        print("python -m venv venv")
        print("venv\\Scripts\\activate  # On Windows")
        print("pip install -r requirements.txt")
        sys.exit(1)

def main():
    check_venv()
    # Load environment variables
    load_dotenv()
    
    # Process images and generate results
    results = process_images(ds)
    
    # Save results to file
    with open('image_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    # Print summary
    print(f"\nProcessed {len(results)} images")

if __name__ == "__main__":
    main()
