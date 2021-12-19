class Read:
    def __init__(self, root):
        file = open(root, 'r')
        lines = file.readlines()
        self.vgs_list, self.vds_list, self.ids_list = Read.get_lists(lines)
        self.unique_list = Read.get_unique(self.vgs_list, self.vds_list, self.ids_list)

    @staticmethod
    def get_unique(vgs_list, vds_list, ids_list):
        unique_list = []
        for i in range(len(vgs_list)):
            for j in range(len(vds_list)):
                vgs = vds_list[i]
                vds = vds_list[j]
                ids = ids_list[i][j]
                unique_list.append([vgs, vds, ids])
        return unique_list

    @staticmethod
    def get_lists(lines):
        n_vgs = 0
        n_vds = 0
        n_ids = 0
        vgs_list = []
        vds_list = []
        ids_list = []
        state = 0
        for l in lines:
            if state == 0:
                if l.startswith('VAR Vgs'):
                    split_list = l.split()
                    n_vgs = int(split_list[3])
                if l.startswith('VAR Vds'):
                    split_list = l.split()
                    n_vds = int(split_list[3])
                if l.startswith('DATA Ids'):
                    split_list = l.split()
                    n_ids = int(split_list[3])
                    state = 1

            if state == 1:
                if l.startswith('VAR_LIST_END')and len(vgs_list) > 0:
                    state = 2
                else:
                    try:
                        vgs_list.append(float(l))
                    except ValueError:
                        pass

            if state == 2:
                if l.startswith('VAR_LIST_END') and len(vds_list) > 0:
                    state = 3
                else:
                    try:
                        vds_list.append(float(l))
                    except ValueError:
                        pass
            if state == 3:
                try:
                    ids_list.append(float(l))
                except ValueError:
                    pass
        if len(vgs_list) == n_vgs and len(vds_list) == n_vds and len(ids_list) == n_vgs*n_vds:
            print('ok')
        else:
            print('error')
            print(len(vgs_list), n_vgs)
            print(len(vds_list), n_vds)
            print(len(ids_list), n_vgs * n_ids)
        ids_list_divided = []
        for i in range(0, len(ids_list), n_vds):
            ids_list_divided.append(ids_list[i:i + n_vds])
        return vgs_list, vds_list, ids_list_divided