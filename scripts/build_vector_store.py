import json
import sys
from pathlib import Path


# 获取项目根目录
ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(ROOT_DIR)
)


from app.knowledge_builder import build_vector_store


PAL_DATA_PATH = "data/pals.json"

VECTOR_STORE_PATH = "data/vector_store.json"



def load_pals():

    with open(
        PAL_DATA_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def main():

    pals = load_pals()


    store = build_vector_store(
        pals
    )


    store.save(
        VECTOR_STORE_PATH
    )


    print(
        f"知识库构建完成，共{len(store.documents)}条"
    )



if __name__ == "__main__":
    main()