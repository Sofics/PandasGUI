from pathlib import Path

from sqlalchemy import create_engine

import cfg
from pandasgui import show
import pandas as pd


def main():
    try:
        # TODO some kind of loading bar / progress dlg?

        TEGGY_ENGINE = create_engine(
            f"mysql+pymysql://{cfg.TeggyDB.username}:{cfg.TeggyDB.password}@{cfg.TeggyDB.host}/{cfg.TeggyDB.name}",
            pool_recycle=3600,
            # echo=True,  # to see sql execution
        )

        all_delived_cells = pd.read_sql_query("""
(SELECT customer, project_nr, project_lead, snap_name, name, delivery_date, datasheet, foundry, node, technology, flavour, domain, tag, metric, delivery_contact, product, gds_name, drm_name, drm_version, drc_name, drc_version, lvs_name, lvs_version, spice_name, spice_version, senumber, area  FROM DeliveredCell dc)
UNION
(SELECT customer, project_nr, project_lead, NULL as snap_name, name, delivery_date, datasheet, foundry, node, technology, flavour, domain, tag, metric, delivery_contact, product, gds_name, drm_name, drm_version, drc_name, drc_version, lvs_name, lvs_version, spice_name, spice_version, senumber, NULL as area FROM OldDeliveredCell odc)
ORDER BY delivery_date desc;
""", TEGGY_ENGINE)

        # TODO make dataframe that closely resembles columns  in TSMC's ip registration template"S:\3 - Technical\9000 - TSMC9000\IP registration\IP Register 2.0_template.xls"
        # Action / IP Category / IP Name / Geometry / Technology (1) / Technology (2) / IP Types / Voltage / description / post in portfolio / reason not post / RFQ project / Non-NDA datasheet or product brief / IP Version / The latest version / design kit / tape-out date / silicon report / DRM (number (version)) / Logic Spice model  (number (version)) / contractually royalty bearing / tsmc comment
        # tsmc_cells_for_ip_registry = None

        # transform None -> NaT, so comparison in GUI query expressions works:
        all_delived_cells["delivery_date"] = pd.to_datetime(all_delived_cells["delivery_date"], errors="coerce")

        named_dataframes = {
            "Delivered cells": all_delived_cells,
            # TODO add a named dataframe with only TSMC cells & columns exactly as how Johan wants it
        }

        show(**named_dataframes)

    except Exception as e:
        import traceback
        traceback.print_exc()
        input()


if __name__ == "__main__":
    main()
