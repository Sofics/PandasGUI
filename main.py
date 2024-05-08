import sys
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

        # if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        #     delivered_cells_df = pd.read_csv(Path(__file__).parent / "resources/delivered_cells.csv")
        # else:
        delivered_cells_df = pd.read_csv("pandasgui/resources/delivered_cells.csv")

        named_dataframes = {
            # TODO put back fetching from DB, even more, make it a special query new + old, using UNION
            # "Delivered cells": pd.read_sql_query(
            #     "SELECT * FROM OldDeliveredCell",
            #     TEST_ENGINE
            # ),
            "Delivered cells": delivered_cells_df
        }

        show(**named_dataframes)

    except Exception as e:
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
