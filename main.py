from scripts.pipeline import load_data, clean_data, transform_data, save_data

def run_pipeline():
    print("Loading data...")
    df = load_data("data/raw/Apple_sales_raw.csv")

    print("Cleaning data...")
    df = clean_data(df)

    print("Transforming data...")
    df = transform_data(df)

    print("Saving data...")
    save_data(df, "data/processed/Apple_sales_clean.csv")

    print("Pipeline complete!")

if __name__ == "__main__":
    run_pipeline()
