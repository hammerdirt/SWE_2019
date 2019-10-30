import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import Utilities.utilities as utilities

seasons_colors = {
    "winter":"cyan",
    "spring":"lime",
    "summer":"saddlebrown",
    "fall":"darkgoldenrod",
}

def seasonalBoxPlots(my_seasons, myday_y, my_month, months, obj_name, seasons, the_title, file_name, my_folders):
    fig, ax = plt.subplots(2,2, figsize=(8,8))
    num_samps = 0
    the_seasons = list(my_seasons.keys())
    width = 0.7
    for i,season in enumerate(the_seasons):
        data_sorted = sorted(my_seasons[season])
        num_samps += len(data_sorted)
        if i < 2:
            axs = ax[0,i]
        if i >= 2:
            key = {2:0, 3:1}
            axs = ax[1,key[i]]
        y = data_sorted
        x = [1 + (np.random.rand(1)*width-width/2.) for x in y]
        if i == 0 or i == 2:
            y_label_text = '{} per meter'.format(obj_name)
            axs.set_ylabel(y_label_text, fontsize=12)
        winter = seasons[season]
        season_months = [months[x] for x in winter]
        ax_title = utilities.makeStringFromList(season_months)+":"
        y_limit = data_sorted[-2] + 0.1
        axs.set_ylim(-.05,y_limit)
        axs.boxplot(data_sorted, widths=width, showfliers=False,)
        axs.scatter(x,y, color=seasons_colors[season], s=100, edgecolor="w", alpha=0.7,label=obj_name)
        if my_month in winter:
            axs.scatter(1 + (np.random.rand(1)*width-width/2.),  myday_y, color="r", s=125, label="Day of interest")
        axs.set_xticklabels([season], fontsize=14)
        axs.set_title(ax_title, ha="left", x=0, fontsize=14)


    the_title_2 = "Grouped by seasons of the year, n={}\n".format(num_samps)

    insert_title = '{}{}'.format(the_title, the_title_2)
    plt.suptitle(insert_title, fontweight="book", fontfamily="sans-serif", fontsize=14, linespacing=1.5)
    plt.legend()
    plt.subplots_adjust(top=0.85, hspace=0.25)
    save_to = my_folders["Charts"] +"/"+ file_name  +".svg"
    plt.savefig(save_to)
    plt.show()
    plt.close()
    return "Chart saved to {}".format(save_to)
