"""script to find out which projects codes are missing registered cells."""
from pprint import pprint

from sqlalchemy.orm import Session

import cfg
from sqlalchemy import create_engine, text

# TODO place this in root to execute

TEGGY_ENGINE = create_engine(
    f"mysql+pymysql://{cfg.TeggyDB.username}:{cfg.TeggyDB.password}@{cfg.TeggyDB.host}/{cfg.TeggyDB.name}",
    pool_recycle=3600,
    # echo=True,  # to see sql execution
)

with Session(bind=TEGGY_ENGINE, autoflush=False, autocommit=False) as teggy_session:
    del_cell_cursor_result = teggy_session.execute(text("""
    SELECT DISTINCT project_nr FROM (
    SELECT project_nr FROM DeliveredCell
    UNION
    SELECT project_nr FROM OldDeliveredCell
) AS proj_nr
    """))
unique_project_numbers = {cr.project_nr for cr in del_cell_cursor_result if cr.project_nr is not None}


OPENSHARKNET_ENGINE = create_engine(
    f"mysql+pymysql://{cfg.OpenSharknetDB.username}:{cfg.OpenSharknetDB.password}@"
    f"{cfg.OpenSharknetDB.host}/{cfg.OpenSharknetDB.name}",
)
OPENSHARKNET_SESSION = Session(
    bind=OPENSHARKNET_ENGINE, autoflush=False, autocommit=False
)


project_responsible_dict = {}  # project nr -> projectleaderinitials

project_cursor_result = OPENSHARKNET_SESSION.execute(text("select code, projectleaderinitials from project"))
for project_row in project_cursor_result:
    project_responsible_dict.update({project_row.code: project_row.projectleaderinitials})


engineer_missing_registered_cells_dict = {}  # engineer initials / None -> project w/o registered cells

for project_nr in project_responsible_dict.keys():
    if project_nr.lower().startswith("cpa") and project_nr not in unique_project_numbers:
        responsible = project_responsible_dict.get(project_nr)
        if responsible not in engineer_missing_registered_cells_dict.keys():
            engineer_missing_registered_cells_dict.update({responsible: [project_nr]})
        else:
            engineer_missing_registered_cells_dict.get(responsible).append(project_nr)

with open("projects_to_check_for_missing_registries.txt", "w") as file:
    for responsible, projects_to_check in engineer_missing_registered_cells_dict.items():
        file.write(f"####################\n{responsible}\n####################\n")
        for project in projects_to_check:
            file.write(f"{project}\n")
        file.write("\n")
