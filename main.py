import sys
from pathlib import Path

from sqlalchemy import create_engine

from pandasgui import show
import pandas as pd


def main():
    # TEST_ENGINE = create_engine(
    #     f"mysql+pymysql://root:test@127.0.0.1:1234/test",
    #     pool_recycle=3600,
    #     echo=False,  # to see sql execution
    # )

    delivered_cells_df = pd.read_csv(Path(__file__).parent / "pandasgui/resources/delivered_cells.csv")

    named_dataframes = {
        # TODO put back fetching from DB, even more, make it a special query new + old, using UNION
        # "Delivered cells": pd.read_sql_query(
        #     "SELECT * FROM OldDeliveredCell",
        #     TEST_ENGINE
        # ),
        "Delivered cells": delivered_cells_df
    }

    show(**named_dataframes)


if __name__ == '__main__':
    main()
