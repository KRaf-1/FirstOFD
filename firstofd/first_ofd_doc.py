from services.firstofd.first_ofd_auth import FirstOFD
import time


class FirstOfdDoc(FirstOFD):
    def get_doc(self, kkt_id):
        time.sleep(1)
        params = {"transactionTypes": "FISCAL_REPORT_CORRECTION,FISCAL_REPORT"}
        return self._get(f"/cp-ofd/kkms/{kkt_id}/transactions", params=params)[
            "transactions"
        ][0]

    def get_doc_info(self, doc_id):
        time.sleep(1)
        return self._get(f"/cp-ofd/transaction/{doc_id}")

    def get_correction_doc(self, kkt_id):
        time.sleep(1)
        params = {
            "fiscalDriveNumber": "",
            "transactionTypes": "BSO_CORRECTION,RECEIPT_CORRECTION",
        }
        return self._get(
            f"https://org.1-ofd.ru/api/cp-ofd/kkms/{kkt_id}/transactions", params=params
        )

    def get_return_ticket(self, kkt_id):
        time.sleep(1)
        params = {
            "transactionTypes": "TICKET",
            "transactionDescription": "transaction.ticket.sell.return",
        }
        return self._get(
            f"https://org.1-ofd.ru/api/cp-ofd/kkms/{kkt_id}/transactions", params=params
        )
