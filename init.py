from src.jp_imports.src.jp_imports.data_process import DataTrade
from src.jp_index.src.data.data_process import DataProcess as DataIndex
from dotenv import load_dotenv
import os

load_dotenv()

def main() -> None:
    dp = DataTrade(str(os.environ.get("DATABASE_URL")))
    dp.process_int_org("yearly", "total", False)

if __name__ == "__main__":
    main()
