import time
from pathlib import Path

from sqlalchemy import create_engine

import custom_back_end.cfg

from custom_back_end.teggydb import TEGGY_ENGINE
from pandasgui import show
import pandas as pd


def main():
    try:
        # TODO some kind of loading bar / progress dlg?

        timestamp = time.time()

        # For how this view got created, see bottom of this file
        all_delived_cells = pd.read_sql_query("select * from AllDeliveredCells;", TEGGY_ENGINE)

        # transform None -> NaT, so comparison in GUI query expressions works:
        all_delived_cells["delivery_date"] = pd.to_datetime(all_delived_cells["delivery_date"], errors="coerce")
        # Turn metrics into strings => no comma and more readable (NaN => "")
        all_delived_cells["metric"] = all_delived_cells["metric"].apply(lambda x: f"{int(x)}" if pd.notna(x) else "")

        # Note: start with delivered cells loaded and others empty until desired differently
        named_dataframes = {
            "Delivered cells": all_delived_cells,
            "Wafer volumes": pd.DataFrame(),
            "Last v. delivered cells": pd.DataFrame(),  # show latest metrics only
            # TODO add a named dataframe with only TSMC cells & columns exactly as how Johan wants it
            # that closely resembles columns  in TSMC's ip registration template"S:\3 - Technical\9000 - TSMC9000\IP registration\IP Register 2.0_template.xls"
            # Action / IP Category / IP Name / Geometry / Technology (1) / Technology (2) / IP Types / Voltage / description / post in portfolio / reason not post / RFQ project / Non-NDA datasheet or product brief / IP Version / The latest version / design kit / tape-out date / silicon report / DRM (number (version)) / Logic Spice model  (number (version)) / contractually royalty bearing / tsmc comment
        }

        print(f"DB and DF stuff took {time.time() - timestamp} seconds.")

        show(**named_dataframes)

    except Exception as e:
        import traceback
        traceback.print_exc()
        input()


if __name__ == "__main__":
    main()



################# view creation queries #####################


# create view AllDeliveredCells as
# (SELECT customer, project_nr, project_lead, snap_name, name, delivery_date, datasheet, foundry, node, technology, flavour, CAST(domain AS CHAR) as domain, tag, metric, delivery_contact, product, gds_name, drm_name, drm_version, drc_name, drc_version, lvs_name, lvs_version, spice_name, spice_version, senumber, area  FROM DeliveredCell dc)
# UNION
# (SELECT customer, project_nr, project_lead, NULL as snap_name, name, delivery_date, datasheet, foundry, node, technology, flavour, domain, tag, metric, delivery_contact, product, gds_name, drm_name, drm_version, drc_name, drc_version, lvs_name, lvs_version, spice_name, spice_version, senumber, NULL as area FROM OldDeliveredCell odc)
# ORDER BY delivery_date desc;


# CREATE VIEW DetailedWaferVolume AS
# WITH LatestDeliveries AS (
#     SELECT
#         product,
#         tag,
#         customer,
#         node,
#         technology,
#         foundry,
#         delivery_date,
#         ROW_NUMBER() OVER (PARTITION BY product, tag ORDER BY delivery_date DESC) AS rn
#     FROM AllDeliveredCells
# ),
# RankedData AS (
#     SELECT
#         wv.date AS date,
#         ld.customer AS customer,
#         wv.ip_name AS ip_name,
#         wv.ip_version AS ip_version,
#         wv.tapeouts AS tapeouts,
#         wv.wafers AS wafers,
#         ld.node AS node,
#         ld.technology AS technology,
#         ld.foundry AS foundry,
#         ld.delivery_date AS delivery_date,
#         LAG(wv.tapeouts) OVER (PARTITION BY wv.ip_name, wv.ip_version ORDER BY wv.date) AS prev_tapeouts,
#         LAG(wv.wafers) OVER (PARTITION BY wv.ip_name, wv.ip_version ORDER BY wv.date) AS prev_wafers
#     FROM WaferVolume wv
#     LEFT JOIN (
#         SELECT *
#         FROM LatestDeliveries
#         WHERE rn = 1
#     ) ld
#     ON wv.ip_name = ld.product AND wv.ip_version = ld.tag
# )
# SELECT
#     date,
#     customer,
#     ip_name,
#     ip_version,
#     tapeouts - COALESCE(prev_tapeouts, 0) AS new_tapeouts,
#     wafers - COALESCE(prev_wafers, 0) AS new_wafers,
#     tapeouts,
#     wafers,
#     node,
#     technology,
#     foundry,
#     delivery_date
# FROM RankedData
# ORDER BY date DESC, new_wafers DESC;