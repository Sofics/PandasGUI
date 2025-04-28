from sqlalchemy import create_engine

from custom_back_end import cfg

OPENSHARKNET_ENGINE = create_engine(
    f"mysql+pymysql://{cfg.OpenSharknetDB.username}:{cfg.OpenSharknetDB.password}@{cfg.OpenSharknetDB.host}/{cfg.OpenSharknetDB.name}",
    pool_recycle=3600,
    # echo=True,  # to see sql execution
)
