from sqlalchemy import create_engine
import pandas as pd

from custom_back_end import cfg

# NOTE: was only needed for gui.py "Daily ID2IP", which is currently commented out

OPENSHARKNET_ENGINE = create_engine(
    f"mysql+pymysql://{cfg.OpenSharknetDB.username}:{cfg.OpenSharknetDB.password}@{cfg.OpenSharknetDB.host}/{cfg.OpenSharknetDB.name}",
    pool_recycle=3600,
    # echo=True,  # to see sql execution
)

SVN_PROJECTS = pd.read_sql_query("""
select projectcode, projectname, svnrepository, svnprojectlead as "projectlead" from svnrepository s;
""", OPENSHARKNET_ENGINE)


def merge_svn_projects(df: pd.DataFrame) -> pd.DataFrame:
    """Merge given DF with projectcode, projectname, and project_lead based on the svnrespository field."""
    return df.merge(SVN_PROJECTS, on="svnrepository", how="left")
