import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import Utilities.utilities as utilities


def monthlyResults(rows, columns,myday_y , my_month, data, months, group_by, width, obj_name, colors,the_title, file_name, my_folders, show):
    fig, ax = plt.subplots(rows,columns, figsize=(8,11), sharey=True)

    rows = np.arange(rows)
    num_samps = 0

    for i,group in enumerate([data]):
        the_data = group[group_by]
        box_plots=[]
        scatter_this = []
        positions = list(the_data.keys())
        for k,v in the_data.items():
            y = [x[1] for x in v[0]]
            box_plots.append(y)
            x = [1 + (np.random.rand(1)*width-width/2.) for x in y]
            scatter_this.append({k:(x,y)})
        box_plots = [value for group in box_plots for value in group]
        box_plots_sorted = sorted(box_plots)
        y_limit = box_plots_sorted[-2]+.1
        scatter_sorted = sorted(scatter_this, key = lambda obj: list(obj.keys())[0] )
        for n,pairs in enumerate(scatter_sorted):
            if n < 4:
                axs = ax[0,n]
            elif 4 <= n < 8:
                index = {4:0,5:1,6:2,7:3}
                axs = ax[1,index[n]]
            elif 8 <= n <= 11:
                index = {8:0,9:1,10:2,11:3}
                axs = ax[2,index[n]]
            axs.set_ylim(-.1,y_limit)
            box_plot_median = np.percentile(box_plots_sorted, .5)
            axs.boxplot(box_plots, showfliers=False, widths=width)
            for k,v in pairs.items():
                if k in [1,5,9]:
                    axs.scatter(v[0], v[1], color=colors[i], s=100, edgecolor="w", alpha=0.7,label=obj_name)
                    axs.set_xticklabels([months[k]], fontsize=14)
                    y_label_text = '{} per meter'.format(obj_name)
                    axs.set_ylabel(y_label_text, fontsize=12)
                else:
                    axs.scatter(v[0], v[1], color=colors[i], s=100, edgecolor="w", alpha=0.7,label=obj_name)
                    axs.set_xticklabels([months[k]], fontsize=14)
                if my_month == k:
                    axs.scatter(1 + (np.random.rand(1)*width-width/2.),  myday_y, color="r", s=125, label="Day of interest")
        num_samps = len(box_plots)

    the_title_2 = "Grouped by month of the year, n={}".format(num_samps)
    insert_title = '{}{}'.format(the_title, the_title_2)
    plt.suptitle(insert_title, fontweight="book", fontfamily="sans-serif", fontsize=14, linespacing=1.5)
    plt.legend()
    plt.subplots_adjust(top=0.9)
    # plt.tight_layout()
    save_to = my_folders["Charts"] +"/"+ file_name  +".svg"
    plt.savefig(save_to)
    if show:
        plt.show()
        plt.close()
    else:
        plt.close()
        return "Chart saved to {}".format(save_to)
