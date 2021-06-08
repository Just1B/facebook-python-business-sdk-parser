class Config:

    BASE_DIR = "/usr/local/lib/python3.9/site-packages"

    FACEBOOK_PACKAGE = "facebook_business"

    ADOBJECT_DIR = "adobjects"

    # https://github.com/facebook/facebook-python-business-sdk/tree/master/facebook_business/adobjects
    FULL_PATH = f"{BASE_DIR}/{FACEBOOK_PACKAGE}/{ADOBJECT_DIR}"

    NEO4J_HOST = "bolt://neo4j:7687"

    EXCLUSION_LIST = ["__init__.py", "abstractobject.py", "abstractcrudobject.py"]
