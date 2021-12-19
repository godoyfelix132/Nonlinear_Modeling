from src.curves import Curve
from src.r import R
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

plt.rc('lines', linewidth=0.5)
plt.rcParams["figure.figsize"] = (10, 6)


class Function:
    @staticmethod
    def get_data_vds_ids(data):
        vds = data.vds_list
        ids = data.ids_list
        vgs = data.vgs_list
        return vds, ids, vgs
    @staticmethod
    def get_objects(vds_list, ids_list, vgs_list):
        object_list = []
        i = 0
        for vgs in vgs_list:
            j = 0
            for vds in vds_list:
                new = R()
                new.vds = vds
                new.vgs = vgs
                new.ids = ids_list[i][j]
                object_list.append(new)
                j = j+1
            i = i+1
        return object_list

    @staticmethod
    def get_ids_vds_curves(vds_list, vgs_list, all_measurements_ol, vds_limit_l =-100, vds_limit_h=1000, vgs_limit_l=-100, vgs_limit_h=100):
        curves_list = []
        for vgs in vgs_list:
            if vgs_limit_l < float(vgs) < vgs_limit_h:
                x_list = []
                y_list = []
                for object in all_measurements_ol:
                    if vgs == object.vgs and vds_limit_l < float(object.vds) < vds_limit_h:
                        x_list.append(object.vds)
                        y_list.append(object.ids)
                new = Curve()
                new.name = 'Vgs = ' + str(vgs)
                new.value = vgs
                new.x_list = x_list
                new.y_list = y_list
                curves_list.append(new)
        return curves_list

    @staticmethod
    def get_ids_vgs_curves(vds_list, vgs_list, all_measurements_ol, vds_limit_l =-100, vds_limit_h=1000, vgs_limit_l=-100, vgs_limit_h=100):
        curves_list = []
        for vds in vds_list:
            if vds_limit_l < float(vds) < vds_limit_h:
                x_list = []
                y_list = []
                for object in all_measurements_ol:
                    if vds == object.vds and vgs_limit_l < float(object.vgs) < vgs_limit_h:
                        x_list.append(object.vgs)
                        y_list.append(object.ids)
                new = Curve()
                new.name = 'Vds = ' + str(vds)
                new.value = vds
                new.x_list = x_list
                new.y_list = y_list
                curves_list.append(new)
        return curves_list


    @staticmethod
    def plot_curve(curve, x_label, y_label, l_width=0.5, l_stile='-'):
        plt.plot(curve.x_list, curve.y_list, label=curve.name, linewidth=l_width, linestyle=l_stile)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(ncol=2)

    @staticmethod
    def plot_curves(ids_vds_curves_ol, x_label, y_label, l_width=0.5, l_stile='-'):
        for curve in ids_vds_curves_ol:
            plt.plot(curve.x_list, curve.y_list, label=curve.name, linewidth=l_width, linestyle=l_stile)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(ncol=2)

    @staticmethod
    def linear_regression(x_list, y_list):
        x_list = np.array(x_list)
        y_list = np.array(y_list)
        linear_regression = LinearRegression()
        linear_regression.fit(x_list.reshape(-1, 1), y_list)
        m = linear_regression.coef_
        b = linear_regression.intercept_
        return m, b