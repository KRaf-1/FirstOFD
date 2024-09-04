from services.firstofd.first_ofd_auth import FirstOFD


class FirstOfdKKT(FirstOFD):
    def get_list(self):
        return self._get("/retail-places/kkms")

    def get_filtered_list(self):
        offline_kkt_list = []
        kkt_list = []
        for kkt in self.get_list():
            if kkt["id"] != "6328":
                for kkt_id in kkt["kkms"]:
                    try:
                        if kkt_id["billingStatus"] and kkt_id["billingStatus"] != 0:
                            kkt_list.append(kkt_id["id"])
                    except Exception:
                        # print(f"KeyError is {arr}")
                        offline_kkt_list.append(kkt_id["id"])
        return kkt_list, offline_kkt_list

    def get_full_list(self):
        full_list = []
        for tt in self.get_list():
            if tt["id"] != "1093934":
                for kkt in tt["kkms"]:
                    full_list.append(kkt)
        return full_list[11:20]
