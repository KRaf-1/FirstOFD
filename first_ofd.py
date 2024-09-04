from services.firstofd.first_ofd_kkt import FirstOfdKKT
from services.firstofd.first_ofd_doc import FirstOfdDoc
import time
import csv
from datetime import datetime
from schemas import DocResponse
import pandas as pd


first_ofd_kkt = FirstOfdKKT()
first_ofd_docs = FirstOfdDoc()


def get_response():
    start = datetime.now()
    data = {
        "Название ТТ": [],
        "Рег. номер": [],
        "Номер ККТ": [],
        "Номер ФН": [],
        "Дата документа": [],
        "Параметры": [],
        "Кол-во ключей": [],
        "Статус": [],
    }
    doc_list = []
    for kkt_id in first_ofd_kkt.get_full_list():
        try:
            if kkt_id["params"]["checkStatus"][0]["description"]:
                data["Статус"].append(kkt_id["params"]["checkStatus"][0]["description"])
            elif kkt_id["declineReason"]:
                data["Статус"].append(kkt_id["declineReason"])
        except Exception as arr:
            print(f"KeyError is {arr}")
            data["Статус"].append("Error")
        doc_info = first_ofd_docs.get_doc_info(
            first_ofd_docs.get_doc(kkt_id["id"])["id"]
        )
        try:
            if doc_info["options"]["retailPlace"]:
                data["Название ТТ"].append(doc_info["options"]["retailPlace"])
        except Exception as arr:
            print(f"KeyError is {arr}")
            print(doc_info)
            data["Название ТТ"].append("Нет торговой точки")
        data["Рег. номер"].append(doc_info["kkmId"])
        data["Номер ККТ"].append(doc_info["options"]["kktNumber"])
        data["Номер ФН"].append(doc_info["options"]["fiscalDriveNumber"])
        data["Дата документа"].append(doc_info["transactionDate"])
        try:
            if doc_info["options"]["kktUsageMode"]:
                data["Параметры"].append(doc_info["options"]["kktUsageMode"])
        except Exception as arr:
            print(f"KeyError is {arr}")
            print(doc_info)
            data["Параметры"].append("Отсутствует тег 1290")
        try:
            if doc_info["options"]["fiscalDriveKeysResource"]:
                data["Кол-во ключей"].append(
                    doc_info["options"]["fiscalDriveKeysResource"]
                )
        except Exception as arr:
            print(f"KeyError is {arr}")
            print(doc_info)
            data["Кол-во ключей"].append("ERROR")
        print(f"Doc time is {datetime.now() - start}")
    print(data)
    data_df = pd.DataFrame(data)
    print(data_df)
    data_df.to_csv("firstofd_params.csv", sep=",", index=False, encoding="utf-8")
    print(f"Total time is {datetime.now() - start}")


def get_docs(doc_list):
    id_list = []
    for doc in doc_list["transactions"]:
        id_list.append(doc["id"])
    return id_list


def get_kkt_params(id_doc):
    param_from_doc = first_ofd_docs.get_doc_info(id_doc)

    return DocResponse(
        name=param_from_doc["options"]["retailPlace"],
        reg_number=param_from_doc["options"]["kktRegId"],
        number=param_from_doc["options"]["kktNumber"],
        fn_number=param_from_doc["options"]["fiscalDriveNumber"],
        doc_date=param_from_doc["transactionDate"],
        params=param_from_doc["options"]["kktUsageMode"],
        keys_count=param_from_doc["options"]["fiscalDriveKeysResource"],
        status=param_from_doc["options"]["params"]["checkStatus"][0]["description"],
    )


def save_data_in_file(data: list[DocResponse]):
    print(f"data is {data}")
    with open(
        f"firstofd_params_{datetime.now()}.csv", "w", encoding="utf-8-sig", newline="\n"
    ) as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
            (
                "Название ТТ",
                "Рег. номер",
                "Номер ККТ",
                "Номер ФН",
                "Дата документа",
                "Параметры",
                "Кол-во ключей",
                "Статус",
            )
        )
        for row in data:
            print(f"row is {row} {type(row)}")
            for kkt in row.kkt_list:
                writer.writerow(
                    (
                        kkt.name,
                        kkt.reg_number,
                        kkt.number,
                        kkt.fn_number,
                        kkt.doc_date,
                        kkt.params,
                        kkt.keys_count,
                        kkt.status,
                    )
                )


get_response()
