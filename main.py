import time

from custom_back_end.teggydb import TEGGY_ENGINE
from custom_back_end.opensharknetdb import merge_svn_projects
from pandasgui import show
import pandas as pd

EFFICIENT_ONE_ROW_CC_QUERY_FOR_MISSING_REG = """
SELECT cc.nr, cc.name, cc.tapeoutdate as "initial tapeoutdate", cc.foundry, cc.node, cc.technology, cc.svnrepository, cc.cellcollectionid
FROM cellcollection cc
LIMIT 1;
"""


def main():
    try:
        print("[DIAG] main() reached", flush=True)
        timestamp = time.time()

        print("[DIAG] querying AllDeliveredCells...", flush=True)
        all_delived_cells = pd.read_sql_query("select * from AllDeliveredCells;", TEGGY_ENGINE)
        print("[DIAG] AllDeliveredCells done", flush=True)

        all_delived_cells["delivery_date"] = pd.to_datetime(all_delived_cells["delivery_date"], errors="coerce")
        all_delived_cells["metric"] = all_delived_cells["metric"].apply(lambda x: f"{int(x)}" if pd.notna(x) else "")

        named_dataframes = {
            "Delivered cells": all_delived_cells,
        }

        print("[DIAG] querying DetailedWaferVolume...", flush=True)
        named_dataframes["Wafer volumes"] = pd.read_sql_query("select * from DetailedWaferVolume limit 1;", TEGGY_ENGINE)
        print("[DIAG] DetailedWaferVolume done", flush=True)

        named_dataframes["Last metric delivered cells"] = all_delived_cells.iloc[:1].copy()

        print("[DIAG] querying cellcollection + merge_svn_projects...", flush=True)
        named_dataframes["Missing registered delivered cells"] = merge_svn_projects(pd.read_sql_query(EFFICIENT_ONE_ROW_CC_QUERY_FOR_MISSING_REG, TEGGY_ENGINE))
        print("[DIAG] cellcollection + merge_svn_projects done", flush=True)

        elapsed = time.time() - timestamp
        print(f"DB and DF stuff took {elapsed} seconds.", flush=True)

        print("[DIAG] calling show()...", flush=True)
        show(**named_dataframes)
        print("[DIAG] show() returned", flush=True)

    except Exception as e:
        import traceback, sys
        traceback.print_exc()
        if sys.stdin.isatty():
            input("Press Enter to close...")


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
