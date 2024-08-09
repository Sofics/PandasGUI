from pathlib import Path

from sqlalchemy import create_engine

import cfg
from pandasgui import show
import pandas as pd


def main():
    try:
        # TEST_ENGINE = create_engine(
        #     f"mysql+pymysql://root:test@127.0.0.1:1234/test",
        #     pool_recycle=3600,
        #     echo=False,  # to see sql execution
        # )

        # TODO some kind of loading bar / progress dlg?

        TEGGY_ENGINE = create_engine(
            f"mysql+pymysql://{cfg.TeggyDB.username}:{cfg.TeggyDB.password}@{cfg.TeggyDB.host}/{cfg.TeggyDB.name}",
            pool_recycle=3600,
            # echo=True,  # to see sql execution
        )

        # TODO remove csv stuff
        csv_path = Path(__file__).parent / "pandasgui/resources/delivered_cells.csv"
        print(csv_path)
        delivered_cells_df = pd.read_csv(str(csv_path))

        named_dataframes = {
            # TODO take from DB again (union with new delivered cells table)
            "Delivered cells": pd.read_sql_query("""
(SELECT customer, project_nr, project_lead, snap_name, name, delivery_date, datasheet, foundry, node, technology, flavour, domain, tag, metric, delivery_contact, product, gds_name, drm_name, drm_version, drc_name, drc_version, lvs_name, lvs_version, spice_name, spice_version, senumber, area  FROM DeliveredCell dc)
UNION
(SELECT customer, project_nr, project_lead, NULL as snap_name, name, delivery_date, datasheet, foundry, node, technology, flavour, domain, tag, metric, delivery_contact, product, gds_name, drm_name, drm_version, drc_name, drc_version, lvs_name, lvs_version, spice_name, spice_version, senumber, NULL as area FROM OldDeliveredCell odc)
ORDER BY delivery_date desc;
""",
                                                 TEGGY_ENGINE
                                                 ),
            # "Delivered cells": delivered_cells_df,
        }

        show(**named_dataframes)

    except Exception as e:
        import traceback
        traceback.print_exc()
        input()


if __name__ == '__main__':
    main()
