import json
import os
from math import log


def append_ksk_kin(ksk):
    tex_str = r'''
    \multicolumn{5}{|c||}{$k_{sk}=''' + str(ksk) + r''', k_{in}=''' + str(ksk + 1) + \
              r'''$} & \multicolumn{5}{c|}{$k_{sk}=''' + str(ksk) + r''', k_{in}=''' + str(ksk + 2) + r'''$} \\
    \hline
    '''
    tex_str += r'''
    {$h_{sk}$} &
    \multicolumn{1}{c|}{$E_{ex}$} &
    \multicolumn{1}{c|}{$\eta_{P}$} &
    \multicolumn{1}{c|}{$\eta_{R}$} &
    \multicolumn{1}{c||}{$I_{eff}$} &
    \multicolumn{1}{c|}{$h_{sk}$} &
    \multicolumn{1}{c|}{$E_{ex}$} &
    \multicolumn{1}{c|}{$\eta_{P}$} &
    \multicolumn{1}{c|}{$\eta_{R}$} &
    \multicolumn{1}{c|}{$I_{eff}$} \\
    \hline 
    '''
    return tex_str


def append_hsk_hin(nref):
    div = pow(2, nref)

    tex_str = r'''
    \multicolumn{5}{|c||}{$h_{in}=h_{sk}'''
    if nref != 0:
        tex_str += '/' + str(div)

    tex_str += r'''$} &
    \multicolumn{5}{|c|}{$h_{in}=h_{sk}'''
    if nref != 0:
        tex_str += '/' + str(div)

    tex_str += r'''$} \\
    \hline
    '''
    return tex_str


def append_res_line(resleft, resright):
    tex_str = '1/' + str(resleft['nDiv']) + ' & ' + '{:.3e}'.format(resleft['exactError']) + ' & ' + \
              '{:.3e}'.format(resleft['eta_p']) + ' & ' + '{:.3e}'.format(resleft['eta_r']) + ' & ' + \
              '{:.3f}'.format(resleft['iEff']) + ' & \n    ' + \
              '1/' + str(resright['nDiv']) + ' & ' + '{:.3e}'.format(resright['exactError']) + ' & ' + \
              '{:.3e}'.format(resright['eta_p']) + ' & ' + '{:.3e}'.format(resright['eta_r']) + ' & ' + \
              '{:.3f}'.format(resright['iEff']) + ' \\\\\n    \\hline\n    '
    return tex_str


def get_rate(vals, ndivs):
    rate = 0.
    hsk = [1. / ndiv for ndiv in ndivs]
    for i in range(len(vals) - 1):
        rate = log(vals[i + 1] / vals[i]) / log(hsk[i + 1] / hsk[i])
    # rate = rate / (len(vals) - 1)
    return rate


def append_rates_line(etapleft, etarleft, exaleft, etapright, etarright, exaright):
    tex_str = 'Rate & ' + \
              '{:.3f}'.format(exaleft) + ' & ' + \
              '{:.3f}'.format(etapleft) + ' & ' + \
              '{:.3f}'.format(etarleft) + ' & - & Rate &' + \
              '{:.3f}'.format(exaright) + ' & ' + \
              '{:.3f}'.format(etapright) + ' & ' + \
              '{:.3f}'.format(etarright) + '& - \\\\\n    '
    return tex_str


def main():
    f = open('../input/SmoothResults.json', 'r')
    data = json.load(f)
    f.close()

    f = open('../input/SmoothResultsk2n1.json', 'r')
    data2 = json.load(f)
    f.close()

    data += data2

    tex_str = r'''
    \documentclass[preview]{standalone}
    \usepackage[utf8]{inputenc}
    \usepackage[margin=0.1in]{geometry}
    \begin{document}
    \begin{center}
    '''

    tex_str += r'''
    \begin{tabular}{|l|l|l|l|l||l|l|l|l|l|}
    \hline
    '''

    for ksk in range(1, 3):
        tex_str += append_ksk_kin(ksk)
        for nref in range(0, 3):
            tex_str += append_hsk_hin(nref)
            etapleft = list()
            etarleft = list()
            exacleft = list()
            etapright = list()
            etarright = list()
            exacright = list()
            ndivs = [4., 8., 16., 32., 64.]
            for ndiv in ndivs:
                resleft = ''
                resright = ''
                for res in data.copy():
                    if res['ksk'] == ksk and res['intRef'] == nref and res['nDiv'] == ndiv:
                        if res['kin'] == res['ksk'] + 1:
                            resleft = res.copy()
                            etapleft.append(resleft['eta_p'])
                            etarleft.append(resleft['eta_r'])
                            exacleft.append(resleft['exactError'])
                        if res['kin'] == res['ksk'] + 2:
                            resright = res.copy()
                            etapright.append(resright['eta_p'])
                            etarright.append(resright['eta_r'])
                            exacright.append(resright['exactError'])
                tex_str += append_res_line(resleft, resright)
            tex_str += append_rates_line(get_rate(etapleft, ndivs), get_rate(etarleft, ndivs),
                                         get_rate(exacleft, ndivs), get_rate(etapright, ndivs),
                                         get_rate(etarright, ndivs), get_rate(exacright, ndivs))

            tex_str += '\\hline\\hline'

    tex_str += r'''
    \end{tabular}
    '''

    tex_str += r'''
    \end{center}
    \end{document}
    '''
    print(tex_str)

    out_file_name = 'table'
    tex_file_name = out_file_name + '.tex'
    pdf_file_name = out_file_name + '.pdf'
    with open(tex_file_name, "w") as text_file:
        text_file.write(tex_str)

    os.system("pdflatex " + tex_file_name)
    os.system("evince " + pdf_file_name)


if __name__ == "__main__":
    main()
