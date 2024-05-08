from pathlib import Path

from sqlalchemy import create_engine

from pandasgui import show
import pandas as pd


def main():
    try:
        # TEST_ENGINE = create_engine(
        #     f"mysql+pymysql://root:test@127.0.0.1:1234/test",
        #     pool_recycle=3600,
        #     echo=False,  # to see sql execution
        # )

        csv_path = Path(__file__).parent / "pandasgui/resources/delivered_cells.csv"
        print(csv_path)
        delivered_cells_df = pd.read_csv(str(csv_path))

        named_dataframes = {
            # TODO take from DB again (union with new delivered cells table)
            # "Delivered cells": pd.read_sql_query(
            #     "SELECT * FROM OldDeliveredCell",
            #     TEST_ENGINE
            # ),
            "Delivered cells": delivered_cells_df,
        }

        show(**named_dataframes)

    except Exception as e:
        import traceback
        traceback.print_exc()
        input()


if __name__ == '__main__':
    main()
